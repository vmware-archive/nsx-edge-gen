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
import re
import ipcalc
import yaml
import json
from nsx_lbr_config  import *
from routed_components_config  import *


#CONFIG_FILE = "nsx_cloud_config.yml"
LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

DEFAULT_OSPF_CIDR = '172.16.100.10/24'

DEBUG = False

MONITOR_MAP             = 'MONITOR_MAP'
APP_RULE_MAP            = 'APP_RULE_MAP'
APP_PROFILE_MAP         = 'APP_PROFILE_MAP'
KNOWN_LSWITCHES         = 'KNOWN_LSWITCHES'
KNOWN_ROUTED_COMPONENTS = 'KNOWN_ROUTED_COMPONENTS'

"""

# Ensure changes to the monitor-id in MONITOR_MAP matches the ones in DEFAULT_ROUTED_COMPONENT_MAP
MONITOR_MAP = {
	'tcp': 	      { 'id': 'monitor-1', 'type': 'tcp',   'name': 'default_tcp_monitor' },   
	'http':       { 'id': 'monitor-2', 'type': 'http',  'name': 'default_http_monitor', 'url': '/' },
	'https':      { 'id': 'monitor-3', 'type': 'https', 'name': 'default_https_monitor', 'url': '/' },
	'go-router':  { 'id': 'monitor-4', 'type': 'http',  'name': 'goRouter_monitor', 'url': '/health' },
	'tcp-router': { 'id': 'monitor-5', 'type': 'http',  'name': 'tcpRouter_monitor', 'url': '/health' },
	'mysql':      { 'id': 'monitor-6', 'type': 'tcp',   'name': 'mysql_monitor' },
}

APP_PROFILE_MAP = {
	'http:http': 	{ 'id': 'applicationProfile-1', 'name': 'HTTP2HTTP', 'ingress' : 'HTTP',  'forward' : 'HTTP',
		'template': 'HTTP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'http:tcp':     { 'id': 'applicationProfile-2', 'name': 'HTTP2TCP', 'ingress' : 'HTTP',  'forward' : 'TCP' ,
		'template': 'HTTP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'https:http':   { 'id': 'applicationProfile-3', 'name': 'HTTPS2HTTP', 'ingress' : 'HTTPS', 'forward' : 'HTTP' ,
		'template': 'HTTPS', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'https:https':  { 'id': 'applicationProfile-4', 'name': 'HTTPS2HTTPS', 'ingress' : 'HTTPS', 'forward' : 'HTTPS' ,
		'template': 'HTTPS', 'sslPassthrough': 'true', 'serverSslEnabled' : 'true' },
	'https:tcp':    { 'id': 'applicationProfile-5', 'name': 'HTTPS2TCP', 'ingress' : 'HTTPS', 'forward' : 'TCP' ,
		'template': 'HTTP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'tcp:tcp':      { 'id': 'applicationProfile-6', 'name': 'TCP2TCP', 'ingress' : 'TCP',   'forward' : 'TCP' ,
		'template': 'TCP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'tcps:tcp':     { 'id': 'applicationProfile-7', 'name': 'TCPS2TCP', 'ingress' : 'TCPS',  'forward' : 'TCP' ,
		'template': 'TCP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'tcps:tcps':    { 'id': 'applicationProfile-8', 'name': 'TCPS2TCPS', 'ingress' : 'TCPS',  'forward' : 'TCPS' ,
		'template': 'TCP', 'sslPassthrough': 'true', 'serverSslEnabled' : 'true' },   	
}

# Dont change order of first two entries or their ids -- they should stay constant..
APP_RULE_MAP = {
	'optionlog': 	           { 'id': 'applicationRule-1', 'name': 'option httplog', 'script' : 'option httplog' },
	'forwardfor': 	           { 'id': 'applicationRule-2', 'name': 'forwardfor', 'script' : 'option forwardfor' },
	'X-Forwarded-Proto:http':  { 'id': 'applicationRule-3', 'name': 'X-Forwarded-Proto:http', 'script' : 'reqadd X-Forwarded-Proto:\ http' },
	'X-Forwarded-Proto:https': { 'id': 'applicationRule-4', 'name': 'X-Forwarded-Proto:https', 'script' : 'reqadd X-Forwarded-Proto:\ https' },	
}


# Ensure the switch matches the entry in KNOWN_LSWITCHES
# Ensure the offset for the non-external components are not overlapping or same
DEFAULT_ROUTED_COMPONENT_LSWITCH_MAP = {
	# Ensure the key matches the name entry
	KNOWN_ROUTED_COMPONENTS[0]: { 'name': 'OPS', 'switch': 'INFRA', 'external': True,           
									'useVIP': False, 'instances' : 1, 'offset' :  5  },
	KNOWN_ROUTED_COMPONENTS[1]: { 'name': 'GO-ROUTER', 'switch': 'ERT', 'external': True, 
							      	'useVIP': True, 'instances' : 4,  'offset' : 10  },
	KNOWN_ROUTED_COMPONENTS[2]: { 'name': 'DIEGO', 'switch': 'ERT', 'external': True,      
									'useVIP': True, 'instances' : 3,  'offset' : 20  },
	KNOWN_ROUTED_COMPONENTS[3]: { 'name': 'TCP-ROUTER', 'switch': 'ERT', 'external': True,  
									'useVIP': True, 'instances' : 4,  'offset' : 30  },
	KNOWN_ROUTED_COMPONENTS[4]: { 'name': 'MYSQL-ERT', 'switch': 'ERT', 'external': False,
									'useVIP': True, 'instances' : 3,  'offset' : 40  },
	KNOWN_ROUTED_COMPONENTS[5]: { 'name': 'MYSQL-TILE', 'switch': 'PCF-TILES', 'external': False,
									'useVIP': True, 'instances' : 3,  'offset' : 10  },								
	KNOWN_ROUTED_COMPONENTS[6]: { 'name': 'RABBITMQ-TILE', 'switch': 'PCF-TILES', 'external': False,
									'useVIP': True, 'instances' : 3,  'offset' : 30  },
	KNOWN_ROUTED_COMPONENTS[7]: { 'name': 'GO-ROUTER-ISO', 'switch': 'ISOZONE', 'external': True,  
							      	'useVIP': True, 'instances' : 2,  'offset' : 10  },
	KNOWN_ROUTED_COMPONENTS[8]: { 'name': 'TCP-ROUTER-ISO', 'switch': 'ISOZONE', 'external': True,  
									'useVIP': True, 'instances' : 2,  'offset' : 30  }
																											
}

# Ensure the monitor-id matches the ones in the MONITOR_MAP
# Ensure the offset for the non-external components are not overlapping or same

DEFAULT_ROUTED_COMPONENT_MAP = {
	KNOWN_ROUTED_COMPONENTS[0]: { 
				'name': 'OPS', 'switch': 'INFRA', 'external': True,   
				'useVIP': False, 'instances' : 1,  'offset' :  5, 'monitor_id' : 'monitor-3', 
				'transport':	{
					'ingress': { 'port': '443', 'protocol': 'https' },
					'egress': { 'port': '443', 'protocol': 'https', 'monitor_port' : '443',  'url' :  '/' },
				}	 
			},
	KNOWN_ROUTED_COMPONENTS[1]: { 
				'name': 'GO-ROUTER', 'switch': 'ERT', 'external': True, 
				'useVIP': True,  'instances' : 4,  'offset' : 10, 'monitor_id' : 'monitor-4', 	
				'transport':	{
					'ingress': { 'port': '443', 'protocol': 'https' },
					'egress': { 'port': '80', 'protocol': 'http', 'monitor_port' : '8080',  'url' :  '/health' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[2]: { 
				'name': 'DIEGO', 'switch': 'ERT', 'external': True,
				'useVIP': True,  'instances' : 3,  'offset' : 20,  'monitor_id' : 'monitor-1',	
				'transport':	{
					'ingress': { 'port': '2222', 'protocol': 'tcp' },
					'egress': { 'port': '2222', 'protocol': 'tcp', 'monitor_port' : '2222' },
				}
			},
	KNOWN_ROUTED_COMPONENTS[3]: { 
				'name': 'TCP-ROUTER', 'switch': 'ERT', 'external': True, 
				'useVIP': True,  'instances' : 4,  'offset' : 30, 'monitor_id' : 'monitor-5',	
				'transport':{
					'ingress': { 'port': '5000', 'protocol': 'tcp' },
					'egress': { 'port': '5000', 'protocol': 'tcp', 'monitor_port' : '80', 'url' :  '/health' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[4]: {
				'name': 'MYSQL-ERT', 'switch': 'PCF-TILES', 'external': False, 
				'useVIP': True,  'instances' : 3,  'offset' :  40,  'monitor_id' : 'monitor-6',	    
				'transport':{
					'ingress': { 'port': '3306', 'protocol': 'tcp' },
					'egress': { 'port': '3306', 'protocol': 'tcp', 'monitor_port' : '1936' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[5]: {
				'name': 'MYSQL-TILE', 'switch': 'PCF-TILES', 'external': False, 
				'useVIP': True,  'instances' : 3,  'offset' :  10,  'monitor_id' : 'monitor-6',	    
				'transport':{
					'ingress': { 'port': '3306', 'protocol': 'tcp' },
					'egress': { 'port': '3306', 'protocol': 'tcp', 'monitor_port' : '1936' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[6]: { 
				'name': 'RABBITMQ-TILE', 'switch': 'PCF-TILES', 'external': False, 
				'useVIP': True,  'instances' : 3,  'offset' :  20,  'monitor_id' : 'monitor-1',	    
				'transport':{
					'ingress': { 'port': '15672,5672,5671', 'protocol': 'tcp' },
					'egress': { 'port': '15672,5672,5671', 'protocol': 'tcp' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[7]: { 
				'name': 'GO-ROUTER-ISO', 'switch': 'ISOZONE', 'external': True, 
				'useVIP': True,  'instances' : 2,  'offset' : 10, 'monitor_id' : 'monitor-4', 	
				'transport':	{
					'ingress': { 'port': '443', 'protocol': 'https' },
					'egress': { 'port': '80', 'protocol': 'http', 'monitor_port' : '8080',  'url' :  '/health' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[8]: { 
				'name': 'TCP-ROUTER-ISO', 'switch': 'ISOZONE', 'external': True, 
				'useVIP': True,  'instances' : 2,  'offset' : 30, 'monitor_id' : 'monitor-5',	
				'transport':{
					'ingress': { 'port': '5000', 'protocol': 'tcp' },
					'egress': { 'port': '5000', 'protocol': 'tcp', 'monitor_port' : '80', 'url' :  '/health' },
				 }
			}
}
"""

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

	def __init__(self, name, switchName, uplink_details, transport=None, useVIP=True, instances=3, offset=5, is_external=True ):

		self.name = name
		self.switch = None
		self.switchName = switchName
		self.switchTemplate = select_switch_template(name, switchName)
		self.external = is_external		

		self.uplink_details = uplink_details

		self.useVIP = useVIP
		self.offset = offset
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


	def validate_component(self):
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
				
		self.wire_app_rules_and_profiles()
		self.caclulate_routed_component_range()

	def wire_app_rules_and_profiles(self):
		ingressProtocol = self.transport['ingress']['protocol']
		egressProtocol = self.transport['egress']['protocol']

		protocolMap = ingressProtocol +':' + egressProtocol

		routed_comps_config_context = get_context()
		default_app_profiles = routed_comps_config_context[APP_PROFILE_MAP]

		appProfile = locate_with_key(default_app_profiles, 'profile', protocolMap.lower())
		if not appProfile:
			appProfile = locate_with_key(default_app_profiles,'profile', 'tcp:tcp')

		self.app_profile = appProfile
		
		default_monitors = routed_comps_config_context[MONITOR_MAP]
		if not self.monitor_id:
			self.monitor_id = locate_with_key(default_monitors, 'monitor', egressProtocol.lower())['id']

		# Always go with defaults of AppRule1 and 2 so they are in beginning
		self.app_rules = [ "applicationRule-1", "applicationRule-2"  ]

		default_app_rules = routed_comps_config_context[APP_RULE_MAP]

		for appRule in default_app_rules:
			
			if appRule['app_rule'] in [ 'optionlog', 'option httplog']:
				continue

			if appRule['app_rule'].endswith(ingressProtocol.lower()):
				self.app_rules.append( appRule['id'])


	def check_for_opsmgr(self):
		if ('OPS' in self.name.upper()):
			self.useVIP = False
			self.offset = 5
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


def locate_with_key(arr, field, key):
	for entry in arr:
		if entry[field] == key:
			return entry

	return None


def parse_routing_component(routeComponentEntry, logical_switches, dlr_enabled):
	print('Parsing Routed Component: {}'.format(routeComponentEntry))

	instances = routeComponentEntry.get('instances')
	offset = routeComponentEntry.get('offset')
	switchName = routeComponentEntry.get('switch')
	monitor_port = routeComponentEntry.get('switch')
	external = routeComponentEntry.get('external')

	routedTransportSpecified = None

	transportEntry = generate_transport(routeComponentEntry, routeComponentEntry['name'])
	new_uplink_details = generate_uplink(routeComponentEntry, routeComponentEntry['name'], dlr_enabled) 

	# Create Routed Components and associated LBR/Pool/AppProfile/AppRules
	routedComponent = RoutedComponent(routeComponentEntry['name'],
										switchName,											
										new_uplink_details,
										transportEntry,
										useVIP=True,
										instances=instances,
										offset=offset,
										is_external=external
									 )

	routedComponent.map_to_switches(logical_switches)
	routedComponent.validate_component()
	return routedComponent

def run_once(f):
    def wrapper(*args, **kwargs):
    	if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

def select_templated_routed_component(routedComponentName):
	routedComponentNameUpper = routedComponentName.upper()

	# Go first with longer name matches (like go-router-isozone rather than go-router)
	routed_comps_config_context = get_context()
	routed_comps_map = routed_comps_config_context[KNOWN_ROUTED_COMPONENTS]
	routed_comps_names = [ routed_comp['id'] for routed_comp in routed_comps_map]
	default_routed_component_names = sorted(routed_comps_names, key=len, reverse=True)
	
	if routedComponentNameUpper in default_routed_component_names:
		return locate_with_key(routed_comps_map, 'id', routedComponentNameUpper)

	# for routedComponent in DEFAULT_ROUTED_COMPONENT_TRANSPORT_MAP:
	# 	if any( token for token in routedComponent.split('-') if token in routedComponentNameUpper):
	# 		return DEFAULT_ROUTED_COMPONENT_TRANSPORT_MAP[routedComponent]

	routedComponent = None
	for key in default_routed_component_names: #DEFAULT_ROUTED_COMPONENT_MAP:
		if key in routedComponentNameUpper or routedComponentNameUpper in key:
			routedComponent = locate_with_key(routed_comps_map, 'id', key)
			return routedComponent

	 
	routedComponentNameUpper = routedComponentNameUpper.replace('-','')
	for routedEntryName in default_routed_component_names: #DEFAULT_ROUTED_COMPONENT_MAP.keys():
		name = routedEntryName.replace('-', '')
		if name in routedComponentNameUpper or routedComponentNameUpper in name:
			routedComponent = locate_with_key(routed_comps_map, 'id', routedEntryName)
			return routedComponent


	raise ValueError('Unable to find a matching known template for Routed Component:{}'.\
						format( routedComponentName))

def select_switch_template(routedComponentName, switchName):
	if not switchName:
		templatedRoutedComp = select_templated_routed_component(routedComponentName)
		return templatedRoutedComp['switch']

	switchUpper = switchName.upper()

	routed_comps_config_context = get_context()
	known_switches = routed_comps_config_context[KNOWN_LSWITCHES]
	if switchUpper in [ switch['id'] for switch in known_switches]:
		return locate_with_key(known_switches, 'id', switchUpper)['id']

	for switch in known_switches:
		if any( token for token in switch['id'].split('-') if token in switchUpper):
			return switch['id']

	if 'ISOZONE' in routedComponentName.upper():
		templatedRoutedComp = select_templated_routed_component(routedComponentName)
		return templatedRoutedComp['switch']['id']

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
	return addr_range[offset]

@run_once
def validate_default_routed_components_map():
	routed_comps_config_context = { }
	nsx_lbr_config = load_lbr_cfg()
	routed_comps_config = load_routed_comps_cfg()
	
	routed_comps_config_context[KNOWN_LSWITCHES]         = routed_comps_config['switches']
	routed_comps_config_context[KNOWN_ROUTED_COMPONENTS] = routed_comps_config['routed_components']

	routed_comps_config_context[MONITOR_MAP]     = nsx_lbr_config['monitors']
	routed_comps_config_context[APP_RULE_MAP]    = nsx_lbr_config['app_rules']
	routed_comps_config_context[APP_PROFILE_MAP] = nsx_lbr_config['app_profiles']

	if DEBUG:
		print('Routed comps config:{}'.format(routed_comps_config_context))
	
	for routedCompKey in routed_comps_config_context[KNOWN_ROUTED_COMPONENTS]:

		switch_ids = [ switch['id'] for switch in routed_comps_config_context[KNOWN_LSWITCHES] ]
		assert routedCompKey['switch'] in switch_ids 
		
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