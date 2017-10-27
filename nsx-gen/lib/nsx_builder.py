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
import copy
import glob
import mobclient
import subprocess
import xmltodict
import dicttoxml

from pprint import pprint

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

sys.path.append(os.path.join(LIB_PATH, os.path.join('../..')))

from util import *
from print_util import *
from routed_components_handler import *
from nsx_urls import *

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

def mapVcenterResources(context, moidMap):
    vcenter_context = context['vcenter']

    lookupVCenterMoid(context, 'datacenter', moidMap)
    lookupVCenterMoid(context, 'datastore', moidMap)

    if DEBUG:
        print('vCenter context updated\n')
        pprint(vars(vcenter_context))

def build(context, verbose=False):
    client.set_context(context, 'nsxmanager')
    moidMap = refresh_moid_map(context)
    if DEBUG:
        pprint(moidMap)   
    
    reconcile_uplinks(context)
    #build_transport_zone('tz', context, 'transport_zone')
    
    build_logical_switches('lswitch', context, 'logical_switches')
    build_nsx_dlrs('dlr', context)
    build_nsx_edge_gateways('edge', context)

def delete(context, verbose=False):
    client.set_context(context, 'nsxmanager')
    refresh_moid_map(context)
  
    delete_nsx_edge_gateways(context) 
    delete_nsx_dlr_gateways(context)      
    delete_logical_switches(context, 'logical_switches')

    # Run delete once more for hte logical switches just to be safe... 
    # Sometimes they stay around
    delete_logical_switches(context, 'logical_switches')

def list(context, verbose=False):
    client.set_context(context, 'nsxmanager')
    moidMap = refresh_moid_map(context)
    if DEBUG:
        pprint(moidMap)    

    reconcile_uplinks(context)
    list_logical_switches(context)
    list_nsx_edge_gateways(context)    

def export_firewall_rules(context, verbose=False):
    client.set_context(context, 'nsxmanager')
    moidMap = refresh_moid_map(context)
    if DEBUG:
        pprint(moidMap)    

    export_nsx_edge_gateway_firewall_rules(context)  

def map_logical_switches_id(logical_switches):
    existinglSwitchesResponse = client.get(NSX_URLS['lswitch']['all'] + '?&startindex=0&pagesize=100')
    existinglSwitchesResponseDoc = xmltodict.parse(existinglSwitchesResponse.text)
    if DEBUG:
        print('LogicalSwitches response :{}\n'.format(existinglSwitchesResponse.text)) 
    
    num_lswitches = len(logical_switches)
    matched_lswitches = 0

    virtualWires = existinglSwitchesResponseDoc['virtualWires']['dataPage']['virtualWire']
    lswitchEntries = virtualWires
    if isinstance(virtualWires, dict):
        lswitchEntries = [ virtualWires ]

    for existingLSwitch in lswitchEntries:
        if (num_lswitches == matched_lswitches):
            break

        for interested_lswitch in logical_switches: 
            if interested_lswitch['name'] == existingLSwitch['name']:
                interested_lswitch['id'] = existingLSwitch['objectId']

                ++matched_lswitches
                break

    if len(logical_switches) > 0:
            print_logical_switches_available(logical_switches)

    if DEBUG:
        for interested_lswitch in logical_switches: 
            if (interested_lswitch.get('id') is None):
                print('Logical Switch instance with name: {} does not exist, possibly deleted already'\
                .format(interested_lswitch['name']))

def check_logical_switch_exists(vcenterMobMap, lswitchName):

    fullMobName = mobclient.lookup_logicalswitch_managed_obj_name(lswitchName)
    # For a lswitch with name ' lswitch-nsx-pcf-CF-Tiles'
    # it would have a MOB name of 'vxw-dvs-29-virtualwire-225-sid-5066-lswitch-nsx-pcf-CF-Tiles'
    if fullMobName is None:
        return False

    if 'vxw-' in fullMobName and '-virtualwire-' in fullMobName:
        print('Logical switch : {} exists with MOB:{}'.format(lswitchName, fullMobName))
        return True

    return False

# Any internal component that requires VIP (like mysql-ert proxy or mysql-tile proxy or rabbitMQ proxy)
# should have an uplink ip thats within the specified Logical switch
# These ips should be added as secondary ip for the logical switch vnic
# Only those that are used to go out should go into the Uplink vnic secondary ip (like Router/DiegoBrain/Ops Mgr)
def reconcile_uplinks(context):
    logicalSwitches = context['logical_switches']
    esgInstances = context['edge_service_gateways']

    enable_dlr = context['nsxmanager']['enable_dlr']

    ospfLogicalSwitch = None
    if enable_dlr:
        for logicalSwitch in logicalSwitches:
            if 'OSPF' in logicalSwitch['name'].upper():
                ospfLogicalSwitch = logicalSwitch

    for esgInstance in esgInstances:
        for routedComponent in esgInstance['routed_components']:

            lswitch = None
            lSwitchName = routedComponent['switch']['name']
            
            for logicalSwitch in logicalSwitches:
                if logicalSwitch['given_name'] in lSwitchName:
                    lswitch = logicalSwitch
                    break
            
            if not lswitch:
                print('Unable to find/map logical switch {} for Routed Component: {}'.\
                            format(routedComponent['name'], lSwitchName))
            
            lswitchCidr = lswitch['cidr']
            routedComponentUplinkIp = routedComponent['uplink_details']['uplink_ip']

            # Check if the provided uplink ip is part of a logical switch
            isExternalUplink = True

            #print 'Routed component {} has uplink ip: {} and lswitch:{}'.format(\
            # routedComponent['name'], routedComponentUplinkIp, lswitch['name'])
            
            # If its part of a logical switch, add the uplink ip to the related logical switch's secondary ip
            if routedComponentUplinkIp in ipcalc.Network(lswitchCidr):
                isExternalUplink = False
                lswitch['secondary_ips'].append(routedComponentUplinkIp)
                #print 'Routed component {} added to secondary for lswitch: {}'.format(\
                # routedComponent['name'], lswitch['name'])
            
            # If we come here - means the uplink ip was not part of a lswitch
            # Can happen in case of VIP exposed on OSPF but the component is on a internal logical switch like for PCF-Tiles
            if isExternalUplink and not routedComponent['external']:
                isExternalUplink = False
                if enable_dlr:
                    ospfLogicalSwitch['secondary_ips'].append(routedComponentUplinkIp)
                #print 'Routed component {} added to secondary for lswitch: {}'.format(\
                # routedComponent['name'], ospfLogicalSwitch['name'])
            
            
            # If the uplink ip is not part of any other logical switches, 
            # mark it as the real uplink for the routed component
            if isExternalUplink:
                routedComponent['uplink_details']['real_uplink_ip'] = routedComponentUplinkIp
                #print 'Routed component {} mareked with routed component uplink ip: {}'.format(\
                # routedComponent['name'], routedComponentUplinkIp)

# Check for existence of transport zone and wire the id
def check_transport_zone(context):
    transport_zone_name = context['nsxmanager'].get('transport_zone')
    if not transport_zone_name:
        transport_zone_name = context['name'] + '-tz'

    print 'Checking for Transport Zone, name: {}'.format(transport_zone_name)
    vdnScopesResponse = client.get(NSX_URLS['scope']['all'])
    vdnScopesDoc = xmltodict.parse(vdnScopesResponse.text)

    if DEBUG:
        print('VDN Scopes output: {}'.format(vdnScopesDoc))

    # Handle multiple Transport zones
    vdnScopes = vdnScopesDoc['vdnScopes'].get('vdnScope')
    if vdnScopes:
        # If just single entry, just wrap it in an array
        if isinstance(vdnScopes, dict):
            vdnScopes = [ vdnScopes ]

        for entry in vdnScopes:
            if DEBUG:
                print('Transport Zone name in entry: {}'.format(entry['name']))
            
            if entry['name'] == transport_zone_name:
                context['nsxmanager']['transport_zone'] = entry['name']
                context['nsxmanager']['transport_zone_id'] = entry['objectId']
                print('Found matching TZ: {}, VDN Scope id :{}\n'.format(entry['name'], entry['objectId']))
                return True

    return False

def build_transport_zone(dir, context, type='transport_zone', alternate_template=None):

    # if found the matching transport zone (either given or default), return
    if check_transport_zone(context):
        return

    # Transport zone does not exist, lets create
    transport_zone_name = context['nsxmanager'].get('transport_zone')
    if not transport_zone_name:
        transport_zone_name = context['name'] + '-tz'

    transport_zone = {}
    transport_zone['name'] = transport_zone_name
    transport_zone['cluster_names'] = context['nsxmanager'].get('transport_zone_clusters').strip()
    if transport_zone['cluster_names'] == '':
        raise Exception('Error! No cluster members specified to create the Transport Zone...!!')
    
    cluster_ids = ''
    for cluster_name in transport_zone['cluster_names'].split(','):
        cluster_id = mobclient.lookup_moid(cluster_name.strip())
        if 'domain' in cluster_id:
            cluster_ids += cluster_id + ','

    cluster_ids = cluster_ids.strip(',')
    if cluster_ids == '':
        raise Exception('Error! No matching cluster members found to create the Transport Zone...!!')
    
    transport_zone['cluster_ids'] = cluster_ids
    tz_context = {
        'context': context,
        'transport_zone': transport_zone,
        'files': []
    }    

    transport_zones_dir = os.path.realpath(os.path.join(dir ))
    if os.path.isdir(transport_zones_dir):
        shutil.rmtree(transport_zones_dir)
    mkdir_p(transport_zones_dir)

    template_dir = '.'
    if alternate_template is not None:
        template_dir = os.path.join(template_dir, alternate_template)

    template.render(
        os.path.join(transport_zones_dir, transport_zone['name'] + '_payload.xml'),
        os.path.join(template_dir, 'vdn_scope_post_payload.xml' ),
        tz_context
    )

    post_response = client.post_xml(NSX_URLS['scope']['all'], 
            os.path.join(transport_zones_dir, transport_zone['name'] + '_payload.xml'))
    data = post_response.text
    if DEBUG:
        print('Transport Zone creation response:{}\n'.format(data))

    if post_response.status_code < 400: 
        print('Created Transport Zone : {}\n'.format(transport_zone['name']))
        context['nsxmanager']['transport_zone'] = transport_zone['name']
        context['nsxmanager']['transport_zone_id'] = data

def delete_transport_zone(context):

    # if no transport zone, nothing to delete
    if not check_transport_zone(context):
        return

    transport_zone_id = context['nsxmanager']['transport_zone_id']
    delete_response = client.delete(NSX_URLS['scope']['all'] + '/' +
             transport_zone_id, False)
    data = delete_response.text

def build_logical_switches(dir, context, type='logical_switches', alternate_template=None):

    logical_switches_dir = os.path.realpath(os.path.join(dir ))
    
    if os.path.isdir(logical_switches_dir):
        shutil.rmtree(logical_switches_dir)
    mkdir_p(logical_switches_dir)

    template_dir = '.'
    if alternate_template is not None:
        template_dir = os.path.join(template_dir, alternate_template)

    vcenterMobMap = refresh_moid_map(context)
    
    transportZone = context['nsxmanager'].get('transport_zone')
    
    try:
        transportZoneClusters = context['nsxmanager'].get('transport_zone_clusters')
    except KeyError:
        pass
    
    if transportZone or transportZoneClusters:
        build_transport_zone(dir, context, 'transport_zone')
    else:
        raise Exception('Error! No transport zone name or cluster members specified to create the Transport Zone...!!')
    
    defaultVdnScopeId = context['nsxmanager']['transport_zone_id']

    enable_dlr = context['nsxmanager']['enable_dlr']
        
    for lswitch in  context[type]: 

        # Skip if DLR is disabled and OSPF is in the switch name
        if not enable_dlr and 'OSPF' in lswitch['name']:
            continue

        if check_logical_switch_exists(vcenterMobMap, lswitch['name']):
            print('\tSkipping creation of Logical Switch: {} !!'.format(lswitch['name']))           
            continue

        logical_switches_context = {
            'context': context,
            'logical_switch': lswitch,
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
        print('Created Logical Switch : {}\n'.format(lswitch['name']))
        if DEBUG:
            print('Logical switch creation response:{}\n'.format(data))

def list_logical_switches(context, reportAll=True):

    existinglSwitchesResponse = client.get(NSX_URLS['lswitch']['all']+ '?&startindex=0&pagesize=100')#'/api/2.0/vdn/virtualwires')
    existinglSwitchesResponseDoc = xmltodict.parse(existinglSwitchesResponse.text)
    if DEBUG:
        print('LogicalSwitches response :{}\n'.format(existinglSwitchesResponse.text)) 
    
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

        retry = 0
        while (retry < 3):
            
            delete_response = client.delete(NSX_URLS['lswitch']['all'] + '/' +
                     lswitch['id'], False)
            data = delete_response.text

            if DEBUG:
                print('NSX Logical Switch {} Deletion response:{}\n'.format(lswitch['name'], data))

            if delete_response.status_code < 400: 
                print('Deleted NSX Logical Switch:{}\n'.format(lswitch['name']))
                break

            print('Deletion of NSX Logical Switch {} failed, details: {}\n'.format(lswitch['name'], data))
            if 'resource is still in use' in str(data):
                retry += 1
                print('Going to retry deletion again... for Logical Switch:{}\n'.format(lswitch['name']))
            else:
                print('Cannot retry deletion..., skipping delete for Logical Switch:{}\n'.format(lswitch['name']))
                break

def build_nsx_dlrs(dir, context, alternate_template=None):
    nsx_dlrs_dir = os.path.realpath(os.path.join(dir ))
    
    if os.path.isdir(nsx_dlrs_dir):
        shutil.rmtree(nsx_dlrs_dir)
    mkdir_p(nsx_dlrs_dir)

    template_dir = '.'
    if alternate_template is not None:
        template_dir = os.path.join(template_dir, alternate_template)

    logical_switches = context['logical_switches']
    map_logical_switches_id(logical_switches)
    if DEBUG:
        print('Logical Switches:{}\n'.format(str(logical_switches)))

    empty_logical_switches = xrange(len(logical_switches) + 1, 10) 
    vcenterMobMap = refresh_moid_map(context)
    vm_network_moid = mobclient.lookup_moid('VM Network')

    # Go with the VM Network for default uplink
    nsxmanager = context['nsxmanager']
    enable_dlr = nsxmanager['enable_dlr']
    if enable_dlr:
        nsxmanager['distributed_portgroup_id'] =  mobclient.lookup_moid(nsxmanager['distributed_portgroup'])

    uplink_port_switch = nsxmanager['uplink_details'].get('uplink_port_switch')
    if uplink_port_switch is None:
        uplink_port_switch = 'VM Network'
        nsxmanager['uplink_details']['uplink_port_switch'] = uplink_port_switch
    
    # if use_port_switch is set to 'VM Network' or port switch id could not be retreived.
    portSwitchId = mobclient.lookup_moid(uplink_port_switch) 
    if (portSwitchId is None):
        #nsxmanager['uplink_details']['uplink_id'] = vm_network_moid
        raise Exception('Error! Uplink Port Group not defined...!!')
    
    nsxmanager['uplink_details']['uplink_id'] = portSwitchId

    dlr_instances = []
    
    for nsx_edge in  context['edge_service_gateways']:
    
        enable_dlr = nsx_edge['enable_dlr']
        if not enable_dlr:
            print('DLR disabled!! Not creating DLR for NSX Edge: ' + nsx_edge['name'])
            continue

        nsx_dlr = copy.deepcopy(nsx_edge)

        vcenter_ctx = context['vcenter']

        nsx_dlr['name'] = nsx_dlr['name'] + '-dlr'
        print('Name of DLR: ' + nsx_dlr['name'])
        nsx_dlr['datacenter_id'] = mobclient.lookup_moid(vcenter_ctx['datacenter']) 

        # Use the cluster name/id for resource pool...
        nsx_dlr['datastore_id'] = mobclient.lookup_moid(vcenter_ctx['datastore']) 
        nsx_dlr['cluster_id'] = mobclient.lookup_moid(vcenter_ctx['cluster'])   
        nsx_dlr['resourcePool_id'] = mobclient.lookup_moid(vcenter_ctx['cluster'])

        
        gateway_address = nsx_dlr.get('gateway_ip')
        if not gateway_address:
            gateway_address = calculate_gateway(context['nsxmanager']['uplink_details']['uplink_ip'])
            nsx_dlr['gateway_ip'] = gateway_address 

        nsx_dlrs_context = {
            'context': context,
            'defaults': context['defaults'],
            'nsxmanager': context['nsxmanager'],
            'dlr': nsx_dlr,
            'logical_switches': logical_switches,
            'empty_logical_switches': empty_logical_switches,
            'gateway_address': gateway_address,
            'files': []
        }    

        template.render(
            os.path.join(nsx_dlrs_dir, nsx_dlr['name'] + '_dlr_post_payload.xml'),
            os.path.join(template_dir, 'dlr_config_post_payload.xml' ),
            nsx_dlrs_context
        )
        
        print('Creating NSX DLR instance: {}\n\n'.format(nsx_dlr['name']))

        post_response = client.post_xml(NSX_URLS['esg']['all'] , 
                                os.path.join(nsx_dlrs_dir, nsx_dlr['name'] + '_dlr_post_payload.xml'), 
                                check=False)
        data = post_response.text
        
        if post_response.status_code < 400: 
            print('Created NSX DLR :{}\n'.format(nsx_dlr['name']))
            print('Success!! Finished creation of NSX DLR instance: {}\n\n'.format(nsx_dlr['name']))
            add_ospf_to_nsx_dlr(nsx_dlrs_dir, context, nsx_dlr)
            print('Success!! Finished adding OSPF & Interfaces for NSX DLR instance: {}\n\n'.format(nsx_dlr['name']))
        else:
            print('Creation of NSX DLR failed, details:\n{}\n'.format(data))
            raise Exception('Creation of NSX DLR failed, details:\n {}'.format(data))           

        dlr_instances.append(nsx_dlr)

    context['nsx_dlrs'] = dlr_instances

def add_ospf_to_nsx_dlr(nsx_dlrs_dir, context, nsx_dlr):

    map_nsx_esg_id( [ nsx_dlr ] )

    template_dir = '.'
    logical_switches = context['logical_switches']
    
    nsx_dlrs_context = {
        'context': context,
        'defaults': context['defaults'],
        'nsxmanager': context['nsxmanager'],
        'dlr': nsx_dlr,
        'logical_switches': logical_switches,
        'gateway_address': nsx_dlr['gateway_ip'],
        'files': []
    }    


    template.render(
        os.path.join(nsx_dlrs_dir, nsx_dlr['name'] + '_dlr_config_put_payload.xml'),
        os.path.join(template_dir, 'dlr_config_put_payload.xml' ),
        nsx_dlrs_context
    )

    put_response = client.put_xml(NSX_URLS['esg']['all'] 
                                    + '/' + nsx_dlr['id'], 
                                    os.path.join(nsx_dlrs_dir, nsx_dlr['name'] 
                                    + '_dlr_config_put_payload.xml'), 
                                check=False)
    data = put_response.text

    if DEBUG:
        print('NSX DLR Config Update response:{}\n'.format(data))

    if put_response.status_code < 400: 
        print('Updated NSX DLR Config for : {}\n'.format(nsx_dlr['name']))      
    else:
        print('Update of NSX DLR Config failed, details:{}\n'.format(data))
        raise Exception('Update of NSX DLR Config failed, details:\n {}'.format(data))

def delete_nsx_dlr_gateways(context):

    nsx_dlrs = context.get('nsx_dlrs')
    if not nsx_dlrs:
        nsx_dlrs = []
        edge_service_gateways = context['edge_service_gateways']
        for edge in  edge_service_gateways:
            nsx_dlrs.append( { 'name': edge['name'] + '-dlr' })

    map_nsx_esg_id(nsx_dlrs)
    
    for nsx_dlr in nsx_dlrs:

        if  nsx_dlr.get('id') is None:
            continue

        delete_response = client.delete(NSX_URLS['esg']['all'] + '/' +
                nsx_dlr['id'])
        data = delete_response.text

        if DEBUG:
            print('NSX DLR Deletion response:{}\n'.format(data))

        if delete_response.status_code < 400: 
            print('Deleted NSX DLR : {}\n'.format(nsx_dlr['name']))
        else:
            print('Deletion of NSX DLR failed, details:{}\n'.format(data +'\n'))    

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
        print('Logical Switches:{}\n'.format(str(logical_switches)))

    empty_logical_switches = xrange(len(logical_switches) + 1, 10) 
    vcenterMobMap = refresh_moid_map(context)
    vm_network_moid = mobclient.lookup_moid('VM Network')

    # Go with the VM Network for default uplink
    nsxmanager = context['nsxmanager']
    bosh_nsx_enabled = nsxmanager['bosh_nsx_enabled']

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

        isozone_routed_components = []
        iso_zones = []


        for routed_component in nsx_edge['routed_components']:
            routed_component_name_upper = routed_component['name'].upper()

            if 'ISOZONE' in routed_component_name_upper:
                isozone_routed_components.append(routed_component)
                iso_zone = { 'name' : routed_component['switch']['given_name'] }

                if iso_zone not in iso_zones:
                    iso_zones.append(iso_zone)
            else:
                if 'OPS' in routed_component_name_upper:
                    opsmgr_routed_component = routed_component
                elif 'GO-ROUTER' in routed_component_name_upper:
                    ert_routed_component = routed_component
                elif 'DIEGO' in routed_component_name_upper:
                    diego_routed_component = routed_component
                elif 'TCP-ROUTER' in routed_component_name_upper:
                    tcp_routed_component = routed_component

        nsx_edge['iso_zones'] = iso_zones

        ertLogicalSwitch = {}
        infraLogicalSwitch = {}
        ospfLogicalSwitch = {}

        for name, lswitch in nsx_edge['global_switches'].iteritems():
            switch_name_upper = name.upper()
            if 'ERT' in switch_name_upper:
                ertLogicalSwitch = lswitch
            elif 'INFRA' in switch_name_upper:
                infraLogicalSwitch = lswitch
            elif 'OSPF' in switch_name_upper:
                ospfLogicalSwitch = lswitch             

        nsx_edge['bosh_nsx_enabled'] = bosh_nsx_enabled
        nsx_edge['http_lbr_enabled'] = nsxmanager['http_lbr_enabled']

        vcenter_ctx = context['vcenter']

        nsx_edge['datacenter_id'] = mobclient.lookup_moid(vcenter_ctx['datacenter']) 

        # Use the cluster name/id for resource pool...
        nsx_edge['datastore_id'] = mobclient.lookup_moid(vcenter_ctx['datastore']) 
        nsx_edge['cluster_id'] = mobclient.lookup_moid(vcenter_ctx['cluster'])   
        nsx_edge['resourcePool_id'] = mobclient.lookup_moid(vcenter_ctx['cluster'])
        
        # TODO: Ignore the vm folder for now...
        #nsx_edge['vmFolder_id'] = mobclient.lookup_moid(vcenter_ctx['vmFolder']) 

        # Get a large cidr (like 16) that would allow all networks to talk to each other
        cross_network_cidr = calculate_cross_network_cidr(infraLogicalSwitch)
        
        gateway_address = nsx_edge.get('gateway_ip')
        if not gateway_address:
            gateway_address = calculate_gateway(context['nsxmanager']['uplink_details']['uplink_ip'])   

        firewall_src_network_list = logical_switches
        firewall_destn_network_list = logical_switches

        cross_logical_network_combo = cross_combine_lists(firewall_src_network_list, firewall_destn_network_list)       

        if DEBUG:
            print('NSX Edge config: {}\n'.format(str(nsx_edge)))   

        nsx_edges_context = {
            'context': context,
            'defaults': context['defaults'],
            'nsxmanager': context['nsxmanager'],
            'static_routes': context['nsxmanager']['static_routes'],
            'edge': nsx_edge,
            'enable_dlr': nsx_edge['enable_dlr'],
            'logical_switches': logical_switches,
            'empty_logical_switches': empty_logical_switches,
            'global_switches': nsx_edge['global_switches'],
            'ospfLogicalSwitch': ospfLogicalSwitch,
            'infraLogicalSwitch': infraLogicalSwitch,
            'ertLogicalSwitch': ertLogicalSwitch,
            'routed_components':  nsx_edge['routed_components'],
            'opsmgr_routed_component': opsmgr_routed_component,
            'ert_routed_component': ert_routed_component,
            'diego_routed_component': diego_routed_component,
            'tcp_routed_component': tcp_routed_component,
            'isozone_routed_components': isozone_routed_components,
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
        print('Creating NSX Edge instance: {}\n\n'.format(nsx_edge['name']))
        post_response = client.post_xml(NSX_URLS['esg']['all'] , 
                                os.path.join(nsx_edges_dir, nsx_edge['name'] + '_post_payload.xml'), 
                                check=False)
        data = post_response.text
        
        if post_response.status_code < 400: 
            print('Success!! Created NSX Edge :{}\n'.format(nsx_edge['name']))
            add_ert_certs_to_nsx_edge(nsx_edges_dir, nsx_edge)
            add_iso_certs_to_nsx_edge(nsx_edges_dir, nsx_edge)
            print('Finished adding certs to NSX Edge :{}!!\n'.format(nsx_edge['name']))

            print('Updating LBR config!!')
            add_lbr_to_nsx_edge(nsx_edges_dir, nsx_edge)
            print('Success!! Finished complete creation of NSX Edge instance: {}\n\n'.format(nsx_edge['name']))
        else:
            print('Creation of NSX Edge failed, details:\n{}\n'.format(data))
            raise Exception('Creation of NSX Edge failed, details:\n {}'.format(data))          


def add_certs_to_nsx_edge(nsx_edges_dir, nsx_edge, cert_section):

    map_nsx_esg_id( [ nsx_edge ] )

    cert_config = cert_section.get('config')
    if not cert_config and not cert_section.get('key'):
        print('No certs section to use an available cert or generate cert was specified for cert: {} for edge instance: {}'.\
                    format( cert_section['name'], nsx_edge['name']))
        raise Exception('Creation of NSX Edge failed, no certs section was provided')   

    if cert_config.get('cert_id'):
        print('Going to use available cert id: {} from its cert_config for edge instance: {}'.\
                    format(cert_config['cert_id'], nsx_edge['name']))
        return

    
    if cert_section.get('key') and cert_section.get('cert'):
        print('Using the provided certs and key for associating with NSX Edge instance: {}'.format(nsx_edge['name']))
        cert_section['key'] = cert_section.get('key').strip() + '\n'
        cert_section['cert'] = cert_section.get('cert').strip() + '\n'
    else:
        # Try to generate certs if key and cert are not provided
        generate_certs(cert_section)
    
    certPayloadFile = os.path.join(nsx_edges_dir, cert_section['name'] + '_cert_post_payload.xml')

    template_dir = '.'
    nsx_cert_context = {
        'certs': cert_section,
        'files': []
    }    

    template.render(
        certPayloadFile,
        os.path.join(template_dir, 'edge_cert_post_payload.xml' ),
        nsx_cert_context
    )

    retry = True
    while (retry):
            
        retry = False
        post_response = client.post_xml(NSX_URLS['cert']['all'] + '/' + nsx_edge['id'], 
                certPayloadFile, check=False)
        data = post_response.text

        if DEBUG:
            print('NSX Edge Cert {} addition response:\{}\n'.format(cert_section['name'], data))

        if post_response.status_code < 400: 
            certPostResponseDoc = xmltodict.parse(data)

            certId = certPostResponseDoc['certificates']['certificate']['objectId']
            cert_section['cert_id'] = certId
            print('Added `{}` cert with id: `{}` to NSX Edge: `{}`\n'.format(cert_section['name'], cert_section['cert_id'], nsx_edge['name']))
            return certId

        elif post_response.status_code == 404: 
            print('NSX Edge {} not yet up, retrying!!'.format(nsx_edge['name']))
            retry = True 
            print('Going to retry addition of cert {} again... for NSX Edge: {}\n'.format(cert_section['name'], nsx_edge['name']))
        else:
            print('Addition of NSX Edge Cert {} failed, details:{}\n'.format(cert_section['name'], data))
            raise Exception('Addition of NSX Edge Cert `{}` failed, details:\n {}'.format(cert_section['name'], data))


def add_ert_certs_to_nsx_edge(nsx_edges_dir, nsx_edge):

    ert_cert_section = nsx_edge['ert_certs']
    if not ert_cert_section:
        print('No Ert certs section defined to use an available cert or generate cert was specified for cert: {} for edge instance: {}'.\
                    format( cert_section['name'], nsx_edge['name']))
        raise Exception('Creation of NSX Edge failed, no ert certs section was provided')   

    if ert_cert_section.get('cert_id'):
        # Use the available cert id, nothing to do
        nsx_edge['cert_id'] = ert_cert_section['cert_id']
        return

    if ert_cert_section.get('key') and ert_cert_section.get('cert'):
        # Use the available key & cert
        ert_cert_id = add_certs_to_nsx_edge(nsx_edges_dir, nsx_edge, ert_cert_section)
        nsx_edge['cert_id'] = ert_cert_id
        return

    sys_domain = ert_cert_section['config'].get('system_domain')
    app_domain = ert_cert_section['config'].get('app_domain')

    if not sys_domain and not app_domain:
        print('No system or app domain defined was specified for Ert Cert generation for edge instance: {}'.\
                    format( nsx_edge['name']))
        raise Exception('Creation of NSX Edge failed, no domains was provided') 

    sys_domain = sys_domain.replace(' ', '')
    app_domain = app_domain.replace(' ', '')
    complete_domain = '{},login.{},uaa.{},{}'.format(sys_domain, sys_domain, sys_domain, app_domain)

    ert_cert_section['config']['domains'] = complete_domain
    ert_cert_id = add_certs_to_nsx_edge(nsx_edges_dir, nsx_edge, ert_cert_section)
    nsx_edge['cert_id'] = ert_cert_id

def add_iso_certs_to_nsx_edge(nsx_edges_dir, nsx_edge):

    ert_certs_section = nsx_edge['ert_certs']
    iso_certs_section = nsx_edge['iso_certs']

    if not iso_certs_section:
        print('No Iso certs section defined to use an available cert or generate cert , going to reuse ERT cert id for edge instance: {}'.\
                    format( nsx_edge['name']))
        return  

    iso_zones = nsx_edge['iso_zones']

    # Generate or directly add cert for each iso segment specified
    index = 0
    for iso_cert in iso_certs_section:

        # Use the available cert id             
        if iso_cert.get('cert_id'):
            certId = iso_cert['cert_id']        
        elif iso_cert.get('key') and iso_cert.get('cert'):          
            add_certs_to_nsx_edge(nsx_edges_dir, nsx_edge, iso_cert)
        else:
            if not iso_cert.get('config') or not iso_cert.get('config').get('domains'):
                print('No domains defined for Iso Zone {} cert generation for edge instance: {}'.\
                            format( iso_cert.get('name'), nsx_edge['name']))
                continue
                #raise Exception('Creation of NSX Edge failed, no domains were provided for iso zone:{}'.format(iso_cert['name']))  


            certId = add_certs_to_nsx_edge(nsx_edges_dir, nsx_edge, iso_cert)

        found_iso_zone = False
        certId = iso_cert['cert_id']
        
        for iso_zone in iso_zones:
            if (iso_zone['name'] == iso_cert.get('switch')):
                found_iso_zone = True
                iso_zone['cert_id'] = certId
                break

        # If the switch name is not matching, just go by the index 
        # hoping the user specified the right cert in the same order as the logical switch
        if not found_iso_zone:
            try:
                iso_zone = iso_zones[index]
                iso_zone['cert_id'] = certId
            except IndexError:
                raise Exception('Unable to find matching switch for specified iso cert, details:\n {}'.format(iso_cert))

        index += 1

    # Ensure every iso zone has some cert_id associated with it,
    # use the ERT cert id for those missing certs
    ert_cert_id = nsx_edge['cert_id']
    for iso_zone in iso_zones:
        if not iso_zone.get('cert_id'):
            iso_zone['cert_id'] = ert_cert_id

def add_lbr_to_nsx_edge(nsx_edges_dir, nsx_edge):
    
    template_dir = '.'

    iso_zones = nsx_edge['iso_zones']
    app_profiles = nsx_edge['app_profiles']
    ert_certId = nsx_edge['cert_id']

    # Link the iso cert id against the corresponding app profiles, 
    # if they are using any ssl/secure protocol and are associated 
    # with Ert or IsoZone switches
    for app_profile in app_profiles:
        switch_name = app_profile.get('switch')
        app_profile_name = app_profile['name']

        if app_profile['requires_cert']:
            if switch_name and 'ISOZONE' in switch_name.upper():
                for iso_zone in iso_zones:
                    if switch_name == iso_zone['name']:
                        app_profile['cert_id'] = iso_zone['cert_id']
                        continue
            # Use the same ert cert id for those not associated with any switches too
            else: #if not switch_name or (switch_name and 'ERT' in switch_name.upper()):
                app_profile['cert_id'] = ert_certId
                continue
            
    nsx_edges_context = {
        'nsx_edge': nsx_edge,
        'app_profiles': app_profiles,
        'app_rules': nsx_edge['app_rules'],
        'monitor_list': nsx_edge['monitor_list'],
        'routed_components':  nsx_edge['routed_components'],
        'files': []
    }    

    template.render(
        os.path.join(nsx_edges_dir, nsx_edge['name'] + '_lbr_config_put_payload.xml'),
        os.path.join(template_dir, 'edge_lbr_config_put_payload.xml' ),
        nsx_edges_context
    )

    put_response = client.put_xml(NSX_URLS['esg']['all'] 
                                    + '/' + nsx_edge['id']
                                    + NSX_URLS['lbrConfig']['all'], 
                                    os.path.join(nsx_edges_dir, nsx_edge['name'] 
                                    + '_lbr_config_put_payload.xml'), 
                                check=False)
    data = put_response.text

    if DEBUG:
        print('NSX Edge LBR Config Update response:{}\n'.format(data))

    if put_response.status_code < 400: 
        print('Updated NSX Edge LBR Config for : {}\n'.format(nsx_edge['name']))        
    else:
        print('Update of NSX Edge LBR Config failed, details:{}\n'.format(data))
        raise Exception('Update of NSX Edge LBR Config failed, details:\n {}'.format(data))

def map_nsx_esg_id(edge_service_gateways):
    existingEsgResponse = client.get('/api/4.0/edges'+ '?&startindex=0&pagesize=100')
    existingEsgResponseDoc = xmltodict.parse(existingEsgResponse.text)

    matched_nsx_esgs = 0
    num_nsx_esgs = len(edge_service_gateways)
    
    if DEBUG:
        print('ESG response :\n{}\n'.format(existingEsgResponse.text)) 

    edgeSummaries = existingEsgResponseDoc['pagedEdgeList']['edgePage'].get('edgeSummary')
    if not edgeSummaries:
        print('No NSX Edge instances found')
        return matched_nsx_esgs

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
            print('NSX ESG instance with name: {} does not exist anymore\n'.format(interested_Esg['name']))

    if DEBUG:
        print('Updated NSX ESG:{}'.format(edge_service_gateways))
    return matched_nsx_esgs   

def list_nsx_edge_gateways(context):
    existingEsgResponse = client.get(NSX_URLS['esg']['all'] )
    existingEsgResponseDoc = xmltodict.parse(existingEsgResponse.text)

    if DEBUG:
        print('NSX ESG response :{}\n'.format(existingEsgResponse.text))

    edgeSummaries = existingEsgResponseDoc['pagedEdgeList']['edgePage'].get('edgeSummary')
    if not edgeSummaries:
        print('No NSX Edge instances found')
        return

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
            print('NSX ESG Deletion response:{}\n'.format(data))

        if delete_response.status_code < 400: 
            print('Deleted NSX ESG : {}\n'.format(nsx_esg['name']))
        else:
            print('Deletion of NSX ESG failed, details:{}\n'.format(data +'\n'))    

def check_cert_config(nsx_context):

    if not nsx_edge.get('certs'):
        print('No cert config was specified for edge instance: {}'.\
                    format( nsx_edge['name']))
        raise Exception('Creation of NSX Edge failed, no cert config was provided') 

    if not nsx_edge['certs'].get('config'):
        print('No cert config was specified for edge instance: {}'.\
                    format( nsx_edge['name']))
        raise Exception('Creation of NSX Edge failed, neither cert_id nor config to generate certs was provided')   

def generate_certs(cert_section):
    output_dir = './' + cert_section['name']    
    cert_config = cert_section.get('config')

    org_unit = cert_config.get('org_unit', 'Pivotal')
    country = cert_config.get('country_code', 'US')

    subprocess.call(
                    [ 
                        './certGen.sh', 
                        cert_config['domains'], 
                        output_dir, 
                        org_unit, 
                        country 
                    ]
                )

    cert_section['key'] = readFileContent(output_dir + '/*.key')
    cert_section['cert'] = readFileContent(output_dir + '/*.crt')
    cert_section['description'] = 'Cert for ' + cert_section['name']

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
    gateway_address  = '{}.{}.{}.1'.format( uplinkIpTokens[0], 
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
            
            # Skip OSPF related communication
            if ( 'OSPF' in pair[0]['given_name'].upper() 
               or 'OSPF' in pair[1]['given_name'].upper() ):
               continue

            # Ensure IsoZones don't talk to each other
            if not ('ISOZONE' in pair[0]['given_name'].upper() 
                and 'ISOZONE' in pair[1]['given_name'].upper()): 
                edited_result.append(pair)

    return edited_result
