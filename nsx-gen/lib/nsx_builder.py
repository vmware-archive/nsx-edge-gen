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

import __builtin__
import os.path
import errno
import shutil
import sys
import yaml
import re
import template
import ipcalc
import client
import glob
import mobclient
import subprocess
import xmltodict
from pprint import pprint

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

sys.path.append(os.path.join(LIB_PATH, os.path.join('../..')))

from util import *
from routed_component import *
from nsx_urls import *

import argparse
from print_util  import *
import pynsxv.library.nsx_logical_switch as lswitch
import pynsxv.library.nsx_dlr as dlr
import pynsxv.library.nsx_esg as esg
import pynsxv.library.nsx_dhcp as dhcp
import pynsxv.library.nsx_lb as lb
import pynsxv.library.nsx_dfw as dfw
import pynsxv.library.nsx_usage as usage

DEBUG = False

moidMap = { }

def initMoidMap(context):
	global moidMap
	if 'vmware_mob_moid_map' not in context:
		mobclient.set_context(context['vcenter'])
	
		moidMap = mobclient.lookup_vsphere_config()
		context['vmware_mob_moid_map'] = moidMap

	mapVcenterResources(context, moidMap)
	return context['vmware_mob_moid_map']

def refresh_moid_map(context):
	if 'vmware_mob_moid_map' not in context:
		return initMoidMap(context)
	else:
		context['vmware_mob_moid_map'].update(mobclient.refresh_vsphere_config())
		return context['vmware_mob_moid_map']

def lookupVCenterMoid(context, field, moidMap):
	vcenter_context = context['vcenter']
	
	moidEntry = moidMap.get(vcenter_context[field])
	if moidEntry:
		moid = moidEntry.get('moid')
		if moid:
			vcenter_context[field + '_id'] = moid
			return

	if field == 'datacenter':
		raise ValueError('Cannot lookup Moid for provided Datacenter:{}'.format(vcenter_context[field]))
	
	# Try adding 'vsan' if its datastore
	if field == 'datastore':
		# Try adding vsan to datastore name
		moidEntry = moidMap['vsan' + vcenter_context[field]]
		if moidEntry:
			moid = moidEntry.get('moid')
			if moid:
				vcenter_context[field + '_id'] = moid
				return
	
	raise ValueError('Cannot lookup Moid for provided Datastore:{}'.format(vcenter_context[field]))

def  mapVcenterResources(context, moidMap):
	vcenter_context = context['vcenter']

	lookupVCenterMoid(context, 'datacenter', moidMap)
	lookupVCenterMoid(context, 'datastore', moidMap)

	if DEBUG:
		print 'vCenter context updated\n'
		pprint(vars(vcenter_context))

def build(context, verbose=False):
	client.set_context(context, 'nsxmanager')
	moidMap = refresh_moid_map(context)
	if DEBUG:
		pprint(moidMap)   
	
	reconcile_uplinks(context)
	build_logical_switches('lswitch', context, 'logical_switches')
	build_nsx_edge_gateways('edge', context)

def delete(context, verbose=False):
	client.set_context(context, 'nsxmanager')
	refresh_moid_map(context)

	delete_nsx_edge_gateways(context)    
	delete_logical_switches(context, 'logical_switches')

def list(context, verbose=False):
	client.set_context(context, 'nsxmanager')
	moidMap = refresh_moid_map(context)
	if DEBUG:
		pprint(moidMap)    

	reconcile_uplinks(context)
	list_logical_switches(context)
	list_nsx_edge_gateways(context)    

def map_logical_switches_id(logical_switches):
	existinglSwitchesResponse = client.get(NSX_URLS['lswitch']['all'] + '?&startindex=0&pagesize=100')
	existinglSwitchesResponseDoc = xmltodict.parse(existinglSwitchesResponse.text)
	if DEBUG:
		print 'LogicalSwitches response :{}\n'.format(existinglSwitchesResponse.text) 
	
	num_lswitches = len(logical_switches)
	matched_lswitches = 0

	virtualWires = existinglSwitchesResponseDoc['virtualWires']['dataPage']['virtualWire']
	lswitchEntries = virtualWires
	if isinstance(virtualWires, dict):
		lswitchEntries = [ virtualWires ]

	for existingLSwitch in lswitchEntries:
		if (num_lswitches == matched_lswitches):
			break

		for interested_lswitch in  logical_switches: 
			if existingLSwitch['name'] == interested_lswitch['name']:
				interested_lswitch['id'] = existingLSwitch['objectId']

				++matched_lswitches
				break

	if len(logical_switches) > 0:
			print_logical_switches_available(logical_switches)

	for interested_lswitch in  logical_switches: 
		if (interested_lswitch.get('id') is None):
			print 'Logical Switch instance with name: {}'  \
				+ ' does not exist, possibly deleted already'.format(interested_lswitch['name'])

def check_logical_switch_exists(vcenterMobMap, lswitchName):

	fullMobName = mobclient.lookup_logicalswitch_managed_obj_name(lswitchName)
	# For a lswitch with name ' lswitch-nsx-pcf-CF-Tiles'
	# it would have a MOB name of 'vxw-dvs-29-virtualwire-225-sid-5066-lswitch-nsx-pcf-CF-Tiles'
	if fullMobName is None:
		return False

	if 'vxw-' in fullMobName and '-virtualwire-' in fullMobName:
		print 'Logical switch : {} exists with MOB:{}'.format(lswitchName, fullMobName)
		return True

	return False

# Any internal component that requires VIP (like mysql-ert proxy or mysql-tile proxy or rabbitMQ proxy)
# should have an uplink ip thats within the specified Logical switch
# These ips should be added as secondary ip for the logical switch vnic
# Only those that are used to go out should go into the Uplink vnic secondary ip (like Router/DiegoBrain/Ops Mgr)
def reconcile_uplinks(context):
	logicalSwitches = context['logical_switches']
	esgInstances = context['edge_service_gateways']


	for esgInstance in esgInstances:
		for routedComponent in esgInstance['routed_components']:

			lswitch = None
			lSwitchName = routedComponent['switch']['name']
			
			for logicalSwitch in logicalSwitches:
				if logicalSwitch['given_name'] in lSwitchName:
					lswitch = logicalSwitch
					break
			
			if not lswitch:
				print 'Unable to find/map logical switch {} for Routed Component: {}'.\
							format(routedComponent['name'], lSwitchName)
			
			lswitchCidr = lswitch['cidr']
			routedComponentUplinkIp = routedComponent['uplink_details']['uplink_ip']

			# Check if the provided uplink ip is part of a logical switch
			isExternalUplink = True
			# If its part of a logical switch, add the uplink ip to the related logical switch's secondary ip
			if routedComponentUplinkIp in ipcalc.Network(lswitchCidr):
				isExternalUplink = False
				lswitch['secondary_ips'].append(routedComponentUplinkIp)

			# If the uplink ip is not part of any other logical switches, 
			# mark it as the real uplink for the routed component
			if isExternalUplink:
				routedComponent['uplink_details']['real_uplink_ip'] = routedComponentUplinkIp

def build_logical_switches(dir, context, type='logical_switches', alternate_template=None):

	logical_switches_dir = os.path.realpath(os.path.join(dir ))
	
	if os.path.isdir(logical_switches_dir):
		shutil.rmtree(logical_switches_dir)
	mkdir_p(logical_switches_dir)

	template_dir = '.'
	if alternate_template is not None:
		template_dir = os.path.join(template_dir, alternate_template)

	vdnScopesResponse = client.get(NSX_URLS['scope']['all'])
	vdnScopesDoc = xmltodict.parse(vdnScopesResponse.text)

	if DEBUG:
		print 'VDN Scopes output: {}'.format(vdnScopesDoc)

	vcenterMobMap = refresh_moid_map(context)
	defaultVdnScopeId = vdnScopesDoc['vdnScopes']['vdnScope']['objectId']

	for lswitch in  context[type]: 

		if check_logical_switch_exists(vcenterMobMap, lswitch['name']):
			print '\tSkipping creation of Logical Switch: {} !!'.format(lswitch['name'])			
			continue

		logical_switches_context = {
			'context': context,
			'logical_switch': lswitch,
			#'managed_service_release_jobs': context['managed_service_release_jobs'],
			'files': []
		}    

		template.render(
			os.path.join(logical_switches_dir, lswitch['name'] + '_payload.xml'),
			os.path.join(template_dir, 'logical_switch_config_post_payload.xml' ),
			logical_switches_context
		)

		# Get the vdn scopes
		#  https://10.193.99.20//api/2.0/vdn/scopes
		# After determining the vdn scope, then post to that scope endpoint

		# POST /api/2.0/vdn/scopes/vdnscope-1/virtualwires
		post_response = client.post_xml(NSX_URLS['scope']['all'] + '/' 
					+ defaultVdnScopeId+'/virtualwires', 
				os.path.join(logical_switches_dir, lswitch['name'] + '_payload.xml'))
		data = post_response.text
		print 'Created Logical Switch : {}\n'.format(lswitch['name'])
		if DEBUG:
			print 'Logical switch creation response:{}\n'.format(data)

def list_logical_switches(context, reportAll=True):

	existinglSwitchesResponse = client.get(NSX_URLS['lswitch']['all']+ '?&startindex=0&pagesize=100')#'/api/2.0/vdn/virtualwires')
	existinglSwitchesResponseDoc = xmltodict.parse(existinglSwitchesResponse.text)
	if DEBUG:
		print 'LogicalSwitches response :{}\n'.format(existinglSwitchesResponse.text) 
	
	virtualWires = existinglSwitchesResponseDoc['virtualWires']['dataPage']['virtualWire']
	lswitchEntries = virtualWires
	if isinstance(virtualWires, dict):
		lswitchEntries = [ virtualWires ]
	
	vcenterMobMap = refresh_moid_map(context)
	print_moid_map(vcenterMobMap)
	
	for lswitch in lswitchEntries:
		lswitch['id'] = lswitch['objectId']

		lswitch['moName'] = mobclient.lookup_logicalswitch_managed_obj_name(lswitch['name']) 
		if not lswitch.get('moName'):
			lswitch['moName'] = ''

	managed_lswitch_names = [ lswitch['name'] for lswitch in context['logical_switches']]

	if reportAll:
		print_logical_switches_available(lswitchEntries)
	else:
		managedLSwitches = [ ]		
		for lswitch in lswitchEntries:
			if lswitch['name'] in managed_lswitch_names:
				managedLSwitches.append(lswitch)
		
		if len(managedLSwitches) > 0:
			print_logical_switches_available(managedLSwitches)

def delete_logical_switches(context, type = 'logical_switches'):

	lswitches = context[type]
	map_logical_switches_id(lswitches)
	
	for lswitch in lswitches:
		
		if  lswitch.get('id') is None:
			continue

		retry = True
		while (retry):
			
			retry = False
			delete_response = client.delete(NSX_URLS['lswitch']['all'] + '/' +
					 lswitch['id'])
			data = delete_response.text

			if DEBUG:
				print 'NSX Logical Switch Deletion response:{}\n'.format(data)

			if delete_response.status_code < 400: 
				print 'Deleted NSX Logical Switch:{}\n'.format(lswitch['name'])

			else:
				print 'Deletion of NSX Logical Switch failed, details: {}\n'.format(data)
				if 'resource is still in use' in str(data):
					retry = True 
					print 'Going to retry deletion again... for Logical Switch:{}\n'.format(lswitch['name'])


def build_nsx_edge_gateways(dir, context, alternate_template=None):
	nsx_edges_dir = os.path.realpath(os.path.join(dir ))
	
	if os.path.isdir(nsx_edges_dir):
		shutil.rmtree(nsx_edges_dir)
	mkdir_p(nsx_edges_dir)

	template_dir = '.'
	if alternate_template is not None:
		template_dir = os.path.join(template_dir, alternate_template)

	logical_switches = context['logical_switches']
	map_logical_switches_id(logical_switches)
	if DEBUG:
		print 'Logical Switches:{}\n'.format(str(logical_switches))

	empty_logical_switches = xrange(len(logical_switches) + 1, 10) 
	vcenterMobMap = refresh_moid_map(context)
	vm_network_moid = mobclient.lookup_moid('VM Network')

	# Go with the VM Network for default uplink
	nsxmanager = context['nsxmanager']

	uplink_port_switch = nsxmanager['uplink_details'].get('uplink_port_switch')
	if uplink_port_switch is None:
		uplink_port_switch = 'VM Network'
		nsxmanager['uplink_details']['uplink_port_switch'] = uplink_port_switch
		
	# if use_port_switch is set to 'VM Network' or port switch id could not be retreived.
	portSwitchId = mobclient.lookup_moid(uplink_port_switch) 
	if (portSwitchId is None):
		nsxmanager['uplink_details']['uplink_id'] = vm_network_moid
	else:
		nsxmanager['uplink_details']['uplink_id'] = portSwitchId
	
	for nsx_edge in  context['edge_service_gateways']:
	
		# Defaults routed components
		# FIX ME -- would have to update this 
		# for any new component that needs direct route via firewall
		opsmgr_routed_component = nsx_edge['routed_components'][0]
		ert_routed_component    = nsx_edge['routed_components'][1]
		diego_routed_component  = nsx_edge['routed_components'][2]
		tcp_routed_component    = nsx_edge['routed_components'][3]

		for routed_component in nsx_edge['routed_components']:
			if 'OPS' in routed_component['name'].upper():
				opsmgr_routed_component = routed_component
			elif 'GO-ROUTER' in routed_component['name'].upper():
				ert_routed_component = routed_component
			elif 'DIEGO' in routed_component['name'].upper():
				diego_routed_component = routed_component
			elif 'TCP-ROUTER' in routed_component['name'].upper():
				tcp_routed_component = routed_component

		ertLogicalSwitch = {}
		infraLogicalSwitch = {}

		for name, lswitch in nsx_edge['global_switches'].iteritems():
			if 'ERT' in name.upper():
				ertLogicalSwitch = lswitch
			elif 'INFRA' in name.upper():
				infraLogicalSwitch = lswitch				

		vcenter_ctx = context['vcenter']

		nsx_edge['datacenter_id'] = mobclient.lookup_moid(vcenter_ctx['datacenter']) 

		# Use the cluster name/id for resource pool...
		nsx_edge['datastore_id'] = mobclient.lookup_moid(vcenter_ctx['datastore']) 
		nsx_edge['cluster_id'] = mobclient.lookup_moid(vcenter_ctx['cluster'])   
		nsx_edge['resourcePool_id'] = mobclient.lookup_moid(vcenter_ctx['cluster'])
		
		# TODO: Ignore the vm folder for now...
		#nsx_edge['vmFolder_id'] = mobclient.lookup_moid(vcenter_ctx['vmFolder']) 

		nsx_edge['monitorMap'] = MONITOR_MAP
		nsx_edge['appRuleMap'] = APP_RULE_MAP
		nsx_edge['appProfileMap'] = APP_PROFILE_MAP

		# Get a large cidr (like 16) that would allow all networks to talk to each other
		cross_network_cidr = calculate_cross_network_cidr(infraLogicalSwitch)
		
		gateway_address = nsx_edge.get('gateway_ip')
		if not gateway_address:
			gateway_address = calculate_gateway(context['nsxmanager']['uplink_details']['uplink_ip'])	

		firewall_src_network_list = logical_switches
		firewall_destn_network_list = logical_switches

		cross_logical_network_combo = cross_combine_lists(firewall_src_network_list, firewall_destn_network_list)		

		if DEBUG:
			print 'NSX Edge config: {}\n'.format(str(nsx_edge))   

		nsx_edges_context = {
			'context': context,
			'defaults': context['defaults'],
			'nsxmanager': context['nsxmanager'],
			'edge': nsx_edge,
			'logical_switches': logical_switches,
			'empty_logical_switches': empty_logical_switches,
			'global_switches': nsx_edge['global_switches'],
			'infraLogicalSwitch': infraLogicalSwitch,
			'ertLogicalSwitch': ertLogicalSwitch,
			'routed_components':  nsx_edge['routed_components'],
			'opsmgr_routed_component': opsmgr_routed_component,
			'ert_routed_component': ert_routed_component,
			'diego_routed_component': diego_routed_component,
			'tcp_routed_component': tcp_routed_component,
			'cross_network_cidr': cross_network_cidr,
			'cross_logical_network_combo': cross_logical_network_combo,
			'gateway_address': gateway_address,
			'files': []
		}    

		template.render(
			os.path.join(nsx_edges_dir, nsx_edge['name'] + '_post_payload.xml'),
			os.path.join(template_dir, 'edge_config_post_payload.xml' ),
			nsx_edges_context
		)
		
		"""
		if True:
		"""
		print 'Creating NSX Edge instance: {}\n\n'.format(nsx_edge['name'])

		post_response = client.post_xml(NSX_URLS['esg']['all'] , 
								os.path.join(nsx_edges_dir, nsx_edge['name'] + '_post_payload.xml'), 
								check=False)
		data = post_response.text
		
		if post_response.status_code < 400: 
			print 'Created NSX Edge :{}\n'.format(nsx_edge['name'])
			certId = add_certs_to_nsx_edge(nsx_edges_dir, nsx_edge)
			print 'Got cert id: {}\n'.format(nsx_edge['cert_id'])
			print 'Now updating LBR config!!'
			add_lbr_to_nsx_edge(nsx_edges_dir, nsx_edge)
			print 'Success!! Finished creation of NSX Edge instance: {}\n\n'.format(nsx_edge['name'])
		else:
			print 'Creation of NSX Edge failed, details:\n{}\n'.format(data)
			raise Exception('Creation of NSX Edge failed, details:\n {}'.format(data))			

def add_certs_to_nsx_edge(nsx_edges_dir, nsx_edge):

	map_nsx_esg_id( [ nsx_edge ] )

	if not nsx_edge.get('certs'):
		print 'No certs section to use an available cert or generate cert was specified for edge instance: {}'.\
					format( nsx_edge['name'])
		raise Exception('Creation of NSX Edge failed, no certs section was provided')	

	if nsx_edge['certs'].get('cert_id'):
		print 'Going to use available cert id: {} for edge instance: {}'.\
					format(nsx_edge['cert_id'], nsx_edge['name'])
		return

	
	if nsx_edge['certs'].get('key') and nsx_edge['certs'].get('cert'):
		print 'Using the provided certs and key for associating with NSX Edge instance: {}'.format(nsx_edge['name'])
		nsx_edge['certs']['key'] = nsx_edge['certs'].get('key').strip() + '\n'
		nsx_edge['certs']['cert'] = nsx_edge['certs'].get('cert').strip() + '\n'
	else:
		cert_config = nsx_edge['certs'].get('config')
		if not cert_config:
			print 'No cert config was specified for edge instance: {}'.\
						format( nsx_edge['name'])
			raise Exception('Creation of NSX Edge failed, no cert config to associate/generate certs was provided')	

		# Try to generate certs if key and cert are not provided
		generate_certs(nsx_edge)
	
	certPayloadFile = os.path.join(nsx_edges_dir, nsx_edge['name'] + '_cert_post_payload.xml')

	template_dir = '.'
	nsx_edges_context = {
		'nsx_edge': nsx_edge,
		'files': []
	}    

	template.render(
		certPayloadFile,
		os.path.join(template_dir, 'edge_cert_post_payload.xml' ),
		nsx_edges_context
	)

	retry = True
	while (retry):
			
		retry = False
		post_response = client.post_xml(NSX_URLS['cert']['all'] + '/' + nsx_edge['id'], 
				certPayloadFile, check=False)
		data = post_response.text

		if DEBUG:
			print 'NSX Edge Cert Addition response:\{}\n'.format(data)

		if post_response.status_code < 400: 
			print 'Added NSX Edge Cert to {}\n'.format(nsx_edge['name'])
			certPostResponseDoc = xmltodict.parse(data)

			certId = certPostResponseDoc['certificates']['certificate']['objectId']
			nsx_edge['cert_id'] = certId

		elif post_response.status_code == 404: 
			print 'NSX Edge not yet up, retrying'
			retry = True 
			print 'Going to retry addition of cert again... for NSX Edge: {}\n'.format(nsx_edge['name'])
		else:
			print 'Addition of NSX Edge Cert failed, details:{}\n'.format(data)
			raise Exception('Addition of NSX Edge failed, details:\n {}'.format(data))

def add_lbr_to_nsx_edge(nsx_edges_dir, nsx_edge):
	
	template_dir = '.'
	
	nsx_edges_context = {
		'nsx_edge': nsx_edge,
		'appProfileMap': nsx_edge['appProfileMap'],
		'appRuleMap': nsx_edge['appRuleMap'],
		'monitorMap': nsx_edge['monitorMap'],
		'routed_components':  nsx_edge['routed_components'],
		'files': []
	}    

	template.render(
		os.path.join(nsx_edges_dir, nsx_edge['name'] + '_lbr_config_put_payload.xml'),
		os.path.join(template_dir, 'edge_lbr_config_put_payload.xml' ),
		nsx_edges_context
	)	
	#exit()

	put_response = client.put_xml(NSX_URLS['esg']['all'] 
									+ '/' + nsx_edge['id']
									+ NSX_URLS['lbrConfig']['all'], 
									os.path.join(nsx_edges_dir, nsx_edge['name'] 
									+ '_lbr_config_put_payload.xml'), 
								check=False)
	data = put_response.text

	if DEBUG:
		print 'NSX Edge LBR Config Update response:{}\n'.format(data)

	if put_response.status_code < 400: 
		print 'Updated NSX Edge LBR Config for : {}\n'.format(nsx_edge['name'])		
	else:
		print 'Update of NSX Edge LBR Config failed, details:{}\n'.format(data)
		raise Exception('Update of NSX Edge LBR Config failed, details:\n {}'.format(data))

def map_nsx_esg_id(edge_service_gateways):
	existingEsgResponse = client.get('/api/4.0/edges')
	existingEsgResponseDoc = xmltodict.parse(existingEsgResponse.text)

	matched_nsx_esgs = 0
	num_nsx_esgs = len(edge_service_gateways)
	
	if DEBUG:
		print 'ESG response :\n{}\n'.format(existingEsgResponse.text) 

	edgeSummaries = existingEsgResponseDoc['pagedEdgeList']['edgePage']['edgeSummary']
	edgeEntries = edgeSummaries
	if isinstance(edgeSummaries, dict):
		edgeEntries = [ edgeSummaries ]

	for existingEsg in edgeEntries:
		if (num_nsx_esgs == matched_nsx_esgs):
			break

		for interested_Esg in  edge_service_gateways: 
			if (interested_Esg['name'] == existingEsg['name'] ):
				interested_Esg['id'] = existingEsg['objectId']
				++matched_nsx_esgs
				break

	for interested_Esg in  edge_service_gateways: 
		if (interested_Esg.get('id') is None):
			print 'NSX ESG instance with name: {} does not exist anymore\n'.format(interested_Esg['name'])

	return matched_nsx_esgs   

def list_nsx_edge_gateways(context):
	existingEsgResponse = client.get(NSX_URLS['esg']['all'] )
	existingEsgResponseDoc = xmltodict.parse(existingEsgResponse.text)

	if DEBUG:
		print 'NSX ESG response :{}\n'.format(existingEsgResponse.text)

	edgeSummaries = existingEsgResponseDoc['pagedEdgeList']['edgePage']['edgeSummary']
	edgeEntries = edgeSummaries
	if isinstance(edgeSummaries, dict):
		edgeEntries = [ edgeSummaries ]

	print_edge_service_gateways_available(edgeEntries)
	
def delete_nsx_edge_gateways(context):

	edge_service_gateways = context['edge_service_gateways']
	map_nsx_esg_id(edge_service_gateways)
	
	for nsx_esg in edge_service_gateways:

		if  nsx_esg.get('id') is None:
			continue

		delete_response = client.delete(NSX_URLS['esg']['all'] + '/' +
				nsx_esg['id'])
		data = delete_response.text

		if DEBUG:
			print 'NSX ESG Deletion response:{}\n'.format(data)

		if delete_response.status_code < 400: 
			print 'Deleted NSX ESG : {}\n'.format(nsx_esg['name'])
		else:
			print 'Deletion of NSX ESG failed, details:{}\n'.format(data +'\n')    


def check_cert_config(nsx_context):

	if not nsx_edge.get('certs'):
		print 'No cert config was specified for edge instance: {}'.\
					format( nsx_edge['name'])
		raise Exception('Creation of NSX Edge failed, no cert config was provided')	

	if not nsx_edge['certs'].get('config'):
		print 'No cert config was specified for edge instance: {}'.\
					format( nsx_edge['name'])
		raise Exception('Creation of NSX Edge failed, neither cert_id nor config to generate certs was provided')	

def generate_certs(nsx_context):

	output_dir = './' + nsx_context['certs']['name']
	cert_config = nsx_context['certs'].get('gen_config')
	if not cert_config:
		cert_config = nsx_context['certs'].get('config')
 
	org_unit = cert_config['org_unit']
	country = cert_config['country_code']

	subprocess.call(
					[ 
						'./certGen.sh', 
						cert_config['system_domain'], 
						cert_config['app_domain'], 
						output_dir, 
						org_unit, 
						country 
					]
				)

	nsx_context['certs']['key'] = readFileContent(output_dir + '/*.key')
	nsx_context['certs']['cert'] = readFileContent(output_dir + '/*.crt')
	nsx_context['certs']['name'] = 'Cert for ' + nsx_context['certs']['name']
	nsx_context['certs']['description'] = nsx_context['certs']['name'] + '-' + nsx_context['certs']['config']['system_domain']

def readFileContent(filePath):
	txt = glob.glob(filePath)
	for textfile in txt:
		with open(textfile, 'r') as myfile:
			response=myfile.read()
		return response

def calculate_cross_network_cidr(infraLogicalSwitch):

	# Get a large cidr (like 16) that would allow all networks to talk to each other
	infraIpSegment = infraLogicalSwitch['cidr'].split('/')[0]
	infraIpTokens  = infraIpSegment.split('.')
	cross_network_cidr = '{}.{}.0.0/16'.format(infraIpTokens[0], 
												infraIpTokens[1])
	return cross_network_cidr

def calculate_gateway(global_uplink_ip):

	
	uplinkIpTokens   = global_uplink_ip.split('.')
	gateway_address  = '{}.{}.{}.1'.format(	uplinkIpTokens[0], 
											uplinkIpTokens[1],
											uplinkIpTokens[2])
	return gateway_address

# Create a cross list of network cidrs for firewall rules
# Ignore pairing of same entries
def cross_combine_lists(list1, list2):
	result = [(x,y) for x in list1 for y in list2]
	edited_result =  [ ]
	for pair in result:
		if pair[0] != pair[1]:
			edited_result.append(pair)

	return edited_result
