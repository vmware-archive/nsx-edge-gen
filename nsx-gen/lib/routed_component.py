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
import re
import ipcalc
import yaml
import json
from print_util  import *


CONFIG_FILE = "nsx_cloud_config.yml"
LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

KNOWN_LSWITCHES = {
	'INFRA' : 'Infra',  
	'ERT' : 'Ert',
	'PCF-TILES' : 'PCF-Tiles', 
	'DYNAMIC-SERVICES': 'Dynamic-Services',
}


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

# Ensure the names in this list match keys in
# DEFAULT_ROUTED_COMPONENT_LSWITCH_MAP & DEFAULT_ROUTED_COMPONENT_MAP
KNOWN_ROUTED_COMPONENTS = [
	'OPS',  
	'GO-ROUTER',
	'DIEGO',
	'TCP-ROUTER',
	'MYSQL-ERT', 
	'MYSQL-TILE',
	'RABBITMQ-TILE'
]

# Ensure the switch matches the entry in KNOWN_LSWITCHES
DEFAULT_ROUTED_COMPONENT_LSWITCH_MAP = {
	# Ensure the key matches the name entry
	KNOWN_ROUTED_COMPONENTS[0]: { 'name': 'OPS', 'switch': 'INFRA',            
									'useVIP': False, 'instances' : 1, 'offset' :  5  },
	KNOWN_ROUTED_COMPONENTS[1]: { 'name': 'GO-ROUTER', 'switch': 'ERT',  
							      	'useVIP': True, 'instances' : 4,  'offset' : 10  },
	KNOWN_ROUTED_COMPONENTS[2]: { 'name': 'DIEGO', 'switch': 'ERT',      
									'useVIP': True, 'instances' : 3,  'offset' : 20  },
	KNOWN_ROUTED_COMPONENTS[3]: { 'name': 'TCP-ROUTER', 'switch': 'ERT',  
									'useVIP': True, 'instances' : 4,  'offset' : 30  },
	KNOWN_ROUTED_COMPONENTS[4]: { 'name': 'MYSQL-ERT', 'switch': 'ERT',
									'useVIP': True, 'instances' : 3,  'offset' : 40  },
	KNOWN_ROUTED_COMPONENTS[5]: { 'name': 'MYSQL-TILE', 'switch': 'PCF-TILES',
									'useVIP': True, 'instances' : 3,  'offset' : 10  },								
	KNOWN_ROUTED_COMPONENTS[6]: { 'name': 'RABBITMQ-TILE', 'switch': 'PCF-TILES',
									'useVIP': True, 'instances' : 3,  'offset' : 30  }																		
}

# Ensure the monitor-id matches the ones in the MONITOR_MAP
DEFAULT_ROUTED_COMPONENT_MAP = {
	KNOWN_ROUTED_COMPONENTS[0]: { 
				'name': 'OPS', 'switch': 'INFRA', 
				'useVIP': False, 'instances' : 1,  'offset' :  5, 'monitor_id' : 'monitor-3', 
				'transport':	{
					'ingress': { 'port': '443', 'protocol': 'https' },
					'egress': { 'port': '443', 'protocol': 'https', 'monitor_port' : '443',  'url' :  '/' },
				}	 
			},
	KNOWN_ROUTED_COMPONENTS[1]: { 
				'name': 'GO-ROUTER', 'switch': 'ERT', 
				'useVIP': True,  'instances' : 4,  'offset' : 10, 'monitor_id' : 'monitor-4', 	
				'transport':	{
					'ingress': { 'port': '443', 'protocol': 'https' },
					'egress': { 'port': '80', 'protocol': 'http', 'monitor_port' : '8080',  'url' :  '/health' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[2]: { 
				'name': 'DIEGO', 'switch': 'ERT', 
				'useVIP': True,  'instances' : 3,  'offset' : 20,  'monitor_id' : 'monitor-1',	
				'transport':	{
					'ingress': { 'port': '2222', 'protocol': 'tcp' },
					'egress': { 'port': '2222', 'protocol': 'tcp', 'monitor_port' : '2222' },
				}
			},
	KNOWN_ROUTED_COMPONENTS[3]: { 
				'name': 'TCP-ROUTER', 'switch': 'ERT', 
				'useVIP': True,  'instances' : 4,  'offset' : 30, 'monitor_id' : 'monitor-5',	
				'transport':{
					'ingress': { 'port': '5000', 'protocol': 'tcp' },
					'egress': { 'port': '5000', 'protocol': 'tcp', 'monitor_port' : '80', 'url' :  '/health' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[4]: {
				'name': 'MYSQL-ERT', 'switch': 'PCF-TILES', 
				'useVIP': True,  'instances' : 3,  'offset' :  40,  'monitor_id' : 'monitor-6',	    
				'transport':{
					'ingress': { 'port': '3306', 'protocol': 'tcp' },
					'egress': { 'port': '3306', 'protocol': 'tcp', 'monitor_port' : '1936' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[5]: {
				'name': 'MYSQL-TILE', 'switch': 'PCF-TILES', 
				'useVIP': True,  'instances' : 3,  'offset' :  10,  'monitor_id' : 'monitor-6',	    
				'transport':{
					'ingress': { 'port': '3306', 'protocol': 'tcp' },
					'egress': { 'port': '3306', 'protocol': 'tcp', 'monitor_port' : '1936' },
				 }
			},
	KNOWN_ROUTED_COMPONENTS[6]: { 
				'name': 'RABBITMQ-TILE', 'switch': 'PCF-TILES', 
				'useVIP': True,  'instances' : 3,  'offset' :  20,  'monitor_id' : 'monitor-1',	    
				'transport':{
					'ingress': { 'port': '15672,5672,5671', 'protocol': 'tcp' },
					'egress': { 'port': '15672,5672,5671', 'protocol': 'tcp' },
				 }
			}
}

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

	def __init__(self, name, switchName, uplink_details, transport=None, useVIP=True, instances=3, offset=5):

		self.name = name
		self.switch = None
		self.switchName = switchName
		self.switchTemplate = select_switch_template(name, switchName)

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
			raise ValueError('Unable to determine switch for given component:{} ,\
			 no switch name specified nor known from templates'.format(self.name))

		print 'Looking up for switch with name: {} for Routed component: {}'.format(keywordToMatch, self.name)

		for logical_switch in logical_switches:
			if keywordToMatch.upper().replace('-','') in logical_switch['given_name'].upper().replace('-',''):
				self.switch = logical_switch
				return
		
		if not self.switch:
			raise ValueError('Unable to find matching switch for given component:{} ,\
			 from any of the defined logical switches'.format(self.name))


	def validate_component(self):
		if not self.switch:
			raise ValueError('Unable to find matching switch for given component:{} ,\
			 from any of the defined logical switches'.format(self.name))

		self.check_for_opsmgr()

		if isinstance(self.uplink_details, basestring):
			self.uplink_details = UplinkDetails(self.uplink_details)
		
		if not self.transport:
			templatedRoutedComp = select_templated_routed_component(self.name)
			if (templatedRoutedComp):
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
		appProfile = APP_PROFILE_MAP[protocolMap.lower()]
		if not appProfile:
			appProfile = APP_PROFILE_MAP['tcp:tcp']

		self.app_profile = appProfile
		
		if not self.monitor_id:
			self.monitor_id = MONITOR_MAP[egressProtocol.lower()]['id']

		# Always go with defaults of AppRule1 and 2 so they are in beginning
		self.app_rules = [ "applicationRule-1", "applicationRule-2"  ]
		for appRule in APP_RULE_MAP.keys():
			
			if appRule in [ 'optionlog', 'option httplog']:
				continue

			if appRule.endswith(ingressProtocol.lower()):
				self.app_rules.append( APP_RULE_MAP[appRule]['id'])


	def check_for_opsmgr(self):
		if ('OPS' in self.name.upper()):
			self.useVIP = False
			self.offset = 5
			self.instances = 1 

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
		\'switch\': {}, \'useVIP\': {},  \'instances\' : {},  \'offset\' :  {},\n \
		\'uplink_details\': {}, \'ips\': {}\n \
		\'app_rules\': {}\n \
		\'app_profile\': {}\n \
		\'monitor_id\': {}\n \
		\'transport\': {}\n \
		}}\n'.format(self.name, self.switch, self.useVIP, 
						self.instances, self.offset,
						self.uplink_details,
						self.ips,  
						self.app_rules,
						self.app_profile,
						self.monitor_id, 
						self.transport
						) 


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

def select_templated_routed_component(routedComponentName):
	routedComponentNameUpper = routedComponentName.upper()

	if routedComponentNameUpper in DEFAULT_ROUTED_COMPONENT_MAP:
		return DEFAULT_ROUTED_COMPONENT_MAP[routedComponentNameUpper]

	# for routedComponent in DEFAULT_ROUTED_COMPONENT_TRANSPORT_MAP:
	# 	if any( token for token in routedComponent.split('-') if token in routedComponentNameUpper):
	# 		return DEFAULT_ROUTED_COMPONENT_TRANSPORT_MAP[routedComponent]

	routedComponent = None
	for key in DEFAULT_ROUTED_COMPONENT_MAP:
		if key in routedComponentNameUpper or routedComponentNameUpper in key:
			routedComponent = DEFAULT_ROUTED_COMPONENT_MAP[key]
			return routedComponent

	 
	routedComponentNameUpper = routedComponentNameUpper.replace('-','')
	for routedEntryName in DEFAULT_ROUTED_COMPONENT_MAP.keys():
		name = routedEntryName.replace('-', '')
		if name in routedComponentNameUpper or routedComponentNameUpper in name:
			routedComponent = DEFAULT_ROUTED_COMPONENT_MAP[routedEntryName]
			return routedComponent


	raise ValueError('Unable to find a matching known template for Routed Component:{}'.\
						format( routedComponentName))

def select_switch_template(routedComponentName, switchName):
	if not switchName:
		templatedRoutedComp = select_templated_routed_component(routedComponentName)
		return templatedRoutedComp['switch']

	switchUpper = switchName.upper()
	if switchUpper in KNOWN_LSWITCHES:
		return KNOWN_LSWITCHES[switchUpper]

	for switch in KNOWN_LSWITCHES:
		if any( token for token in switch.split('-') if token in switchUpper):
			return KNOWN_LSWITCHES[switch]
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

def generate_uplink(routedComponentEntry, routedComponentName):
	cidr = None
	uplink_ip = None
	uplink = routedComponentEntry.get('uplink_details')
	if uplink:
		uplink_ip = uplink.get('uplink_ip')
		cidr = uplink.get('cidr')

	else:
		uplink_ip = routedComponentEntry.get('uplink_ip')

	if not uplink_ip:
		raise ValueError('No Uplink IP provided for Routed Component: {}'.format(routedComponentName))

	return UplinkDetails(uplink_ip, cidr)

@run_once
def validate_default_routed_components_map():
	for routedCompKey in KNOWN_ROUTED_COMPONENTS:

		if routedCompKey in DEFAULT_ROUTED_COMPONENT_LSWITCH_MAP:
			lswitchEntry =  DEFAULT_ROUTED_COMPONENT_LSWITCH_MAP[routedCompKey]
			assert lswitchEntry['name'] == routedCompKey
			assert lswitchEntry['switch'] in KNOWN_LSWITCHES.keys()
		else:
			raise Exception('Routed Component[{}] not found... in DEFAULT_ROUTED_COMPONENT_LSWITCH_MAP'.format(routedCompKey))

		if routedCompKey in DEFAULT_ROUTED_COMPONENT_MAP:
			routedComp =  DEFAULT_ROUTED_COMPONENT_MAP[routedCompKey]
			assert routedComp['name'] == routedCompKey
		else:
			raise Exception('Routed Component[{}] not found... in DEFAULT_ROUTED_COMPONENT_MAP'.format(routedCompKey))

	print 'Validation of Default Routed components successful...\n'


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
			print 'Routed component: {}'.format(routedComponent)

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
	print 'Calling main...'
	file_cfg = Config().read(CONFIG_FILE)
	file_cfg.validate()

if __name__ == "__main__":
	main()	

"""