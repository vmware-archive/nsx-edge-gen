#!/bin/bash
echo "Use build, list, delete"
echo "Default option: list"
echo ""

RUN_CMD=${1:-list}
CONFIG_NAME=test-nsx
rm -rf $CONFIG_NAME

./nsx-gen/bin/nsxgen -i $CONFIG_NAME init

./nsx-gen/bin/nsxgen -c $CONFIG_NAME  \
  -esg_name_1 edge1 \
  -esg_size_1 compact \
  -esg_cli_user_1 admin \
  -esg_cli_pass_1 'P1v0t4l!P1v0t4l!' \
  -esg_ert_certs_1 Foundation1 \
  -nsxmanager_dportgroup DPortGroupTest \
  -nsxmanager_en_dlr true \
  -nsxmanager_bosh_nsx_enabled true \
  -nsxmanager_tz TestTZ \
  -nsxmanager_tz_clusters 'Cluster1,Cluster2' \
  -esg_ert_certs_config_sysd_1 sys2.test.pivotal.io \
  -esg_ert_certs_config_appd_1 apps3.test.pivotal.io \
  -esg_iso_certs_1_1 iso-1 \
  -esg_iso_certs_config_switch_1_1 IsoZone-1 \
  -esg_iso_certs_config_ou_1_1 Pivotal \
  -esg_iso_certs_config_cc_1_1 US \
  -esg_iso_certs_config_domains_1_1 zone1-app.test.pivotal.io \
  -esg_opsmgr_uplink_ip_1 10.193.99.171 \
  -esg_go_router_uplink_ip_1 10.193.99.172 \
  -esg_diego_brain_uplink_ip_1 10.193.99.173 \
  -esg_tcp_router_uplink_ip_1 10.193.99.174 \
  -esg_go_router_ssl_term_1 true \
  -esg_mysql_ert_uplink_ip_1 192.168.23.250 \
  -esg_mysql_ert_inst_1 5  \
  -esg_mysql_tile_uplink_ip_1 192.168.27.250 \
  -esg_mysql_tile_inst_1 2  \
  -esg_rabbitmq_tile_uplink_ip_1 192.168.27.251 \
  -esg_rabbitmq_tile_inst_1 5 \
  -esg_rabbitmq_tile_off_1 10 \
  -vcenter_addr vcsa-01.test.pivotal.io \
  -vcenter_user administrator@vsphere.local \
  -vcenter_pass 'passwd!' \
  -vcenter_dc "" \
  -vcenter_ds vsanDatastore \
  -vcenter_cluster Cluster1 \
  -nsxmanager_addr 10.193.99.20 \
  -nsxmanager_user admin \
  -nsxmanager_pass 'passwd!' \
  -nsxmanager_uplink_ip 10.193.99.170 \
  -nsxmanager_uplink_port 'VM Network' \
  -esg_gateway_1 10.193.99.1  \
 -isozone_switch_name_1 IsoZone-1 \
 -isozone_switch_cidr_1 192.168.34.0/22 \
 -isozone_switch_name_2 IsoZone-2 \
 -isozone_switch_cidr_2 192.168.38.0/22 \
 -esg_go_router_isozone_1_uplink_ip_1  10.193.99.181 \
 -esg_go_router_isozone_1_switch_1 IsoZone-1  \
 -esg_go_router_isozone_1_inst_1 2 \
 -esg_tcp_router_isozone_1_uplink_ip_1  10.193.99.182 \
 -esg_tcp_router_isozone_1_switch_1  IsoZone-1 \
 -esg_tcp_router_isozone_1_inst_1 2 \
 -esg_go_router_isozone_1_ssl_term_1 false \
 -esg_go_router_isozone_2_uplink_ip_1  10.193.99.184 \
 -esg_go_router_isozone_2_inst_1 1 \
 -esg_go_router_isozone_2_switch_1 IsoZone-2 \
 -esg_tcp_router_isozone_2_uplink_ip_1  10.193.99.185 \
 -esg_tcp_router_isozone_2_switch_1  IsoZone-2 \
 -esg_tcp_router_isozone_2_inst_1 2 \
 -export_dir export-output \
$RUN_CMD

  # -esg_iso_certs_2_1  iso-2 \
  # -esg_iso_certs_config_switch_2_1 IsoZone-2 \
  # -esg_iso_certs_config_ou_2_1 Pivotal \
  # -esg_iso_certs_config_cc_2_1 US \
  # -esg_iso_certs_config_domains_2_1 zone2-app.test.pivotal.io \


 #  -nsxmanager_sr_name teststatic \
 #  -nsxmanager_sr_subnet 10.0.0.0/8 \
 #  -nsxmanager_sr_gateway 10.114.216.180 \
 #  -nsxmanager_sr_hop 1 \
 # -isozone_switch_name_1 IsoZone-1 \
 # -isozone_switch_cidr_1 192.168.34.0/22 \
 # -isozone_switch_name_2 IsoZone-2 \
 # -isozone_switch_cidr_2 192.168.38.0/22 \
 # -isozone_switch_name_3 IsoZone-3 \
 # -isozone_switch_cidr_3 192.168.42.0/22 \
 # -esg_go_router_isozone_1_uplink_ip_1  10.193.99.181 \
 # -esg_go_router_isozone_1_switch_1 IsoZone-1  \
 # -esg_go_router_isozone_1_inst_1 2 \
 # -esg_tcp_router_isozone_1_uplink_ip_1  10.193.99.182 \
 # -esg_tcp_router_isozone_1_switch_1  IsoZone-1 \
 # -esg_tcp_router_isozone_1_inst_1 2 \
 # -esg_go_router_isozone_2_uplink_ip_1  10.193.99.184 \
 # -esg_go_router_isozone_2_inst_1 1 \
 # -esg_go_router_isozone_2_switch_1 IsoZone-2 \
 # -esg_tcp_router_isozone_2_uplink_ip_1  10.193.99.185 \
 # -esg_tcp_router_isozone_2_switch_1  IsoZone-2 \
 # -esg_tcp_router_isozone_2_inst_1 2 \

#  -esg_go_router_isozone_1_uplink_ip_1 10.193.99.175 \
#  -esg_tcp_router_isozone_1_uplink_ip_1 10.193.99.176 \
#   -esg_go_router_isozone_2_switch_1 IsoZone-2 \
