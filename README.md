<div align="center">

# Logstail Agent

</div>

![Logstail Logo](https://apps.logstail.com/static/media/logstail_text_logo.5c0a8cbe.png)

Logstail Unified Agent Installation script


# **Requirements**
* Python3.6 or newer version
* A supported OS by Logstail Agent (Windows, Debian, Linux, RedHat)

# **How to run the script**
1. Download the repository and go inside the Logstail_Agent folder where the source code is located.
2. Open a terminal. (Make sure you have root/ admin privilages)
3. Use python to execute the main.py file
```
python3 main.py
 ```
or
 ```
 python main.py
 ```
5. The script will auto-detect your operating system. Make sure the installation is correct!
  ```
Welcome to Logstail Agent Instalation
--------------------------------
Gathering System info...
Detected windows amd64.
--------------------------------
Is this the operating system type you want to install for? (Y/n):
```
5. Select the component you want to install
```
--------------------------------
Select your monitoring component
1: Logs Collection
2: Metric Collection
3: Network Traffic
4: Uptime Monitoring
5: Security Monitoring (SIEM)
Q: Quit
--------------------------------
Select Component:
```
+ **Logs Collection:** Logs component is a lightweight shipper for forwarding and centralizing log data. Installed as an agent on your servers, it monitors the log files or locations that you specify, collects log events, and forwards them to Logstail Servers for indexing.
+ **Metric Collection:** Metrics component is a lightweight shipper that you can install on your servers to periodically collect metrics from the operating system and from services running on the server. It takes the metrics and statistics that it collects and ships them to the Logstail Servers.
+ **Network Traffic:** Network component is a lightweight network packet analyzer that sends data from your hosts and containers to Logstail Servers. It supports many application layer protocols, from database to key-value stores to HTTP and low-level protocols. It provides visibility between the servers of your network
+ **Uptime Monitoring:** Uptime component is a lightweight daemon that periodically checks the status and response time of your services using ICMP, TCP, or HTTP. Uptime monitors whether your services are available and reachable.
+ **Security Monitoring (SIEM):** SIEM is a multi-platform component that runs on endpoints to monitor their security. It provides prevention, detection, and response capabilities for different threats. It can be deployed to various operating systems and devices, such as Linux, Windows, macOS, Solaris, AIX, laptops, desktops, servers, cloud instances, containers, or virtual machines. It communicates with the Logstail Correlation server, sending data in near real-time through an encrypted and authenticated channel. To access SIEM you must have an enterprise plan in Logstail Platform!

6. Select one of the available options
 ```
Select your option
1: Install
2: Status
3: Show modules
4: Enable module
5: Disable module
6: Restart Collector
7: Uninstal
Q: Quit
Enter an option:
```
+ **Install:** Installs the selected collector to the system and enables it. To install a collector make sure you have copied your Logstail Client Token from https://apps.logstail.com/home/overview
+ **Status:** Prints the current status of the selected collector. If the status is **OK** or **RUNNING** you are good to go! Else check your confifuration. If you cant solve the issue contact Logstail Support!
+ **Show modules:** Prints all the available modules of a collector and their status (enabled, disabled). Only enabled and properly configured modules gather and ship logs and metrics to Logstail Platform.
+ **Enable module:** Use this option to enable a module on the selected collector. Make sure to use the above option first to view all the available modules! **NOTE:** Some module require extra configuration, follow our guides to properly configure them. https://apps.logstail.com/shippers
  After enabling a module make sure to Add the related dashboard from https://apps.logstail.com/apps2go and start analyzing your data. If the dashboard is empty make sure your configuration is correct!
  If you need help contact Logstail Support!
+ **Disable module:** Use this option to disable an already enabled module. After disabling a module you will no longer be able to view data related to this module on the platform.
+ **Restart Collector:** Use this option to restart the selected collector. We recommend running this option when you manually alter the configuration or when your data are not getting shipped to the Logstail Platform!
+ **Uninstall:** Use this option to uninstall the selected collector. After uninstalling a collector any data related to this collector will stop getting shipped to Logstail Platform.


# **Extras**
+ To install the Security Monitoring (SIEM) collector you must first get in touch with us. Also this collector is included in the Enterprise Plan.  
+ If you wish to ship data from a non-supported source contact us and we will develop this source at no-cost.
+ If you find any bugs while running the script let us know and we will get it patched as soon as possible.
