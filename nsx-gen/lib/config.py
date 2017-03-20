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
import yaml
import re
import ipcalc
from print_util  import *

CONFIG_FILE = "nsx_cloud_config.yml"
LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

MONITOR_MAP = {
	'tcp': 	      { 'id': 'monitor-1', 'type': 'tcp',   'name': 'default_tcp_monitor' },   
	'http':       { 'id': 'monitor-2', 'type': 'http',  'name': 'default_http_monitor', 'url': '/' },
	'https':      { 'id': 'monitor-3', 'type': 'https', 'name': 'default_https_monitor', 'url': '/' },
	'go-router':  { 'id': 'monitor-4', 'type': 'http',  'name': 'goRouter_monitor', 'url': '/health' },
	'tcp-router': { 'id': 'monitor-5', 'type': 'http',  'name': 'tcpRouter_monitor', 'url': '/health' },
	'mysql':      { 'id': 'monitor-6', 'type': 'tcp',  'name': 'mysql_monitor' },
}

APP_PROFILE_MAP = {
	'http:http': 	{ 'id': 'applicationProfile-1', 'name': 'HTTP2HTTP', 'incoming' : 'HTTP',  'forward' : 'HTTP',
	 	'template': 'HTTP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'http:tcp':     { 'id': 'applicationProfile-2', 'name': 'HTTP2TCP', 'incoming' : 'HTTP',  'forward' : 'TCP' ,
	 	'template': 'HTTP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'https:http':   { 'id': 'applicationProfile-3', 'name': 'HTTPS2HTTP', 'incoming' : 'HTTPS', 'forward' : 'HTTP' ,
	 	'template': 'HTTPS', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'https:https':  { 'id': 'applicationProfile-4', 'name': 'HTTPS2HTTPS', 'incoming' : 'HTTPS', 'forward' : 'HTTPS' ,
	 	'template': 'HTTPS', 'sslPassthrough': 'true', 'serverSslEnabled' : 'true' },
	'https:tcp':    { 'id': 'applicationProfile-5', 'name': 'HTTPS2TCP', 'incoming' : 'HTTPS', 'forward' : 'TCP' ,
	 	'template': 'HTTP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'tcp:tcp':      { 'id': 'applicationProfile-6', 'name': 'TCP2TCP', 'incoming' : 'TCP',   'forward' : 'TCP' ,
	 	'template': 'TCP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'tcps:tcp':     { 'id': 'applicationProfile-7', 'name': 'TCPS2TCP', 'incoming' : 'TCPS',  'forward' : 'TCP' ,
	 	'template': 'TCP', 'sslPassthrough': 'false', 'serverSslEnabled' : 'false' },
	'tcps:tcps':    { 'id': 'applicationProfile-8', 'name': 'TCPS2TCPS', 'incoming' : 'TCPS',  'forward' : 'TCPS' ,
	 	'template': 'TCP', 'sslPassthrough': 'true', 'serverSslEnabled' : 'true' },   	
}

APP_RULE_MAP = {
	'optionlog': 	           { 'id': 'applicationRule-1', 'name': 'option httplog', 'script' : 'option httplog' },
	'forwardfor': 	           { 'id': 'applicationRule-2', 'name': 'forwardfor', 'script' : 'option forwardfor' },
	'X-Forwarded-Proto:http':  { 'id': 'applicationRule-3', 'name': 'X-Forwarded-Proto:http', 'script' : 'reqadd X-Forwarded-Proto:\ http' },
	'X-Forwarded-Proto:https': { 'id': 'applicationRule-4', 'name': 'X-Forwarded-Proto:https', 'script' : 'reqadd X-Forwarded-Proto:\ https' },	
}

DEFAULT_ROUTED_COMPONENT_MAP = {
	'OPS': 	        { 'switch': 'Infra', 'instances' : 1,  'offset' : 5 },
	'GO-ROUTER': 	{ 'switch': 'Ert',   'instances' : 4,  'offset' : 10 },
	'DEIGO': 	    { 'switch': 'Ert',   'instances' : 3,  'offset' : 20 },
	'TCP-ROUTER':  	{ 'switch': 'Ert',   'instances' : 4,  'offset' : 30 },
}
	

class Config(dict):

	def __init__(self, *arg, **kw):
		super(Config, self).__init__(*arg, **kw)

	def validate(self):
		self.name = self.get('name', 'nsx-pcf')

		self.validate_defaults()
		self.validate_vcenter()
		self.validate_nsxmanager()
		self.validate_logical_switches()
		self.validate_nsx_edges()

		return self
		
	def validate_vcenter(self):
		self.vcenter = self.get('vcenter')
		if self.vcenter is None:
			raise ValueError('vcenter section not defined')

		fields = [ 'address', 'admin_user', 'admin_passwd', 'datacenter', \
				'datastore', 'cluster', 'gateway'] #, 'vmFolder', 'host']
		for field in fields:
			if self.vcenter[field] is None:
				raise ValueError(field + ' field not set for vcenter')

		self.vcenter['url'] = 'https://' + self.vcenter['address']

	def validate_defaults(self):
		self.defaults = self.get('defaults')
		if self.defaults is None:
			raise ValueError('defaults section not defined')

		fields = [ 'ntp_ips', 'dns_ips']
		for field in fields:
			if self.defaults[field] is None:
				raise ValueError(field + ' field not set for defaults')

		fields = [ 'syslog_ips', 'ldap_ips']
		for field in fields:
			if self.defaults[field] is None or self.defaults[field] == '':
				self.defaults[field] = '1.1.1.1'
	
	def validate_nsxmanager(self):
		self.nsxmanager = self.get('nsxmanager')
		if self.nsxmanager is None:
			raise ValueError('nsxmanager section not defined')
		
		fields = [ 'address', 'admin_user', 'admin_passwd', 'uplink_details']
		for field in fields:
			if self.nsxmanager[field] is None:
				raise ValueError(field + ' field not set for nsxmanager')
		
		self.nsxmanager['url'] = 'https://' + self.nsxmanager['address']

		uplink_details = self.nsxmanager['uplink_details']
		if uplink_details.get('uplink_ip') is None:
			raise ValueError('uplink ip field not set for nsxmanager->uplink_details')

		if uplink_details.get('cidr') is None:
			uplink_details['cidr'] = uplink_details['uplink_ip'] + '/24'


		addr_range = ipcalc.Network(uplink_details['cidr'])
		uplink_details['subnet_mask'] = addr_range.netmask()
		uplink_details['subnet_length'] = string.atoi(uplink_details['cidr'].split('/')[1])

	def validate_logical_switches(self):
		self.logical_switches = self.get('logical_switches')
		if self.logical_switches is None:
			raise ValueError('logical_switches section not defined')		
		
		fields = [ 'name',  'primary_ip', 'cidr'] #, 'secondary_ips']
		for lswitch in self.logical_switches:
			for field in fields:
				if lswitch[field] is None:
					raise ValueError(field + ' field not set for logical_switch')		

			# Go with default cidr of 22 (limit it to 1024 ips)
			addr, cidr = lswitch['cidr'].split('/')		
			if cidr < 22:
				lswitch['cidr'] = addr + '/22'			

			givenName = lswitch['name'].replace(' ', '-')
			lswitch['givenName'] = givenName
			addr_range = ipcalc.Network(lswitch['cidr'])
			lswitch['name'] = 'lswitch-'+self.get('name') + '-' + lswitch['name']
			lswitch['subnet_mask'] = addr_range.netmask()
			lswitch['gateway'] = addr_range[0]
			lswitch['primary_ip'] = addr_range[1]
			lswitch['subnet_length'] = string.atoi(lswitch['cidr'].split('/')[1])
			lswitch['name'] = lswitch['name'].replace(' ', '-')		
			
 		print_logical_switches_configured(self.logical_switches)

	def validate_nsx_edges(self):
		self.nsx_edges = self.get('edge_service_gateways')
		if self.nsx_edges is None:
			raise ValueError('edge_service_gateways section not defined')
		
		global_switches =  { }
		for lswitch in self.logical_switches:
			global_switches[lswitch['givenName'].upper()] = lswitch

		fields = [ 'name', 'size', 'cli', 'routed_components']
		for nsx_edge in self.nsx_edges:
			for field in fields:
				if nsx_edge[field] is None:
					raise ValueError(field + ' field not set for nsx_edge')
				
				# if field == 'uplink':
				# 	uplink_context = nsx_edge['uplink']
				# 	uplink_context['name'] = nsx_edge['name'] + '-uplink'
				# 	uplink_context['name'] = uplink_context['name'].replace(' ', '-')

				if field == 'size':
					size = nsx_edge['size']
					if not size or size not in [ 'xlarge', 'quadlarge', 'large', 'compact' ]:
					    nsx_edge['size'] = 'large'


			nsx_edge['global_switches'] =  global_switches
			nsx_edge['appProfile_Map'] = APP_PROFILE_MAP
			nsx_edge['appRule_Map'] = APP_RULE_MAP
			nsx_edge['monitor_Map'] = MONITOR_MAP


			nsx_edge['global_uplink_details'] = self.nsxmanager['uplink_details']

			routed_component_context = nsx_edge['routed_components']
			nsx_edge['routed_components'] = self.validate_routed_components(nsx_edge, \
															routed_component_context)						

			name = 'esg-' + self.get('name')
			if  self.get('name') != nsx_edge['name']:
				name = name + '-' + nsx_edge['name']
			nsx_edge['name'] = name
			
			#print 'NSX Edge Config:{}\n'.format(str(nsx_edge))
		print_edge_service_gateways_configured(self.nsx_edges)

	def validate_routed_components(self, nsx_edge, routed_component_context):
		fields = [ 'name', 'switch', 'uplink_details'] #, 'switch', 'offset']

		for routed_component_entry in routed_component_context:
			for field in fields:
				if routed_component_entry[field] is None:
					raise ValueError(field + ' field not set for routed_component')

			# Go with default cidr of 32 (limit it to 1 ip)
			uplink_details = routed_component_entry['uplink_details']
			if uplink_details['uplink_ip'] is None:
				raise ValueError('uplink_ip field not set within uplink_details for routed_component ' 
					+ routed_component_entry['name'])

			if not uplink_details.get('cidr'):
				uplink_details['cidr'] = uplink_details['uplink_ip'] + '/24'

			addr_range = ipcalc.Network(uplink_details['cidr'])
			uplink_details['subnet_length'] = string.atoi(uplink_details['cidr'].split('/')[1])
			uplink_details['subnet_mask'] = addr_range.netmask()
			
			self.check_and_validate_schemes_for_routed_component(routed_component_entry)

			# Map the type of incoming to monitor type in LBR					
			# Default monitor type is 1 - TCP
			routed_component_entry['monitor_type'] = MONITOR_MAP['tcp']
			
			if routed_component_entry['transport']['forward_scheme']['protocol'] == 'https':
				routed_component_entry['monitor_type'] = MONITOR_MAP['https']
			elif  routed_component_entry['transport']['forward_scheme']['protocol'] == 'http':
			 	routed_component_entry['monitor_type'] = MONITOR_MAP['http']

			if routed_component_entry['transport'].get('incoming_scheme') is not None:
				traffic_combo = routed_component_entry['transport']['incoming_scheme']['protocol'] \
						+ ':' + routed_component_entry['transport']['forward_scheme']['protocol']
				routed_component_entry['appProfile'] = APP_PROFILE_MAP[traffic_combo]
			

			requestedComponentType = routed_component_entry['name'].replace(' ', '-').upper()
			requestedSwitchType = routed_component_entry['switch'].replace(' ', '-').upper()

			if all(searchString in requestedComponentType for searchString in [ 'GO', 'ROUTER']):
				routed_component_entry['monitor_type'] = MONITOR_MAP['go-router']
			elif all(searchString in requestedComponentType for searchString in [ 'TCP', 'ROUTER']):
				routed_component_entry['monitor_type'] = MONITOR_MAP['tcp-router']
			
			matched_switch_defn = nsx_edge['global_switches']['ERT']

			for switchName, switch_defn in nsx_edge['global_switches'].iteritems():
				if requestedSwitchType  in switchName:
					matched_switch_defn = switch_defn
					#print 'Found switch type to be: {}\n'.format(str(matched_switch_defn))
					# Save the external uplink ip with the switch for later SNAT
					switch_defn['uplink_ip'] = routed_component_entry['uplink_details']['uplink_ip']
					routed_component_entry['logical_switch'] = switch_defn
					break

			for routed_component_name, builtin_routed_component in DEFAULT_ROUTED_COMPONENT_MAP.iteritems():	
				
				if routed_component_name in requestedComponentType \
					or requestedComponentType in routed_component_name:
					matched_routed_component_defn = builtin_routed_component
					#print 'Found component type to be: {}\n'.format(str(matched_routed_component_defn))
					break

			self.caclulate_routed_component_range(routed_component_entry, matched_switch_defn, 
												matched_routed_component_defn)
			#print 'Updated routed component: {}\n'.format(str(routed_component_entry))

		print_routed_components(routed_component_context)
		return routed_component_context


	def caclulate_routed_component_range(self, routed_component_entry, switch, defaultConfigEntry):

		if routed_component_entry.get('instances') is None:
			routed_component_entry['instances'] = defaultConfigEntry['instances']

		if routed_component_entry.get('offset') is None:
			routed_component_entry['offset'] = defaultConfigEntry['offset']

		ips = []
		addr_range = ipcalc.Network(switch['cidr'])
		offset = routed_component_entry['offset']
		instances = routed_component_entry['instances']

		for index in xrange(offset, offset +instances):
			ips.append(addr_range[index])

		routed_component_entry['ips'] = ','.join([str(ip) for ip in ips])
		
		return routed_component_entry

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

	def read(self, config_file=CONFIG_FILE):
		self.read_config(config_file)
		return self

	def check_and_validate_schemes_for_routed_component(self, routed_component):
		
		routed_component_name = routed_component['name'].replace(' ', '-').upper()

		if routed_component.get('transport') is None:
			routed_component['transport'] = { }

		endpoint = routed_component['transport']

		# Default is HTTPS/443 incoming and HTTP/80 forward
		if endpoint.get('forward_scheme') is None:
			endpoint['forward_scheme'] = { 'protocol' : 'http', 'port': 80}

		if endpoint.get('incoming_scheme') is None:
			endpoint['incoming_scheme'] = { 'protocol' : 'https', 'port': 443}
		
		# OPS Mgr is 443/HTTPS
		if 'OPS' in routed_component_name:
			endpoint['forward_scheme'] = { 'protocol' : 'https', 'port': 443}
			endpoint['incoming_scheme'] = { 'protocol' : 'https', 'port': 443}

		# ERT Router is 443/HTTPS incoming and then 80/HTTP
		elif 'ERT' in routed_component_name or 'GO-ROUTER' in routed_component_name:
			endpoint['forward_scheme'] = { 'protocol' : 'http', 'port': 80}
			endpoint['incoming_scheme'] = { 'protocol' : 'https', 'port': 443}

		# Diego is ssh/2222 throughout
		elif 'DIEGO' in routed_component_name:
			endpoint['forward_scheme'] = { 'protocol' : 'tcp', 'port': 2222}
			endpoint['incoming_scheme'] = { 'protocol' : 'tcp', 'port': 2222}

		# Tcp-router is tcp/5000 throughout
		elif 'TCP' in routed_component_name:
			endpoint['forward_scheme'] = { 'protocol' : 'tcp', 'port': 5000}
			endpoint['incoming_scheme'] = { 'protocol' : 'tcp', 'port': 5000}

		elif 'MYSQL' in routed_component_name:
			endpoint['forward_scheme'] = { 'protocol' : 'tcp', 'port': 3306}
			endpoint['incoming_scheme'] = { 'protocol' : 'tcp', 'port': 3306}

		incomingProtocol = routed_component['transport']['incoming_scheme']['protocol']
		for appRule, val in APP_RULE_MAP.iteritems():
			 if appRule.endswith(incomingProtocol):
			 	routed_component['app_rule'] = val['id']
			 	
		return

def read_yaml(file):
	return yaml.safe_load(file)


def write_yaml(file, data):
	file.write(yaml.safe_dump(data, default_flow_style='false', explicit_start='true'))
	
