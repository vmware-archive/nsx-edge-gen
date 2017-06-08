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

NSX_URLS = {
	'scope': 			 { 'all': '/api/2.0/vdn/scopes' },
	'lswitch':           { 'all': '/api/2.0/vdn/virtualwires' },
	'esg':               { 'all': '/api/4.0/edges' },
	'lbrConfig':         { 'all': '/loadbalancer/config' },
	'appProfile':        { 'all': '/loadbalancer/config/applicationprofiles' },
	'virtservers':       { 'all': '/loadbalancer/config/virtualservers'},
	'lbrPool':           { 'all': '/loadbalancer/config/pools'},
	'cert':              { 'all': '/api/2.0/services/truststore/certificate'},
	'ipsets':            { 'all': '/api/2.0/services/ipset/scope/globalroot-0'},
	'applicationsets':   { 'all': '/api/2.0/services/application/scope/globalroot-0'},
}