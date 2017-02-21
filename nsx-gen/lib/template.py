#!/usr/bin/env python

# tile-generator
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

import os
import sys
import errno
import base64
import shutil
import yaml
from util import *

from jinja2 import Environment, FileSystemLoader, exceptions

PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.realpath(os.path.join(PATH, '..', 'templates'))

def render_base64(file):
	try:
		with open(os.path.realpath(os.path.join('..', file)), 'rb') as f:
			return base64.b64encode(f.read())
	except Exception as e:
		print >> sys.stderr, e
		sys.exit(1)

def render_hyphens(input):
	return input.replace('_','-')

def render_yaml(input):
	return yaml.safe_dump(input, default_flow_style=False)

TEMPLATE_ENVIRONMENT = Environment(trim_blocks=True, lstrip_blocks=True)
TEMPLATE_ENVIRONMENT.loader = FileSystemLoader(TEMPLATE_PATH)
TEMPLATE_ENVIRONMENT.globals['base64'] = render_base64
TEMPLATE_ENVIRONMENT.filters['hyphens'] = render_hyphens
TEMPLATE_ENVIRONMENT.filters['yaml'] = render_yaml

def render(target_path, template_file, config):
	target_dir = os.path.dirname(target_path)
	if target_dir != '':
		mkdir_p(target_dir)
	with open(target_path, 'wb') as target:
		target.write(TEMPLATE_ENVIRONMENT.get_template(template_file).render(config))

def exists(template_file):
	return os.exists(path(template_file))

def path(template_file):
	return os.path.join(TEMPLATE_PATH, template_file)
