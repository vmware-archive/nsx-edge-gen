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

def print_moid_map(moidMap):
	print
	print('-'*150) 
	print('{:<60}{:<60}{:<10}'.format('', 'vCenter Managed Object ID Map', ''))
	print("{:<80} | {:<20} | {:60} ".format('Name', 
											'Moid', 
											'Url Path'))
	print('-'*150)
	for key, val in moidMap.iteritems():
		print('{:<80} | {:<20} | {:60}'.format(key, 
												val['moid'], 
												val['href']))
	print('-'*150)
	print  	


def print_logical_switches_available(switches):
	print
	print('-'*220)
	print('{:<80}{:<60}{:<10}'.format('', 'Logical Switch Instances', ''))
	print("{:<60} | {:<20} | {:80} | {:<15}".format(	'Name', 
														'Moid', 
														'Managed Object Name', 
														'Subnet'))
	print('-'*220) 
	for switch in switches:
		print('{:<60} | {:<20} | {:80} | {:<15}'.format(switch['name'], 
														switch.get('id', ''), 
														switch.get('moName', ''), 
														'---'))
	print('-'*220)
	print  	

def print_logical_switches_configured(switches):
	print
	print('-'*150)
	print('{:<50}{:<60}{:<10}'.format('', 'Logical Switches (from configuration)', ''))
	print("{:<60} | {:<20} | {:20}".format(	'Name', 
											'CIDR', 
											'Primary IP'))
	print('-'*150)
	for switch in switches:
		print('{:<60} | {:<20} | {:20}'.format(switch['name'], 
												switch.get('cidr'), 
												switch.get('primary_ip')))
	print('-'*150)
	print  	


def print_routed_components(routed_components):
	print
	print('-'*200)
	print('{:<80}{:<60}{:<10}'.format('', 'Routed Components (from configuration)', '')) 
	print("{:<30} | {:<30} | {:<50} |{:10}| {:<80}".format('Name', 
															'Network', 
															'Logical Switch', 
															'Instances', 
															'IPs'))
	print('-'*200)
	for component in routed_components:
		print('{:<30} | {:<30} | {:<50} |{:10}| {:<80}'.format(component['name'], 
													component['switch'],
													component['logical_switch']['name'],
													component['instances'], 
													component['ips']))
	print('-'*200)
	print

def print_edge_service_gateways_available(esgs):
	print
	print('-'*200)
	print('{:<80}{:<60}{:<10}'.format('', 'Edge Service Gateway Instances', '')) 
	print("{:<40} | {:<10} | {:<20} | {:20} | {:10} | {:<40}| {:<15}| {:<40}".format('Name', 
																			'Moid', 
																			'Datacenter',
																			'Datastore', 
																			'Size', 
																			'FQDN',
																			'Status',
																			'Vnics'))
	print('-'*200) 
	for esg in esgs:	
		esgAppliance = esg['appliancesSummary']
		#vnics = ', '.join([vic['name'] for vnic in esg['vnics']])
		
		#print vnics
		
		print('{:<40} | {:<10} | {:<20} | {:20} | {:10} | {:<40}| {:<15}| {:<40}'.format(	esg['name'], 
																		esg['id'],
																		esg['datacenterName'],
																		esgAppliance.get('dataStoreNameOfActiveVse', ''),
																		esgAppliance['applianceSize'],
																		esgAppliance['fqdn'],
																		esg['edgeStatus'],
																		'')) #vnics))
	print('-'*200)
	print

def print_edge_service_gateways_configured(esgs):
	print
	print('-'*200)
	print('{:<80}{:<60}{:<10}'.format('', 'Edge Service Gateways (from configuration)', ''))
	print("{:<30} | {:<30} | {:<50} | {:20} | {:15} | {:<50}".format('Name', 
																	'Moid', 
																	'Routed Components', 
																	'Uplink Port', 
																	'Uplink IP', 
																	'Creds'))
	print('-'*200) 
	for esg in esgs:

		index = 0
		count = 0
		value = None
		size = len(esg['routed_components'])/3 + 1
		routed_component_arr = []
		for routed_component in esg['routed_components']:
			count += 1 
			if value:
				value = ','.join([routed_component['name'], value])
			else:
				value = routed_component['name']

			if (count % 3) == 0:
				routed_component_arr.append(value)
				value = None
				index += 1 

		#routed_components = ','.join([routed_component['name'] for routed_component in esg['routed_components']])
		cli_creds = 'user={}, passwd={}'.format(esg['cli']['username'], esg['cli']['password'])
		
		print('{:<30} | {:<30} | {:<50} | {:20} | {:15} | {:<50}'.format(	esg['name'], 
																		esg.get('id', ''),
																		routed_component_arr[0],
																		esg['global_uplink_details']['uplink_port_switch'],
																		esg['global_uplink_details']['uplink_ip'], 
																		cli_creds))

		line = 1
		while (line < len(routed_component_arr)):
			print('{:<30} | {:<30} | {:<50} | {:20} | {:15} | {:<50}'.format('', '', routed_component_arr[line], '', '', ''))
			line += 1
		
		print('')
		print('-'*200)
		print('{:<80}{:<60}{:<10}'.format('', 'Firewall (from configuration)', ''))
		print("{:<40} | {:<20} | {:<80} | {:<60} ".format(	'Name', 
															'Ingress/Egress',
															'Source', 
															'Destination'))
		print('-'*200)

		ruleMap = {
			'ops'    : { 'name': 'Allow Ingress -> Ops Manager', 'type': 'Ingress', 'ports' : 'tcp/22,80,443' },
			'ert'    : { 'name': 'Allow Ingress -> Elastic Runtime', 'type': 'Ingress', 'ports' : 'tcp/80,443,443' },
			'diego'  : { 'name': 'Allow Ingress -> SSH for Apps', 'type': 'Ingress', 'ports' : 'tcp/2222' },
			'tcp'    : { 'name': 'Allow Ingress -> Tcp Router', 'type': 'Ingress', 'ports' : 'tcp/5000' },
			'any1'   : { 'name': 'Allow Inside <-> Inside', 'type': 'Both', 'ports' : 'any' },
			'any2'   : { 'name': 'Allow Egress -> All Outbound', 'type': 'Egress', 'ports' : 'any' },
		} 

		for routed_component in esg['routed_components']:			
			rule = None
			for ruleName, ruleRow in ruleMap.iteritems():
				if ruleName in routed_component['name']:
					rule = ruleRow
					break

			if not rule:
				continue

			if rule['type'] == 'Ingress':
				srcRule = 'any'
				destRule = rule['ports']
			elif rule['type'] == 'Egress':
				srcRule = rule['ports']
				destRule = 'any'
			else:
				srcRule = rule['ports']
				destRule = rule['ports']

			print('{:<40} | {:<20} | {:<80} | {:<80}'.format( rule['name'], rule['type'], srcRule, destRule))  

		for ruleName, ruleRow in ruleMap.iteritems():
			if not 'any' in ruleName:
				continue

			rule = ruleRow
			if rule['type'] == 'Ingress':
				srcRule = 'any'
				destRule = rule['ports']
			elif rule['type'] == 'Egress':
				srcRule = rule['ports']
				destRule = 'any'
			else:
				srcRule = rule['ports']
				destRule = rule['ports']

			print('{:<40} | {:<20} | {:<80} | {:<80}'.format( rule['name'], rule['type'], srcRule, destRule))  
																			
		print('-'*215)

		print('{:<80}{:<40}{:<15}{:<10}'.format('', 'Routed Component (from configuration) for Edge Instance: ',esg['name'], ''))
		print("{:<22} | {:<12} |{:<5}|{:<5}|{:<6}| {:<15}| {:<15}| {:<25} |  {:<15} |{:<10}| {:<20} | {:<20} | {:<20} ".format( \
															'Name',
															'Switch',
															'VIP',
															'Inst',
															'Offset',
															'Uplink IP',
															'IPs', 
															'App Profile',
															'App Rules', 
															'Monitor Id',
															'Ingress:Port',
															'Egress:Port',
															'Protocol:Monitor Url'
															))
		print('-'*215)

		for entry in esg['routed_components']:	
			useVip = 'Y'		
			if not entry['useVIP']:
				useVip = 'N'
			transport = entry['transport']
			uplink_ip = entry['uplink_details']['uplink_ip']

			ips = entry['ips'].split(',')
			#appRule = entry['app_rules']

			appProfile = entry['app_profile']['id']
			monitorId = entry['monitor_id']
			ingressCombo = transport['ingress']['protocol'] + ':' + str(transport['ingress']['port'])
			egressCombo = transport['egress']['protocol'] + ':' + str(transport['egress']['port'])

			monitorCombo = ''
			monitorPort = transport['egress']['monitorPort']
			if monitorPort:
				monitorCombo = str(monitorPort)
				monitorUrl = transport['egress']['url']
				if monitorUrl:
					 monitorCombo = monitorCombo + ':' +  monitorUrl

			index = 0
			ruleCount = len(entry['app_rules'])
			ipCount = len(ips)

			count = ruleCount
			if count < ipCount:
				count = ipCount
				

			while index < count:
				
				ip = '  '
				appRuleId = '  '

				if index < ruleCount:
					appRuleId = entry['app_rules'][index]
				if index < ipCount:
					ip = ips[index]

				if (index == 0):
					print("{:<22} | {:<12} |{:<5}|{:<5}|{:<6}| {:<15}| {:<15}| {:<25} | {:<15} |{:<10}|{:<22}|{:<22}|{:<22}".format( \
															entry['name'],
															entry['switchName'],
															useVip,
															entry['instances'],
															entry['offset'],
															uplink_ip,
															ip,  
															appProfile,
															appRuleId, 
															monitorId,
															ingressCombo,
															egressCombo,
															monitorCombo ))

				else:
					print("{:<22} | {:<12} |{:<5}|{:<5}|{:<6}| {:<15}| {:<15}| {:<25} | {:<17} |{:<10}|{:<22}|{:<22}|{:<22}".format( \
															'',
															'',
															'',
															'',
															'',
															'', 
															ip,
															'',
															appRuleId,
															'',
															'',
															'',
															'' ))
				index = index + 1
																			
		print('-'*215)		
		print
		print('-'*160)

		print('{:<10}{:<80}{:<15}{:<10}'.format('', 'Routed Component Static IPs Assignment (from configuration) for Edge Instance: ',esg['name'], ''))
		print("{:<22} | {:<22} | {:<12} | {:<15}| {:<80} ".format( \
															'Header ',
															'Name',
															'Switch',
															'Uplink IP',
															'IPs' 
															))
		print('-'*160)

		for entry in esg['routed_components']:	
			uplink_ip = entry['uplink_details']['uplink_ip']

			print("{:<22} | {:<22} | {:<12} | {:<15}| {:<80}".format( \
													'static ips assignment',
													entry['name'],
													entry['switchName'],
													uplink_ip,
													entry['ips']))
																		
		print('-'*160)		
