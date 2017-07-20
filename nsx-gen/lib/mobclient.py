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

import base64
import cookielib
import ssl
import requests
import re
import time
from pyquery import PyQuery
from lxml import html, etree
import urllib
import urllib2
from urllib2 import urlopen, Request

try:
    # Python 3
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    from urlparse import urlparse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

DEBUG = False
# Grab following resource types from mob tree
# leaving first letter for some that have upper case like Cluster, Datastore, Datacenter, Network
RESOURCE_TYPES = [ 'atacenter', 'atastore', 'host', 'domain', 'luster', 'virtualwire', 'portgroup', 'etwork']

def get_context():
    if get_context.context is not None:
        return get_context.context
    else:
        raise Error(resourceType + ' config not loaded!!')

get_context.context = None

def set_context(context):
    get_context.context = context


def create_url_opener():
    cookies = cookielib.LWPCookieJar()
    handlers = [
            urllib2.HTTPHandler(debuglevel=1),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies)
        ]
    opener = urllib2.build_opener(*handlers)
    return opener    

def createBaseAuthToken(user, passwd):
    return base64.b64encode('%s:%s' % (user, passwd))

def lookupSessionNonce(response):
    pq = PyQuery(response)
    vmware_session_nonce = ''
    hidden_entry = pq('input:hidden')
    if hidden_entry.attr('name') == 'vmware-session-nonce' :
        vmware_session_nonce = hidden_entry.attr('value')
    if DEBUG:
        print('vmware-session-nonce: ' + vmware_session_nonce)
    return vmware_session_nonce


def init_vmware_session():
    context = get_context()

    vcenterMobServiceInstanceUrl = '/mob/?moid=ServiceInstance&method=retrieveContent'
    data = None #'vmware-session-nonce': context['vmware-session-nonce']}
    cookies = None
    serviceInstanceGetRespSock = queryVCenterMob(context, vcenterMobServiceInstanceUrl, 'GET', data, cookies)

    serviceInstanceGetRespInfo = serviceInstanceGetRespSock.info()
    cookies = serviceInstanceGetRespSock.info()['Set-Cookie']
    serviceInstanceGetResp = serviceInstanceGetRespSock.read()
    
    serviceInstanceGetRespSock.close()
    
    if DEBUG:
        print('Cookies: ' + cookies)
        print('Info: ' + str(serviceInstanceGetRespInfo))
        print('vCenter MOB response :\n' + str(serviceInstanceGetResp)+ '\n-----\n')

    #if response.status_code != requests.codes.ok:
    #        raise Error('Unable to connect to vcenter, error message: ' + vcenterServiceInstanceResponse.text)

    vmware_session_nonce = lookupSessionNonce(serviceInstanceGetResp)
    context['vmware-session-nonce'] = vmware_session_nonce
    context['vmware-cookies'] = cookies
    return

def lookup_vsphere_config():
    context = get_context()

    init_vmware_session()
    data = { 'vmware-session-nonce': context['vmware-session-nonce']}
    cookies = context['vmware-cookies']

    processVCenterMobRequest(context, '/mob/?moid=ServiceInstance&method=retrieveContent', 'POST', data, cookies )
    return traversedMoidTree(context, data, cookies)

def refresh_vsphere_config():
    context = get_context()

    # if things were run within 5 seconds, return cached data..
    moidMap = checkMoidMap()
    if moidMap:
        return moidMap

    init_vmware_session()

    data = { }
    cookies = context['vmware-cookies']

    # Now fetch everything
    return traversedMoidTree(context, data, cookies)

def checkMoidMap():
    context = get_context()

    lastRefresh = context.get('LAST_REFRESH')
    if lastRefresh and (time.time() - lastRefresh < 5):
        moidMap = context['vcenterMobMap']
        if moidMap:
            return moidMap

    return None

def traversedMoidTree(context, data, cookies):

    method = 'GET'
    # Fetch everything under the root group-d1
    detailedMoidMap = processVCenterMobRequest(context, '/mob/?moid=group-d1', method, data, cookies)
    
    # Now traverse the datacenter, datastore and host
    datacenterMoidMap = { }
    for key, entry in detailedMoidMap.iteritems():
        if 'datacenter' in entry['moid']:            
            detailedVcenterMobUrl = '/mob/?moid=' + entry['moid']
            datacenterMoidMap.update(processVCenterMobRequest(context, detailedVcenterMobUrl, method, data, cookies))

    detailedMoidMap.update(datacenterMoidMap)
    if DEBUG:
        print('Datacenters Moid Map:\n' + str(detailedMoidMap))

    hostMobUrl = '/mob/?moid=' + detailedMoidMap['host']['moid']
    detailedMoidMap.update(processVCenterMobRequest(context, hostMobUrl, 'GET', data, cookies))
   
    datastoreMoidMap = { }
    for key, entry in detailedMoidMap.iteritems():
        if 'datastore' in entry['moid']:            
            detailedVcenterMobUrl = '/mob/?moid=' + entry['moid']
            datastoreMoidMap.update(processVCenterMobRequest(context, detailedVcenterMobUrl, method, data, cookies))

    detailedMoidMap.update(datastoreMoidMap)

    if DEBUG:
        print('Entire Moid Map:\n' + str(detailedMoidMap))
   
    # Save the tree locally
    context['vcenterMobMap'] = detailedMoidMap
    context['LAST_REFRESH'] = time.time()

    return context['vcenterMobMap']


def processVCenterMobRequest(context, vcenterMobUrl, method, data, cookies):
    mobRespSock = queryVCenterMob(context, vcenterMobUrl,  method, data, cookies)
    mobResp = mobRespSock.read()
    mobRespSock.close()
    
    if DEBUG:
        print('\n\n Mob Response for url[' + vcenterMobUrl + ']:\n' + mobResp)

    moidMap = generateMoidMap(mobResp, RESOURCE_TYPES)
    return moidMap


def generateMoidMap(response, resourceTypes):

    """
    for e in tree.xpath("//td/a[contains(text(),'datacenter')]/.."):
        print('Entry: ' + str(e) + '\n\t content: ' + e.text_content() + '\n') 
        if e.attrib.has_key('href') and e.attrib['href'].find('datacenter') != -1:
            print('Found Match 3 ............' + e.text)
    if response is None or response == '':
        with open('/Users/sparameswaran/workspace/nsx-edge-gen/complete_mob.html', 'r') as myfile:
        #with open('/Users/sparameswaran/workspace/nsx-edge-gen/group-dump.html', 'r') as myfile:
             response=myfile.read()#.replace('\n', '')
    """

    response = html_decode(response)
    tree = html.fromstring(response)
    
    moidMap = {}   

    #for entry in tree.xpath("//td/a[contains(text(),'datacenter')]/.."):
    for entry in tree.xpath("//td/a/.."):
        href_and_rest = etree.tostring(entry)        
        if href_and_rest is None or 'alarm' in href_and_rest or 'javascript' in href_and_rest:
            continue

        if "onclick" in href_and_rest or 'doPath' in href_and_rest or 'query' in href_and_rest:
            continue
        
        if not any(searchString in href_and_rest for searchString in resourceTypes):
            continue

        if DEBUG:
            print('Entry content is: ' + href_and_rest)
        
        
        # for child in entry:
        #     print('child:' + child.tag + ', content: ' + etree.tostring(child)  + ', value: ' + child.text_content() + ', complete string: ' + str(child))
        #     for nested_child in child:
        #         print('\t nestedchild:' + nested_child.tag + ', value: ' + etree.tostring(nested_child) + ' content: ' + nested_child.text_content() + ', complete string: ' + str(nested_child))
        #         for nested_child2 in nested_child:
        #             print('\t nestedchild2:' + nested_child2.tag + ', value: ' + etree.tostring(nested_child2) + ' content: ' +nested_child2.text_content() + ', complete string: ' + str(nested_child2))


        """
        Sample entry:
        <td class="clean"><a href="https://vcsa-01.haas-94.pez.pivotal.io/mob/?moid=dvportgroup%2d168">dvportgroup-168</a> (vxw-dvs-29-virtualwire-115-sid-5013-lswitch-test2-Services)</td>
        <td><a href="https://vcsa-01.haas-94.pez.pivotal.io/mob/?moid=group%2dd1">group-d1</a> (Datacenters)</td>
        <td class="html-attribute-name">class="<span class="html-attribute-value">clean</span>"&gt;
        <span class="html-tag"><a class="html-attribute-name">href</a></span>
        ="<a class="html-attribute-value html-external-link" target="_blank" href="https://vcsa-01.haas-94.pez.pivotal.io/mob/?moid=datacenter-2">/mob/?moid=datacenter-2</a>
        datacenter-2<span class="html-tag"/> (Datacenter)<span class="html-tag"/></td>
        
        Add lazy capture for the name as in (datastore1 (3)) using .*?\( .. )
        """

        match = re.search(r'href="(.*?)">(.*)</.*?\((.*)\).*', href_and_rest)
        if match is not None:
            href = match.group(1)
            moid = match.group(2).replace('/mob/?moid=','')
            mobName = match.group(3)
            moidMap[mobName] = { 'moid' :  moid, 'href': href }
            if DEBUG:
                print('Mob Name: ' + mobName + ', moid : ' + moid + ', href: ' + href )

    if DEBUG:
        print('Entry Map: ' + str(moidMap))
    return moidMap   

def lookup_moid(resourceName):

    vcenterMobMap = checkMoidMap()
    if not vcenterMobMap:
        vcenterMobMap = refresh_vsphere_config()

    if resourceName in vcenterMobMap:
        return vcenterMobMap[resourceName]['moid']
    if 'atastore' in resourceName:
        if resourceName in vcenterMobMap:
            return vcenterMobMap[resourceName]['moid']
        elif 'vsan' + resourceName in vcenterMobMap:
            return vcenterMobMap['vsan' + resourceName]['moid']

    print('Unable to lookup Moid for resource: ' + resourceName)
    return resourceName

def lookup_logicalswitch_managed_obj_name( resourceName):
    
    vcenterMobMap = checkMoidMap()
    if not vcenterMobMap:
        vcenterMobMap = refresh_vsphere_config()
        
    """
    # For logical switches, the user associated name would be something like:
    moid: dvportgroup-272 
    name in moid map: vxw-dvs-29-virtualwire-179-sid-5029-lswitch-test4-Infra
    user associated name: lswitch-test4-Infra
    """

    for key in vcenterMobMap:
        #print('key[{}] : {}'.format(key, str(vcenterMobMap[key])))
        if resourceName in key:
            return key        

    # If the length of the lswitch name is over 40 characters, 
    # then things get trimmed in the generated virtualwires
    # Sample virtualwire: vxw-dvs-50-virtualwire-16-sid-5015-lswitch-edge-nsx-pipeline-sample-Dynamic-Serv
    if len(resourceName) > 40:
        lswitch_initial_chars = resourceName[0:5]
        for key in vcenterMobMap:
            #print('key[{}] : {}'.format(key, str(vcenterMobMap[key])))
            if 'virtualwire' in key and lswitch_initial_chars in key:
                associated_lsw_name = key[key.index(lswitch_initial_chars):]
                if associated_lsw_name in resourceName:
                    return key  

    print('Unable to lookup Moid for resource: {}'.format(resourceName))
    return resourceName

def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return mark_safe(force_unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

def create_non_verify_sslcontext():
    urlctx = ssl.create_default_context()
    urlctx.check_hostname = False
    urlctx.verify_mode = ssl.CERT_NONE
    return urlctx  

def queryVCenterMob(vcenter_ctx, url, method, data, cookies): 
    vcenterOriginUrl = 'https://' + vcenter_ctx['address']
    vcenterMobUrl = vcenterOriginUrl + url

    urlctx = create_non_verify_sslcontext()
    opener = create_url_opener()
    #data = urllib.urlencode({ 'vmware-session-nonce': context['vmware-session-nonce']})
    if data is not None and method == 'POST':
        req = urllib2.Request(vcenterMobUrl, data=urllib.urlencode(data))#, auth=auth, data=data, verify=False, headers=headers)
    else:
        req = urllib2.Request(vcenterMobUrl)

    base64string = createBaseAuthToken(vcenter_ctx.get('admin_user'), vcenter_ctx.get('admin_passwd'))
    #print('Url: {}'.format(vcenterMobUrl))
    
    req.add_header('Authorization', "Basic %s" % base64string)
    req.add_header('User-Agent', "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30")
    req.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
    req.add_header('Accept-Language', 'en-US,en;q=0.8')
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml,;q=0.9,*/*;q=0.8")
    # req.add_header('Referer', vcenterMobUrl)
    # req.add_header('Origin', vcenterOriginUrl) 
    # req.add_header('Host',  vcenter_ctx['address']) 

    if cookies is not None:
        req.add_header("Cookie", cookies)
    req.get_method = lambda: method

    sock = urllib2.urlopen(req, context=urlctx)
    return sock