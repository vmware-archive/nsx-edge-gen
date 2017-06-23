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
              [-esg_ert_certs_1 ESG_ERT_CERTS_NAME_1]
              [-esg_ert_certs_cert_id_1 ESG_ERT_CERTS_CERT_ID_1]
              [-esg_ert_certs_key_1 ESG_ERT_CERTS_KEY_1]
              [-esg_ert_certs_cert_1 ESG_ERT_CERTS_CERT_1]
              [-esg_ert_certs_config_ou_1 ESG_ERT_CERTS_CONFIG_ORG_UNIT_1]
              [-esg_ert_certs_config_cc_1 ESG_ERT_CERTS_CONFIG_COUNTRY_1]
              [-esg_ert_certs_config_sysd_1 ESG_ERT_CERTS_CONFIG_SYSTEMDOMAIN_1]
              [-esg_ert_certs_config_appd_1 ESG_ERT_CERTS_CONFIG_APPDOMAIN_1]
              [-esg_iso_certs_1_1 ESG_ISO_CERTS_NAME_1_1]
              [-esg_iso_certs_cert_id_1_1 ESG_ISO_CERTS_CERT_ID_1_1]
              [-esg_iso_certs_key_1_1 ESG_ISO_CERTS_KEY_1_1]
              [-esg_iso_certs_cert_1_1 ESG_ISO_CERTS_CERT_1_1]
              [-esg_iso_certs_config_switch_1_1 ESG_ISO_CERTS_CONFIG_SWITCH_1_1]
              [-esg_iso_certs_config_ou_1_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_1_1]
              [-esg_iso_certs_config_cc_1_1 ESG_ISO_CERTS_CONFIG_COUNTRY_1_1]
              [-esg_iso_certs_config_domains_1_1 ESG_ISO_CERTS_CONFIG_DOMAINS_1_1]
              [-esg_iso_certs_2_1 ESG_ISO_CERTS_NAME_2_1]
              [-esg_iso_certs_cert_id_2_1 ESG_ISO_CERTS_CERT_ID_2_1]
              [-esg_iso_certs_key_2_1 ESG_ISO_CERTS_KEY_2_1]
              [-esg_iso_certs_cert_2_1 ESG_ISO_CERTS_CERT_2_1]
              [-esg_iso_certs_config_switch_2_1 ESG_ISO_CERTS_CONFIG_SWITCH_2_1]
              [-esg_iso_certs_config_ou_2_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_2_1]
              [-esg_iso_certs_config_cc_2_1 ESG_ISO_CERTS_CONFIG_COUNTRY_2_1]
              [-esg_iso_certs_config_domains_2_1 ESG_ISO_CERTS_CONFIG_DOMAINS_2_1]
              [-esg_iso_certs_3_1 ESG_ISO_CERTS_NAME_3_1]
              [-esg_iso_certs_cert_id_3_1 ESG_ISO_CERTS_CERT_ID_3_1]
              [-esg_iso_certs_key_3_1 ESG_ISO_CERTS_KEY_3_1]
              [-esg_iso_certs_cert_3_1 ESG_ISO_CERTS_CERT_3_1]
              [-esg_iso_certs_config_switch_3_1 ESG_ISO_CERTS_CONFIG_SWITCH_3_1]
              [-esg_iso_certs_config_ou_3_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_3_1]
              [-esg_iso_certs_config_cc_3_1 ESG_ISO_CERTS_CONFIG_COUNTRY_3_1]
              [-esg_iso_certs_config_domains_3_1 ESG_ISO_CERTS_CONFIG_DOMAINS_3_1]
              [-esg_iso_certs_4_1 ESG_ISO_CERTS_NAME_4_1]
              [-esg_iso_certs_cert_id_4_1 ESG_ISO_CERTS_CERT_ID_4_1]
              [-esg_iso_certs_key_4_1 ESG_ISO_CERTS_KEY_4_1]
              [-esg_iso_certs_cert_4_1 ESG_ISO_CERTS_CERT_4_1]
              [-esg_iso_certs_config_switch_4_1 ESG_ISO_CERTS_CONFIG_SWITCH_4_1]
              [-esg_iso_certs_config_ou_4_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_4_1]
              [-esg_iso_certs_config_cc_4_1 ESG_ISO_CERTS_CONFIG_COUNTRY_4_1]
              [-esg_iso_certs_config_domains_4_1 ESG_ISO_CERTS_CONFIG_DOMAINS_4_1]
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
              [-nsxmanager_addr NSXMANAGER_ADDRESS]
              [-nsxmanager_en_dlr NSXMANAGER_ENABLE_DLR]
              [-nsxmanager_bosh_nsx_enabled NSXMANAGER_BOSH_NSX_ENABLED]
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
                        export:   return the firewall rules of a Edge Service Gateway
                        init:    create a new nsx cloud config file

optional arguments:
  -h, --help            show this help message and exit
  -i INIT, --init INIT  name for nsx config directory on init
  -c NSX_CONF, --nsx_conf NSX_CONF
                        nsx configuration yml file
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
  -esg_ert_certs_1 ESG_ERT_CERTS_NAME_1, --esg_ert_certs_name_1 ESG_ERT_CERTS_NAME_1
                        esg instance 1 ert certs name
  -esg_ert_certs_cert_id_1 ESG_ERT_CERTS_CERT_ID_1, --esg_ert_certs_cert_id_1 ESG_ERT_CERTS_CERT_ID_1
                        esg instance 1 ert certs cert id
  -esg_ert_certs_key_1 ESG_ERT_CERTS_KEY_1, --esg_ert_certs_key_1 ESG_ERT_CERTS_KEY_1
                        esg instance 1 ert certs key
  -esg_ert_certs_cert_1 ESG_ERT_CERTS_CERT_1, --esg_ert_certs_cert_1 ESG_ERT_CERTS_CERT_1
                        esg instance 1 ert certs cert
  -esg_ert_certs_config_ou_1 ESG_ERT_CERTS_CONFIG_ORG_UNIT_1, --esg_ert_certs_config_org_unit_1 ESG_ERT_CERTS_CONFIG_ORG_UNIT_1
                        esg instance 1 ert certs config org unit
  -esg_ert_certs_config_cc_1 ESG_ERT_CERTS_CONFIG_COUNTRY_1, --esg_ert_certs_config_country_1 ESG_ERT_CERTS_CONFIG_COUNTRY_1
                        esg instance 1 ert certs config country
  -esg_ert_certs_config_sysd_1 ESG_ERT_CERTS_CONFIG_SYSTEMDOMAIN_1, --esg_ert_certs_config_systemdomain_1 ESG_ERT_CERTS_CONFIG_SYSTEMDOMAIN_1
                        esg instance 1 ert certs config systemdomain
  -esg_ert_certs_config_appd_1 ESG_ERT_CERTS_CONFIG_APPDOMAIN_1, --esg_ert_certs_config_appdomain_1 ESG_ERT_CERTS_CONFIG_APPDOMAIN_1
                        esg instance 1 ert certs config appdomain
  -esg_iso_certs_1_1 ESG_ISO_CERTS_NAME_1_1, --esg_iso_certs_name_1_1 ESG_ISO_CERTS_NAME_1_1
                        esg instance 1 iso certs name 1
  -esg_iso_certs_cert_id_1_1 ESG_ISO_CERTS_CERT_ID_1_1, --esg_iso_certs_cert_id_1_1 ESG_ISO_CERTS_CERT_ID_1_1
                        esg instance 1 iso certs cert id 1
  -esg_iso_certs_key_1_1 ESG_ISO_CERTS_KEY_1_1, --esg_iso_certs_key_1_1 ESG_ISO_CERTS_KEY_1_1
                        esg instance 1 iso certs key 1
  -esg_iso_certs_cert_1_1 ESG_ISO_CERTS_CERT_1_1, --esg_iso_certs_cert_1_1 ESG_ISO_CERTS_CERT_1_1
                        esg instance 1 iso certs cert 1
  -esg_iso_certs_config_switch_1_1 ESG_ISO_CERTS_CONFIG_SWITCH_1_1, --esg_iso_certs_config_switch_1_1 ESG_ISO_CERTS_CONFIG_SWITCH_1_1
                        esg instance 1 iso certs config switch 1
  -esg_iso_certs_config_ou_1_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_1_1, --esg_iso_certs_config_org_unit_1_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_1_1
                        esg instance 1 iso certs config org unit 1
  -esg_iso_certs_config_cc_1_1 ESG_ISO_CERTS_CONFIG_COUNTRY_1_1, --esg_iso_certs_config_country_1_1 ESG_ISO_CERTS_CONFIG_COUNTRY_1_1
                        esg instance 1 iso certs config country 1
  -esg_iso_certs_config_domains_1_1 ESG_ISO_CERTS_CONFIG_DOMAINS_1_1, --esg_iso_certs_config_domains_1_1 ESG_ISO_CERTS_CONFIG_DOMAINS_1_1
                        esg instance 1 iso certs config domains 1
  -esg_iso_certs_2_1 ESG_ISO_CERTS_NAME_2_1, --esg_iso_certs_name_2_1 ESG_ISO_CERTS_NAME_2_1
                        esg instance 1 iso certs name 2
  -esg_iso_certs_cert_id_2_1 ESG_ISO_CERTS_CERT_ID_2_1, --esg_iso_certs_cert_id_2_1 ESG_ISO_CERTS_CERT_ID_2_1
                        esg instance 1 iso certs cert id 2
  -esg_iso_certs_key_2_1 ESG_ISO_CERTS_KEY_2_1, --esg_iso_certs_key_2_1 ESG_ISO_CERTS_KEY_2_1
                        esg instance 1 iso certs key 2
  -esg_iso_certs_cert_2_1 ESG_ISO_CERTS_CERT_2_1, --esg_iso_certs_cert_2_1 ESG_ISO_CERTS_CERT_2_1
                        esg instance 1 iso certs cert 2
  -esg_iso_certs_config_switch_2_1 ESG_ISO_CERTS_CONFIG_SWITCH_2_1, --esg_iso_certs_config_switch_2_1 ESG_ISO_CERTS_CONFIG_SWITCH_2_1
                        esg instance 1 iso certs config switch 2
  -esg_iso_certs_config_ou_2_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_2_1, --esg_iso_certs_config_org_unit_2_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_2_1
                        esg instance 1 iso certs config org unit 2
  -esg_iso_certs_config_cc_2_1 ESG_ISO_CERTS_CONFIG_COUNTRY_2_1, --esg_iso_certs_config_country_2_1 ESG_ISO_CERTS_CONFIG_COUNTRY_2_1
                        esg instance 1 iso certs config country 2
  -esg_iso_certs_config_domains_2_1 ESG_ISO_CERTS_CONFIG_DOMAINS_2_1, --esg_iso_certs_config_domains_2_1 ESG_ISO_CERTS_CONFIG_DOMAINS_2_1
                        esg instance 1 iso certs config domains 2
  -esg_iso_certs_3_1 ESG_ISO_CERTS_NAME_3_1, --esg_iso_certs_name_3_1 ESG_ISO_CERTS_NAME_3_1
                        esg instance 1 iso certs name 3
  -esg_iso_certs_cert_id_3_1 ESG_ISO_CERTS_CERT_ID_3_1, --esg_iso_certs_cert_id_3_1 ESG_ISO_CERTS_CERT_ID_3_1
                        esg instance 1 iso certs cert id 3
  -esg_iso_certs_key_3_1 ESG_ISO_CERTS_KEY_3_1, --esg_iso_certs_key_3_1 ESG_ISO_CERTS_KEY_3_1
                        esg instance 1 iso certs key 3
  -esg_iso_certs_cert_3_1 ESG_ISO_CERTS_CERT_3_1, --esg_iso_certs_cert_3_1 ESG_ISO_CERTS_CERT_3_1
                        esg instance 1 iso certs cert 3
  -esg_iso_certs_config_switch_3_1 ESG_ISO_CERTS_CONFIG_SWITCH_3_1, --esg_iso_certs_config_switch_3_1 ESG_ISO_CERTS_CONFIG_SWITCH_3_1
                        esg instance 1 iso certs config switch 3
  -esg_iso_certs_config_ou_3_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_3_1, --esg_iso_certs_config_org_unit_3_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_3_1
                        esg instance 1 iso certs config org unit 3
  -esg_iso_certs_config_cc_3_1 ESG_ISO_CERTS_CONFIG_COUNTRY_3_1, --esg_iso_certs_config_country_3_1 ESG_ISO_CERTS_CONFIG_COUNTRY_3_1
                        esg instance 1 iso certs config country 3
  -esg_iso_certs_config_domains_3_1 ESG_ISO_CERTS_CONFIG_DOMAINS_3_1, --esg_iso_certs_config_domains_3_1 ESG_ISO_CERTS_CONFIG_DOMAINS_3_1
                        esg instance 1 iso certs config domains 3
  -esg_iso_certs_4_1 ESG_ISO_CERTS_NAME_4_1, --esg_iso_certs_name_4_1 ESG_ISO_CERTS_NAME_4_1
                        esg instance 1 iso certs name 4
  -esg_iso_certs_cert_id_4_1 ESG_ISO_CERTS_CERT_ID_4_1, --esg_iso_certs_cert_id_4_1 ESG_ISO_CERTS_CERT_ID_4_1
                        esg instance 1 iso certs cert id 4
  -esg_iso_certs_key_4_1 ESG_ISO_CERTS_KEY_4_1, --esg_iso_certs_key_4_1 ESG_ISO_CERTS_KEY_4_1
                        esg instance 1 iso certs key 4
  -esg_iso_certs_cert_4_1 ESG_ISO_CERTS_CERT_4_1, --esg_iso_certs_cert_4_1 ESG_ISO_CERTS_CERT_4_1
                        esg instance 1 iso certs cert 4
  -esg_iso_certs_config_switch_4_1 ESG_ISO_CERTS_CONFIG_SWITCH_4_1, --esg_iso_certs_config_switch_4_1 ESG_ISO_CERTS_CONFIG_SWITCH_4_1
                        esg instance 1 iso certs config switch 4
  -esg_iso_certs_config_ou_4_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_4_1, --esg_iso_certs_config_org_unit_4_1 ESG_ISO_CERTS_CONFIG_ORG_UNIT_4_1
                        esg instance 1 iso certs config org unit 4
  -esg_iso_certs_config_cc_4_1 ESG_ISO_CERTS_CONFIG_COUNTRY_4_1, --esg_iso_certs_config_country_4_1 ESG_ISO_CERTS_CONFIG_COUNTRY_4_1
                        esg instance 1 iso certs config country 4
  -esg_iso_certs_config_domains_4_1 ESG_ISO_CERTS_CONFIG_DOMAINS_4_1, --esg_iso_certs_config_domains_4_1 ESG_ISO_CERTS_CONFIG_DOMAINS_4_1
                        esg instance 1 iso certs config domains 4
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
  -nsxmanager_addr NSXMANAGER_ADDRESS, --nsxmanager_address NSXMANAGER_ADDRESS
                        nsxmanager address
  -nsxmanager_en_dlr NSXMANAGER_ENABLE_DLR, --nsxmanager_enable_dlr NSXMANAGER_ENABLE_DLR
                        nsxmanager enable dlr
  -nsxmanager_bosh_nsx_enabled NSXMANAGER_BOSH_NSX_ENABLED, --nsxmanager_bosh_nsx_enabled NSXMANAGER_BOSH_NSX_ENABLED
                        nsxmanager bosh nsx enabled
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

```
