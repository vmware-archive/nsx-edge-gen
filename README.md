# nsx-edge-gen

Generate nsx logical switches, edge service gateways and lbs against Vmware NSX 6.3 API version

# Requirements
Ensure Python min version 2.7.10
Install the required python libraries using `pip install -r requirements.txt`

# nsx_cloud_config.yml
Create a new template using nsx-gen init.
For initializing a brand new one from available template, use init command to nsxgen
./nsx-gen/bin/nsxgen init [identifier]

Example: 
`./nsx-gen/bin/nsxgen init test` would create a new folder `test` with the default template.
 `./nsx-gen/bin/nsxgen init` would create a default `nsx-pcf` folder with the default template of nsx_cloud-config.yml

# Configure networks, dns, credentials
Then edit/update the nsx_cloud_config.yml file to generate logical switches and edge service gateways

# Build Logical switches and ESG
./nsx-gen/bin/nsxgen [-c path-to-config] build 

If no -c flag specified, check current folder for locating the nsx_cloud_config.yml and use it.
If file not in current folder, use `-c <directory-path> ` as argument.
Example:
./nsx-gen/bin/nsxgen build            (if nsx_cloud_config.yml available in current folder)
./nsx-gen/bin/nsxgen -c nsx-pcf build (if init as used and nsx_cloud_config.yml file is under nsx-pcf)

## Use command line args
Build/Delete config can be overriden using command line args.
Refer to [command line usage docs][] for complete set of available args

Example:
```
# Sample init and build using command line args
# Initialize a default configuration with name `sabha` 
./nsx-gen/bin/nsxgen -i sabha init

# Folder named `sabha` created now with default config

# Run build overriding the default configs
./nsx-gen/bin/nsxgen -c sabha  -esg_name_1 sabha -esg_size_1 compact -esg_cli_user_1 admin -esg_cli_pass_1 'P1v0t4l!' -esg_certs_1 autogen -esg_certs_config_sysd_1 sys2.test.pez.pivotal.io -esg_certs_config_appd_1 apps3.test.pez.pivotal.io -esg_opsmgr_uplink_ip_1 10.13.92.171 -esg_go_router_uplink_ip_1 10.13.92.172 -esg_diego_brain_uplink_ip_1 10.13.92.173 -esg_tcp_router_uplink_ip_1 10.13.92.174 -vcenter_addr vcsa-01.test.pez.pivotal.io -vcenter_user administrator@vsphere.local -vcenter_pass 'testAdmin123' -vcenter_dc Datacenter -vcenter_ds vsanDatastore -vcenter_cluster Cluster1 -nsxmanager_addr 10.13.92.20 -nsxmanager_user admin -nsxmanager_pass 'testNsxAdmin123' -nsxmanager_tz testtrasnsportzone -nsxmanager_uplink_ip 10.13.92.170 -nsxmanager_uplink_port 'VM Network' -esg_gateway_1 10.13.92.1  $RUN_CMD


```

# List Logical switches and ESG
List local configuration as well as connect to the vcenter/nsx manager and show configured components
./nsx-gen/bin/nsxgen [-c path-to-config] list

Example:
./nsx-gen/bin/nsxgen list            (if nsx_cloud_config.yml available in current folder)
./nsx-gen/bin/nsxgen -c nsx-pcf list (if init was used earlier and nsx_cloud_config.yml file is under nsx-pcf)


# Destroy Logical switches and ESG
Destroy components wired using the specified configuration
./nsx-gen/bin/nsxgen [-c path-to-config] delete

Example:
./nsx-gen/bin/nsxgen delete            (if nsx_cloud_config.yml available in current folder)
./nsx-gen/bin/nsxgen -c nsx-pcf delete (if init was used earlier and nsx_cloud_config.yml file is under nsx-pcf)

[command line usage docs]: docs/usage.md
