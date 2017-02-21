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
import errno
import shutil
import sys
import yaml
import re
import template
import ipcalc
import client
import xmltodict
from util import *

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

sys.path.append(os.path.join(LIB_PATH, os.path.join('../..')))

import argparse
from pprint import pprint
import pynsxv.library.nsx_logical_switch as lswitch
import pynsxv.library.nsx_dlr as dlr
import pynsxv.library.nsx_esg as esg
import pynsxv.library.nsx_dhcp as dhcp
import pynsxv.library.nsx_lb as lb
import pynsxv.library.nsx_dfw as dfw
import pynsxv.library.nsx_usage as usage

#from pynsxv.library.nsx_logical_switch import logical_switch_list,logical_switch_create
#from nsxramlclient.client import NsxClient

DEBUG = False
def build(context, verbose=False):
    #setup_parsers()
    client.set_context(context)

    # response = client.get('/api/2.0/vdn/virtualwires') 
    # print('Response code:', response.status_code)
    # #pprint (vars(response))
    # if response.status_code == 200 :
    #     data = response.text
    #     print(data)
    # else:
    #     data = response.content
    #     print('Error, code:' + response.status_code + ', msg:' + data)
        
    #build_logical_switches('lswitch', context)
    build_nsx_edge_lbrs('edge', context)

def setup_parsers():
    parser = argparse.ArgumentParser(description='PyNSXv Command Line Client for NSX for vSphere')
    parser.add_argument("-i",
                        "--ini",
                        help="nsx configuration file",
                        default="nsx.ini")
    parser.add_argument("-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-d",
                        "--debug",
                        help="print low level debug of http transactions",
                        action="store_true")

    subparsers = parser.add_subparsers()
    lswitch.contruct_parser(subparsers)
    dlr.contruct_parser(subparsers)
    esg.contruct_parser(subparsers)
    dhcp.contruct_parser(subparsers)
    lb.contruct_parser(subparsers)
    dfw.contruct_parser(subparsers)
    usage.contruct_parser(subparsers)
    print 'Finished setting up parsers'

def map_logical_switches_id(logical_switches):
    existinglSwitchesResponse = client.get('/api/2.0/vdn/virtualwires')
    existinglSwitchesResponseDoc = xmltodict.parse(existinglSwitchesResponse.text)

    num_lswitches = len(logical_switches)
    matched_lswitches = 0

    for existingLSwitch in existinglSwitchesResponseDoc['virtualWires']['dataPage']['virtualWire']:
        if (num_lswitches == matched_lswitches):
            break

        for interested_lswitch in  logical_switches: 
            if existingLSwitch['name'] == interested_lswitch['name']:
                interested_lswitch['id'] = existingLSwitch['objectId']
                ++matched_lswitches
                break
        


def build_logical_switches(dir, context, alternate_template=None):
    logical_switches_dir = os.path.realpath(os.path.join(dir ))
    
    if os.path.isdir(logical_switches_dir):
        shutil.rmtree(logical_switches_dir)
    mkdir_p(logical_switches_dir)

    template_dir = '.'
    if alternate_template is not None:
        template_dir = os.path.join(template_dir, alternate_template)

    vdnScopesResponse = client.get('/api/2.0/vdn/scopes')
    vdnScopesDoc = xmltodict.parse(vdnScopesResponse.text)
    #print('%v', vdnScopesDoc)
    defaultVdnScopeId = vdnScopesDoc['vdnScopes']['vdnScope']['objectId']

    for lswitch in  context['logical_switches']:  
        logical_switches_context = {
            'context': context,
            'logical_switch': lswitch,
            #'managed_service_release_jobs': context['managed_service_release_jobs'],
            'files': []
        }    

        template.render(
            os.path.join(logical_switches_dir, 'lswitch' + lswitch['name'] + '_payload.xml'),
            os.path.join(template_dir, 'logical_switch_config_post_payload.xml' ),
            logical_switches_context
        )

        # Get the vdn scopes
        #  https://10.193.99.20//api/2.0/vdn/scopes
        # After determining the vdn scope, then post to that scope endpoint

        # POST /api/2.0/vdn/scopes/vdnscope-1/virtualwires
        post_response = client.post_xml('/api/2.0/vdn/scopes/'+defaultVdnScopeId+'/virtualwires', 
                os.path.join(logical_switches_dir, 'lswitch' + lswitch['name'] + '_payload.xml'))
        data = post_response.text
        print('Created Logical Switch : ' +  lswitch['name'] +'\n')
        if DEBUG:
            print 'Logical switch creation response:\n' + data

def build_nsx_edge_lbrs(dir, context, alternate_template=None):
    nsx_edges_dir = os.path.realpath(os.path.join(dir ))
    
    if os.path.isdir(nsx_edges_dir):
        shutil.rmtree(nsx_edges_dir)
    mkdir_p(nsx_edges_dir)

    template_dir = '.'
    if alternate_template is not None:
        template_dir = os.path.join(template_dir, alternate_template)

    logical_switches = context['logical_switches']
    map_logical_switches_id(logical_switches)
    print 'Logical Switches:\n' + str(logical_switches) + '\n'

    #empty_logical_switches = xrange(1 + len(logical_switches), 10)  
    empty_logical_switches = xrange(len(logical_switches), 10)  
    for nsx_edge in  context['edge_service_gateways']:
        nsx_edge['datacenter_id'] = context['nsx_defaults']['datacenter']  
        nsx_edge['resourcePoolId'] = context['nsx_defaults']['resourcePool']  
        nsx_edge['datastoreId'] = context['nsx_defaults']['datastore'] 
        nsx_edge['clusterId'] = context['nsx_defaults']['cluster']   
        nsx_edge['hostId'] = context['nsx_defaults']['host']  
        nsx_edge['vmFolderId'] = context['nsx_defaults']['vmFolder']  
        print('Nsx Edge config: ' + str(nsx_edge) + '\n')
        nsx_edges_context = {
            'context': context,
            'edge': nsx_edge,
            'logical_switches': logical_switches,
            'empty_logical_switches': empty_logical_switches,
            'uplink': context['uplink'],
            'files': []
        }    

        template.render(
            os.path.join(nsx_edges_dir, nsx_edge['name'] + '_post_payload.xml'),
            os.path.join(template_dir, 'edge_config_post_payload.xml' ),
            nsx_edges_context
        )

        post_response = client.post_xml('/api/4.0/edges', 
                os.path.join(nsx_edges_dir, nsx_edge['name'] + '_post_payload.xml'))
        data = post_response.text
        if DEBUG:
            print 'NSX Edge creation response:\n' + data

        if post_response.status_code < 400: 
            print('Created NSX Edge : ' +  nsx_edge['name'] +'\n')
        else:
            print('Creation of NSX Edge failed, details:\n' +  data +'\n')    

