Complete args supported 
```
$ python ./nsx-gen/bin/nsxgen -h
usage: nsxgen [-h] [-i INIT] [-c NSX_CONF]
              [-isozone_switch_name_1 ISOZONE_SWITCH_NAME_1]
              [-isozone_switch_cidr_1 ISOZONE_SWITCH_CIDR_1]
              [-isozone_switch_name_2 ISOZONE_SWITCH_NAME_2]
              [-isozone_switch_cidr_2 ISOZONE_SWITCH_CIDR_2]
              [-isozone_switch_name_3 ISOZONE_SWITCH_NAME_3]
              [-isozone_switch_cidr_3 ISOZONE_SWITCH_CIDR_3]
              [-isozone_switch_name_4 ISOZONE_SWITCH_NAME_4]
              [-isozone_switch_cidr_4 ISOZONE_SWITCH_CIDR_4]
              [-isozone_switch_name_5 ISOZONE_SWITCH_NAME_5]
              [-isozone_switch_cidr_5 ISOZONE_SWITCH_CIDR_5]
              [-esg_name_1 ESG_NAME_1] [-esg_size_1 ESG_SIZE_1]
              [-esg_gateway_1 ESG_GATEWAY_IP_1]
              [-esg_ospf_password_1 ESG_OSPF_PASSWORD_1]
              [-esg_cli_user_1 ESG_CLI_USERNAME_1]
              [-esg_cli_pass_1 ESG_CLI_PASSWORD_1]
              [-esg_certs_1 ESG_CERTS_NAME_1]
              [-esg_certs_config_ou_1 ESG_CERTS_CONFIG_ORGUNIT_1]
              [-esg_certs_config_cc_1 ESG_CERTS_CONFIG_COUNTRY_1]
              [-esg_certs_config_sysd_1 ESG_CERTS_CONFIG_SYSTEMDOMAIN_1]
              [-esg_certs_config_appd_1 ESG_CERTS_CONFIG_APPDOMAIN_1]
              [-esg_opsmgr_uplink_ip_1 ESG_OPSMGR_UPLINK_IP_1]
              [-esg_opsmgr_switch_1 ESG_OPSMGR_SWITCH_1]
              [-esg_opsmgr_inst_1 ESG_OPSMGR_INSTANCES_1]
              [-esg_opsmgr_off_1 ESG_OPSMGR_OFFSET_1]
              [-esg_go_router_uplink_ip_1 ESG_GO_ROUTER_UPLINK_IP_1]
              [-esg_go_router_switch_1 ESG_GO_ROUTER_SWITCH_1]
              [-esg_go_router_inst_1 ESG_GO_ROUTER_INSTANCES_1]
              [-esg_go_router_off_1 ESG_GO_ROUTER_OFFSET_1]
              [-esg_diego_brain_uplink_ip_1 ESG_DIEGO_BRAIN_UPLINK_IP_1]
              [-esg_diego_brain_switch_1 ESG_DIEGO_BRAIN_SWITCH_1]
              [-esg_diego_brain_inst_1 ESG_DIEGO_BRAIN_INSTANCES_1]
              [-esg_diego_brain_off_1 ESG_DIEGO_BRAIN_OFFSET_1]
              [-esg_tcp_router_uplink_ip_1 ESG_TCP_ROUTER_UPLINK_IP_1]
              [-esg_tcp_router_switch_1 ESG_TCP_ROUTER_SWITCH_1]
              [-esg_tcp_router_inst_1 ESG_TCP_ROUTER_INSTANCES_1]
              [-esg_tcp_router_off_1 ESG_TCP_ROUTER_OFFSET_1]
              [-esg_mysql_ert_uplink_ip_1 ESG_MYSQL_ERT_UPLINK_IP_1]
              [-esg_mysql_ert_switch_1 ESG_MYSQL_ERT_SWITCH_1]
              [-esg_mysql_ert_inst_1 ESG_MYSQL_ERT_INSTANCES_1]
              [-esg_mysql_ert_off_1 ESG_MYSQL_ERT_OFFSET_1]
              [-esg_mysql_tile_uplink_ip_1 ESG_MYSQL_TILE_UPLINK_IP_1]
              [-esg_mysql_tile_switch_1 ESG_MYSQL_TILE_SWITCH_1]
              [-esg_mysql_tile_inst_1 ESG_MYSQL_TILE_INSTANCES_1]
              [-esg_mysql_tile_off_1 ESG_MYSQL_TILE_OFFSET_1]
              [-esg_rabbitmq_tile_uplink_ip_1 ESG_RABBITMQ_TILE_UPLINK_IP_1]
              [-esg_rabbitmq_tile_switch_1 ESG_RABBITMQ_TILE_SWITCH_1]
              [-esg_rabbitmq_tile_inst_1 ESG_RABBITMQ_TILE_INSTANCES_1]
              [-esg_rabbitmq_tile_off_1 ESG_RABBITMQ_TILE_OFFSET_1]
              [-esg_go_router_isozone_1_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_1_UPLINK_IP_1]
              [-esg_go_router_isozone_1_switch_1 ESG_GO_ROUTER_ISOZONE_1_SWITCH_1]
              [-esg_go_router_isozone_1_inst_1 ESG_GO_ROUTER_ISOZONE_1_INSTANCES_1]
              [-esg_go_router_isozone_1_off_1 ESG_GO_ROUTER_ISOZONE_1_OFFSET_1]
              [-esg_tcp_router_isozone_1_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_1_UPLINK_IP_1]
              [-esg_tcp_router_isozone_1_switch_1 ESG_TCP_ROUTER_ISOZONE_1_SWITCH_1]
              [-esg_tcp_router_isozone_1_inst_1 ESG_TCP_ROUTER_ISOZONE_1_INSTANCES_1]
              [-esg_tcp_router_isozone_1_off_1 ESG_TCP_ROUTER_ISOZONE_1_OFFSET_1]
              [-esg_go_router_isozone_2_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_2_UPLINK_IP_1]
              [-esg_go_router_isozone_2_switch_1 ESG_GO_ROUTER_ISOZONE_2_SWITCH_1]
              [-esg_go_router_isozone_2_inst_1 ESG_GO_ROUTER_ISOZONE_2_INSTANCES_1]
              [-esg_go_router_isozone_2_off_1 ESG_GO_ROUTER_ISOZONE_2_OFFSET_1]
              [-esg_tcp_router_isozone_2_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_2_UPLINK_IP_1]
              [-esg_tcp_router_isozone_2_switch_1 ESG_TCP_ROUTER_ISOZONE_2_SWITCH_1]
              [-esg_tcp_router_isozone_2_inst_1 ESG_TCP_ROUTER_ISOZONE_2_INSTANCES_1]
              [-esg_tcp_router_isozone_2_off_1 ESG_TCP_ROUTER_ISOZONE_2_OFFSET_1]
              [-esg_go_router_isozone_3_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_3_UPLINK_IP_1]
              [-esg_go_router_isozone_3_switch_1 ESG_GO_ROUTER_ISOZONE_3_SWITCH_1]
              [-esg_go_router_isozone_3_inst_1 ESG_GO_ROUTER_ISOZONE_3_INSTANCES_1]
              [-esg_go_router_isozone_3_off_1 ESG_GO_ROUTER_ISOZONE_3_OFFSET_1]
              [-esg_tcp_router_isozone_3_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_3_UPLINK_IP_1]
              [-esg_tcp_router_isozone_3_switch_1 ESG_TCP_ROUTER_ISOZONE_3_SWITCH_1]
              [-esg_tcp_router_isozone_3_inst_1 ESG_TCP_ROUTER_ISOZONE_3_INSTANCES_1]
              [-esg_tcp_router_isozone_3_off_1 ESG_TCP_ROUTER_ISOZONE_3_OFFSET_1]
              [-esg_go_router_isozone_4_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_4_UPLINK_IP_1]
              [-esg_go_router_isozone_4_switch_1 ESG_GO_ROUTER_ISOZONE_4_SWITCH_1]
              [-esg_go_router_isozone_4_inst_1 ESG_GO_ROUTER_ISOZONE_4_INSTANCES_1]
              [-esg_go_router_isozone_4_off_1 ESG_GO_ROUTER_ISOZONE_4_OFFSET_1]
              [-esg_tcp_router_isozone_4_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_4_UPLINK_IP_1]
              [-esg_tcp_router_isozone_4_switch_1 ESG_TCP_ROUTER_ISOZONE_4_SWITCH_1]
              [-esg_tcp_router_isozone_4_inst_1 ESG_TCP_ROUTER_ISOZONE_4_INSTANCES_1]
              [-esg_tcp_router_isozone_4_off_1 ESG_TCP_ROUTER_ISOZONE_4_OFFSET_1]
              [-esg_go_router_isozone_5_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_5_UPLINK_IP_1]
              [-esg_go_router_isozone_5_switch_1 ESG_GO_ROUTER_ISOZONE_5_SWITCH_1]
              [-esg_go_router_isozone_5_inst_1 ESG_GO_ROUTER_ISOZONE_5_INSTANCES_1]
              [-esg_go_router_isozone_5_off_1 ESG_GO_ROUTER_ISOZONE_5_OFFSET_1]
              [-esg_tcp_router_isozone_5_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_5_UPLINK_IP_1]
              [-esg_tcp_router_isozone_5_switch_1 ESG_TCP_ROUTER_ISOZONE_5_SWITCH_1]
              [-esg_tcp_router_isozone_5_inst_1 ESG_TCP_ROUTER_ISOZONE_5_INSTANCES_1]
              [-esg_tcp_router_isozone_5_off_1 ESG_TCP_ROUTER_ISOZONE_5_OFFSET_1]
              [-esg_name_2 ESG_NAME_2] [-esg_size_2 ESG_SIZE_2]
              [-esg_gateway_2 ESG_GATEWAY_IP_2]
              [-esg_ospf_password_2 ESG_OSPF_PASSWORD_2]
              [-esg_cli_user_2 ESG_CLI_USERNAME_2]
              [-esg_cli_pass_2 ESG_CLI_PASSWORD_2]
              [-esg_certs_2 ESG_CERTS_NAME_2]
              [-esg_certs_config_ou_2 ESG_CERTS_CONFIG_ORGUNIT_2]
              [-esg_certs_config_cc_2 ESG_CERTS_CONFIG_COUNTRY_2]
              [-esg_certs_config_sysd_2 ESG_CERTS_CONFIG_SYSTEMDOMAIN_2]
              [-esg_certs_config_appd_2 ESG_CERTS_CONFIG_APPDOMAIN_2]
              [-esg_opsmgr_uplink_ip_2 ESG_OPSMGR_UPLINK_IP_2]
              [-esg_opsmgr_switch_2 ESG_OPSMGR_SWITCH_2]
              [-esg_opsmgr_inst_2 ESG_OPSMGR_INSTANCES_2]
              [-esg_opsmgr_off_2 ESG_OPSMGR_OFFSET_2]
              [-esg_go_router_uplink_ip_2 ESG_GO_ROUTER_UPLINK_IP_2]
              [-esg_go_router_switch_2 ESG_GO_ROUTER_SWITCH_2]
              [-esg_go_router_inst_2 ESG_GO_ROUTER_INSTANCES_2]
              [-esg_go_router_off_2 ESG_GO_ROUTER_OFFSET_2]
              [-esg_diego_brain_uplink_ip_2 ESG_DIEGO_BRAIN_UPLINK_IP_2]
              [-esg_diego_brain_switch_2 ESG_DIEGO_BRAIN_SWITCH_2]
              [-esg_diego_brain_inst_2 ESG_DIEGO_BRAIN_INSTANCES_2]
              [-esg_diego_brain_off_2 ESG_DIEGO_BRAIN_OFFSET_2]
              [-esg_tcp_router_uplink_ip_2 ESG_TCP_ROUTER_UPLINK_IP_2]
              [-esg_tcp_router_switch_2 ESG_TCP_ROUTER_SWITCH_2]
              [-esg_tcp_router_inst_2 ESG_TCP_ROUTER_INSTANCES_2]
              [-esg_tcp_router_off_2 ESG_TCP_ROUTER_OFFSET_2]
              [-esg_mysql_ert_uplink_ip_2 ESG_MYSQL_ERT_UPLINK_IP_2]
              [-esg_mysql_ert_switch_2 ESG_MYSQL_ERT_SWITCH_2]
              [-esg_mysql_ert_inst_2 ESG_MYSQL_ERT_INSTANCES_2]
              [-esg_mysql_ert_off_2 ESG_MYSQL_ERT_OFFSET_2]
              [-esg_mysql_tile_uplink_ip_2 ESG_MYSQL_TILE_UPLINK_IP_2]
              [-esg_mysql_tile_switch_2 ESG_MYSQL_TILE_SWITCH_2]
              [-esg_mysql_tile_inst_2 ESG_MYSQL_TILE_INSTANCES_2]
              [-esg_mysql_tile_off_2 ESG_MYSQL_TILE_OFFSET_2]
              [-esg_rabbitmq_tile_uplink_ip_2 ESG_RABBITMQ_TILE_UPLINK_IP_2]
              [-esg_rabbitmq_tile_switch_2 ESG_RABBITMQ_TILE_SWITCH_2]
              [-esg_rabbitmq_tile_inst_2 ESG_RABBITMQ_TILE_INSTANCES_2]
              [-esg_rabbitmq_tile_off_2 ESG_RABBITMQ_TILE_OFFSET_2]
              [-esg_go_router_isozone_1_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_1_UPLINK_IP_2]
              [-esg_go_router_isozone_1_switch_2 ESG_GO_ROUTER_ISOZONE_1_SWITCH_2]
              [-esg_go_router_isozone_1_inst_2 ESG_GO_ROUTER_ISOZONE_1_INSTANCES_2]
              [-esg_go_router_isozone_1_off_2 ESG_GO_ROUTER_ISOZONE_1_OFFSET_2]
              [-esg_tcp_router_isozone_1_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_1_UPLINK_IP_2]
              [-esg_tcp_router_isozone_1_switch_2 ESG_TCP_ROUTER_ISOZONE_1_SWITCH_2]
              [-esg_tcp_router_isozone_1_inst_2 ESG_TCP_ROUTER_ISOZONE_1_INSTANCES_2]
              [-esg_tcp_router_isozone_1_off_2 ESG_TCP_ROUTER_ISOZONE_1_OFFSET_2]
              [-esg_go_router_isozone_2_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_2_UPLINK_IP_2]
              [-esg_go_router_isozone_2_switch_2 ESG_GO_ROUTER_ISOZONE_2_SWITCH_2]
              [-esg_go_router_isozone_2_inst_2 ESG_GO_ROUTER_ISOZONE_2_INSTANCES_2]
              [-esg_go_router_isozone_2_off_2 ESG_GO_ROUTER_ISOZONE_2_OFFSET_2]
              [-esg_tcp_router_isozone_2_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_2_UPLINK_IP_2]
              [-esg_tcp_router_isozone_2_switch_2 ESG_TCP_ROUTER_ISOZONE_2_SWITCH_2]
              [-esg_tcp_router_isozone_2_inst_2 ESG_TCP_ROUTER_ISOZONE_2_INSTANCES_2]
              [-esg_tcp_router_isozone_2_off_2 ESG_TCP_ROUTER_ISOZONE_2_OFFSET_2]
              [-esg_go_router_isozone_3_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_3_UPLINK_IP_2]
              [-esg_go_router_isozone_3_switch_2 ESG_GO_ROUTER_ISOZONE_3_SWITCH_2]
              [-esg_go_router_isozone_3_inst_2 ESG_GO_ROUTER_ISOZONE_3_INSTANCES_2]
              [-esg_go_router_isozone_3_off_2 ESG_GO_ROUTER_ISOZONE_3_OFFSET_2]
              [-esg_tcp_router_isozone_3_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_3_UPLINK_IP_2]
              [-esg_tcp_router_isozone_3_switch_2 ESG_TCP_ROUTER_ISOZONE_3_SWITCH_2]
              [-esg_tcp_router_isozone_3_inst_2 ESG_TCP_ROUTER_ISOZONE_3_INSTANCES_2]
              [-esg_tcp_router_isozone_3_off_2 ESG_TCP_ROUTER_ISOZONE_3_OFFSET_2]
              [-esg_go_router_isozone_4_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_4_UPLINK_IP_2]
              [-esg_go_router_isozone_4_switch_2 ESG_GO_ROUTER_ISOZONE_4_SWITCH_2]
              [-esg_go_router_isozone_4_inst_2 ESG_GO_ROUTER_ISOZONE_4_INSTANCES_2]
              [-esg_go_router_isozone_4_off_2 ESG_GO_ROUTER_ISOZONE_4_OFFSET_2]
              [-esg_tcp_router_isozone_4_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_4_UPLINK_IP_2]
              [-esg_tcp_router_isozone_4_switch_2 ESG_TCP_ROUTER_ISOZONE_4_SWITCH_2]
              [-esg_tcp_router_isozone_4_inst_2 ESG_TCP_ROUTER_ISOZONE_4_INSTANCES_2]
              [-esg_tcp_router_isozone_4_off_2 ESG_TCP_ROUTER_ISOZONE_4_OFFSET_2]
              [-esg_go_router_isozone_5_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_5_UPLINK_IP_2]
              [-esg_go_router_isozone_5_switch_2 ESG_GO_ROUTER_ISOZONE_5_SWITCH_2]
              [-esg_go_router_isozone_5_inst_2 ESG_GO_ROUTER_ISOZONE_5_INSTANCES_2]
              [-esg_go_router_isozone_5_off_2 ESG_GO_ROUTER_ISOZONE_5_OFFSET_2]
              [-esg_tcp_router_isozone_5_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_5_UPLINK_IP_2]
              [-esg_tcp_router_isozone_5_switch_2 ESG_TCP_ROUTER_ISOZONE_5_SWITCH_2]
              [-esg_tcp_router_isozone_5_inst_2 ESG_TCP_ROUTER_ISOZONE_5_INSTANCES_2]
              [-esg_tcp_router_isozone_5_off_2 ESG_TCP_ROUTER_ISOZONE_5_OFFSET_2]
              [-nsxmanager_addr NSXMANAGER_ADDRESS]
              [-nsxmanager_en_dlr NSXMANAGER_ENABLE_DLR]
              [-nsxmanager_user NSXMANAGER_ADMIN_USER]
              [-nsxmanager_pass NSXMANAGER_ADMIN_PASSWD]
              [-nsxmanager_tz NSXMANAGER_TRANSPORTZONE]
              [-nsxmanager_dportgroup NSXMANAGER_DISTRIBUTED_PORTGROUP]
              [-nsxmanager_uplink_ip NSXMANAGER_UPLINK_IP]
              [-nsxmanager_uplink_port NSXMANAGER_UPLINK_PORT_SWITCH]
              [-nsxmanager_sr_name NSXMANAGER_STATIC_ROUTE_NAME]
              [-nsxmanager_sr_subnet NSXMANAGER_STATIC_ROUTE_SUBNET]
              [-nsxmanager_sr_gateway NSXMANAGER_STATIC_ROUTE_GATEWAY]
              [-nsxmanager_sr_hop NSXMANAGER_STATIC_ROUTE_HOP] [-ntp NTP_IPS]
              [-dns DNS_IPS] [-log SYSLOG_IPS] [-ldap LDAP_IPS]
              [-vcenter_addr VCENTER_ADDRESS]
              [-vcenter_user VCENTER_ADMIN_USER]
              [-vcenter_pass VCENTER_ADMIN_PASSWD]
              [-vcenter_dc VCENTER_DATACENTER] [-vcenter_ds VCENTER_DATASTORE]
              [-vcenter_cluster VCENTER_CLUSTER] [-vcenter_fd VCENTER_FOLDER]
              [-vcenter_host VCENTER_HOST]
              command

positional arguments:
  command               build:   build a new Edge Service Gateway
                        delete:  delete a Edge Service Gateway
                        list:    return a list of all Edge Service Gateways
                        init:    create a new nsx cloud config file

optional arguments:
  -h, --help            show this help message and exit
  -i INIT, --init INIT  name for nsx config directory on init
  -c NSX_CONF, --nsx_conf NSX_CONF
                        nsx configuration yml file
  -isozone_switch_name_1 ISOZONE_SWITCH_NAME_1, --isozone_switch_name_1 ISOZONE_SWITCH_NAME_1
                        isozone_switch instance 1 name
  -isozone_switch_cidr_1 ISOZONE_SWITCH_CIDR_1, --isozone_switch_cidr_1 ISOZONE_SWITCH_CIDR_1
                        isozone_switch instance 1 cidr
  -isozone_switch_name_2 ISOZONE_SWITCH_NAME_2, --isozone_switch_name_2 ISOZONE_SWITCH_NAME_2
                        isozone_switch instance 2 name
  -isozone_switch_cidr_2 ISOZONE_SWITCH_CIDR_2, --isozone_switch_cidr_2 ISOZONE_SWITCH_CIDR_2
                        isozone_switch instance 2 cidr
  -isozone_switch_name_3 ISOZONE_SWITCH_NAME_3, --isozone_switch_name_3 ISOZONE_SWITCH_NAME_3
                        isozone_switch instance 3 name
  -isozone_switch_cidr_3 ISOZONE_SWITCH_CIDR_3, --isozone_switch_cidr_3 ISOZONE_SWITCH_CIDR_3
                        isozone_switch instance 3 cidr
  -isozone_switch_name_4 ISOZONE_SWITCH_NAME_4, --isozone_switch_name_4 ISOZONE_SWITCH_NAME_4
                        isozone_switch instance 4 name
  -isozone_switch_cidr_4 ISOZONE_SWITCH_CIDR_4, --isozone_switch_cidr_4 ISOZONE_SWITCH_CIDR_4
                        isozone_switch instance 4 cidr
  -isozone_switch_name_5 ISOZONE_SWITCH_NAME_5, --isozone_switch_name_5 ISOZONE_SWITCH_NAME_5
                        isozone_switch instance 5 name
  -isozone_switch_cidr_5 ISOZONE_SWITCH_CIDR_5, --isozone_switch_cidr_5 ISOZONE_SWITCH_CIDR_5
                        isozone_switch instance 5 cidr
  -esg_name_1 ESG_NAME_1, --esg_name_1 ESG_NAME_1
                        esg instance 1 name
  -esg_size_1 ESG_SIZE_1, --esg_size_1 ESG_SIZE_1
                        esg instance 1 size
  -esg_gateway_1 ESG_GATEWAY_IP_1, --esg_gateway_ip_1 ESG_GATEWAY_IP_1
                        esg instance 1 gateway ip
  -esg_ospf_password_1 ESG_OSPF_PASSWORD_1, --esg_ospf_password_1 ESG_OSPF_PASSWORD_1
                        esg instance 1 ospf password
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
  -esg_opsmgr_switch_1 ESG_OPSMGR_SWITCH_1, --esg_opsmgr_switch_1 ESG_OPSMGR_SWITCH_1
                        esg instance 1 routed opsmgr switch
  -esg_opsmgr_inst_1 ESG_OPSMGR_INSTANCES_1, --esg_opsmgr_instances_1 ESG_OPSMGR_INSTANCES_1
                        esg instance 1 routed opsmgr instances
  -esg_opsmgr_off_1 ESG_OPSMGR_OFFSET_1, --esg_opsmgr_offset_1 ESG_OPSMGR_OFFSET_1
                        esg instance 1 routed opsmgr offset
  -esg_go_router_uplink_ip_1 ESG_GO_ROUTER_UPLINK_IP_1, --esg_go_router_uplink_ip_1 ESG_GO_ROUTER_UPLINK_IP_1
                        esg instance 1 routed go_router uplink ip
  -esg_go_router_switch_1 ESG_GO_ROUTER_SWITCH_1, --esg_go_router_switch_1 ESG_GO_ROUTER_SWITCH_1
                        esg instance 1 routed go_router switch
  -esg_go_router_inst_1 ESG_GO_ROUTER_INSTANCES_1, --esg_go_router_instances_1 ESG_GO_ROUTER_INSTANCES_1
                        esg instance 1 routed go_router instances
  -esg_go_router_off_1 ESG_GO_ROUTER_OFFSET_1, --esg_go_router_offset_1 ESG_GO_ROUTER_OFFSET_1
                        esg instance 1 routed go_router offset
  -esg_diego_brain_uplink_ip_1 ESG_DIEGO_BRAIN_UPLINK_IP_1, --esg_diego_brain_uplink_ip_1 ESG_DIEGO_BRAIN_UPLINK_IP_1
                        esg instance 1 routed diego_brain uplink ip
  -esg_diego_brain_switch_1 ESG_DIEGO_BRAIN_SWITCH_1, --esg_diego_brain_switch_1 ESG_DIEGO_BRAIN_SWITCH_1
                        esg instance 1 routed diego_brain switch
  -esg_diego_brain_inst_1 ESG_DIEGO_BRAIN_INSTANCES_1, --esg_diego_brain_instances_1 ESG_DIEGO_BRAIN_INSTANCES_1
                        esg instance 1 routed diego_brain instances
  -esg_diego_brain_off_1 ESG_DIEGO_BRAIN_OFFSET_1, --esg_diego_brain_offset_1 ESG_DIEGO_BRAIN_OFFSET_1
                        esg instance 1 routed diego_brain offset
  -esg_tcp_router_uplink_ip_1 ESG_TCP_ROUTER_UPLINK_IP_1, --esg_tcp_router_uplink_ip_1 ESG_TCP_ROUTER_UPLINK_IP_1
                        esg instance 1 routed tcp_router uplink ip
  -esg_tcp_router_switch_1 ESG_TCP_ROUTER_SWITCH_1, --esg_tcp_router_switch_1 ESG_TCP_ROUTER_SWITCH_1
                        esg instance 1 routed tcp_router switch
  -esg_tcp_router_inst_1 ESG_TCP_ROUTER_INSTANCES_1, --esg_tcp_router_instances_1 ESG_TCP_ROUTER_INSTANCES_1
                        esg instance 1 routed tcp_router instances
  -esg_tcp_router_off_1 ESG_TCP_ROUTER_OFFSET_1, --esg_tcp_router_offset_1 ESG_TCP_ROUTER_OFFSET_1
                        esg instance 1 routed tcp_router offset
  -esg_mysql_ert_uplink_ip_1 ESG_MYSQL_ERT_UPLINK_IP_1, --esg_mysql_ert_uplink_ip_1 ESG_MYSQL_ERT_UPLINK_IP_1
                        esg instance 1 routed mysql_ert uplink ip
  -esg_mysql_ert_switch_1 ESG_MYSQL_ERT_SWITCH_1, --esg_mysql_ert_switch_1 ESG_MYSQL_ERT_SWITCH_1
                        esg instance 1 routed mysql_ert switch
  -esg_mysql_ert_inst_1 ESG_MYSQL_ERT_INSTANCES_1, --esg_mysql_ert_instances_1 ESG_MYSQL_ERT_INSTANCES_1
                        esg instance 1 routed mysql_ert instances
  -esg_mysql_ert_off_1 ESG_MYSQL_ERT_OFFSET_1, --esg_mysql_ert_offset_1 ESG_MYSQL_ERT_OFFSET_1
                        esg instance 1 routed mysql_ert offset
  -esg_mysql_tile_uplink_ip_1 ESG_MYSQL_TILE_UPLINK_IP_1, --esg_mysql_tile_uplink_ip_1 ESG_MYSQL_TILE_UPLINK_IP_1
                        esg instance 1 routed mysql_tile uplink ip
  -esg_mysql_tile_switch_1 ESG_MYSQL_TILE_SWITCH_1, --esg_mysql_tile_switch_1 ESG_MYSQL_TILE_SWITCH_1
                        esg instance 1 routed mysql_tile switch
  -esg_mysql_tile_inst_1 ESG_MYSQL_TILE_INSTANCES_1, --esg_mysql_tile_instances_1 ESG_MYSQL_TILE_INSTANCES_1
                        esg instance 1 routed mysql_tile instances
  -esg_mysql_tile_off_1 ESG_MYSQL_TILE_OFFSET_1, --esg_mysql_tile_offset_1 ESG_MYSQL_TILE_OFFSET_1
                        esg instance 1 routed mysql_tile offset
  -esg_rabbitmq_tile_uplink_ip_1 ESG_RABBITMQ_TILE_UPLINK_IP_1, --esg_rabbitmq_tile_uplink_ip_1 ESG_RABBITMQ_TILE_UPLINK_IP_1
                        esg instance 1 routed rabbitmq_tile uplink ip
  -esg_rabbitmq_tile_switch_1 ESG_RABBITMQ_TILE_SWITCH_1, --esg_rabbitmq_tile_switch_1 ESG_RABBITMQ_TILE_SWITCH_1
                        esg instance 1 routed rabbitmq_tile switch
  -esg_rabbitmq_tile_inst_1 ESG_RABBITMQ_TILE_INSTANCES_1, --esg_rabbitmq_tile_instances_1 ESG_RABBITMQ_TILE_INSTANCES_1
                        esg instance 1 routed rabbitmq_tile instances
  -esg_rabbitmq_tile_off_1 ESG_RABBITMQ_TILE_OFFSET_1, --esg_rabbitmq_tile_offset_1 ESG_RABBITMQ_TILE_OFFSET_1
                        esg instance 1 routed rabbitmq_tile offset
  -esg_go_router_isozone_1_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_1_UPLINK_IP_1, --esg_go_router_isozone_1_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_1_UPLINK_IP_1
                        esg instance 1 routed go_router_isozone_1 uplink ip
  -esg_go_router_isozone_1_switch_1 ESG_GO_ROUTER_ISOZONE_1_SWITCH_1, --esg_go_router_isozone_1_switch_1 ESG_GO_ROUTER_ISOZONE_1_SWITCH_1
                        esg instance 1 routed go_router_isozone_1 switch
  -esg_go_router_isozone_1_inst_1 ESG_GO_ROUTER_ISOZONE_1_INSTANCES_1, --esg_go_router_isozone_1_instances_1 ESG_GO_ROUTER_ISOZONE_1_INSTANCES_1
                        esg instance 1 routed go_router_isozone_1 instances
  -esg_go_router_isozone_1_off_1 ESG_GO_ROUTER_ISOZONE_1_OFFSET_1, --esg_go_router_isozone_1_offset_1 ESG_GO_ROUTER_ISOZONE_1_OFFSET_1
                        esg instance 1 routed go_router_isozone_1 offset
  -esg_tcp_router_isozone_1_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_1_UPLINK_IP_1, --esg_tcp_router_isozone_1_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_1_UPLINK_IP_1
                        esg instance 1 routed tcp_router_isozone_1 uplink ip
  -esg_tcp_router_isozone_1_switch_1 ESG_TCP_ROUTER_ISOZONE_1_SWITCH_1, --esg_tcp_router_isozone_1_switch_1 ESG_TCP_ROUTER_ISOZONE_1_SWITCH_1
                        esg instance 1 routed tcp_router_isozone_1 switch
  -esg_tcp_router_isozone_1_inst_1 ESG_TCP_ROUTER_ISOZONE_1_INSTANCES_1, --esg_tcp_router_isozone_1_instances_1 ESG_TCP_ROUTER_ISOZONE_1_INSTANCES_1
                        esg instance 1 routed tcp_router_isozone_1 instances
  -esg_tcp_router_isozone_1_off_1 ESG_TCP_ROUTER_ISOZONE_1_OFFSET_1, --esg_tcp_router_isozone_1_offset_1 ESG_TCP_ROUTER_ISOZONE_1_OFFSET_1
                        esg instance 1 routed tcp_router_isozone_1 offset
  -esg_go_router_isozone_2_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_2_UPLINK_IP_1, --esg_go_router_isozone_2_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_2_UPLINK_IP_1
                        esg instance 1 routed go_router_isozone_2 uplink ip
  -esg_go_router_isozone_2_switch_1 ESG_GO_ROUTER_ISOZONE_2_SWITCH_1, --esg_go_router_isozone_2_switch_1 ESG_GO_ROUTER_ISOZONE_2_SWITCH_1
                        esg instance 1 routed go_router_isozone_2 switch
  -esg_go_router_isozone_2_inst_1 ESG_GO_ROUTER_ISOZONE_2_INSTANCES_1, --esg_go_router_isozone_2_instances_1 ESG_GO_ROUTER_ISOZONE_2_INSTANCES_1
                        esg instance 1 routed go_router_isozone_2 instances
  -esg_go_router_isozone_2_off_1 ESG_GO_ROUTER_ISOZONE_2_OFFSET_1, --esg_go_router_isozone_2_offset_1 ESG_GO_ROUTER_ISOZONE_2_OFFSET_1
                        esg instance 1 routed go_router_isozone_2 offset
  -esg_tcp_router_isozone_2_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_2_UPLINK_IP_1, --esg_tcp_router_isozone_2_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_2_UPLINK_IP_1
                        esg instance 1 routed tcp_router_isozone_2 uplink ip
  -esg_tcp_router_isozone_2_switch_1 ESG_TCP_ROUTER_ISOZONE_2_SWITCH_1, --esg_tcp_router_isozone_2_switch_1 ESG_TCP_ROUTER_ISOZONE_2_SWITCH_1
                        esg instance 1 routed tcp_router_isozone_2 switch
  -esg_tcp_router_isozone_2_inst_1 ESG_TCP_ROUTER_ISOZONE_2_INSTANCES_1, --esg_tcp_router_isozone_2_instances_1 ESG_TCP_ROUTER_ISOZONE_2_INSTANCES_1
                        esg instance 1 routed tcp_router_isozone_2 instances
  -esg_tcp_router_isozone_2_off_1 ESG_TCP_ROUTER_ISOZONE_2_OFFSET_1, --esg_tcp_router_isozone_2_offset_1 ESG_TCP_ROUTER_ISOZONE_2_OFFSET_1
                        esg instance 1 routed tcp_router_isozone_2 offset
  -esg_go_router_isozone_3_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_3_UPLINK_IP_1, --esg_go_router_isozone_3_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_3_UPLINK_IP_1
                        esg instance 1 routed go_router_isozone_3 uplink ip
  -esg_go_router_isozone_3_switch_1 ESG_GO_ROUTER_ISOZONE_3_SWITCH_1, --esg_go_router_isozone_3_switch_1 ESG_GO_ROUTER_ISOZONE_3_SWITCH_1
                        esg instance 1 routed go_router_isozone_3 switch
  -esg_go_router_isozone_3_inst_1 ESG_GO_ROUTER_ISOZONE_3_INSTANCES_1, --esg_go_router_isozone_3_instances_1 ESG_GO_ROUTER_ISOZONE_3_INSTANCES_1
                        esg instance 1 routed go_router_isozone_3 instances
  -esg_go_router_isozone_3_off_1 ESG_GO_ROUTER_ISOZONE_3_OFFSET_1, --esg_go_router_isozone_3_offset_1 ESG_GO_ROUTER_ISOZONE_3_OFFSET_1
                        esg instance 1 routed go_router_isozone_3 offset
  -esg_tcp_router_isozone_3_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_3_UPLINK_IP_1, --esg_tcp_router_isozone_3_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_3_UPLINK_IP_1
                        esg instance 1 routed tcp_router_isozone_3 uplink ip
  -esg_tcp_router_isozone_3_switch_1 ESG_TCP_ROUTER_ISOZONE_3_SWITCH_1, --esg_tcp_router_isozone_3_switch_1 ESG_TCP_ROUTER_ISOZONE_3_SWITCH_1
                        esg instance 1 routed tcp_router_isozone_3 switch
  -esg_tcp_router_isozone_3_inst_1 ESG_TCP_ROUTER_ISOZONE_3_INSTANCES_1, --esg_tcp_router_isozone_3_instances_1 ESG_TCP_ROUTER_ISOZONE_3_INSTANCES_1
                        esg instance 1 routed tcp_router_isozone_3 instances
  -esg_tcp_router_isozone_3_off_1 ESG_TCP_ROUTER_ISOZONE_3_OFFSET_1, --esg_tcp_router_isozone_3_offset_1 ESG_TCP_ROUTER_ISOZONE_3_OFFSET_1
                        esg instance 1 routed tcp_router_isozone_3 offset
  -esg_go_router_isozone_4_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_4_UPLINK_IP_1, --esg_go_router_isozone_4_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_4_UPLINK_IP_1
                        esg instance 1 routed go_router_isozone_4 uplink ip
  -esg_go_router_isozone_4_switch_1 ESG_GO_ROUTER_ISOZONE_4_SWITCH_1, --esg_go_router_isozone_4_switch_1 ESG_GO_ROUTER_ISOZONE_4_SWITCH_1
                        esg instance 1 routed go_router_isozone_4 switch
  -esg_go_router_isozone_4_inst_1 ESG_GO_ROUTER_ISOZONE_4_INSTANCES_1, --esg_go_router_isozone_4_instances_1 ESG_GO_ROUTER_ISOZONE_4_INSTANCES_1
                        esg instance 1 routed go_router_isozone_4 instances
  -esg_go_router_isozone_4_off_1 ESG_GO_ROUTER_ISOZONE_4_OFFSET_1, --esg_go_router_isozone_4_offset_1 ESG_GO_ROUTER_ISOZONE_4_OFFSET_1
                        esg instance 1 routed go_router_isozone_4 offset
  -esg_tcp_router_isozone_4_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_4_UPLINK_IP_1, --esg_tcp_router_isozone_4_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_4_UPLINK_IP_1
                        esg instance 1 routed tcp_router_isozone_4 uplink ip
  -esg_tcp_router_isozone_4_switch_1 ESG_TCP_ROUTER_ISOZONE_4_SWITCH_1, --esg_tcp_router_isozone_4_switch_1 ESG_TCP_ROUTER_ISOZONE_4_SWITCH_1
                        esg instance 1 routed tcp_router_isozone_4 switch
  -esg_tcp_router_isozone_4_inst_1 ESG_TCP_ROUTER_ISOZONE_4_INSTANCES_1, --esg_tcp_router_isozone_4_instances_1 ESG_TCP_ROUTER_ISOZONE_4_INSTANCES_1
                        esg instance 1 routed tcp_router_isozone_4 instances
  -esg_tcp_router_isozone_4_off_1 ESG_TCP_ROUTER_ISOZONE_4_OFFSET_1, --esg_tcp_router_isozone_4_offset_1 ESG_TCP_ROUTER_ISOZONE_4_OFFSET_1
                        esg instance 1 routed tcp_router_isozone_4 offset
  -esg_go_router_isozone_5_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_5_UPLINK_IP_1, --esg_go_router_isozone_5_uplink_ip_1 ESG_GO_ROUTER_ISOZONE_5_UPLINK_IP_1
                        esg instance 1 routed go_router_isozone_5 uplink ip
  -esg_go_router_isozone_5_switch_1 ESG_GO_ROUTER_ISOZONE_5_SWITCH_1, --esg_go_router_isozone_5_switch_1 ESG_GO_ROUTER_ISOZONE_5_SWITCH_1
                        esg instance 1 routed go_router_isozone_5 switch
  -esg_go_router_isozone_5_inst_1 ESG_GO_ROUTER_ISOZONE_5_INSTANCES_1, --esg_go_router_isozone_5_instances_1 ESG_GO_ROUTER_ISOZONE_5_INSTANCES_1
                        esg instance 1 routed go_router_isozone_5 instances
  -esg_go_router_isozone_5_off_1 ESG_GO_ROUTER_ISOZONE_5_OFFSET_1, --esg_go_router_isozone_5_offset_1 ESG_GO_ROUTER_ISOZONE_5_OFFSET_1
                        esg instance 1 routed go_router_isozone_5 offset
  -esg_tcp_router_isozone_5_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_5_UPLINK_IP_1, --esg_tcp_router_isozone_5_uplink_ip_1 ESG_TCP_ROUTER_ISOZONE_5_UPLINK_IP_1
                        esg instance 1 routed tcp_router_isozone_5 uplink ip
  -esg_tcp_router_isozone_5_switch_1 ESG_TCP_ROUTER_ISOZONE_5_SWITCH_1, --esg_tcp_router_isozone_5_switch_1 ESG_TCP_ROUTER_ISOZONE_5_SWITCH_1
                        esg instance 1 routed tcp_router_isozone_5 switch
  -esg_tcp_router_isozone_5_inst_1 ESG_TCP_ROUTER_ISOZONE_5_INSTANCES_1, --esg_tcp_router_isozone_5_instances_1 ESG_TCP_ROUTER_ISOZONE_5_INSTANCES_1
                        esg instance 1 routed tcp_router_isozone_5 instances
  -esg_tcp_router_isozone_5_off_1 ESG_TCP_ROUTER_ISOZONE_5_OFFSET_1, --esg_tcp_router_isozone_5_offset_1 ESG_TCP_ROUTER_ISOZONE_5_OFFSET_1
                        esg instance 1 routed tcp_router_isozone_5 offset
  -esg_name_2 ESG_NAME_2, --esg_name_2 ESG_NAME_2
                        esg instance 2 name
  -esg_size_2 ESG_SIZE_2, --esg_size_2 ESG_SIZE_2
                        esg instance 2 size
  -esg_gateway_2 ESG_GATEWAY_IP_2, --esg_gateway_ip_2 ESG_GATEWAY_IP_2
                        esg instance 2 gateway ip
  -esg_ospf_password_2 ESG_OSPF_PASSWORD_2, --esg_ospf_password_2 ESG_OSPF_PASSWORD_2
                        esg instance 2 ospf password
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
  -esg_opsmgr_switch_2 ESG_OPSMGR_SWITCH_2, --esg_opsmgr_switch_2 ESG_OPSMGR_SWITCH_2
                        esg instance 2 routed opsmgr switch
  -esg_opsmgr_inst_2 ESG_OPSMGR_INSTANCES_2, --esg_opsmgr_instances_2 ESG_OPSMGR_INSTANCES_2
                        esg instance 2 routed opsmgr instances
  -esg_opsmgr_off_2 ESG_OPSMGR_OFFSET_2, --esg_opsmgr_offset_2 ESG_OPSMGR_OFFSET_2
                        esg instance 2 routed opsmgr offset
  -esg_go_router_uplink_ip_2 ESG_GO_ROUTER_UPLINK_IP_2, --esg_go_router_uplink_ip_2 ESG_GO_ROUTER_UPLINK_IP_2
                        esg instance 2 routed go_router uplink ip
  -esg_go_router_switch_2 ESG_GO_ROUTER_SWITCH_2, --esg_go_router_switch_2 ESG_GO_ROUTER_SWITCH_2
                        esg instance 2 routed go_router switch
  -esg_go_router_inst_2 ESG_GO_ROUTER_INSTANCES_2, --esg_go_router_instances_2 ESG_GO_ROUTER_INSTANCES_2
                        esg instance 2 routed go_router instances
  -esg_go_router_off_2 ESG_GO_ROUTER_OFFSET_2, --esg_go_router_offset_2 ESG_GO_ROUTER_OFFSET_2
                        esg instance 2 routed go_router offset
  -esg_diego_brain_uplink_ip_2 ESG_DIEGO_BRAIN_UPLINK_IP_2, --esg_diego_brain_uplink_ip_2 ESG_DIEGO_BRAIN_UPLINK_IP_2
                        esg instance 2 routed diego_brain uplink ip
  -esg_diego_brain_switch_2 ESG_DIEGO_BRAIN_SWITCH_2, --esg_diego_brain_switch_2 ESG_DIEGO_BRAIN_SWITCH_2
                        esg instance 2 routed diego_brain switch
  -esg_diego_brain_inst_2 ESG_DIEGO_BRAIN_INSTANCES_2, --esg_diego_brain_instances_2 ESG_DIEGO_BRAIN_INSTANCES_2
                        esg instance 2 routed diego_brain instances
  -esg_diego_brain_off_2 ESG_DIEGO_BRAIN_OFFSET_2, --esg_diego_brain_offset_2 ESG_DIEGO_BRAIN_OFFSET_2
                        esg instance 2 routed diego_brain offset
  -esg_tcp_router_uplink_ip_2 ESG_TCP_ROUTER_UPLINK_IP_2, --esg_tcp_router_uplink_ip_2 ESG_TCP_ROUTER_UPLINK_IP_2
                        esg instance 2 routed tcp_router uplink ip
  -esg_tcp_router_switch_2 ESG_TCP_ROUTER_SWITCH_2, --esg_tcp_router_switch_2 ESG_TCP_ROUTER_SWITCH_2
                        esg instance 2 routed tcp_router switch
  -esg_tcp_router_inst_2 ESG_TCP_ROUTER_INSTANCES_2, --esg_tcp_router_instances_2 ESG_TCP_ROUTER_INSTANCES_2
                        esg instance 2 routed tcp_router instances
  -esg_tcp_router_off_2 ESG_TCP_ROUTER_OFFSET_2, --esg_tcp_router_offset_2 ESG_TCP_ROUTER_OFFSET_2
                        esg instance 2 routed tcp_router offset
  -esg_mysql_ert_uplink_ip_2 ESG_MYSQL_ERT_UPLINK_IP_2, --esg_mysql_ert_uplink_ip_2 ESG_MYSQL_ERT_UPLINK_IP_2
                        esg instance 2 routed mysql_ert uplink ip
  -esg_mysql_ert_switch_2 ESG_MYSQL_ERT_SWITCH_2, --esg_mysql_ert_switch_2 ESG_MYSQL_ERT_SWITCH_2
                        esg instance 2 routed mysql_ert switch
  -esg_mysql_ert_inst_2 ESG_MYSQL_ERT_INSTANCES_2, --esg_mysql_ert_instances_2 ESG_MYSQL_ERT_INSTANCES_2
                        esg instance 2 routed mysql_ert instances
  -esg_mysql_ert_off_2 ESG_MYSQL_ERT_OFFSET_2, --esg_mysql_ert_offset_2 ESG_MYSQL_ERT_OFFSET_2
                        esg instance 2 routed mysql_ert offset
  -esg_mysql_tile_uplink_ip_2 ESG_MYSQL_TILE_UPLINK_IP_2, --esg_mysql_tile_uplink_ip_2 ESG_MYSQL_TILE_UPLINK_IP_2
                        esg instance 2 routed mysql_tile uplink ip
  -esg_mysql_tile_switch_2 ESG_MYSQL_TILE_SWITCH_2, --esg_mysql_tile_switch_2 ESG_MYSQL_TILE_SWITCH_2
                        esg instance 2 routed mysql_tile switch
  -esg_mysql_tile_inst_2 ESG_MYSQL_TILE_INSTANCES_2, --esg_mysql_tile_instances_2 ESG_MYSQL_TILE_INSTANCES_2
                        esg instance 2 routed mysql_tile instances
  -esg_mysql_tile_off_2 ESG_MYSQL_TILE_OFFSET_2, --esg_mysql_tile_offset_2 ESG_MYSQL_TILE_OFFSET_2
                        esg instance 2 routed mysql_tile offset
  -esg_rabbitmq_tile_uplink_ip_2 ESG_RABBITMQ_TILE_UPLINK_IP_2, --esg_rabbitmq_tile_uplink_ip_2 ESG_RABBITMQ_TILE_UPLINK_IP_2
                        esg instance 2 routed rabbitmq_tile uplink ip
  -esg_rabbitmq_tile_switch_2 ESG_RABBITMQ_TILE_SWITCH_2, --esg_rabbitmq_tile_switch_2 ESG_RABBITMQ_TILE_SWITCH_2
                        esg instance 2 routed rabbitmq_tile switch
  -esg_rabbitmq_tile_inst_2 ESG_RABBITMQ_TILE_INSTANCES_2, --esg_rabbitmq_tile_instances_2 ESG_RABBITMQ_TILE_INSTANCES_2
                        esg instance 2 routed rabbitmq_tile instances
  -esg_rabbitmq_tile_off_2 ESG_RABBITMQ_TILE_OFFSET_2, --esg_rabbitmq_tile_offset_2 ESG_RABBITMQ_TILE_OFFSET_2
                        esg instance 2 routed rabbitmq_tile offset
  -esg_go_router_isozone_1_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_1_UPLINK_IP_2, --esg_go_router_isozone_1_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_1_UPLINK_IP_2
                        esg instance 2 routed go_router_isozone_1 uplink ip
  -esg_go_router_isozone_1_switch_2 ESG_GO_ROUTER_ISOZONE_1_SWITCH_2, --esg_go_router_isozone_1_switch_2 ESG_GO_ROUTER_ISOZONE_1_SWITCH_2
                        esg instance 2 routed go_router_isozone_1 switch
  -esg_go_router_isozone_1_inst_2 ESG_GO_ROUTER_ISOZONE_1_INSTANCES_2, --esg_go_router_isozone_1_instances_2 ESG_GO_ROUTER_ISOZONE_1_INSTANCES_2
                        esg instance 2 routed go_router_isozone_1 instances
  -esg_go_router_isozone_1_off_2 ESG_GO_ROUTER_ISOZONE_1_OFFSET_2, --esg_go_router_isozone_1_offset_2 ESG_GO_ROUTER_ISOZONE_1_OFFSET_2
                        esg instance 2 routed go_router_isozone_1 offset
  -esg_tcp_router_isozone_1_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_1_UPLINK_IP_2, --esg_tcp_router_isozone_1_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_1_UPLINK_IP_2
                        esg instance 2 routed tcp_router_isozone_1 uplink ip
  -esg_tcp_router_isozone_1_switch_2 ESG_TCP_ROUTER_ISOZONE_1_SWITCH_2, --esg_tcp_router_isozone_1_switch_2 ESG_TCP_ROUTER_ISOZONE_1_SWITCH_2
                        esg instance 2 routed tcp_router_isozone_1 switch
  -esg_tcp_router_isozone_1_inst_2 ESG_TCP_ROUTER_ISOZONE_1_INSTANCES_2, --esg_tcp_router_isozone_1_instances_2 ESG_TCP_ROUTER_ISOZONE_1_INSTANCES_2
                        esg instance 2 routed tcp_router_isozone_1 instances
  -esg_tcp_router_isozone_1_off_2 ESG_TCP_ROUTER_ISOZONE_1_OFFSET_2, --esg_tcp_router_isozone_1_offset_2 ESG_TCP_ROUTER_ISOZONE_1_OFFSET_2
                        esg instance 2 routed tcp_router_isozone_1 offset
  -esg_go_router_isozone_2_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_2_UPLINK_IP_2, --esg_go_router_isozone_2_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_2_UPLINK_IP_2
                        esg instance 2 routed go_router_isozone_2 uplink ip
  -esg_go_router_isozone_2_switch_2 ESG_GO_ROUTER_ISOZONE_2_SWITCH_2, --esg_go_router_isozone_2_switch_2 ESG_GO_ROUTER_ISOZONE_2_SWITCH_2
                        esg instance 2 routed go_router_isozone_2 switch
  -esg_go_router_isozone_2_inst_2 ESG_GO_ROUTER_ISOZONE_2_INSTANCES_2, --esg_go_router_isozone_2_instances_2 ESG_GO_ROUTER_ISOZONE_2_INSTANCES_2
                        esg instance 2 routed go_router_isozone_2 instances
  -esg_go_router_isozone_2_off_2 ESG_GO_ROUTER_ISOZONE_2_OFFSET_2, --esg_go_router_isozone_2_offset_2 ESG_GO_ROUTER_ISOZONE_2_OFFSET_2
                        esg instance 2 routed go_router_isozone_2 offset
  -esg_tcp_router_isozone_2_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_2_UPLINK_IP_2, --esg_tcp_router_isozone_2_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_2_UPLINK_IP_2
                        esg instance 2 routed tcp_router_isozone_2 uplink ip
  -esg_tcp_router_isozone_2_switch_2 ESG_TCP_ROUTER_ISOZONE_2_SWITCH_2, --esg_tcp_router_isozone_2_switch_2 ESG_TCP_ROUTER_ISOZONE_2_SWITCH_2
                        esg instance 2 routed tcp_router_isozone_2 switch
  -esg_tcp_router_isozone_2_inst_2 ESG_TCP_ROUTER_ISOZONE_2_INSTANCES_2, --esg_tcp_router_isozone_2_instances_2 ESG_TCP_ROUTER_ISOZONE_2_INSTANCES_2
                        esg instance 2 routed tcp_router_isozone_2 instances
  -esg_tcp_router_isozone_2_off_2 ESG_TCP_ROUTER_ISOZONE_2_OFFSET_2, --esg_tcp_router_isozone_2_offset_2 ESG_TCP_ROUTER_ISOZONE_2_OFFSET_2
                        esg instance 2 routed tcp_router_isozone_2 offset
  -esg_go_router_isozone_3_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_3_UPLINK_IP_2, --esg_go_router_isozone_3_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_3_UPLINK_IP_2
                        esg instance 2 routed go_router_isozone_3 uplink ip
  -esg_go_router_isozone_3_switch_2 ESG_GO_ROUTER_ISOZONE_3_SWITCH_2, --esg_go_router_isozone_3_switch_2 ESG_GO_ROUTER_ISOZONE_3_SWITCH_2
                        esg instance 2 routed go_router_isozone_3 switch
  -esg_go_router_isozone_3_inst_2 ESG_GO_ROUTER_ISOZONE_3_INSTANCES_2, --esg_go_router_isozone_3_instances_2 ESG_GO_ROUTER_ISOZONE_3_INSTANCES_2
                        esg instance 2 routed go_router_isozone_3 instances
  -esg_go_router_isozone_3_off_2 ESG_GO_ROUTER_ISOZONE_3_OFFSET_2, --esg_go_router_isozone_3_offset_2 ESG_GO_ROUTER_ISOZONE_3_OFFSET_2
                        esg instance 2 routed go_router_isozone_3 offset
  -esg_tcp_router_isozone_3_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_3_UPLINK_IP_2, --esg_tcp_router_isozone_3_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_3_UPLINK_IP_2
                        esg instance 2 routed tcp_router_isozone_3 uplink ip
  -esg_tcp_router_isozone_3_switch_2 ESG_TCP_ROUTER_ISOZONE_3_SWITCH_2, --esg_tcp_router_isozone_3_switch_2 ESG_TCP_ROUTER_ISOZONE_3_SWITCH_2
                        esg instance 2 routed tcp_router_isozone_3 switch
  -esg_tcp_router_isozone_3_inst_2 ESG_TCP_ROUTER_ISOZONE_3_INSTANCES_2, --esg_tcp_router_isozone_3_instances_2 ESG_TCP_ROUTER_ISOZONE_3_INSTANCES_2
                        esg instance 2 routed tcp_router_isozone_3 instances
  -esg_tcp_router_isozone_3_off_2 ESG_TCP_ROUTER_ISOZONE_3_OFFSET_2, --esg_tcp_router_isozone_3_offset_2 ESG_TCP_ROUTER_ISOZONE_3_OFFSET_2
                        esg instance 2 routed tcp_router_isozone_3 offset
  -esg_go_router_isozone_4_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_4_UPLINK_IP_2, --esg_go_router_isozone_4_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_4_UPLINK_IP_2
                        esg instance 2 routed go_router_isozone_4 uplink ip
  -esg_go_router_isozone_4_switch_2 ESG_GO_ROUTER_ISOZONE_4_SWITCH_2, --esg_go_router_isozone_4_switch_2 ESG_GO_ROUTER_ISOZONE_4_SWITCH_2
                        esg instance 2 routed go_router_isozone_4 switch
  -esg_go_router_isozone_4_inst_2 ESG_GO_ROUTER_ISOZONE_4_INSTANCES_2, --esg_go_router_isozone_4_instances_2 ESG_GO_ROUTER_ISOZONE_4_INSTANCES_2
                        esg instance 2 routed go_router_isozone_4 instances
  -esg_go_router_isozone_4_off_2 ESG_GO_ROUTER_ISOZONE_4_OFFSET_2, --esg_go_router_isozone_4_offset_2 ESG_GO_ROUTER_ISOZONE_4_OFFSET_2
                        esg instance 2 routed go_router_isozone_4 offset
  -esg_tcp_router_isozone_4_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_4_UPLINK_IP_2, --esg_tcp_router_isozone_4_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_4_UPLINK_IP_2
                        esg instance 2 routed tcp_router_isozone_4 uplink ip
  -esg_tcp_router_isozone_4_switch_2 ESG_TCP_ROUTER_ISOZONE_4_SWITCH_2, --esg_tcp_router_isozone_4_switch_2 ESG_TCP_ROUTER_ISOZONE_4_SWITCH_2
                        esg instance 2 routed tcp_router_isozone_4 switch
  -esg_tcp_router_isozone_4_inst_2 ESG_TCP_ROUTER_ISOZONE_4_INSTANCES_2, --esg_tcp_router_isozone_4_instances_2 ESG_TCP_ROUTER_ISOZONE_4_INSTANCES_2
                        esg instance 2 routed tcp_router_isozone_4 instances
  -esg_tcp_router_isozone_4_off_2 ESG_TCP_ROUTER_ISOZONE_4_OFFSET_2, --esg_tcp_router_isozone_4_offset_2 ESG_TCP_ROUTER_ISOZONE_4_OFFSET_2
                        esg instance 2 routed tcp_router_isozone_4 offset
  -esg_go_router_isozone_5_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_5_UPLINK_IP_2, --esg_go_router_isozone_5_uplink_ip_2 ESG_GO_ROUTER_ISOZONE_5_UPLINK_IP_2
                        esg instance 2 routed go_router_isozone_5 uplink ip
  -esg_go_router_isozone_5_switch_2 ESG_GO_ROUTER_ISOZONE_5_SWITCH_2, --esg_go_router_isozone_5_switch_2 ESG_GO_ROUTER_ISOZONE_5_SWITCH_2
                        esg instance 2 routed go_router_isozone_5 switch
  -esg_go_router_isozone_5_inst_2 ESG_GO_ROUTER_ISOZONE_5_INSTANCES_2, --esg_go_router_isozone_5_instances_2 ESG_GO_ROUTER_ISOZONE_5_INSTANCES_2
                        esg instance 2 routed go_router_isozone_5 instances
  -esg_go_router_isozone_5_off_2 ESG_GO_ROUTER_ISOZONE_5_OFFSET_2, --esg_go_router_isozone_5_offset_2 ESG_GO_ROUTER_ISOZONE_5_OFFSET_2
                        esg instance 2 routed go_router_isozone_5 offset
  -esg_tcp_router_isozone_5_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_5_UPLINK_IP_2, --esg_tcp_router_isozone_5_uplink_ip_2 ESG_TCP_ROUTER_ISOZONE_5_UPLINK_IP_2
                        esg instance 2 routed tcp_router_isozone_5 uplink ip
  -esg_tcp_router_isozone_5_switch_2 ESG_TCP_ROUTER_ISOZONE_5_SWITCH_2, --esg_tcp_router_isozone_5_switch_2 ESG_TCP_ROUTER_ISOZONE_5_SWITCH_2
                        esg instance 2 routed tcp_router_isozone_5 switch
  -esg_tcp_router_isozone_5_inst_2 ESG_TCP_ROUTER_ISOZONE_5_INSTANCES_2, --esg_tcp_router_isozone_5_instances_2 ESG_TCP_ROUTER_ISOZONE_5_INSTANCES_2
                        esg instance 2 routed tcp_router_isozone_5 instances
  -esg_tcp_router_isozone_5_off_2 ESG_TCP_ROUTER_ISOZONE_5_OFFSET_2, --esg_tcp_router_isozone_5_offset_2 ESG_TCP_ROUTER_ISOZONE_5_OFFSET_2
                        esg instance 2 routed tcp_router_isozone_5 offset
  -nsxmanager_addr NSXMANAGER_ADDRESS, --nsxmanager_address NSXMANAGER_ADDRESS
                        nsxmanager address
  -nsxmanager_en_dlr NSXMANAGER_ENABLE_DLR, --nsxmanager_enable_dlr NSXMANAGER_ENABLE_DLR
                        nsxmanager enable dlr
  -nsxmanager_user NSXMANAGER_ADMIN_USER, --nsxmanager_admin_user NSXMANAGER_ADMIN_USER
                        nsxmanager admin user
  -nsxmanager_pass NSXMANAGER_ADMIN_PASSWD, --nsxmanager_admin_passwd NSXMANAGER_ADMIN_PASSWD
                        nsxmanager admin passwd
  -nsxmanager_tz NSXMANAGER_TRANSPORTZONE, --nsxmanager_transportzone NSXMANAGER_TRANSPORTZONE
                        nsxmanager transportzone
  -nsxmanager_dportgroup NSXMANAGER_DISTRIBUTED_PORTGROUP, --nsxmanager_distributed_portgroup NSXMANAGER_DISTRIBUTED_PORTGROUP
                        nsxmanager distributed portgroup
  -nsxmanager_uplink_ip NSXMANAGER_UPLINK_IP, --nsxmanager_uplink_ip NSXMANAGER_UPLINK_IP
                        nsxmanager uplink ip
  -nsxmanager_uplink_port NSXMANAGER_UPLINK_PORT_SWITCH, --nsxmanager_uplink_port_switch NSXMANAGER_UPLINK_PORT_SWITCH
                        nsxmanager uplink port switch
  -nsxmanager_sr_name NSXMANAGER_STATIC_ROUTE_NAME, --nsxmanager_static_route_name NSXMANAGER_STATIC_ROUTE_NAME
                        nsxmanager static route name
  -nsxmanager_sr_subnet NSXMANAGER_STATIC_ROUTE_SUBNET, --nsxmanager_static_route_subnet NSXMANAGER_STATIC_ROUTE_SUBNET
                        nsxmanager static route subnet
  -nsxmanager_sr_gateway NSXMANAGER_STATIC_ROUTE_GATEWAY, --nsxmanager_static_route_gateway NSXMANAGER_STATIC_ROUTE_GATEWAY
                        nsxmanager static route gateway
  -nsxmanager_sr_hop NSXMANAGER_STATIC_ROUTE_HOP, --nsxmanager_static_route_hop NSXMANAGER_STATIC_ROUTE_HOP
                        nsxmanager static route hop
  -ntp NTP_IPS, --ntp_ips NTP_IPS
                        default ntp ips
  -dns DNS_IPS, --dns_ips DNS_IPS
                        default dns ips
  -log SYSLOG_IPS, --syslog_ips SYSLOG_IPS
                        default syslog ips
  -ldap LDAP_IPS, --ldap_ips LDAP_IPS
                        default ldap ips
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
```