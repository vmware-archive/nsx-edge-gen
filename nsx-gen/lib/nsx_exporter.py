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
import sys
import yaml
import re
import client
import copy
import glob
import xmltodict
import dicttoxml

from collections import OrderedDict
from yaml.dumper import Dumper
from yaml.representer import SafeRepresenter

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring as et_tostring

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

sys.path.append(os.path.join(LIB_PATH, os.path.join('../..')))

from nsx_builder import *
from util import *
from nsx_urls import *

DEBUG = False

def refresh_nsx_ip_set_map(context):
    if 'nsx_ip_set_map' not in context:

        get_all_ipsets_response = client.get(NSX_URLS['ipsets']['all'])
        data = get_all_ipsets_response.text
        existingIpSetDict = xmltodict.parse(data)
        
        nsx_ip_set_map = {}
        for entry in existingIpSetDict['list']['ipset']:
            nsx_ip_set_map[entry['objectId']] = entry

        context['nsx_ip_set_map'] = nsx_ip_set_map
        return nsx_ip_set_map
    else:
        return context['nsx_ip_set_map']

def refresh_nsx_app_id_map(context):
    if 'nsx_app_id_map' not in context:

        get_all_ipsets_response = client.get(NSX_URLS['applicationsets']['all'])
        data = get_all_ipsets_response.text
        existingIpSetDict = xmltodict.parse(data)
        
        nsx_app_id_map = {}
        for entry in existingIpSetDict['list']['application']:
            nsx_app_id_map[entry['objectId']] = entry

        context['nsx_app_id_map'] = nsx_app_id_map
        return nsx_app_id_map
    else:
        return context['nsx_app_id_map']

def export_firewall_rules(context):
    client.set_context(context, 'nsxmanager')
    export_nsx_edge_gateway_firewall_rules(context)  

def export_nsx_edge_gateway_firewall_rules(context):

    #edge_service_gateways = context['edge_service_gateways']
    edge_service_gateways = []
    export_context = context.get('export')
    if not export_context:
        raise Exception('Export of NSX Edges failed, no values passed for nsxedge_names')   

    for edge_name in export_context['nsxedge_names'].split(','):
        edge_service_gateways.append({ 'name' : edge_name })

    export_dir = export_context['export_directory']
    mkdir_p(export_dir)

    print 'Full export section: {}, Export dir: {}'.format(export_context, export_dir)

    map_nsx_esg_id( edge_service_gateways )

    nsx_ip_set_map = refresh_nsx_ip_set_map(context)
    nsx_app_id_map = refresh_nsx_app_id_map(context)
    
    for nsx_esg in edge_service_gateways:

        if  nsx_esg.get('id') is None:
            continue

        nsx_url_get_response = client.get(NSX_URLS['esg']['all'] + '/' +
                nsx_esg['id'])
        data = nsx_url_get_response.text
        if DEBUG:
            print('NSX ESG Get response:{}\n'.format(data))

        if nsx_url_get_response.status_code < 400: 
            print '\nNSX Edge \'{}\' (id: {}) exported!!\n'.format(nsx_esg['name'], nsx_esg['id'])
            nsx_response_xml_tree = ET.ElementTree(ET.fromstring(data))

            transform_ip_set(nsx_response_xml_tree, nsx_ip_set_map)
            transform_application_set(nsx_response_xml_tree, nsx_app_id_map)
            
            nsx_edge_xml_output = '{}/{}.xml'.format(export_dir, nsx_esg['name'])            
            nsx_response_xml_tree.write(nsx_edge_xml_output)
            print 'Saved NSX Edge \'{}\' full payload (xml) : {}'\
                    .format(nsx_esg['name'], nsx_edge_xml_output)


            nsx_edge_firewall_rules_xml = nsx_response_xml_tree.findall('.//firewallRules')[0]
            nsx_edge_firewall_rules_xml_output = '{}/{}-firewall-rules.xml'.format(export_dir, nsx_esg['name'])            
            ET.ElementTree(nsx_edge_firewall_rules_xml).write(nsx_edge_firewall_rules_xml_output)
            print 'Saved NSX Edge \'{}\' firewall rules (xml) : {}'\
                    .format(nsx_esg['name'], nsx_edge_firewall_rules_xml_output)

            existingEsgResponseDoc = xmltodict.parse(et_tostring(nsx_response_xml_tree.getroot(), encoding='utf8', method='xml'))

            firewall_dict = existingEsgResponseDoc['edge']['features']['firewall']['firewallRules']

            #fix_ip_sets(context, firewall_dict)

            firewall_rules_xml =  dicttoxml.dicttoxml(
                                    firewall_dict,
                                    custom_root='firewallRules')

            if DEBUG:
                print('Retrieved NSX ESG instance \'{}\' firewall rules as XML:\n{}\n'.format(nsx_esg['name'], 
                                                        firewall_rules_xml))

            yaml.SafeDumper.add_representer(OrderedDict,
                    lambda dumper, value: represent_odict(dumper, u'tag:yaml.org,2002:map', value))
            yaml_content = yaml.safe_dump(firewall_dict, allow_unicode = True, encoding = None, default_flow_style=False) 

            if DEBUG:
                print('Retrieved NSX ESG instance \'{}\' firewall rules as YAML:\n{}\n'\
                        .format(nsx_esg['name'], yaml_content))

            nsx_edge_yml_output = '{}/{}-firewall-rules.yml'.format(export_dir, nsx_esg['name'])
            with open(nsx_edge_yml_output, 'w') as outfile:
                outfile.write(yaml_content)

            print 'Saved NSX Edge \'{}\' firewall rules (yml) : {}'\
                    .format(nsx_esg['name'], nsx_edge_yml_output)
            
        else:
            print('Retrieval of NSX ESG failed, details:{}\n'.format(data +'\n'))    

    print ''


"""
Change from
    <source>
        <exclude>false</exclude>
        <ipAddress>192.168.10.0/26</ipAddress>
        <groupingObjectId>ipset-7</groupingObjectId>
        <groupingObjectId>ipset-8</groupingObjectId>
    </source>
Change to:
    <source>
        <exclude>false</exclude>
        <ipAddress>192.168.10.0/26</ipAddress>
        <ipAddress>192.168.10.0-192.168.10.100</ipAddress>
        <ipAddress>192.168.20.100/26</ipAddress>
    </source>
"""
def transform_ip_set(nsx_response_xml_tree, nsx_ip_set_map):
    #for entry in tree.xpath("//td/a[contains(text(),'datacenter')]/.."):
    for parent_node in nsx_response_xml_tree.findall('.//groupingObjectId/..'):
        for entry in parent_node.findall('./groupingObjectId'):
            value = entry.text
            if 'ipset' in value:
                ipset_id = value 
                ipAddress = ET.SubElement(parent_node, 'ipAddress')
                ipAddress.text = nsx_ip_set_map[ipset_id]['value']
                parent_node.remove(entry)

    return nsx_response_xml_tree

"""
Change from
    <application>
        <applicationId>application-352</applicationId>
        <applicationId>application-370</applicationId>
    </application>
Change to:
    <application>
        <service>
            <protocol>tcp</protocol>
            <port>80</port>
            <port>443</port>
            <port>4443</port>
            <sourcePort>any</sourcePort>
        </service>
    </application>
"""
def transform_application_set(nsx_response_xml_tree, nsx_app_id_map):
    #for entry in tree.xpath("//td/a[contains(text(),'datacenter')]/.."):
    for parent_node in nsx_response_xml_tree.findall('.//application'):
        for entry in parent_node.findall('./applicationId'):
            value = entry.text
            if 'application-' in value:
                app_id = value 
                service = ET.SubElement(parent_node, 'service')
                service_port = ET.SubElement(service, 'port')
                service_port.text = nsx_app_id_map[app_id]['element']['value']
                service_protocol = ET.SubElement(service, 'protocol')
                service_protocol.text = nsx_app_id_map[app_id]['element']['applicationProtocol']
                
                parent_node.remove(entry)

    return nsx_response_xml_tree

def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

def represent_odict(dump, tag, mapping, flow_style=None):
    """Like BaseRepresenter.represent_mapping, but does not issue the sort().
    """
    value = []
    node = yaml.MappingNode(tag, value, flow_style=flow_style)
    if dump.alias_key is not None:
        dump.represented_objects[dump.alias_key] = node
    best_style = True
    if hasattr(mapping, 'items'):
        mapping = mapping.items()
    for item_key, item_value in mapping:
        node_key = dump.represent_data(item_key)
        node_value = dump.represent_data(item_value)
        if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
            best_style = False
        if not (isinstance(node_value, yaml.ScalarNode) and not node_value.style):
            best_style = False
        value.append((node_key, node_value))
    if flow_style is None:
        if dump.default_flow_style is not None:
            node.flow_style = dump.default_flow_style
        else:
            node.flow_style = best_style
    return node

"""
def fix_ip_sets(context, firewall_dict):
    nsx_ip_set_map = refresh_nsx_ip_set_map(context)

    for firewall_rule in firewall_dict['firewallRule']:
        if DEBUG:
            print 'Original Firewall entry: {}'.format(firewall_rule)

        src = firewall_rule.get('source')
        if src:
            firewall_rule['source'] = translate_ip_set(src, nsx_ip_set_map)

        dest = firewall_rule.get('destination')
        if dest:
            firewall_rule['destination'] = translate_ip_set(dest, nsx_ip_set_map)

        if DEBUG:
            print 'Updated Firewall Rule: {}'.format(firewall_rule)

def translate_ip_set(target_set, nsx_ip_set_map):
    new_target_set = {}

    # if isinstance(target_set, __builtin__.dict):
    #   print 'Target is dict'
    # elif isinstance(target_set, __builtin__.list):
    #   print 'Target is list'  
    
    for key, value in target_set.iteritems():
    
        if key == 'groupingObjectId':
            values = value
            if not isinstance(value, __builtin__.list):
                values = [ value ]

            translated_ips = [ ]
            for ipval in values:                
                ipset = nsx_ip_set_map[ipval]
                translated_ips.append(ipset['value'])
            
            new_target_set['ipAddress'] = translated_ips    
        else:
            new_target_set[key] = value 

    #print 'Updated target set: {}'.format(new_target_set)
    return new_target_set   
"""   