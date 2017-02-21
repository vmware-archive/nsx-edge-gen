#!/usr/bin/env python

# nsxgen
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

import os.path
import string
import sys
import yaml
import re
import ipcalc

CONFIG_FILE = "nsx_cloud_config.yml"
LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

class Config(dict):

	def __init__(self, *arg, **kw):
		super(Config, self).__init__(*arg, **kw)

	def validate(self):
		self.name = self.get('name', 'nsx-gen')
		self.validate_vcenter()
		self.validate_nsx_manager()
		self.validate_defaults()	
		self.validate_logical_switches()
		self.validate_uplink()
		self.validate_nsx_edges()
		
	def validate_vcenter(self):
		self.vcenter = self.get('vcenter')
		if self.vcenter is None:
			raise ValueError('vcenter section not defined')

		fields = [ 'address', 'admin_user', 'admin_passwd']
		for field in fields:
			if self.vcenter[field] is None:
				raise ValueError(field + ' field not set for vcenter')

	def validate_nsx_manager(self):
		self.nsx_manager = self.get('nsx_manager')
		if self.nsx_manager is None:
			raise ValueError('nsx_manager section not defined')
		
		fields = [ 'address', 'nsx_mgr_user', 'nsx_mgr_passwd']
		for field in fields:
			if self.nsx_manager[field] is None:
				raise ValueError(field + ' field not set for nsx_manager')
		if self.nsx_manager['use_local'] == True:
			self.nsx_manager['url'] = 'http://127.0.0.1:8080'
		else:
			self.nsx_manager['url'] = 'https://' + self.nsx_manager['address'] #+':8080'


	def validate_defaults(self):
		self.nsx_defaults = self.get('nsx_defaults')
		if self.nsx_defaults is None:
			raise ValueError('nsx_defaults section not defined')
		
		fields = [ 'transport_zone', 'datacenter', 'datastore', 'distributed_portswitch']
		for field in fields:
			if self.nsx_defaults[field] is None:
				raise ValueError(field + ' field not set for nsx_defaults')		

		if self.nsx_defaults['vmFolder'] is None:
			self.nsx_defaults['vmFolder'] = self.name			
	
	def validate_uplink(self):
		self.uplink = self.get('uplink')
		if self.uplink is None:
			raise ValueError('uplink section not defined')
		
		fields = [ 'id', 'cidr'] #, 'primary_ip', 'secondary_ips']
		for field in fields:
			if self.uplink[field] is None:
				raise ValueError(field + ' field not set for uplink')		

		addr_range = ipcalc.Network(self.uplink['cidr'])
		self.uplink['gateway'] = addr_range[1]
		self.uplink['primary_ip'] = addr_range[1]
		self.uplink['subnet_length'] = string.atoi(self.uplink['cidr'].split('/')[1])
		self.uplink['subnet_mask'] = addr_range.netmask()

	def validate_logical_switches(self):
		self.logical_switches = self.get('logical_switches')
		if self.logical_switches is None:
			raise ValueError('logical_switches section not defined')
		
		fields = [ 'name', 'cidr'] #, 'primary_ip', 'secondary_ips']
		for lswitch in self.logical_switches:
			for field in fields:
				if lswitch[field] is None:
					raise ValueError(field + ' field not set for logical_switch')		


			addr_range = ipcalc.Network(lswitch['cidr'])
			lswitch['name'] = 'lswitch-'+self.get('name') + '-' + lswitch['name']
			lswitch['subnet_mask'] = addr_range.netmask()
			lswitch['gateway'] = addr_range[0]
			lswitch['primary_ip'] = addr_range[1]
			lswitch['subnet_length'] = string.atoi(lswitch['cidr'].split('/')[1])
 
	def validate_nsx_edges(self):
		self.nsx_edges = self.get('edge_service_gateways')
		if self.nsx_edges is None:
			raise ValueError('edge_service_gateways section not defined')
		
		fields = [ 'name', 'id', 'size', 'cli', 'dns', 'pools', 'virtualservers']
		for nsx_edge in self.nsx_edges:
			for field in fields:
				if nsx_edge[field] is None:
					raise ValueError(field + ' field not set for nsx_edge')		

			nsx_edge['name'] = 'esg-'+self.get('name') + '-' + nsx_edge['name']
			
	def read_config(self):
		try:
			with open(CONFIG_FILE) as config_file:
				self.update(read_yaml(config_file))
		except IOError as e:
			print >> sys.stderr, 'Not a nsx config file. Use "nsxgen init" in the root of your repository to create one.'
			sys.exit(1)

	def read(self):
		self.read_config()
		self.validate()
		return self

def read_yaml(file):
	return yaml.safe_load(file)

def write_yaml(file, data):
	file.write(yaml.safe_dump(data, default_flow_style=False, explicit_start=True))

