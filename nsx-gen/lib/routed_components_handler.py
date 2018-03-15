#!/usr/bin/env python

# nsx-edge-gen
#
# Copyright (c) 2015-Present Pivotal Software, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Sabha Parameswaran'

import os.path
import string
import sys
#import traceback
import copy
import re
import ipcalc
import yaml
import json
from nsx_lbr_config  import *
from routed_components_config  import *

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

DEFAULT_OSPF_CIDR = '172.16.100.10/24'

DEBUG = False

MONITOR_LIST             = 'MONITOR_LIST'
APP_RULE_LIST            = 'APP_RULE_LIST'
DEFAULT_APP_PROFILE_LIST = 'APP_PROFILE_LIST'
KNOWN_LSWITCHES          = 'KNOWN_LSWITCHES'
KNOWN_ROUTED_COMPONENTS  = 'KNOWN_ROUTED_COMPONENTS'

class TransportScheme:

	"""
	def __init__(self, is_ingress, port=80, protocol='HTTP'):

		self.port = str(port)
		self.protocol = protocol
		self.is_ingress = is_ingress
		self.monitor_port = str(port)
		self.url = '/'
	"""

	def __init__(self, is_ingress, port=80, protocol='http', 
						monitor_port=80, url='/'):
		
		self.protocol = 'http'
		self.port = '80'
		self.monitor_port = None

		self.url = url
		self.is_ingress = is_ingress
		
		if protocol:
			self.protocol = protocol.lower()
		
		if port:
			self.port = str(port)
				
		if monitor_port:
			self.monitor_port = str(monitor_port)
		

	def __str__(self):
		return '{{ \'port\': {}, \'protocol\': {}, \'is_ingress\': {}, \'monitor_port\' : {},  \'url\' :  {} }}'.\
				format(self.port, self.protocol, self.is_ingress, self.monitor_port, self.url)

	def __getitem__(self, field):
		if field == 'port':
			return self.port
		elif field == 'protocol':
			return self.protocol
		elif field == 'monitor_port':
			return self.monitor_port
		elif field == 'url':
			return self.url
		elif field == 'is_ingress':
			return self.is_ingress
		return self.protocol

	def __setitem__(self, field, val):
		if field == 'port':
			self.port = val
		elif field == 'protocol':
			self.protocol = val
		elif field == 'monitor_port':
			self.monitor_port = val
		elif field == 'url':
			self.url
		elif field == 'is_ingress':
			self.is_ingress = val	

class RoutedComponentTransport:

	def __init__(self, ingress_scheme, egress_scheme):
		self.ingress = ingress_scheme
		self.egress = egress_scheme

	def __getitem__(self, field):
		if field == 'ingress':
			return self.ingress
		else:
			return self.egress

	def __str__(self):
		return '{{ \'ingress\': {},  \n \
				\'egress\' : {} }}'.format(self.ingress, self.egress)

class UplinkDetails:

	"""
	def __init__(self, uplink_ip):
		self.uplink_ip = uplink_ip
		self.validate()	 
	
	def __init__(self, uplink_ip, cidr):
		self.cidr = cidr
		self.uplink_ip = uplink_ip

		self.validate()
	"""

	def __init__(self, uplink_ip, cidr=None, subnet_length=None, subnet_mask=None):
		self.cidr = cidr
		self.uplink_ip = uplink_ip
		self.subnet_length = subnet_length
		self.subnet_mask = subnet_mask

		self.real_uplink_ip = None

		self.validate()

	def validate(self):
		if not self.cidr:
			uplinkIpTokens = self.uplink_ip.split('.')
			self.cidr = '{}.{}.{}.0/24'.format(uplinkIpTokens[0], 
											   uplinkIpTokens[1],
											   uplinkIpTokens[2])
		if not self.subnet_length or not self.subnet_mask:
			self.calculate_subnet()

	def calculate_subnet(self):
		addr_range = ipcalc.Network(self.cidr)
		self.subnet_length = string.atoi(self.cidr.split('/')[1])
		self.subnet_mask = addr_range.netmask()

	def __setitem__(self, field, val):
		if field == 'real_uplink_ip':
			self.real_uplink_ip = val

	def __getitem__(self, field):
		if field == 'cidr':
			return self.cidr
		elif field == 'uplink_ip':
			return self.uplink_ip
		elif field == 'real_uplink_ip':
			return self.real_uplink_ip
		elif field == 'subnet_length':
			return self.subnet_length
		elif field == 'subnet_mask':
			return self.subnet_mask
		
		return self.uplink_ip

	def __str__(self):
		return '{{ \'uplink_ip\': {}, \'cidr\' : {}, \'subnet_length\': {}. \'subnet_mask\': {} }}'\
				.format(self.uplink_ip, self.cidr, self.subnet_length, self.subnet_mask)


class RoutedComponent:

	def __init__(self, name, switchName, uplink_details, transport=None, useVIP=True, ssl_term=True, instances=3, offset=5, is_external=True ):

		self.name = name
		self.switch = None
		self.switchName = switchName
		self.switchTemplate = select_switch_template(name, switchName)
		self.external = is_external


		self.uplink_details = uplink_details

		self.useVIP = useVIP
		self.offset = offset
		self.ssl_term = ssl_term
		self.instances = instances
		self.transport = transport
		self.monitor_id = None
		self.ips = ''
		
		#self.validate()

	def map_to_switches(self, logical_switches):

		# Try to match using the provided switch name from the routed component
		keywordToMatch = self.switchName
		# Else try to use the known templates to match switch name by type
		if not keywordToMatch:
			keywordToMatch = self.switchTemplate
		
		if not keywordToMatch:
			raise ValueError('Unable to determine switch for given component:{} ,\n\
			 no switch name specified nor known from templates'.format(self.name))

		print('Looking up for switch with name: {} for Routed component: {}'.format(keywordToMatch, self.name))

		isozone_switches =  [ lswitch['name'] for lswitch in logical_switches if 'ISOZONE' in lswitch['name'].upper()]
		for logical_switch in logical_switches:

			if not self.switchName and 'ISOZONE' in keywordToMatch.upper() and len(isozone_switches) > 1:
				raise ValueError('Unable to choose a matching switch for given component:{} ,\n\
 					as there are multiple IsoZone related logical switches.\n\
 					Specify the associated switch name'.format(self.name))

			given_name = logical_switch.get('given_name')
			if given_name:
				given_name = given_name.upper()
			else:
				given_name = logical_switch['name'].upper()

			if keywordToMatch.upper().replace('-','') in given_name.replace('-',''):
				self.switch = logical_switch
				return
		
		if not self.switch:
			raise ValueError('Unable to find matching switch for given component:{} ,\n\
 				from any of the defined logical switches'.format(self.name))


	def validate_component(self, app_profiles):
		if not self.switch:
			raise ValueError('Unable to find matching switch for given component:{} ,\n\
			 from any of the defined logical switches'.format(self.name))

		templatedRoutedComp = select_templated_routed_component(self.name)
		self.check_for_opsmgr()

		if isinstance(self.uplink_details, basestring):
			self.uplink_details = UplinkDetails(self.uplink_details)

		if (templatedRoutedComp):
			if not self.external:
				self.external = templatedRoutedComp['external']
		
			if not self.transport:
				self.useVIP = templatedRoutedComp['useVIP']
				if not self.offset:
					self.offset = templatedRoutedComp['offset']

				if not self.instances:
					self.instances = templatedRoutedComp['instances']
				
				if not self.switchTemplate:
					self.switchTemplate = templatedRoutedComp['switch']

				
				self.monitor_id = templatedRoutedComp['monitor_id']
				self.transport = generate_transport(templatedRoutedComp, self.name)

				if not self.transport:
					raise ValueError('Unable to generate transport type for Routed Component:{}'.format( \
							self.name))
				
		self.wire_app_rules_and_profiles(app_profiles)
		self.caclulate_routed_component_range()

	# Pass the update app_profiles as we duplicate app profile per Ert/Iso switch
	def wire_app_rules_and_profiles(self, app_profiles):
		ingressProtocol = self.transport['ingress']['protocol']
		egressProtocol = self.transport['egress']['protocol']
		protocolMap = ingressProtocol +':' + egressProtocol

		# If the component does not want ssl termination,
		# then let it flow through to tcps (not https as monitoring is off on http)
		# Change the egress protocol/port/monitor_ports
		if ingressProtocol == 'https' and self.ssl_term == False:
			protocolMap = ingressProtocol +':tcps'
			self.transport['egress']['protocol'] = 'https'
			self.transport['egress']['port'] = '443'
			self.transport['egress']['monitor_port'] = '443'
			self.monitor_id = 'monitor-3' # Use https monitor


		routed_comps_config_context = get_context()
		
		self.app_profile = locate_app_profile(app_profiles, self.switchName, 'profile', protocolMap.lower())
		# if 'ISOZONE' in self.switchName.upper():
		# 	print 'Switch name: ' + self.switchName
		# 	switchIndex = self.switchName.upper().replace('ISOZONE', '').replace('-', '')
		# 	self.app_profile['name'] = self.app_profile['name'] + '-' + self.switchName
		# 	self.app_profile['id'] = self.app_profile['id'] + switchIndex  
		# 	print 'New App profile: {}'.format(self.app_profile)
		
		default_monitors = routed_comps_config_context[MONITOR_LIST]
		if not self.monitor_id:
			self.monitor_id = locate_entry_in_list(default_monitors, 'monitor', egressProtocol.lower())['id']

		# Always go with defaults of AppRule1, 2 and possibly 5 & 6 so they are in beginning
		self.app_rules = [ "applicationRule-1", "applicationRule-2", 
							"applicationRule-5", "applicationRule-6", "applicationRule-7" ]

		default_app_rules = routed_comps_config_context[APP_RULE_LIST]

		for appRule in default_app_rules:
			
			if appRule['app_rule'] in [ 'optionlog', 'forwardfor', 'nooptionhttpclose', 
			                          'nooptionhttpserverclose', 'optionhttpkeepalive' ]:
				continue

			if appRule['app_rule'].endswith(ingressProtocol.lower()):
				self.app_rules.append( appRule['id'])

		print('Updated app profile for {} is {}'.format(self.name, self.app_profile))

	def check_for_opsmgr(self):
		if ('OPSMGR' in self.name.upper()):
			self.useVIP = False
			self.instances = 1 
			self.external = True

	def caclulate_routed_component_range(self):

		ips = []
		addr_range = ipcalc.Network(self.switch['cidr'])

		if not self.offset or not self.instances:
			raise Exception('Routed Component: {} missing offset and instances,\n \
			 cannot use known templates to arrive at these values'.format(self.name))

		for index in xrange(self.offset, self.offset + self.instances):
			ips.append(addr_range[index])

		#routed_component_entry['ips'] = ','.join([str(ip) for ip in ips])
		self.ips = ','.join([str(ip) for ip in ips])
		
	def __getitem__(self, field):
		if field == 'name':
			return self.name
		elif field == 'ips':
			return self.ips	
		elif field == 'external':
			return self.external		
		elif field == 'uplink_details':
			return self.uplink_details
		elif field == 'offset':
			return self.offset
		elif field == 'instances':
			return self.instances
		elif field == 'switch':
			return self.switch
		elif field == 'switchName':
			return self.switchName	
		elif field == 'useVIP':
			return self.useVIP
		elif field == 'transport':
			return self.transport
		elif field == 'app_rules':
			return self.app_rules
		elif field == 'app_profile':
			return self.app_profile
		elif field == 'monitor_id':
			return self.monitor_id

		return self.name

	def __str__(self):
		
		return '{}: {{\n \
		\'switch\': {}, \'external\': {}, \'useVIP\': {},\n \
		\'instances\' : {},  \'offset\' :  {},\n \
		\'uplink_details\': {}, \'ips\': {}\n \
		\'app_rules\': {}\n \
		\'app_profile\': {}\n \
		\'monitor_id\': {}\n \
		\'transport\': {}\n \
		}}\n'.format(self.name, 
						self.switch,
						self.external, 
						self.useVIP, 
						self.instances, 
						self.offset,
						self.uplink_details,
						self.ips,  
						self.app_rules,
						self.app_profile,
						self.monitor_id, 
						self.transport
						) 


def get_context():
	if get_context.context is not None:
		return get_context.context

get_context.context = None

def set_context(context):
	if DEBUG:
		print('Set Routed Components Handler context with {}'.format(context))
	get_context.context = context


def locate_entry_in_list(arr, field, value):
	for entry in arr:
		if entry[field] == value:
			return entry

	return None

def locate_app_profile(app_profiles, lswitchName, field, value):
	# First see if the app profiles that are specific to a switch (ERT or ISOZONE)
	for entry in app_profiles:
		associated_switch = entry.get('switch')
		if associated_switch and associated_switch != '':
			if entry[field] == value and associated_switch.upper() == lswitchName.upper():
				return entry

	# Fall back for those app profiles that are not specific to any switch
	# Like http2http, tcp2tcp
	for entry in app_profiles:
		associated_switch = entry.get('switch')
		if not associated_switch or associated_switch == '':
			if entry[field] == value:
				return entry

	return None

def parse_routing_component(routeComponentEntry, logical_switches, app_profiles, dlr_enabled):
	print('Parsing Routed Component: {}'.format(routeComponentEntry))

	instances = routeComponentEntry.get('instances')
	offset = routeComponentEntry.get('offset')
	switchName = routeComponentEntry.get('switch')
	monitor_port = routeComponentEntry.get('switch')
	external = routeComponentEntry.get('external')
	ssl_term = routeComponentEntry.get('ssl_terminate')
	if not ssl_term or ssl_term == 'true':
		ssl_term = True
	else:
		ssl_term = False

	routedTransportSpecified = None

	transportEntry = generate_transport(routeComponentEntry, routeComponentEntry['name'])
	new_uplink_details = generate_uplink(routeComponentEntry, routeComponentEntry['name'], dlr_enabled) 

	# Create Routed Components and associated LBR/Pool/AppProfile/AppRules
	routedComponent = RoutedComponent(routeComponentEntry['name'],
										switchName,											
										new_uplink_details,
										transportEntry,
										useVIP=True,
										ssl_term=ssl_term,
										instances=instances,
										offset=offset,
										is_external=external
									 )

	routedComponent.map_to_switches(logical_switches)
	routedComponent.validate_component(app_profiles)
	return routedComponent

def run_once(f):
    def wrapper(*args, **kwargs):
    	if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

def get_default_app_profiles():
	routed_comps_config_context = get_context()
	return routed_comps_config_context[DEFAULT_APP_PROFILE_LIST]

def get_default_app_rules():
	routed_comps_config_context = get_context()
	return routed_comps_config_context[APP_RULE_LIST]

def get_default_monitors():
	routed_comps_config_context = get_context()
	return routed_comps_config_context[MONITOR_LIST]

def select_templated_routed_component(routedComponentName):
	routedComponentNameUpper = routedComponentName.upper()

	# Go first with longer name matches (like go-router-isozone rather than go-router)
	routed_comps_config_context = get_context()
	routed_comps_map = routed_comps_config_context[KNOWN_ROUTED_COMPONENTS]
	routed_comps_names = [ routed_comp['name'] for routed_comp in routed_comps_map]
	default_routed_component_names = sorted(routed_comps_names, key=len, reverse=True)
	
	if routedComponentNameUpper in default_routed_component_names:
		return locate_entry_in_list(routed_comps_map, 'name', routedComponentNameUpper)

	# for routedComponent in DEFAULT_ROUTED_COMPONENT_TRANSPORT_MAP:
	# 	if any( token for token in routedComponent.split('-') if token in routedComponentNameUpper):
	# 		return DEFAULT_ROUTED_COMPONENT_TRANSPORT_MAP[routedComponent]

	routedComponent = None
	for key in default_routed_component_names: #DEFAULT_ROUTED_COMPONENT_MAP:
		if key in routedComponentNameUpper or routedComponentNameUpper in key:
			routedComponent = locate_entry_in_list(routed_comps_map, 'name', key)
			return routedComponent

	 
	routedComponentNameUpper = routedComponentNameUpper.replace('-','')
	for routedEntryName in default_routed_component_names: #DEFAULT_ROUTED_COMPONENT_MAP.keys():
		name = routedEntryName.replace('-', '')
		if name in routedComponentNameUpper or routedComponentNameUpper in name:
			routedComponent = locate_entry_in_list(routed_comps_map, 'id', routedEntryName)
			return routedComponent


	raise ValueError('Unable to find a matching known template for Routed Component:{}'.\
						format( routedComponentName))

def select_switch_template(routedComponentName, switchName):
	if not switchName:
		templatedRoutedComp = select_templated_routed_component(routedComponentName)
		return templatedRoutedComp['switch_type']

	switchUpper = switchName.upper()

	routed_comps_config_context = get_context()
	known_switches = routed_comps_config_context[KNOWN_LSWITCHES]
	if switchUpper in [ switch['id'] for switch in known_switches]:
		return locate_entry_in_list(known_switches, 'id', switchUpper)['id']

	for switch in known_switches:
		if any( token for token in switch['id'].split('-') if token in switchUpper):
			return switch['id']

	if 'ISO' in routedComponentName.upper():
		templatedRoutedComp = select_templated_routed_component(routedComponentName)
		return templatedRoutedComp['switch_type']['id']

	raise ValueError('Unable to find match for specified switch:{} \
							for Routed Component:{}'.format( switchName, routedComponentName))


def generate_transport(routedComponentEntry, routedComponentName):
	transport = routedComponentEntry.get('transport')
	if transport:
		ingressT = transport.get('ingress')					
		egressT = transport.get('egress')

		if not ingressT or not egressT:
			raise ValueError('Incomplete transport details provided for Routed Component: {}'.\
				format(routedComponentName))
		
		ingressTransport = TransportScheme(	True, 
											ingressT.get('port'), 
											ingressT.get('protocol'),
											ingressT.get('monitor_port'),
											ingressT.get('url')
										)
		egressTransport = TransportScheme(	False, 
											egressT.get('port'), 
											egressT.get('protocol'),
											egressT.get('monitor_port'),
											egressT.get('url')
										)

		return RoutedComponentTransport(ingressTransport, egressTransport)

def generate_uplink(routedComponentEntry, routedComponentName, dlr_enabled):
	cidr = None
	uplink_ip = None

	uplink = routedComponentEntry.get('uplink_details')
	if uplink:
		uplink_ip = uplink.get('uplink_ip')
		cidr = uplink.get('cidr')

	else:
		uplink_ip = routedComponentEntry.get('uplink_ip')

	templatedRoutedComp = select_templated_routed_component(routedComponentName)

	is_external = routedComponentEntry.get('external')
	if not is_external:
		is_external = templatedRoutedComp['external']


	if is_external:
		if not uplink_ip:
			raise ValueError('No Uplink IP provided for Routed Component: {}'.format(routedComponentName))
		return UplinkDetails(uplink_ip, cidr)


	if dlr_enabled:
		# For internal components, arrive at the uplink ip of the OSPF subnet
		uplink_ip = calculate_ospf_uplink_ip(templatedRoutedComp['offset'])
	
	return UplinkDetails(uplink_ip, DEFAULT_OSPF_CIDR)

def calculate_ospf_uplink_ip( offset):
		
	addr_range = ipcalc.Network(DEFAULT_OSPF_CIDR)
	if offset > 250:
		offset %= 210
	return addr_range[offset]

@run_once
def validate_default_routed_components_map():
	routed_comps_config_context = { }
	nsx_lbr_config = load_lbr_cfg()
	routed_comps_config = load_routed_comps_cfg()
	
	routed_comps_config_context[KNOWN_LSWITCHES]         = routed_comps_config['switch_types']
	routed_comps_config_context[KNOWN_ROUTED_COMPONENTS] = routed_comps_config['routed_components']

	routed_comps_config_context[MONITOR_LIST]     = nsx_lbr_config['monitors']
	routed_comps_config_context[APP_RULE_LIST]    = nsx_lbr_config['app_rules']

	default_app_profiles = nsx_lbr_config['app_profiles']
	routed_comps_config_context[DEFAULT_APP_PROFILE_LIST] = nsx_lbr_config['app_profiles']

	if DEBUG:
		print('Routed comps config:{}'.format(routed_comps_config_context))
	
	for routedCompKey in routed_comps_config_context[KNOWN_ROUTED_COMPONENTS]:

		switch_ids = [ switch['id'] for switch in routed_comps_config_context[KNOWN_LSWITCHES] ]
		assert routedCompKey['switch_type'] in switch_ids 
		
#		else:
#			raise Exception('Routed Component[{}] not found with matching switch id...'.format(routedCompKey))

	set_context(routed_comps_config_context)
	print('Validation of Default Routed components successful against template...\n')


"""
# For local testing...
class Config(dict):

	def __init__(self, *arg, **kw):
		super(Config, self).__init__(*arg, **kw)

	def validate(self):
		self.esg = self.get('edge_service_gateways')
		self.routedComps = self.esg[0]['routed_components']
		
		for routedComp in self.routedComps:
			if routedComp.get('uplink_details'):
				uplink_ip = routedComp['uplink_details']['uplink_ip']
			else:
				uplink_ip = routedComp['uplink_ip']
			routedComponent = RoutedComponent(routedComp['name'],											
											uplink_ip )
			print('Routed component: {}'.format(routedComponent))

		return self

	def read(self, config_file=CONFIG_FILE):
		self.read_config(config_file)
		return self

	def read_config(self, input_config_file=CONFIG_FILE):
		if os.path.isdir(input_config_file):
			input_config_file = input_config_file + '/' + CONFIG_FILE

		try:
			with open(input_config_file) as config_file:
				self.update(read_yaml(config_file))
		except IOError as e:
			
			print >> sys.stderr, 'Not a nsx config file. Use "nsxgen init" in the root of your ' \
							+ 'repository to create one.'
			sys.exit(1)

def read_yaml(file):
	return yaml.safe_load(file)

def main():
	print('Calling main...')
	file_cfg = Config().read(CONFIG_FILE)
	file_cfg.validate()

if __name__ == "__main__":
	main()	

"""