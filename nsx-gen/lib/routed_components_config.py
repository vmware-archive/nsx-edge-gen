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

import os.path
import string
import sys
import yaml
import re


ROUTED_COMPONENTS_CONFIG_FILE = 'routed_components_template.yml'

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.realpath(os.path.join(LIB_PATH, '..'))
TEMPLATE_PATH = os.path.realpath(os.path.join(LIB_PATH, '..', 'templates'))


class Config(dict):


	def read_config(self, input_config_file=ROUTED_COMPONENTS_CONFIG_FILE):
		#print('Input config file:{}'.format(input_config_file))
		input_config_file = TEMPLATE_PATH + '/' + ROUTED_COMPONENTS_CONFIG_FILE

		try:
			with open(input_config_file) as config_file:
				self.update(read_yaml(config_file))
		except IOError as e:			
			print >> sys.stderr, 'Not a routed components config file.'
			sys.exit(1)

	def read(self, config_file=ROUTED_COMPONENTS_CONFIG_FILE):
		self.read_config(config_file)
		return self

def read_yaml(file):
	return yaml.safe_load(file)

def load_routed_comps_cfg():
	routed_comps_cfg = Config().read()
	#print('Routed Components config : {}'.format(routed_comps_cfg))
	return routed_comps_cfg

def main():
	load_routed_comps_cfg()


if __name__ == "__main__":
	main()	