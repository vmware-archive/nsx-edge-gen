#!/bin/bash
#mglynn@pivotal.io

set -e

if [ $# -lt 2 ]; then
  echo "Run certGen.sh with arguments!!"
  echo "./certGen.sh system-domain app-domain [output-directory] [org-unit] [2-letter country code] [vip]"
  echo "Example: ./certGen.sh pcf-sys.corp.local pcf-app.corp.local . Pivotal US"
  echo "Default for output-directory: . (assumes current working directory)"
  echo "Default for org-unit: Pivotal"
  echo "Default for country: US"
  exit
fi

SYS_DOMAIN=$1
APP_DOMAIN=$2
OUTPUT_DIR=${3:-.}
ORG_UNIT=${4:-Pivotal}
COUNTRY=${5:-US}

VIP=$6

mkdir -p $OUTPUT_DIR
SSL_FILE=${OUTPUT_DIR}/sslconf-${SYS_DOMAIN}.conf

#Generate SSL Config with SANs
if [ ! -f $SSL_FILE ]; then
 cat > $SSL_FILE <<EOM
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
[req_distinguished_name]
#countryName = Country Name (2 letter code)
#countryName_default = US
#stateOrProvinceName = State or Province Name (full name)
#stateOrProvinceName_default = TX
#localityName = Locality Name (eg, city)
#localityName_default = Frisco
#organizationalUnitName     = Organizational Unit Name (eg, section)
#organizationalUnitName_default   = Pivotal Labs
#commonName = Pivotal
#commonName_max = 64
[ v3_req ]
# Extensions to add to a certificate request
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = *.${SYS_DOMAIN}
#IP.1 = ${VIP}
DNS.2 = *.login.${SYS_DOMAIN}
#IP.2 = ${VIP}
DNS.3 = *.uaa.${SYS_DOMAIN}
#IP.3 = ${VIP}
DNS.4 = *.${APP_DOMAIN}
#IP.4 = ${VIP}
EOM
fi

openssl genrsa -out ${OUTPUT_DIR}/${SYS_DOMAIN}.key 2048 >/dev/null 2>&1

openssl req -new -out ${OUTPUT_DIR}/${SYS_DOMAIN}.csr                   \
                 -subj "/CN=*.${SYS_DOMAIN}/O=${ORG_UNIT}/C=${COUNTRY}" \
                 -key ${OUTPUT_DIR}/${SYS_DOMAIN}.key                   \
                 -config ${SSL_FILE}                                    \
                 >/dev/null 2>&1

openssl req -text -noout -in ${OUTPUT_DIR}/${SYS_DOMAIN}.csr >/dev/null 2>&1

openssl x509 -req -days 3650                              \
                 -in ${OUTPUT_DIR}/${SYS_DOMAIN}.csr      \
                 -signkey ${OUTPUT_DIR}/${SYS_DOMAIN}.key \
                 -out ${OUTPUT_DIR}/${SYS_DOMAIN}.crt     \
                 -extensions v3_req                       \
                 -extfile ${SSL_FILE}                     \
                 >/dev/null 2>&1

openssl x509 -in ${OUTPUT_DIR}/${SYS_DOMAIN}.crt -text -noout >/dev/null 2>&1

echo "Finished self-signed cert generation"
echo "      App Domain: ${APP_DOMAIN}"
echo "   System Domain: ${SYS_DOMAIN}"
echo ""