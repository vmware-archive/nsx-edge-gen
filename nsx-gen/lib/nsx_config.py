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

import copy
import os.path
import string
import sys
import yaml
import re
import ipcalc
from print_util  import *

from routed_components_handler  import *
#from routed_component  import *

CONFIG_FILE = "nsx_cloud_config.yml"
LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

class NSXConfig(dict):

    def __init__(self, *arg, **kw):
        super(NSXConfig, self).__init__(*arg, **kw)

    """
    def __setitem__(self, field, val):
        if field == 'defaults':
            self.defaults = val
        elif field == 'vcenter':
            self.vcenter = val
        elif field == 'nsxmanager':
            self.nsxmanager = val
        elif field == 'edge_service_gateways':
            self.nsx_edges = val
        elif field == 'logical_switches':
            self.logical_switches = val
        else:
            print('Unknown field..' + field)
    """

    def validate(self):
        self.name = self.get('name', 'nsx-pcf')
        if len(self.name) > 15:
            raise ValueError('Name of config "'+ self.name + '" over 15 characters!!\n\
            Change name of config to avoid trim/overlap in generated virtualwire names!')

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
                    'uplink_details']
        for field in fields:
            if self.nsxmanager[field] is None:
                raise ValueError(field + ' field not set for nsxmanager')
        
        self.nsxmanager['url'] = 'https://' + self.nsxmanager['address']

        enable_dlr = self.nsxmanager['enable_dlr']
        if not enable_dlr or enable_dlr == 'false':
            self.nsxmanager['enable_dlr'] = False
            print('DLR disabled, won\'t create OSPF Logical switch or DLR!!')
        else:
            self.nsxmanager['enable_dlr'] = True
            print('DLR enabled, will create OSPF Logical switch and DLR!!')
            # If DLR is enabled, then it needs distributed portgroup defined
            distributed_portgroup = self.nsxmanager['distributed_portgroup']
            if not distributed_portgroup:
                raise ValueError('distributed_portgroup field not set for nsxmanager')
    
        for tag in ['bosh_nsx_enabled', 'http_lbr_enabled' ]:
            tagValue = self.nsxmanager.get(tag)
            if not tagValue or tagValue == 'false':
                self.nsxmanager[tag] = False
            else:
                self.nsxmanager[tag] = True

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
        
        enable_dlr = self.get('nsxmanager')['enable_dlr']
        
        fields = [ 'name',  'cidr'] #, 'primary_ip', 'secondary_ips']
        given_logical_switches = copy.deepcopy(self.logical_switches)
        #self.logical_switches = [ ]
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
            lswitch['name'] = 'lsw-'+self.get('name') + '-' + lswitch['name']
            lswitch['subnet_mask'] = addr_range.netmask()
            lswitch['gateway'] = addr_range[0]
            lswitch['primary_ip'] = addr_range[1]
            lswitch['subnet_length'] = string.atoi(lswitch['cidr'].split('/')[1])
            lswitch['name'] = lswitch['name'].replace(' ', '-')
            
            # This will be filled in later once we have parsed the routed components
            lswitch['secondary_ips'] = []       
            #print('Logical Switch Entry:', lswitch)
            
            # Skip OSPF Switch if DLR not enabled
            #if not (lswitch['given_name'] == 'OSPF' and not enable_dlr):
            #   filtered_logical_switches.append(lswitch)               
        
        #self.logical_switches = filtered_logical_switches  
        print_logical_switches_configured(self.logical_switches)
        
    def validate_nsx_edges(self):
        self.nsx_edges = self.get('edge_service_gateways')
        if self.nsx_edges is None:
            raise ValueError('edge_service_gateways section not defined')
        
        self.nsxmanager = self.get('nsxmanager')
        enable_dlr = self.nsxmanager['enable_dlr']

        global_switches =  { }
        for lswitch in self.logical_switches:
            if not enable_dlr and 'OSPF' in lswitch['name']:
                continue

            if lswitch.get('given_name'):
                given_name = lswitch['given_name'].upper()
            else:
                given_name = lswitch['name'].upper()
            global_switches[given_name] = lswitch

        fields = [ 'name', 'size', 'cli', 'routed_components', 'gateway_ip', 'ospf_password']
        for nsx_edge in self.nsx_edges:

            for field in fields:
                if nsx_edge[field] is None:
                    raise ValueError(field + ' field not set for nsx_edge')
        
            size = nsx_edge['size']
            if not size or size not in [ 'xlarge', 'quadlarge', 'large', 'compact' ]:
                nsx_edge['size'] = 'large'

            # If DLR is enabled, then it needs ospf password defined
            nsx_edge['enable_dlr'] = enable_dlr
            if enable_dlr:
                ospf_password = nsx_edge['ospf_password']
                if not ospf_password:
                    raise ValueError('ospf_password field not set for nsx_edge')
                elif len(ospf_password) > 7:
                    raise ValueError('ospf_password field length more than 7 characters for nsx_edge')

            nsx_edge['global_switches'] =  global_switches
            nsx_edge['global_uplink_details'] = self.nsxmanager['uplink_details']


            nsx_edge['monitor_list'] = get_default_monitors()
            nsx_edge['app_rules'] = get_default_app_rules()
            if DEBUG:
                print 'App Rules: {}'.format(nsx_edge['app_rules']) 
                print 'Monitor List: {}'.format(nsx_edge['monitor_list'])   
        
            default_app_profiles = get_default_app_profiles()
            app_profiles = copy.copy(default_app_profiles)
            
            index = 1
            for builtin_app_profile in default_app_profiles:
                
                # Create new app profiles only for those that require ssl/cert handling
                if builtin_app_profile['requires_cert'] != 'true':
                    continue

                index = 1
                for lswitch in self.logical_switches:

                    lswitch_name_upper = lswitch['given_name'].upper()
                    # Skip non-ert and non-isozone switches from any associated app profiles
                    if not ('ISOZONE' in lswitch_name_upper):# or 'ERT' in lswitch_name_upper):
                        continue

                    new_app_profile = copy.copy(builtin_app_profile)
                    new_app_profile['id'] = builtin_app_profile['id'] + str(index)
                    new_app_profile['switch'] = lswitch['given_name']
                    new_app_profile['name'] = builtin_app_profile['name'] + '-' + lswitch['given_name']
                    app_profiles.append(new_app_profile)
                    index += 1
                
            nsx_edge['app_profiles'] = app_profiles
            if DEBUG:
                print 'All App Profiles: {}'.format(app_profiles)
            
            routed_component_context = nsx_edge['routed_components']

            nsx_edge['routed_components'] = [ ]
            for entry in routed_component_context:
                routedComponent = parse_routing_component(entry, self.logical_switches, 
                                                        app_profiles, enable_dlr)
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
    
