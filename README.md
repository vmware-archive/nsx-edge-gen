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
Refer to [command line usage docs][]

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
