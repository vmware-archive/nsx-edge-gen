Complete args supported 
```
$ python ./nsx-gen/bin/nsxgen -h
usage: nsxgen [-h] [-i INIT] [-c NSX_CONF] [-esg_name_1 ESG_NAME_1]
              [-esg_size_1 ESG_SIZE_1] [-esg_gateway_1 ESG_GATEWAY_IP_1]
              [-esg_cli_user_1 ESG_CLI_USERNAME_1]
              [-esg_cli_pass_1 ESG_CLI_PASSWORD_1]
              [-esg_certs_1 ESG_CERTS_NAME_1]
              [-esg_certs_config_ou_1 ESG_CERTS_CONFIG_ORGUNIT_1]
              [-esg_certs_config_cc_1 ESG_CERTS_CONFIG_COUNTRY_1]
              [-esg_certs_config_sysd_1 ESG_CERTS_CONFIG_SYSTEMDOMAIN_1]
              [-esg_certs_config_appd_1 ESG_CERTS_CONFIG_APPDOMAIN_1]
              [-esg_opsmgr_uplink_ip_1 ESG_OPSMGR_UPLINK_IP_1]
              [-esg_opsmgr_inst_1 ESG_OPSMGR_INSTANCES_1]
              [-esg_opsmgr_off_1 ESG_OPSMGR_OFFSET_1]
              [-esg_go_router_uplink_ip_1 ESG_GO_ROUTER_UPLINK_IP_1]
              [-esg_go_router_inst_1 ESG_GO_ROUTER_INSTANCES_1]
              [-esg_go_router_off_1 ESG_GO_ROUTER_OFFSET_1]
              [-esg_diego_brain_uplink_ip_1 ESG_DIEGO_BRAIN_UPLINK_IP_1]
              [-esg_diego_brain_inst_1 ESG_DIEGO_BRAIN_INSTANCES_1]
              [-esg_diego_brain_off_1 ESG_DIEGO_BRAIN_OFFSET_1]
              [-esg_tcp_router_uplink_ip_1 ESG_TCP_ROUTER_UPLINK_IP_1]
              [-esg_tcp_router_inst_1 ESG_TCP_ROUTER_INSTANCES_1]
              [-esg_tcp_router_off_1 ESG_TCP_ROUTER_OFFSET_1]
              [-esg_name_2 ESG_NAME_2] [-esg_size_2 ESG_SIZE_2]
              [-esg_gateway_2 ESG_GATEWAY_IP_2]
              [-esg_cli_user_2 ESG_CLI_USERNAME_2]
              [-esg_cli_pass_2 ESG_CLI_PASSWORD_2]
              [-esg_certs_2 ESG_CERTS_NAME_2]
              [-esg_certs_config_ou_2 ESG_CERTS_CONFIG_ORGUNIT_2]
              [-esg_certs_config_cc_2 ESG_CERTS_CONFIG_COUNTRY_2]
              [-esg_certs_config_sysd_2 ESG_CERTS_CONFIG_SYSTEMDOMAIN_2]
              [-esg_certs_config_appd_2 ESG_CERTS_CONFIG_APPDOMAIN_2]
              [-esg_opsmgr_uplink_ip_2 ESG_OPSMGR_UPLINK_IP_2]
              [-esg_opsmgr_inst_2 ESG_OPSMGR_INSTANCES_2]
              [-esg_opsmgr_off_2 ESG_OPSMGR_OFFSET_2]
              [-esg_go_router_uplink_ip_2 ESG_GO_ROUTER_UPLINK_IP_2]
              [-esg_go_router_inst_2 ESG_GO_ROUTER_INSTANCES_2]
              [-esg_go_router_off_2 ESG_GO_ROUTER_OFFSET_2]
              [-esg_diego_brain_uplink_ip_2 ESG_DIEGO_BRAIN_UPLINK_IP_2]
              [-esg_diego_brain_inst_2 ESG_DIEGO_BRAIN_INSTANCES_2]
              [-esg_diego_brain_off_2 ESG_DIEGO_BRAIN_OFFSET_2]
              [-esg_tcp_router_uplink_ip_2 ESG_TCP_ROUTER_UPLINK_IP_2]
              [-esg_tcp_router_inst_2 ESG_TCP_ROUTER_INSTANCES_2]
              [-esg_tcp_router_off_2 ESG_TCP_ROUTER_OFFSET_2]
              [-vcenter_addr VCENTER_ADDRESS]
              [-vcenter_user VCENTER_ADMIN_USER]
              [-vcenter_pass VCENTER_ADMIN_PASSWD]
              [-vcenter_dc VCENTER_DATACENTER] [-vcenter_ds VCENTER_DATASTORE]
              [-vcenter_cluster VCENTER_CLUSTER] [-vcenter_fd VCENTER_FOLDER]
              [-vcenter_host VCENTER_HOST]
              [-nsxmanager_addr NSXMANAGER_ADDRESS]
              [-nsxmanager_user NSXMANAGER_ADMIN_USER]
              [-nsxmanager_pass NSXMANAGER_ADMIN_PASSWD]
              [-nsxmanager_tz NSXMANAGER_TRANSPORTZONE]
              [-nsxmanager_uplink_ip NSXMANAGER_UPLINK_IP]
              [-nsxmanager_uplink_port NSXMANAGER_UPLINK_PORT_SWITCH]
              [-ntp NTP_IPS] [-dns DNS_IPS] [-log SYSLOG_IPS] [-ldap LDAP_IPS]
              command

positional arguments:
  command               build: build a new Edge Service Gateway delete: delete
                        a Edge Service Gateway" list: return a list of all
                        Edge Service Gateways init: create a new nsx cloud
                        config file

optional arguments:
  -h, --help            show this help message and exit
  -i INIT, --init INIT  name for nsx config directory on init
  -c NSX_CONF, --nsx_conf NSX_CONF
                        nsx configuration yml file
  -esg_name_1 ESG_NAME_1, --esg_name_1 ESG_NAME_1
                        esg instance 1 name
  -esg_size_1 ESG_SIZE_1, --esg_size_1 ESG_SIZE_1
                        esg instance 1 size
  -esg_gateway_1 ESG_GATEWAY_IP_1, --esg_gateway_ip_1 ESG_GATEWAY_IP_1
                        esg instance 1 gateway ip
  -esg_cli_user_1 ESG_CLI_USERNAME_1, --esg_cli_username_1 ESG_CLI_USERNAME_1
                        esg instance 1 cli username
  -esg_cli_pass_1 ESG_CLI_PASSWORD_1, --esg_cli_password_1 ESG_CLI_PASSWORD_1
                        esg instance 1 cli password
  -esg_certs_1 ESG_CERTS_NAME_1, --esg_certs_name_1 ESG_CERTS_NAME_1
                        esg instance 1 certs name
  -esg_certs_config_ou_1 ESG_CERTS_CONFIG_ORGUNIT_1, --esg_certs_config_orgunit_1 ESG_CERTS_CONFIG_ORGUNIT_1
                        esg instance 1 certs config orgunit
  -esg_certs_config_cc_1 ESG_CERTS_CONFIG_COUNTRY_1, --esg_certs_config_country_1 ESG_CERTS_CONFIG_COUNTRY_1
                        esg instance 1 certs config country
  -esg_certs_config_sysd_1 ESG_CERTS_CONFIG_SYSTEMDOMAIN_1, --esg_certs_config_systemdomain_1 ESG_CERTS_CONFIG_SYSTEMDOMAIN_1
                        esg instance 1 certs config systemdomain
  -esg_certs_config_appd_1 ESG_CERTS_CONFIG_APPDOMAIN_1, --esg_certs_config_appdomain_1 ESG_CERTS_CONFIG_APPDOMAIN_1
                        esg instance 1 certs config appdomain
  -esg_opsmgr_uplink_ip_1 ESG_OPSMGR_UPLINK_IP_1, --esg_opsmgr_uplink_ip_1 ESG_OPSMGR_UPLINK_IP_1
                        esg instance 1 routed opsmgr uplink ip
  -esg_opsmgr_inst_1 ESG_OPSMGR_INSTANCES_1, --esg_opsmgr_instances_1 ESG_OPSMGR_INSTANCES_1
                        esg instance 1 routed opsmgr instances
  -esg_opsmgr_off_1 ESG_OPSMGR_OFFSET_1, --esg_opsmgr_offset_1 ESG_OPSMGR_OFFSET_1
                        esg instance 1 routed opsmgr offset
  -esg_go_router_uplink_ip_1 ESG_GO_ROUTER_UPLINK_IP_1, --esg_go_router_uplink_ip_1 ESG_GO_ROUTER_UPLINK_IP_1
                        esg instance 1 routed go_router uplink ip
  -esg_go_router_inst_1 ESG_GO_ROUTER_INSTANCES_1, --esg_go_router_instances_1 ESG_GO_ROUTER_INSTANCES_1
                        esg instance 1 routed go_router instances
  -esg_go_router_off_1 ESG_GO_ROUTER_OFFSET_1, --esg_go_router_offset_1 ESG_GO_ROUTER_OFFSET_1
                        esg instance 1 routed go_router offset
  -esg_diego_brain_uplink_ip_1 ESG_DIEGO_BRAIN_UPLINK_IP_1, --esg_diego_brain_uplink_ip_1 ESG_DIEGO_BRAIN_UPLINK_IP_1
                        esg instance 1 routed diego_brain uplink ip
  -esg_diego_brain_inst_1 ESG_DIEGO_BRAIN_INSTANCES_1, --esg_diego_brain_instances_1 ESG_DIEGO_BRAIN_INSTANCES_1
                        esg instance 1 routed diego_brain instances
  -esg_diego_brain_off_1 ESG_DIEGO_BRAIN_OFFSET_1, --esg_diego_brain_offset_1 ESG_DIEGO_BRAIN_OFFSET_1
                        esg instance 1 routed diego_brain offset
  -esg_tcp_router_uplink_ip_1 ESG_TCP_ROUTER_UPLINK_IP_1, --esg_tcp_router_uplink_ip_1 ESG_TCP_ROUTER_UPLINK_IP_1
                        esg instance 1 routed tcp_router uplink ip
  -esg_tcp_router_inst_1 ESG_TCP_ROUTER_INSTANCES_1, --esg_tcp_router_instances_1 ESG_TCP_ROUTER_INSTANCES_1
                        esg instance 1 routed tcp_router instances
  -esg_tcp_router_off_1 ESG_TCP_ROUTER_OFFSET_1, --esg_tcp_router_offset_1 ESG_TCP_ROUTER_OFFSET_1
                        esg instance 1 routed tcp_router offset
  -esg_name_2 ESG_NAME_2, --esg_name_2 ESG_NAME_2
                        esg instance 2 name
  -esg_size_2 ESG_SIZE_2, --esg_size_2 ESG_SIZE_2
                        esg instance 2 size
  -esg_gateway_2 ESG_GATEWAY_IP_2, --esg_gateway_ip_2 ESG_GATEWAY_IP_2
                        esg instance 2 gateway ip
  -esg_cli_user_2 ESG_CLI_USERNAME_2, --esg_cli_username_2 ESG_CLI_USERNAME_2
                        esg instance 2 cli username
  -esg_cli_pass_2 ESG_CLI_PASSWORD_2, --esg_cli_password_2 ESG_CLI_PASSWORD_2
                        esg instance 2 cli password
  -esg_certs_2 ESG_CERTS_NAME_2, --esg_certs_name_2 ESG_CERTS_NAME_2
                        esg instance 2 certs name
  -esg_certs_config_ou_2 ESG_CERTS_CONFIG_ORGUNIT_2, --esg_certs_config_orgunit_2 ESG_CERTS_CONFIG_ORGUNIT_2
                        esg instance 2 certs config orgunit
  -esg_certs_config_cc_2 ESG_CERTS_CONFIG_COUNTRY_2, --esg_certs_config_country_2 ESG_CERTS_CONFIG_COUNTRY_2
                        esg instance 2 certs config country
  -esg_certs_config_sysd_2 ESG_CERTS_CONFIG_SYSTEMDOMAIN_2, --esg_certs_config_systemdomain_2 ESG_CERTS_CONFIG_SYSTEMDOMAIN_2
                        esg instance 2 certs config systemdomain
  -esg_certs_config_appd_2 ESG_CERTS_CONFIG_APPDOMAIN_2, --esg_certs_config_appdomain_2 ESG_CERTS_CONFIG_APPDOMAIN_2
                        esg instance 2 certs config appdomain
  -esg_opsmgr_uplink_ip_2 ESG_OPSMGR_UPLINK_IP_2, --esg_opsmgr_uplink_ip_2 ESG_OPSMGR_UPLINK_IP_2
                        esg instance 2 routed opsmgr uplink ip
  -esg_opsmgr_inst_2 ESG_OPSMGR_INSTANCES_2, --esg_opsmgr_instances_2 ESG_OPSMGR_INSTANCES_2
                        esg instance 2 routed opsmgr instances
  -esg_opsmgr_off_2 ESG_OPSMGR_OFFSET_2, --esg_opsmgr_offset_2 ESG_OPSMGR_OFFSET_2
                        esg instance 2 routed opsmgr offset
  -esg_go_router_uplink_ip_2 ESG_GO_ROUTER_UPLINK_IP_2, --esg_go_router_uplink_ip_2 ESG_GO_ROUTER_UPLINK_IP_2
                        esg instance 2 routed go_router uplink ip
  -esg_go_router_inst_2 ESG_GO_ROUTER_INSTANCES_2, --esg_go_router_instances_2 ESG_GO_ROUTER_INSTANCES_2
                        esg instance 2 routed go_router instances
  -esg_go_router_off_2 ESG_GO_ROUTER_OFFSET_2, --esg_go_router_offset_2 ESG_GO_ROUTER_OFFSET_2
                        esg instance 2 routed go_router offset
  -esg_diego_brain_uplink_ip_2 ESG_DIEGO_BRAIN_UPLINK_IP_2, --esg_diego_brain_uplink_ip_2 ESG_DIEGO_BRAIN_UPLINK_IP_2
                        esg instance 2 routed diego_brain uplink ip
  -esg_diego_brain_inst_2 ESG_DIEGO_BRAIN_INSTANCES_2, --esg_diego_brain_instances_2 ESG_DIEGO_BRAIN_INSTANCES_2
                        esg instance 2 routed diego_brain instances
  -esg_diego_brain_off_2 ESG_DIEGO_BRAIN_OFFSET_2, --esg_diego_brain_offset_2 ESG_DIEGO_BRAIN_OFFSET_2
                        esg instance 2 routed diego_brain offset
  -esg_tcp_router_uplink_ip_2 ESG_TCP_ROUTER_UPLINK_IP_2, --esg_tcp_router_uplink_ip_2 ESG_TCP_ROUTER_UPLINK_IP_2
                        esg instance 2 routed tcp_router uplink ip
  -esg_tcp_router_inst_2 ESG_TCP_ROUTER_INSTANCES_2, --esg_tcp_router_instances_2 ESG_TCP_ROUTER_INSTANCES_2
                        esg instance 2 routed tcp_router instances
  -esg_tcp_router_off_2 ESG_TCP_ROUTER_OFFSET_2, --esg_tcp_router_offset_2 ESG_TCP_ROUTER_OFFSET_2
                        esg instance 2 routed tcp_router offset
  -vcenter_addr VCENTER_ADDRESS, --vcenter_address VCENTER_ADDRESS
                        vcenter address
  -vcenter_user VCENTER_ADMIN_USER, --vcenter_admin_user VCENTER_ADMIN_USER
                        vcenter admin user
  -vcenter_pass VCENTER_ADMIN_PASSWD, --vcenter_admin_passwd VCENTER_ADMIN_PASSWD
                        vcenter admin passwd
  -vcenter_dc VCENTER_DATACENTER, --vcenter_datacenter VCENTER_DATACENTER
                        vcenter datacenter
  -vcenter_ds VCENTER_DATASTORE, --vcenter_datastore VCENTER_DATASTORE
                        vcenter datastore
  -vcenter_cluster VCENTER_CLUSTER, --vcenter_cluster VCENTER_CLUSTER
                        vcenter cluster
  -vcenter_fd VCENTER_FOLDER, --vcenter_folder VCENTER_FOLDER
                        vcenter folder
  -vcenter_host VCENTER_HOST, --vcenter_host VCENTER_HOST
                        vcenter host
  -nsxmanager_addr NSXMANAGER_ADDRESS, --nsxmanager_address NSXMANAGER_ADDRESS
                        nsxmanager address
  -nsxmanager_user NSXMANAGER_ADMIN_USER, --nsxmanager_admin_user NSXMANAGER_ADMIN_USER
                        nsxmanager admin user
  -nsxmanager_pass NSXMANAGER_ADMIN_PASSWD, --nsxmanager_admin_passwd NSXMANAGER_ADMIN_PASSWD
                        nsxmanager admin passwd
  -nsxmanager_tz NSXMANAGER_TRANSPORTZONE, --nsxmanager_transportzone NSXMANAGER_TRANSPORTZONE
                        nsxmanager transportzone
  -nsxmanager_uplink_ip NSXMANAGER_UPLINK_IP, --nsxmanager_uplink_ip NSXMANAGER_UPLINK_IP
                        nsxmanager uplink ip
  -nsxmanager_uplink_port NSXMANAGER_UPLINK_PORT_SWITCH, --nsxmanager_uplink_port_switch NSXMANAGER_UPLINK_PORT_SWITCH
                        nsxmanager uplink port switch
  -ntp NTP_IPS, --ntp_ips NTP_IPS
                        default ntp ips
  -dns DNS_IPS, --dns_ips DNS_IPS
                        default dns ips
  -log SYSLOG_IPS, --syslog_ips SYSLOG_IPS
                        default syslog ips
  -ldap LDAP_IPS, --ldap_ips LDAP_IPS
                        default ldap ips
```
