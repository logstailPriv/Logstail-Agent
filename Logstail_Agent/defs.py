'''
Unless explicitly stated otherwise all files in this repository are licensed
under the Apache License Version 2.0.
This product includes software developed at Logstail (https://logstail.com/).
Copyright 2023-present Logstail
'''

CERT = "https://raw.githubusercontent.com/logstail/public-certs/master/SectigoRSADomainValidationSecureServerCA.crt"

URLS = {"debian" :
 {"x86_64":{
       "metrics": "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-oss-8.8.1-amd64.deb",
       "logs": "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-8.8.1-amd64.deb",
       "uptime": "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-oss-8.8.1-amd64.deb",
       "network": "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-8.8.1-amd64.deb",
       "siem": "https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.4.4-1_amd64.deb"},
  "aarch64":{
       "metrics": "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-oss-8.8.1-arm64.deb",
       "logs": "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-8.8.1-arm64.deb",
       "uptime": "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-oss-8.8.1-arm64.deb",
       "network": "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-8.8.1-arm64.deb",
       "siem": "https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.4.4-1_arm64.deb"}
},
"rpm" :
 {"x86_64":{
       "metrics": "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-oss-8.8.1-x86_64.rpm",
       "logs": "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-8.8.1-x86_64.rpm",
       "uptime": "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-oss-8.8.1-x86_64.rpm",
       "network": "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-8.8.1-x86_64.rpm",
       "siem": "https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.4.4-1_x86_64.rpm"},
  "aarch64":{
       "metrics": "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-oss-8.8.1-aarch64.rpm",
       "logs": "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-8.8.1-aarch64.rpm",
       "uptime": "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-oss-8.8.1-aarch64.rpm",
       "network": "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-8.8.1-aarch64.rpm",
       "siem": "https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.4.4-1_aarch64.rpm"}
},
"linux" :
 {"x86_64":{
       "metrics": "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-oss-8.8.1-linux-x86_64.tar.gz",
       "logs": "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-8.8.1-linux-x86_64.tar.gz",
       "uptime": "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-oss-8.8.1-linux-x86_64.tar.gz",
       "network": "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-8.8.1-linux-x86_64.tar.gz",
       "siem": "https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.4.4-1_linux-x86_64.tar.gz"},
  "aarch64":{
       "metrics": "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-oss-8.8.1-linux-arm64.tar.gz",
       "logs": "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-8.8.1-linux-arm64.tar.gz",
       "uptime": "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-oss-8.8.1-linux-arm64.tar.gz",
       "network": "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-8.8.1-linux-arm64.tar.gz",
       "siem": "https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.4.4-1_linux-arm64.tar.gz"}
},
}


URLS_WIN = {"metrics": "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-oss-8.8.2-windows-x86_64.zip",
       "logs": "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-8.8.2-windows-x86_64.zip",
       "uptime": "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-oss-8.8.2-windows-x86_64.zip",
       "network": "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-8.8.2-windows-x86_64.zip",
       "siem": "https://packages.wazuh.com/4.x/windows/wazuh-agent-4.4.4-1.msi"}


MAPPINGS = {'metrics':'metricbeat',
            'logs': 'filebeat',
            'uptime': 'heartbeat',
            'network': 'packetbeat',
            'windows': 'winlogbeat',
            'siem': 'wazuh-agent'} #change
