#!/usr/bin/env python
# coding=utf-8
#
# Copyright © 2015-2016 VMware, Inc. All Rights Reserved.
#
# Licensed under the X11 (MIT) (the “License”) set forth below;
#
# you may not use this file except in compliance with the License. Unless required by applicable law or agreed to in
# writing, software distributed under the License is distributed on an “AS IS” BASIS, without warranties or conditions
# of any kind, EITHER EXPRESS OR IMPLIED. See the License for the specific language governing permissions and
# limitations under the License. Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# "THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.”

__author__ = 'Sabha Parameswaran'

import argparse
import ConfigParser
import os.path
import string
import sys
import yaml
from tabulate import tabulate
from argparse import RawTextHelpFormatter
from pkg_resources import resource_filename

CONFIG_FILE = "nsx_cloud_config.yml"
LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))

import config
from config import Config

ROUTED_COMPONENTS = [ 'opsmgr', 'go_router', 'diego_brain', 'tcp_router']

ATTRIBUTE_MAP_ARRAY = {
    'vcenter' : [ 
        [ 'addr', 'address'],
        [ 'user', 'admin_user'],
        [ 'pass', 'admin_passwd'],
        [ 'dc', 'datacenter'],
        [ 'ds', 'datastore'],
        [ 'c', 'cluster'],
        [ 'fd', 'folder'],
        [ 'h', 'host'],
    ],

    'defaults': [
        [ 'ntp', 'ntp_ips'],
        [ 'dns', 'dns_ips'],
        [ 'log', 'syslog_ips'],
        [ 'ldap', 'ldap_ips'],
    ],

    'nsxmanager': [
        [ 'addr', 'address'],
        [ 'user', 'admin_user'],
        [ 'pass', 'admin_passwd'],
        [ 'tz', 'transportzone'],
        [ 'uplink_ip', 'uplink_ip'],
        [ 'uplink_port', 'uplink_port_switch'],
    ],

    'esg': [
        [ 'name', 'name'],
        [ 'size', 'size'],
        [ 'cli_user', 'cli_username'],
        [ 'cli_pass', 'cli_password'],
        [ 'certs', 'certs_name'],
        [ 'certs_config_ou', 'certs_config_orgunit'],
        [ 'certs_config_cc', 'certs_config_country'],
        [ 'certs_config_sysd', 'certs_config_systemdomain'],
        [ 'certs_config_appd', 'certs_config_appdomain'],
    ],

    'routed_components':  [
        [ 'uplink_ip', 'uplink_ip'],
        [ 'inst', 'instances'],
        [ 'off', 'offset'],
    ],
}


def contruct_parser(parser):

    parser.add_argument("command", help="""
    build: build a new Edge Service Gateway
    delete: delete a Edge Service Gateway"
    list:   return a list of all Edge Service Gateways
    """)

    parser.add_argument("-c",
                        "--nsx-conf",
                        help="nsx configuration yml file",
                        default="nsx_cloud_config.yml")
    
    """

    fieldArr = [
        [ 'addr', 'addr'],
        [ 'user', 'username'],
        [ 'pass', 'password'],
        [ 'dc', 'datacenter'],
        [ 'ds', 'datastore'],
        [ 'c', 'cluster'],
        [ 'fd', 'folder'],
        [ 'h', 'host'],
    ]

    for field in fieldArr:
        prefix = 'vcenter'
        parser.add_argument('-{}-{}'.format(prefix, field[0]), 
                        '--{}-{}'.format(prefix, field[1]),
                        help="{} {}".format(prefix, field[1].replace('-', ' '))
                    )

    fieldArr = [
        [ 'ntp', 'ntp-ips'],
        [ 'dns', 'dns-ips'],
        [ 'log', 'syslog-ips'],
        [ 'ldap', 'ldap-ips'],
    ]

    for field in fieldArr:
        prefix = ''
        parser.add_argument('-{}-{}'.format(prefix, field[0]), 
                        '--{}-{}'.format(prefix, field[1]),
                        help="{} {}".format(prefix, field[1].replace('-', ' '))
                    )

    fieldArr = [
        [ 'addr', 'manager-addr'],
        [ 'user', 'manager-username'],
        [ 'pass', 'manager-password'],
        [ 'tz', 'transportzone'],
        [ 'uplink-ip', 'uplink-ip'],
        [ 'uplink-port', 'uplink-port-switch'],
    ]

    for field in fieldArr:
        prefix = 'nsx'
        parser.add_argument('-{}-{}'.format(prefix, field[0]), 
                        '--{}-{}'.format(prefix, field[1]),
                        help="{} {}".format(prefix, field[1].replace('-', ' '))
                    )
    
    for index in xrange(1, 3):
        prefix = 'esg'
        parser.add_argument('-{}-{}'.format(prefix, index), 
                                '--{}-{}-{}'.format(prefix, 'name', index),
                                help="{} {} name".format(prefix, index)
                            )

        fieldArr = [
            [ 'size', 'size'],
            [ 'cli-user', 'cli-username'],
            [ 'cli-pass', 'cli-password'],
            [ 'cert', 'cert-name'],
            [ 'cert-config-ou', 'cert-config-orgunit'],
            [ 'cert-config-cc', 'cert-config-country'],
            [ 'cert-config-sysd', 'cert-config-systemdomain'],
            [ 'cert-config-appd', 'cert-config-appdomain'],
        ]

        for field in fieldArr:
            parser.add_argument('-{}-{}-{}'.format(prefix, field[0], index), 
                                '--{}-{}-{}'.format(prefix, field[1], index),
                                help="{} instance {} {}".format(prefix, index, field[1].replace('-', ' '))
                                )

        for component in [ 'opsmgr', 'go-router', 'diego-brain', 'tcp-router']:

            fieldArr = [
                [ 'uplink-ip', 'uplink-ip'],
                [ 'inst', 'instances'],
                [ 'off', 'offset'],
            ]

            for field in fieldArr:
                parser.add_argument('-{}-{}-{}-{}'.format(prefix, component, field[0], index), 
                                    '--{}-{}-{}-{}'.format(prefix, component, field[1], index),
                                    help="{} instance {} routed {} {}".format(prefix, index, component, field[1].replace('-', ' '))
                                    )

        """

    for section in ATTRIBUTE_MAP_ARRAY:
        print 'Section: ' + section 
        
        prefix = section
        if section == 'defaults':
            prefix = ''

        if section not in ['esg', 'routed_components']:  
            for field in ATTRIBUTE_MAP_ARRAY[section]:
                parser.add_argument('-{}_{}'.format(prefix, field[0]), 
                                '--{}_{}'.format(prefix, field[1]),
                                help="{} {}".format(prefix, field[1].replace('_', ' '))
                            )

        
        if section == 'esg': 
            for index in xrange(1, 3): 
                
                for field in ATTRIBUTE_MAP_ARRAY[section]:
                    parser.add_argument('-{}_{}_{}'.format(prefix, field[0], index), 
                                '--{}_{}_{}'.format(prefix, field[1], index),
                                help="{} instance {} {}".format(section, index, field[1].replace('_', ' '))
                                )

                for component in ROUTED_COMPONENTS:
                    for compField in ATTRIBUTE_MAP_ARRAY['routed_components']:            
                        parser.add_argument('-{}_{}_{}_{}'.format(prefix, component, compField[0], index), 
                                '--{}_{}_{}_{}'.format(prefix, component, compField[1], index),
                                help="{} instance {} routed {} {}".format(prefix, index, component, compField[1].replace('_', ' '))
                                )

    parser.set_defaults(func=_nsx_gen_main)
    

def construct_config(args):
    argDict = vars(args)
    global_config = {}

    for section in ATTRIBUTE_MAP_ARRAY:
        prefix = section
        global_config[section] = { }
        if section == 'defaults':
            prefix = ''

        if section not in ['esg', 'routed_components']:
            for field in ATTRIBUTE_MAP_ARRAY[section]:
                key = '{}_{}'.format(prefix, field[1])
                val =  argDict[key]
                if val:
                    global_config[section][field[1]] = val
                    
        elif section == 'esg': 
            prefix = section
            global_config['edge_service_gateways'] = [ ]

            for index in xrange(1, 4): 
                esgEntry = {  }

                key = '{}_{}_{}'.format(prefix, 'name', index)
                
                name =  argDict[key]
                if name:
                    esgEntry['name'] = name
                else:
                    break

                for field in ATTRIBUTE_MAP_ARRAY[section]:
                    key = '{}_{}_{}'.format(prefix, field[1], index)
                    val =  argDict[key]
                    if val:
                        if 'certs_config' in key:
                            field[1] =  field[1].replace('certs_config_', '')
                            if not esgEntry['certs'].get('config'):
                                esgEntry['certs']['config'] = { }
                            esgEntry['certs']['config']= { field[1] : val }

                        elif 'certs' in key:
                            field[1] =  field[1].replace('certs_', '')
                            esgEntry['certs'] = { field[1] : val }

                        else:
                            esgEntry[field[1]] = val 
                                
                for component in ROUTED_COMPONENTS:
                    componentName = component.replace('_', '-')
                    esgEntry[componentName] = { }
                    for compField in ATTRIBUTE_MAP_ARRAY['routed_components']:                        

                        key = '{}_{}_{}_{}'.format(prefix, component, compField[1], index)
                        val =  argDict[key]
                        if val:

                            if 'uplink_ip' in key:
                                compField[1] = compField[1].replace('uplink_details_', '')
                                if not esgEntry[componentName].get('uplink_details'):
                                    esgEntry[componentName]['uplink_details'] = { }
                                esgEntry[componentName]['uplink_details']= { compField[1] : val }
                                
                            else:
                                esgEntry[componentName][compField[1]] = val 
                
                global_config['edge_service_gateways'].append(esgEntry) 
        
    print 'Final Config... : ' + str(global_config)

def _nsx_gen_main(args):
    print 'args : ' + str(args)
    config = Config().read(args.nsx_conf)
    assert config, 'could not read config file {}'.format(args.nsx_conf)

    """
    if args.transport_zone:
        transport_zone = args.transport_zone
    else:
        transport_zone = config.get('defaults', 'transport_zone')
    """
    try:
        command_selector = {
            'list': _logical_switch_list_print,
            'create': _logical_switch_create,
            'delete': _logical_switch_delete,
            'read': _logical_switch_read,
            'construct': construct_config,
            }
        command_selector[args.command](args)
    except KeyError:
        print('Unknown command')


def main():
    main_parser = argparse.ArgumentParser()
    contruct_parser(main_parser)
    args = main_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
