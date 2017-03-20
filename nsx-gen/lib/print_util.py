
def print_moid_map(moidMap):
	print
	print '-'*150 
	print '{:<60}{:<60}{:<10}'.format('', 'vCenter Managed Object ID Map', '')
	print "{:<80} | {:<20} | {:60} ".format('Name', 
											'Moid', 
											'Url Path')
	print '-'*150 
	for key, val in moidMap.iteritems():
		print '{:<80} | {:<20} | {:60}'.format(key, 
												val['moid'], 
												val['href'])
	print '-'*150
	print  	


def print_logical_switches_available(switches):
	print
	print '-'*220 
	print '{:<80}{:<60}{:<10}'.format('', 'Logical Switch Instances', '')
	print "{:<60} | {:<20} | {:80} | {:<15}".format(	'Name', 
														'Moid', 
														'Managed Object Name', 
														'Subnet')
	print '-'*220 
	for switch in switches:
		print '{:<60} | {:<20} | {:80} | {:<15}'.format(switch['name'], 
														switch.get('id', ''), 
														switch.get('moName', ''), 
														'---')
	print '-'*220
	print  	

def print_logical_switches_configured(switches):
	print
	print '-'*150 
	print '{:<50}{:<60}{:<10}'.format('', 'Logical Switches (from configuration)', '')
	print "{:<60} | {:<20} | {:20}".format(	'Name', 
											'CIDR', 
											'Primary IP')
	print '-'*150 
	for switch in switches:
		print '{:<60} | {:<20} | {:20}'.format(switch['name'], 
												switch.get('cidr'), 
												switch['primary_ip'])
	print '-'*150
	print  	


def print_routed_components(routed_components):
	print
	print '-'*200
	print '{:<80}{:<60}{:<10}'.format('', 'Routed Components (from configuration)', '') 
	print "{:<30} | {:<30} | {:<50} |{:10}| {:<80}".format('Name', 
															'Network', 
															'Logical Switch', 
															'Instances', 
															'IPs')
	print '-'*200 
	for component in routed_components:
		print '{:<30} | {:<30} | {:<50} |{:10}| {:<80}'.format(component['name'], 
													component['switch'],
													component['logical_switch']['name'],
													component['instances'], 
													component['ips'])
	print '-'*200
	print

def print_edge_service_gateways_available(esgs):
	print
	print '-'*200
	print '{:<80}{:<60}{:<10}'.format('', 'Edge Service Gateway Instances', '') 
	print "{:<40} | {:<10} | {:<20} | {:20} | {:10} | {:<40}| {:<15}| {:<40}".format('Name', 
																			'Moid', 
																			'Datacenter',
																			'Datastore', 
																			'Size', 
																			'FQDN',
																			'Status',
																			'Vnics')
	print '-'*200 
	for esg in esgs:	
		esgAppliance = esg['appliancesSummary']
		#vnics = ', '.join([vic['name'] for vnic in esg['vnics']])
		
		#print vnics
		
		print '{:<40} | {:<10} | {:<20} | {:20} | {:10} | {:<40}| {:<15}| {:<40}'.format(	esg['name'], 
																		esg['id'],
																		esg['datacenterName'],
																		esgAppliance.get('dataStoreNameOfActiveVse', ''),
																		esgAppliance['applianceSize'],
																		esgAppliance['fqdn'],
																		esg['edgeStatus'],
																		'') #vnics)
	print '-'*200
	print

def print_edge_service_gateways_configured(esgs):
	print
	print '-'*200
	print '{:<80}{:<60}{:<10}'.format('', 'Edge Service Gateways (from configuration)', '')
	print "{:<30} | {:<30} | {:<50} | {:20} | {:10} | {:<50}".format('Name', 
																	'Moid', 
																	'Routed Components', 
																	'Uplink Port', 
																	'Uplink IP', 
																	'Creds')
	print '-'*200 
	for esg in esgs:
		routed_components = ','.join([routed_component['name'] for routed_component in esg['routed_components']])
		cli_creds = 'user={}, passwd={}'.format(esg['cli']['username'], esg['cli']['password'])
		
		print '{:<30} | {:<30} | {:<50} | {:20} | {:10} | {:<50}'.format(	esg['name'], 
																		esg.get('id', ''),
																		routed_components,
																		esg['global_uplink_details']['uplink_port_switch'],
																		esg['global_uplink_details']['primary_ip'], 
																		cli_creds)
		print '-'*200
		print 
		print '{:<80}{:<60}{:<10}'.format('', 'Firewall (from configuration)', '')
		print "{:<40} | {:<20} | {:<80} | {:<80} ".format(	'Name', 
															'Ingress/Egress',
															'Source', 
															'Destination')
		print '-'*200

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

			print '{:<40} | {:<20} | {:<80} | {:<80}'.format( rule['name'], rule['type'], srcRule, destRule)  

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

			print '{:<40} | {:<20} | {:<80} | {:<80}'.format( rule['name'], rule['type'], srcRule, destRule)  
																			
		print '-'*200
		print
