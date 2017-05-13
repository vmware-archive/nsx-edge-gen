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

from routed_component  import *

CONFIG_FILE = "nsx_cloud_config.yml"
LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

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
				'datastore', 'cluster'] #, 'vmFolder', 'host']
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
		
		fields = [ 'address', 'admin_user', 'admin_passwd', 
					'distributed_port_switch', 'uplink_details']
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

		#print('NSX Manager context:{}'.format(self.nsxmanager))

	def validate_logical_switches(self):
		self.logical_switches = self.get('logical_switches')
		if self.logical_switches is None:
			raise ValueError('logical_switches section not defined')		
		
		fields = [ 'name',  'cidr'] #, 'primary_ip', 'secondary_ips']
		for lswitch in self.logical_switches:
			for field in fields:
				if lswitch[field] is None:
					raise ValueError(field + ' field not set for logical_switch')		

			# Go with default cidr of 22 (limit it to 1024 ips)
			addr, cidr = lswitch['cidr'].split('/')		
			if cidr < 22:
				lswitch['cidr'] = addr + '/22'			

			given_name = lswitch['name'].replace(' ', '-')
			lswitch['given_name'] = given_name
			addr_range = ipcalc.Network(lswitch['cidr'])
			lswitch['name'] = 'lswitch-'+self.get('name') + '-' + lswitch['name']
			lswitch['subnet_mask'] = addr_range.netmask()
			lswitch['gateway'] = addr_range[0]
			lswitch['primary_ip'] = addr_range[1]
			lswitch['subnet_length'] = string.atoi(lswitch['cidr'].split('/')[1])
			lswitch['name'] = lswitch['name'].replace(' ', '-')

			# This will be filled in later once we have parsed the routed components
			lswitch['secondary_ips'] = []		
			
			print('Logical Switch Entry:', lswitch)
 		print_logical_switches_configured(self.logical_switches)

	def validate_nsx_edges(self):
		self.nsx_edges = self.get('edge_service_gateways')
		if self.nsx_edges is None:
			raise ValueError('edge_service_gateways section not defined')
		
		global_switches =  { }
		for lswitch in self.logical_switches:
			global_switches[lswitch['given_name'].upper()] = lswitch

		fields = [ 'name', 'size', 'cli', 'routed_components', 'gateway_ip', 'ospf_password']
		for nsx_edge in self.nsx_edges:

			for field in fields:
				if nsx_edge[field] is None:
					raise ValueError(field + ' field not set for nsx_edge')
				
				if field == 'size':
					size = nsx_edge[field]
					if not size or size not in [ 'xlarge', 'quadlarge', 'large', 'compact' ]:
					    nsx_edge['size'] = 'large'

				if field == 'ospf_password':
					if len(nsx_edge[field]) > 7:
						raise ValueError(field + ' field length more than 7 characters for nsx_edge')

			nsx_edge['global_switches'] =  global_switches
			nsx_edge['global_uplink_details'] = self.nsxmanager['uplink_details']

			routed_component_context = nsx_edge['routed_components']

			nsx_edge['routed_components'] = [ ]
			for entry in routed_component_context:
				routedComponent = parse_routing_component(entry, self.logical_switches)
				print('Routed component: {}'.format(routedComponent))
				nsx_edge['routed_components'].append(routedComponent)

			name = 'esg-' + self.get('name')
			if  self.get('name') != nsx_edge['name']:
				name = name + '-' + nsx_edge['name']
			nsx_edge['name'] = name
			
		print_edge_service_gateways_configured(self.nsx_edges)



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



def read_yaml(file):
	return yaml.safe_load(file)

def write_yaml(file, data):
	file.write(yaml.safe_dump(data, default_flow_style='false', explicit_start='true'))
	
