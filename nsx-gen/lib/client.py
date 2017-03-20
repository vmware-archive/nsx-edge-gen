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


from __future__ import absolute_import, division, print_function

__author__ = 'Sabha Parameswaran'

import sys
import yaml
import json
import requests
import time
from requests.auth import HTTPDigestAuth
from pprint import pprint

try:
	# Python 3
	from urllib.parse import urlparse
except ImportError:
	# Python 2
	from urlparse import urlparse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class auth(requests.auth.AuthBase):

	def __init__(self, context, resourceType='nsxmanager'):
		self.context = context
		self.resourceType = resourceType

	def __call__(self, request):
		username = self.context.get(self.resourceType).get('admin_user')
		password = self.context.get(self.resourceType).get('admin_passwd')
		return requests.auth.HTTPBasicAuth(username, password)(request)	

def get_context():
	if get_context.context is not None:
		return get_context.context
	else:
		raise Error(resourceType + ' config not loaded!!')

get_context.context = None

def set_context(context, resourceType):
	get_context.context = context
	get_context.context['resourceType'] = resourceType


def get(url, stream=False, check=True):
	context = get_context()
	resourceType = context['resourceType']
	url = context.get(resourceType).get('url') + url
	headers = { 'Accept': 'text/html,application/xhtml+xml,application/xml' }
	
	response = requests.get(url, auth=auth(context), verify=False, headers=headers, stream=stream)
	check_response(response, check=check)
	return response

def put(url, payload, check=True):
	context = get_context()
	resourceType = context['resourceType']
	url = context.get(resourceType).get('url') + url
	response = requests.put(url, auth=auth(context), verify=False, data=payload)
	check_response(response, check=check)
	return response

def put_json(url, payload):
	context = get_context()
	resourceType = context['resourceType']
	url = context.get(resourceType).get('url') + url
	response = requests.put(url, auth=auth(context), verify=False, json=payload)
	check_response(response, check=check)
	return response

def put_xml(url, filename, check=True):
	context = get_context()
	resourceType = context['resourceType']
	url = context.get(resourceType).get('url') + url
	payload = open(filename).read()
	headers = {'Content-Type': 'application/xml'}
	response = requests.put(url, auth=auth(context), verify=False, data=payload, headers=headers)
	check_response(response, check=check)
	return response	

def post(url, payload, check=True):
	context = get_context()
	resourceType = context['resourceType']
	url = context.get(resourceType).get('url') + url
	response = requests.post(url, auth=auth(context), verify=False, data=payload)
	check_response(response, check=check)
	return response

def post_xml(url, filename, check=True):
	context = get_context()
	resourceType = context['resourceType']
	url = context.get(resourceType).get('url') + url
	payload = open(filename).read()
	headers = {'Content-Type': 'application/xml'}
	response = requests.post(url, auth=auth(context), verify=False, data=payload, headers=headers)
	check_response(response, check=check)
	return response

def post_yaml(url, filename, payload):
	context = get_context()
	resourceType = context['resourceType']
	url = context.get(resourceType).get('url') + url
	files = { filename: yaml.safe_dump(payload) }
	response = requests.post(url, auth=auth(context), verify=False, files=files)
	check_response(response)
	return response

def delete(url, check=True):
	context = get_context()
	resourceType = context['resourceType']
	url = context.get(resourceType).get('url') + url
	response = requests.delete(url, auth=auth(context), verify=False)
	check_response(response, check=check)
	return response

def check_response(response, check=True):
	#pprint(vars(response))
	if check and (response.status_code != requests.codes.ok and response.status_code > 400):
		
		print('-', response.status_code, response.request.url, file=sys.stderr)
		try:
			errors = response.json()["errors"]
			print('- '+('\n- '.join(json.dumps(errors, indent=4).splitlines())), file=sys.stderr)
		except:
			print(response.text, file=sys.stderr)
		sys.exit(1)
