# nsx-edge-gen is no longer actively maintained by VMware.

# nsx-edge-gen

Generate nsx logical switches, edge service gateways and lbs against Vmware NSX 6.3 API version

## Requirements
Ensure Python min version 2.7.10
Install the required python libraries using `pip install -r requirements.txt`

## NSX + PCF Architecture 

The generated NSX instance can have logical switches can be linked directly to it or via a DLR (Distributed Logical Router) using OSPF. 
Note: DLR is disabled by default. 

### Without DLR (direct connection from NSX Edge instance to Logical switches)
  ![](docs/overview-4-2017.png)


### With DLR Enabled (indirect connection from NSX Edge instance to Logical switches via DLR)
  ![](docs/overview-dlr-5-2017.png)

To enable DLR use the following flag: ` --nsxmanager_enable_dlr <true|false>`
Set `--nsxmanager_enable_dlr true ` or  ` -nsxmanager_en_dlr true ` in command line to nsx-gen or via the nsx_cloud_config.yml file (specified under nsxmanager section).
```
nsxmanager:
  address: 12.1.1.1
  ...
  transport_zone: TZ # Specified TransportZone should exist or would be created
  transport_zone_clusters: Cluster1,Cluster2 # Optional, needed on creation of transport zone
  distributed_portgroup: TestDistributedPortGroup # Required for DLR
  enable_dlr: true
```
Using a DLR does requires specifying a Distributed PortGroup as well as a password for the OSPF user.

This is more optimal architecture to avoid load on the NSX Edge instance for east-west traffic.
The firewall also would be defined on the DFW (Distributed firewall) when DLR is enabled

### With PCF 1.11 that has NSX integration 

If the tool is used against PCF1.11 that has nsx integration builtin, then its best to avoid binding ips to the loadbalancer pools in NSX, as PCF Ops Mgr 1.11+ and Bosh would handle registration of specific job types to pools using security groups. For PCF 1.10 and older releases, there is no such integration, and its best to just allow the nsx-edge-gen to do the member population inside the pools.

To denote PCF1.11 nsx integration or not, use the following flag: ` --nsxmanager_bosh_nsx_enabled <true|false>`
Set `--nsxmanager_bosh_nsx_enabled true ` or  ` -nsxmanager_bosh_nsx_enabled true ` in command line to nsx-gen or via the nsx_cloud_config.yml file (specified under nsxmanager section).

Setting it to true indicates there is bosh nsx integration and pool members wont be assigned any static ips
Setting it to false indicates there is no bosh nsx integration and pool members would be assigned static ips determined by nsx-edge-gen

### SSL Termination
NSX Loadbalancer can be configured to terminate SSL and decrypt the data and forward the plain data to GoRouter (default behavior) or just let the LBR do a pass-through of encrypted data to GoRouter and let it terminate the SSL and decrypt the data. The flag `esg_go_router_ssl_term_1` and `esg_go_router_isozone_1_ssl_term_1` can be applied for default gorouters as well as any iso-segment gorouters (replace the isozone index and suffix for the edge instance index).

Set flag `esg_go_router_ssl_term_1` to true (default) if ssl should be terminated by LBR and only unencrypted traffic forwarded to GoRouter. Use `esg_go_router_isozone_1_ssl_term_1` for isozone-1 and `esg_go_router_isozone_2_ssl_term_1` for isozone-2 all in nsx edge instance 1.

``` 
  -esg_go_router_ssl_term_1 true \
  -esg_go_router_isozone_1_ssl_term_1 true \

```

Set to false if encypted traffic should be forwarded as pass-through by LBR and ssl needs to be terminated only at GoRouter
``` 
  -esg_go_router_ssl_term_1 false \
  -esg_go_router_isozone_1_ssl_term_1 false \
```

# Generating initial config
Create a new config from template using nsx-gen init. The config file used to drive nsxgen is nsx_cloud_config.yml.

For initializing a brand new one from available template, use init command to nsxgen
./nsx-gen/bin/nsxgen init [identifier]

Example: 
```
`./nsx-gen/bin/nsxgen -i test init` would create a new folder `test` with the default template.
 `./nsx-gen/bin/nsxgen init` would create a default `nsx-pcf` folder with the default template of nsx_cloud_config.yml
```

Note: Ensure the identifier used for initialization of nsx_cloud_config is `unique` and also within `15 charactes` in length to avoid name collision with other instances as well as name not getting snipped when it comes to logical switches.

# Configuration
The default nsx_cloud_config.yml specifies the default set of logical switches and routed components.

## VCenter, NSXManager
Edit/update the nsx_cloud_config.yml file to update the vcenter, nsxmanager configs along with other information (networks, dns, credentials etc.).

## Logical Switches

A logical switch is associated with separate subnet for each type of component typically installed for PCF.
* Infra - Ops manager and BOSH Director
* Ert - for core PCF ERT tile to use
* PCF-Tiles - for mysql, rabbit, any other supporting service tiles
* Dynamic-Services - for services that would be kicked off dynamically by BOSH using the ODB broker model
* IsoZone-## - for Isolation segments with their own router and diego cells
Note: There can be additional logical switches per isolation segment as shown in the sample nsx_cloud_config.yml template. Use `IsoZone-` for naming the Zones and ensure the matching switch name is specifed for the routed components running in that Isolation Segment.

Avoid editing the default set of logical switches names or subnet. 
Additional logical switches with their own subnets can be added if necessary.

All of these logical switches can be linked directly to the NSX Edge instance or via a DLR (Distributed Logical Router) using OSPF. This can be controlled by following flag: `--nsxmanager_enable_dlr true ` either at command line or via the nsx_cloud_config.yml file.

## Edge Service Gateways
For every instance of edge service gateway to be created, specify its name, cli credentials, its gateway ip (can be the same for all instances) as well as certs needed to generate.

Based on the certs section within each edge gateway entry, self-signed certs can be generated for the specified system and org domains (under esg -> ert_certs -> config). If certs already exist, then insert the key and cert contents under certs section to be loaded into the loadbalancers. Or if a global cert is already available on the NSX, specify the cert id associated with the cert.
Similarly, certs can be generated for individual isolation segments (check for iso_certs in below snippet). If no config section is present under individual iso_certs section, then the ert certs would be used for those isolation segments.

Example:
```
edge_service_gateways:
- name: test-esg
  size: large
  gateway_ip: 10.114.216.1
  cli:
    username: testuser
    password: Test$assword123456
  ert_certs:
    name: Foundation1
    # cert_id: cert-11 # Uncomment and edit this in order to use an existing cert id
    # # Uncomment and edit below in order to use an existing cert and private key
    # # Ensure the alignment is correct and no extra newlines in either beginning or end of the entry
    # key: |+ # PEM encoded private key 
    #   -----BEGIN RSA PRIVATE KEY-----
    #   MIIEoQIBAAKCAQEAxFT4ktPgj8sBMumiK4nVXGC6UGqXgQkZly/7xC+c5T8pdsvl
    #   ..........................
    #   KdnT9tJIN80VMPkbsNPn2hxx3K7Wbb/tzvRtjCUkqP7/fnVXIQ==
    #   -----END RSA PRIVATE KEY-----
    # cert: |+ # PEM encoded cert 
    #   -----BEGIN CERTIFICATE-----
    #   MIIDwjCCAqqgAwIBAgIJAOx8KRhUILhrMA0GCSqGSIb3DQEBBQUAMEcxJjAkBgNV
    #   ...........
    #   TAvqkR+T
    #   -----END CERTIFICATE-----    
    config:
      org_unit: Pivotal
      country_code: US  # Default - US
      system_domain: pcf-sys-test.corp.local
      app_domain: pcf-app1-test.corp.local,pcf-app2-test.corp.local # comma separated list
  iso_certs:
  # Array of isolation zones and their cert config
  - name: IsoZone1
    switch: IsoZone-1
    config:
      org_unit: Pivotal
      country_code: US  # Default - US
      domains: pcf-zone1-prod-app-test.corp.local,pcf-zone1-test-app-test.corp.local # comma separated list 
```

### Routed Components

A Routed Component is associated with specific components routable from outside or internally.
Default routed components include opsmgr, go-router (CF entry point via Go-Router), diego-brain (for ssh access), 
tcp-router (for tcp routing), mysql-ert (for inbuilt mysql proxy used within ERT), mysql-tile (for the MySQL Service Tile) and rabbitmq-tile (for RabbitMQ).  Dont change the name of these default routable components.

Each routed component (except for Ops Mgr) would use a VIP and Loadbalancer instance to distribute load to members handling the specific functionality. Each routed component should specify its logical switch and its uplink ip. The uplink ip is used as the VIP. Since MySQL, RabbitMQ tiles and the internal MySQl service within ERT are not exposed outside, they would use an internal ip from within the subnet specified by their logical switch as uplink ip, compared to other routed components that have to allow external communication to flow through.

Each routed component can specify the number of instances that the loadbalancer can distribute the load across and the offset to use to assign the ips for these members.

Also, each routed component specifies the transport details for ingress and egress for its loadbalancer. For example, go-router's associated Loadbalancer instance should allow ingress over HTTPS but forwards over HTTP to the go-router. The ports can also be specified. For example, tcp-router accepts TCP over 5000 port for its loadbalancer and forwards to the tcp-router on 5000.

Example:
```
  - name: go-router # go router
    switch: Ert.    # Belong to Ert logical switch
    instances: 4    # 4 instances of go-router
    offset: 10
    external: true
    uplink_details:
      uplink_ip: 10.114.216.172 # This gets exposed outside
    #transport:
      # Default ingress scheme is https/443 for ert
      ingress:
        port: 443
        protocol: https
      # Default egress scheme is http/8080 for ert
      egress: 
        port: 8080
        protocol: http
        monitor_port: 80
        url: /health

  - name: mysql-tile  # MySQL Tile's proxy
    switch: PCF-Tiles # Belong to PCF-Tiles logical switch
    instances: 3      # for 3 proxies in 3 AZs
    offset: 10
    external: false
    uplink_details:
      uplink_ip: 192.168.27.250 # This should be on the PCF-Tiles network, not external facing
    transport:
      # Use defaults - tcp/3306 incoming, tcp/3306 forward
      ingress:
        port: 3306
        protocol: tcp
      egress: 
        port: 3306
        protocol: tcp
        monitor_port: 1936


```
The default set of routed components are already filled in code to take care of default number of instances, offset, transport details etc.

Note: Now its possible to expose the Bosh director and associated management services via Loadbalancer/vip using `opsdir` routed component.
Just specify the uplink ip for the ops dir and following ports would be automatically get exposed: 8443,4222,25555,25250,443
```
  -esg_opsmgr_uplink_ip_1 10.74.37.171 \
  -esg_go_router_uplink_ip_1 10.74.37.172 \
  -esg_opsdir_uplink_ip_1 10.74.37.176 \
```

Default instance ip for the Bosh Director would be use offset `10` from the Infra logical switch subnet (like 192.168.10.10)
Specify the offsets by either declaring the section in the nsx_cloud_config.yml :
```
   - name: opsdir
     switch: Infra
     external: true
     instances: 1
     offset: 10
     uplink_details:
       uplink_ip: 10.114.216.176 # This gets exposed outside   
    #transport: # uncomment to change the defaults
      # ingress:
      #  port: 8443,4222,25555,25250,443
      #  protocol: tcp
      # egress: 
      #  port: 8443,4222,25555,25250,443
      #  protocol: tcp
```

or via additional command line args:
```
  -esg_opsdir_uplink_ip_1 10.74.37.176 \
  -esg_opsdir_off_1 10 \
```

Avoid editing the default set of routed_components. 
Additional new routed components can be added if necessary.

Note: The default uplink ip for the routed components in the template has been changed to 1.1.1.x (those exposed externally). For those components that are not overiding this default ip, the routed components would be ignored from the setup. This is to avoid errors later when a default uplink ip is not part of the defined network subnets and block creation of the edge.
Sample warning error for those components that miss the uplink ip:
```
WARNING!! Ignoring Routed component: go-router-nossl as it was not supplied with Uplink IP!!
```

# Build Logical switches and ESG
Build new instances of ESGs and logical switches using the build command as arg to nsxgen

```
./nsx-gen/bin/nsxgen [-c path-to-config] build 
```
If no -c flag specified, check current folder for locating the nsx_cloud_config.yml and use it.
If file not in current folder, use `-c <directory-path> ` as argument.
Example:
./nsx-gen/bin/nsxgen build            (if nsx_cloud_config.yml available in current folder)
./nsx-gen/bin/nsxgen -c nsx-pcf build (if init as used and nsx_cloud_config.yml file is under nsx-pcf)

# Export ESG Configuration
Export existing ESG instance configurations using the export command as arg to nsxgen
```
 ./nsx-gen/bin/nsxgen -c nsx-pcf \
   -nsxedge_names esg-test1,esg-test2,... \
   -export_dir exported-config-output \
   ..other_args.. \
   export 
```
This would export the entire esg instance configuration (in xml), as well as the firewall rules (in both xml & yml)

Sample output:
```
Full export section: {'nsxedge_names': 'esg-sabha-test,esg-sabha6', 'export_directory': 'export-output'}, Export dir: export-output
....

NSX Edge 'esg-sabha-test' (id: edge-396) exported!!

Saved NSX Edge 'esg-sabha-test' full payload (xml) : export-output/esg-sabha-test.xml
Saved NSX Edge 'esg-sabha-test' firewall rules (xml) : export-output/esg-sabha-test-firewall-rules.xml
Saved NSX Edge 'esg-sabha-test' firewall rules (yml) : export-output/esg-sabha-test-firewall-rules.yml

NSX Edge 'esg-sabha6' (id: edge-467) exported!!

Saved NSX Edge 'esg-sabha6' full payload (xml) : export-output/esg-sabha6.xml
Saved NSX Edge 'esg-sabha6' firewall rules (xml) : export-output/esg-sabha6-firewall-rules.xml
Saved NSX Edge 'esg-sabha6' firewall rules (yml) : export-output/esg-sabha6-firewall-rules.yml
```

nsxgen would also auto-update the firewall config to translate/transform any ip-sets or application sets to actual the real ips or ranges or ports/protocols during the export so the rules can be reused later across envs and instances.

Example:
```
Change from:
    <source>
        <groupingObjectId>ipset-7</groupingObjectId>
    </source>
Change to:
    <source>
        <ipAddress>192.168.10.0-192.168.10.100</ipAddress>
    </source>

Change from:
    <application>
        <applicationId>application-352</applicationId>
        <applicationId>application-370</applicationId>
    </application>
Change to:
    <application>
        <service>
            <protocol>tcp</protocol>
            <port>80</port>
        </service>
        <service>
            <protocol>tcp</protocol>
            <port>443</port>        
        </service>
    </application>
```

## Command line args
Build/Export/Delete config can be overriden using command line args.

Built-in templated routed components can be overridden by using command line args.
Known routed component templates include opsmgr, go-router, tcp-router, diego-brain, mysql-ert, mysql-tile, rabbitmq-tile
The uplink ip (assigned for component or to Loadbalancer VIP), instances (# of dedicated ips to loadbalance against), offset (from a given range) can be overridden via command line args for these components

Refer to [command line usage docs][] for complete set of available args

Example:
```
# Sample init and build using command line args
# Initialize a default configuration with name `sabha` 
./nsx-gen/bin/nsxgen -i sabha init

# Folder named 'sabha' created now with default config

# Run build overriding the default configs
RUN_CMD=build

# Following would create 2 isolation segments overriding the single Isolation segment in the template file
# each with its own go-router and tcp-router with uplink
# IsoZone-1 : -isozone_switch_name_1 IsoZone-1  
# IsoZone-2 : -isozone_switch_name_2 IsoZone-2 

# Uplink for GoRouter in IsoZone-1 (part of ESG instance 1):  -esg_go_router_isozone_1_uplink_ip_1  10.13.92.181 
# Switch Name for the above GoRouter : -esg_go_router_isozone_1_switch_1 IsoZone-1 
# Uplink for TcpRouter in IsoZone-1 (part of ESG instance 1):  -esg_tcp_router_isozone_1_uplink_ip_1  10.13.92.182

# Uplink for GoRouter in IsoZone-2 (part of ESG instance 1):  -esg_go_router_isozone_2_uplink_ip_1  10.13.92.184 
# Switch Name for the above GoRouter : -esg_go_router_isozone_2_switch_1 IsoZone-2 
# Uplink for TcpRouter in IsoZone-1 (part of ESG instance 1):  -esg_tcp_router_isozone_2_uplink_ip_1  10.13.92.185

./nsx-gen/bin/nsxgen -c sabha \
  -esg_name_1 sabha \
  -esg_size_1 compact \
  -esg_cli_user_1 admin \
  -esg_cli_pass_1 'P1v0t4l!P1v0t4l!' \
  -nsxmanager_dportgroup DPortGroupTest \
  -nsxmanager_en_dlr true \
  -esg_ert_certs_1 autogen \
  -esg_ert_certs_config_sysd_1 sys2.test.pez.pivotal.io \
  -esg_ert_certs_config_appd_1 apps2.test.pez.pivotal.io \
  -esg_opsmgr_uplink_ip_1 10.13.92.171 \
  -esg_go_router_uplink_ip_1 10.13.92.172 \
  -esg_diego_brain_uplink_ip_1 10.13.92.173 \
  -esg_tcp_router_uplink_ip_1 10.13.92.174 \
  -esg_mysql_ert_uplink_ip_1 192.168.23.250 \
  -esg_mysql_ert_inst_1 5  \
  -esg_mysql_tile_uplink_ip_1 192.168.27.250 \
  -esg_mysql_tile_inst_1 2  \
  -esg_rabbitmq_tile_uplink_ip_1 192.168.27.251 \
  -esg_rabbitmq_tile_inst_1 5 \
  -esg_rabbitmq_tile_off_1 10 \
  -vcenter_addr vc-01.test.pez.pivotal.io \
  -vcenter_user administrator@vsphere.local \
  -vcenter_pass 'testAdmin123' \
  -vcenter_dc Datacenter \
  -vcenter_ds Datastore \
  -vcenter_cluster Cluster \
  -nsxmanager_addr 10.13.92.21 \
  -nsxmanager_user admin \
  -nsxmanager_pass 'testNsxAdmin123' \
  -nsxmanager_tz testtz \
  -nsxmanager_uplink_ip 10.13.92.170 \
  -nsxmanager_uplink_port 'VM Network' \
  -esg_gateway_1 10.13.92.1 \
  -isozone_switch_name_1 IsoZone-1 \
  -isozone_switch_cidr_1 192.168.34.0/22 \
  -isozone_switch_name_2 IsoZone-2 \
  -isozone_switch_cidr_2 192.168.38.0/22 \
  -isozone_switch_name_3 IsoZone-3 \
  -isozone_switch_cidr_3 192.168.42.0/22 \
  -esg_go_router_isozone_1_uplink_ip_1  10.13.92.181 \
  -esg_go_router_isozone_1_switch_1 IsoZone-1  \
  -esg_go_router_isozone_1_inst_1 2 \
  -esg_tcp_router_isozone_1_uplink_ip_1  10.13.92.182 \
  -esg_tcp_router_isozone_1_switch_1  IsoZone-1 \
  -esg_tcp_router_isozone_1_inst_1 2 \
  -esg_go_router_isozone_2_uplink_ip_1  10.13.92.184 \
  -esg_go_router_isozone_2_inst_1 2 \
  -esg_go_router_isozone_2_switch_1 IsoZone-2 \
  -esg_tcp_router_isozone_2_uplink_ip_1  10.13.92.185 \
  -esg_tcp_router_isozone_2_switch_1  IsoZone-2 \
  -esg_tcp_router_isozone_2_inst_1 1 \
  $RUN_CMD

```

For a new component that is not part of the known templated components, one would have to add the entry into the config file 
and specify the switch, ingress and egress transports (with port/protocol/monitor_port etc.) and its uplink details.
Command line arg overriding is not supported for new types.

Sample Entry in template:
```
# Sample service entry
- name: test-service
 uplink_ip: 10.193.99.41
 switch: PCF-Tiles
 instances: 4
 external: true # Allow external access
 offset: 30
 transport:
   #Use defaults - https/443 incoming, http/80 forward
   ingress:
     port: 443
     protocol: https
   egress:
     port: 80
     protocol: http
     monitor_port: 80  
```


## nsxgen output

When the nsxgen is executed, it first outputs the configurations loaded (doing a merge of the file template and the command line args) and emits the logical switches and routable components config before proceeding to build or tear down the edge instance.
The derived instance ips, routing and monitor details along with application profiles, rules would be all displayed for each routable component.

Sample output:
```
Validation of Default Routed components successful...


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                                Command Line Args Mapped
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
{'edge_service_gateways': [{'cli': {'username': 'admin'}, 'routed_components': [{'name': 'opsmgr', 'uplink_details': {'uplink_ip': '10.193.99.171'}}, {'name': 'go-router', 'uplink_details': {'uplink_ip': '10.193.99.172'}}, ..... 'vcenter': {'datacenter': 'Datacenter', 'admin_user': 'administrator@vsphere.local', 'cluster': 'Cluster1', ...'address': 'test.haas.pivotal.io', 'datastore': 'vsanDatastore'}}


------------------------------------------------------------------------------------------------------------------------------------------------------
                                                  Logical Switches (from configuration)
Name                                                         | CIDR                 | Primary IP
------------------------------------------------------------------------------------------------------------------------------------------------------
lswitch-sabha-Infra                                          | 192.168.10.0/26      | 192.168.10.1
lswitch-sabha-Ert                                            | 192.168.20.0/22      | 192.168.20.1
lswitch-sabha-PCF-Tiles                                      | 192.168.24.0/22      | 192.168.24.1
lswitch-sabha-Dynamic-Services                               | 192.168.28.0/22      | 192.168.28.1
lswitch-sabha-IsoZone-01                                     | 192.168.32.0/22      | 192.168.32.1
------------------------------------------------------------------------------------------------------------------------------------------------------

Parsing Routed Component: {'instances': 1, 'switch': 'Infra', 'name': 'opsmgr', 'uplink_details': {'uplink_ip': '10.193.99.171'}, 'offset': 5}
Looking up for switch with name: Infra for Routed component: opsmgr
Routed component: opsmgr: {
 		'switch': {'secondary_ips': [], 'primary_ip': IP('192.168.10.1/26'), 'name': 'lswitch-sabha-Infra',  'gateway': IP('192.168.10.0/26')}, 'useVIP': False,  'instances' : 1,  'offset' :  5,
         .....
  		'monitor_id': monitor-3
 		'transport': { 'ingress': { 'port': 443, 'protocol': https, 'is_ingress': True, 'monitor_port' : None,  'url' :  None },
 				'egress' : { 'port': 443, 'protocol': https, 'is_ingress': False, 'monitor_port' : 443,  'url' :  / } }
 		}

.........


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                                Edge Service Gateways (from configuration)
Name                           | Moid                           | Routed Components                                  | Uplink Port          | Uplink IP  | Creds
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
esg-sabha                      |                                | opsmgr,go-router,diego-brain,tcp-router,mysql-ert,mysql-tile,rabbitmq-tile | VM Network           | 10.193.99.170 | user=admin, passwd=P1v0t4l!P1v0t4l!
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                                                                                Firewall (from configuration)
Name                                     | Ingress/Egress       | Source                                                                           | Destination
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Allow Ingress -> Ops Manager             | Ingress              | any                                                                              | tcp/22,80,443
Allow Ingress -> SSH for Apps            | Ingress              | any                                                                              | tcp/2222
Allow Ingress -> Tcp Router              | Ingress              | any                                                                              | tcp/5000
Allow Ingress -> Elastic Runtime         | Ingress              | any                                                                              | tcp/80,443,443
Allow Egress -> All Outbound             | Egress               | any                                                                              | any
Allow Inside <-> Inside                  | Both                 | any                                                                              | any

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                                Routed Component (from configuration) for Edge Instance: esg-sabha-sabha3
Name                   | Switch       |VIP  |Inst |Offset| Uplink IP      | IPs            | App Rules                 |  App Profile     |Monitor Id| Ingress:Port         | Egress:Port          | Port:Monitor Url
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
opsmgr                 | Infra        |N    |1    |5    | 10.193.99.171  | 192.168.10.5   | applicationProfile-4      | applicationRule-1 |monitor-3 |https:443             |https:443             |:https/
                       |              |     |     |     |                |                |                           | applicationRule-2 |          |                      |                      |
                       |              |     |     |     |                |                |                           | applicationRule-4 |          |                      |                      |
go-router              | Ert          |Y    |4    |10   | 10.193.99.172  | 192.168.20.10  | applicationProfile-3      | applicationRule-1 |monitor-4 |https:443             |http:80               |:http/health
                       |              |     |     |     |                | 192.168.20.11  |                           | applicationRule-2 |          |                      |                      |
                       |              |     |     |     |                | 192.168.20.12  |                           | applicationRule-4 |          |                      |                      |
                       |              |     |     |     |                | 192.168.20.13  |                           |                   |          |                      |                      |
diego-brain            | Ert          |Y    |3    |20   | 10.193.99.173  | 192.168.20.20  | applicationProfile-6      | applicationRule-1 |monitor-1 |tcp:2222              |tcp:2222              |:tcp
                       |              |     |     |     |                | 192.168.20.21  |                           | applicationRule-2 |          |                      |                      |
                       |              |     |     |     |                | 192.168.20.22  |                           |                   |          |                      |                      |
tcp-router             | Ert          |Y    |4    |30   | 10.193.99.174  | 192.168.20.30  | applicationProfile-6      | applicationRule-1 |monitor-5 |tcp:5000              |tcp:5000              |:tcp/health
                       |              |     |     |     |                | 192.168.20.31  |                           | applicationRule-2 |          |                      |                      |
                       |              |     |     |     |                | 192.168.20.32  |                           |                   |          |                      |                      |
                       |              |     |     |     |                | 192.168.20.33  |                           |                   |          |                      |                      |
mysql-ert              | Ert          |Y    |5    |40   | 192.168.23.250 | 192.168.20.40  | applicationProfile-6      | applicationRule-1 |monitor-6 |tcp:3306              |tcp:3306              |:tcp
                       |              |     |     |     |                | 192.168.20.41  |                           | applicationRule-2 |          |                      |                      |
                       |              |     |     |     |                | 192.168.20.42  |                           |                   |          |                      |                      |
                       |              |     |     |     |                | 192.168.20.43  |                           |                   |          |                      |                      |
                       |              |     |     |     |                | 192.168.20.44  |                           |                   |          |                      |                      |
mysql-tile             | PCF-Tiles    |Y    |2    |10   | 192.168.27.250 | 192.168.24.10  | applicationProfile-6      | applicationRule-1 |monitor-1 |tcp:3306              |tcp:3306              |:tcp
                       |              |     |     |     |                | 192.168.24.11  |                           | applicationRule-2 |          |                      |                      |
rabbitmq-tile          | PCF-Tiles    |Y    |5    |10   | 192.168.27.251 | 192.168.24.10  | applicationProfile-6      | applicationRule-1 |monitor-1 |tcp:15672,5671,5672   |tcp:15672,5671,5672   |:tcp
                       |              |     |     |     |                | 192.168.24.11  |                           | applicationRule-2 |          |                      |                      |
                       |              |     |     |     |                | 192.168.24.12  |                           |                   |          |                      |                      |
                       |              |     |     |     |                | 192.168.24.13  |                           |                   |          |                      |                      |
                       |              |     |     |     |                | 192.168.24.14  |                           |                   |          |                      |                      |
go-router-isozone-1    | IsoZone-01   |Y    |2    |10   | 10.193.99.175  | 192.168.32.10  | applicationProfile-3      | applicationRule-1 |monitor-4 |https:443             |http:80               |:http/health
                       |              |     |     |     |                | 192.168.32.11  |                           | applicationRule-2 |          |                      |                      |
                       |              |     |     |     |                |                |                           | applicationRule-4 |          |                      |                      |
tcp-router-isozone-1   | IsoZone-01   |Y    |2    |30   | 10.193.99.176  | 192.168.32.30  | applicationProfile-6      | applicationRule-1 |monitor-5 |tcp:5000              |tcp:5000              |:tcp/health
                       |              |     |     |     |                | 192.168.32.31  |                           | applicationRule-2 |          |                      |                      |
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


```

# List Logical switches and ESG
List local configuration as well as connect to the vcenter/nsx manager and show configured components
./nsx-gen/bin/nsxgen [-c path-to-config] list

Example:
```
./nsx-gen/bin/nsxgen list            (if nsx_cloud_config.yml available in current folder)
./nsx-gen/bin/nsxgen -c nsx-pcf list (if init was used earlier and nsx_cloud_config.yml file is under nsx-pcf)
```

# Destroy Logical switches and ESG
Destroy components wired using the specified configuration
./nsx-gen/bin/nsxgen [-c path-to-config] delete

Example:
```
./nsx-gen/bin/nsxgen delete            (if nsx_cloud_config.yml available in current folder)
./nsx-gen/bin/nsxgen -c nsx-pcf delete (if init was used earlier and nsx_cloud_config.yml file is under nsx-pcf)
```

[command line usage docs]: docs/usage.md
