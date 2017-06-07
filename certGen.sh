#!/bin/bash
# author: mglynn@pivotal.io

set -e

if [ $# -lt 2 ]; then
  echo "Run certGen.sh with arguments!!"
  echo "./certGen.sh comma-separated-domain-names [output-directory] [org-unit] [2-letter country code]"
  echo "Example: ./certGen.sh pcf-sys.corp.local,pcf-app.corp.local . Pivotal US"
  echo "Default for output-directory: autogen"
  echo "Default for org-unit: Pivotal"
  echo "Default for country: US"
  exit
fi

DOMAINS=$1
OUTPUT_DIR=${2:-autogen}
ORG_UNIT=${3:-Pivotal}
COUNTRY=${4:-US}
#VIP=$5

rm -rf $OUTPUT_DIR 2>/dev/null
mkdir -p $OUTPUT_DIR

index=1
ROOT_DOMAIN=''
for domain in `echo $DOMAINS | sed -e 's/,/ /g' `
do
  index=$(expr $index + 1)
  if [ "$ROOT_DOMAIN" = "" ]; then
    ROOT_DOMAIN=$domain
  fi
  echo "DNS.$index = *.${domain}" >> $OUTPUT_DIR/app-domains.txt
done

SSL_FILE=${OUTPUT_DIR}/sslconf-${ROOT_DOMAIN}.conf

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
#stateOrProvinceName_default = CA
#localityName = Locality Name (eg, city)
#localityName_default = SanFrancisco
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
EOM
fi

cat $OUTPUT_DIR/app-domains.txt >> $SSL_FILE 

openssl genrsa -out ${OUTPUT_DIR}/${ROOT_DOMAIN}.key 2048 >/dev/null 2>&1

openssl req -new -out ${OUTPUT_DIR}/${ROOT_DOMAIN}.csr                   \
                 -subj "/CN=*.${ROOT_DOMAIN}/O=${ORG_UNIT}/C=${COUNTRY}" \
                 -key ${OUTPUT_DIR}/${ROOT_DOMAIN}.key                   \
                 -config ${SSL_FILE}                                    \
                 >/dev/null 2>&1

openssl req -text -noout -in ${OUTPUT_DIR}/${ROOT_DOMAIN}.csr >/dev/null 2>&1

openssl x509 -req -days 3650                              \
                 -in ${OUTPUT_DIR}/${ROOT_DOMAIN}.csr      \
                 -signkey ${OUTPUT_DIR}/${ROOT_DOMAIN}.key \
                 -out ${OUTPUT_DIR}/${ROOT_DOMAIN}.crt     \
                 -extensions v3_req                       \
                 -extfile ${SSL_FILE}                     \
                 >/dev/null 2>&1

openssl x509 -in ${OUTPUT_DIR}/${ROOT_DOMAIN}.crt -text -noout >/dev/null 2>&1

echo "Finished self-signed cert generation"
echo "      Domains: ${DOMAINS}"
echo ""