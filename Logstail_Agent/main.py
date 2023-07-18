'''
Unless explicitly stated otherwise all files in this repository are licensed
under the Apache License Version 2.0.
This product includes software developed at Logstail (https://logstail.com/).
Copyright 2023-present Logstail
'''
import ssl
import time
import os
import platform
import urllib.request
import subprocess
import re
#deb
from debian_agent import install as deb_install
from debian_agent import install_siem as deb_install_siem
from debian_agent import show_status as deb_status
from debian_agent import show_modules as deb_show_modules
from debian_agent import enable_module as deb_enable_module
from debian_agent import disable_module as deb_disable_module
from debian_agent import restart as deb_restart
from debian_agent import uninstall as deb_uninstall
#rpm
from rpm_agent import install as rpm_install
from rpm_agent import install_siem as rpm_install_siem
from rpm_agent import show_status as rpm_status
from rpm_agent import show_modules as rpm_show_modules
from rpm_agent import enable_module as rpm_enable_module
from rpm_agent import disable_module as rpm_disable_module
from rpm_agent import restart as rpm_restart
from rpm_agent import uninstall as rpm_uninstall
#linux
from linux_agent import install as linux_install
from linux_agent import install_siem as linux_install_siem
from linux_agent import show_status as linux_status
from linux_agent import show_modules as linux_show_modules
from linux_agent import enable_module as linux_enable_module
from linux_agent import disable_module as linux_disable_module
from linux_agent import restart as linux_restart
from linux_agent import uninstall as linux_uninstall
#windows
from win_agent import install as win_install
from win_agent import show_modules as win_show_modules
from win_agent import enable_module as win_enable_module
from win_agent import disable_module as win_disable_module
from win_agent import show_status as win_status
from win_agent import restart as win_restart
from win_agent import install_siem as win_install_siem
from win_agent import uninstall as win_uninstall
from win_agent import uninstall_siem as win_uninstall_siem
from welcome import welcome

def extract_ports(string):
    match = re.search(r'LogstailEnterprise(\d+)#(\d+)', string)
    if match:
        number1 = match.group(1)
        number2 = match.group(2)
        return number1, number2
    else:
        return None

def print_agent_components():
    print('--------------------------------')
    print('Select your monitoring component')
    print('1: Logs Collection')
    print('2: Metric Collection')
    print('3: Network Traffic')
    print('4: Uptime Monitoring')
    print('5: Security Monitoring (SIEM)')
    print('Q: Quit')
    print('--------------------------------')

def print_collectors_options():
    print('--------------------------------')
    print('Select your option')
    print('1: Install')
    print('2: Status')
    print('3: Show modules')
    print('4: Enable module')
    print('5: Disable module')
    print('6: Restart Collector')
    print('7: Uninstal')
    print('Q: Quit')
    print('--------------------------------')

def collectors_options_input():
   COLLECTORS_OPTIONS_INPUTS = ['1', '2', '3', '4', '5', '6', '7', 'Q']
   print_collectors_options()
   user_input = input(f'Enter an option: ')
   while user_input not in COLLECTORS_OPTIONS_INPUTS:
      print(f'Invalid input!')
      print_collectors_options()
      user_input = input(f'Enter an option: ')
   return user_input

def collector_functions(option, user_os, user_arch, component):
    if user_os == 'debian':
       if option == '1':
          if component != 'siem':
             print(f'Get your token from the Logstail Platform!')
             user_token = input(f'Enter your Logstail Token: ')
             deb_install(user_os, component, user_arch, user_token) #REMEMBER to change to vars
          else:
             print(f'Contact Logstail team to get the unique Logstail Enterprise key to setup Cloud SIEM. ')
             logstail_key = input(f'Enter your unique Logstail Enterprise key: ')
             result = extract_ports(logstail_key)
             if result:
                logs_port, auth_port = result
             else:
                print("Logstail Enterprise key not correct.\nContact support@logstail.com")
                return
             agent_name = input(f'Enter a name for your agent (If you have more that one agents make sure it\'s unique): ')
             deb_install_siem(user_os, component, user_arch, logs_port, auth_port, agent_name)
          return
       elif option == '2':
          #status
          deb_status(component)
          return
       elif option == '3':
          #show modules
          deb_show_modules(component) #REMEMBER to change to vars
          return
       elif option == '4':
          #enable module
          deb_enable_module(component) #REMEMBER to change to vars
          return
       elif option == '5':
          #disable module
          deb_disable_module(component) #REMEMBER to change to vars
          return
       elif option == '6':
          #Restart
          deb_restart(component)  #REMEMBER to change to vars
          return
       elif option == '7':
          if (input(f'You are about to unistall {component} collector. Are you sure? (Y/n): ') == 'Y'):
             if component == 'siem':
                deb_uninstall_siem(user_os, component, user_arch)
             else:
                deb_uninstall(component)
          return
       elif option == 'Q':
          #exit()
          return
    elif user_os == 'windows':
       if option == '1':
          if component != 'siem':
             print(f'Get your token from the Logstail Platform!')
             user_token = input(f'Enter your Logstail Token: ')
             win_install(user_os, component, 'x86_64', user_token) #REMEMBER to change to vars
          else:
             print(f'Contact Logstail team to get the unique Logstail Enterprise key to setup Cloud SIEM. ')
             logstail_key = input(f'Enter your unique Logstail Enterprise key: ')
             result = extract_ports(logstail_key)
             if result:
                logs_port, auth_port = result
             else:
                print("Logstail Enterprise key not correct.\nContact support@logstail.com")
                return
             #logs_port = input(f'Enter the port for the log shipping: ')
             #auth_port = input(f'Enter the port for authentication: ')
             agent_name = input(f'Enter a name for your agent (If you have more that one agents make sure it\'s unique): ')
             win_install_siem(user_os, component, user_arch, logs_port, auth_port, agent_name)
          return
       elif option == '2':
          #status
          win_status(component)
          return
       elif option == '3':
          #show modules
          win_show_modules(component) #REMEMBER to change to vars
          return
       elif option == '4':
          #enable module
          win_enable_module(component) #REMEMBER to change to vars
          return
       elif option == '5':
          #disable module
          win_disable_module(component) #REMEMBER to change to vars
          return
       elif option == '6':
          #Restart
          win_restart(component)  #REMEMBER to change to vars
          return
       elif option == '7':
          if (input(f'You are about to unistall {component} collector. Are you sure? (Y/n): ') == 'Y'):
             if component == 'siem':
                win_uninstall_siem(user_os, component, user_arch)
             else:                   
                win_uninstall(component)
          return
       elif option == 'Q':
          #exit()
          return
    elif user_os == 'linux':
       if option == '1':
          if component != 'siem':
             print(f'Get your token from the Logstail Platform!')
             user_token = input(f'Enter your Logstail Token: ')
             linux_install(user_os, component, user_arch, user_token) #REMEMBER to change to vars
          else:
             print(f'Contact Logstail team to get the unique Logstail Enterprise key to setup Cloud SIEM. ')
             logstail_key = input(f'Enter your unique Logstail Enterprise key: ')
             result = extract_ports(logstail_key)
             if result:
                logs_port, auth_port = result
             else:
                print("Logstail Enterprise key not correct.\nContact support@logstail.com")
                return
             agent_name = input(f'Enter a name for your agent (If you have more that one agents make sure it\'s unique): ')
             linux_install_siem(user_os, component, user_arch, logs_port, auth_port, agent_name)
          return
       elif option == '2':
          #status
          linux_status(component)
          return
       elif option == '3':
          #show modules
          linux_show_modules(component) #REMEMBER to change to vars
          return
       elif option == '4':
          #enable module
          linux_enable_module(component) #REMEMBER to change to vars
          return
       elif option == '5':
          #disable module
          linux_disable_module(component) #REMEMBER to change to vars
          return
       elif option == '6':
          #Restart
          linux_restart(component)  #REMEMBER to change to vars
          return
       elif option == '7':
          if (input(f'You are about to unistall {component} collector. Are you sure? (Y/n): ') == 'Y'):
             if component == 'siem':
                linux_uninstall_siem(user_os, component, user_arch)
             else:
                linux_uninstall(component)
          return
       elif option == 'Q':
          #exit()
          return  
    elif user_os == 'rpm':
       if option == '1':
          if component != 'siem':
             print(f'Get your token from the Logstail Platform!')
             user_token = input(f'Enter your Logstail Token: ')
             rpm_install(user_os, component, user_arch, user_token) #REMEMBER to change to vars
          else:
             print(f'Contact Logstail team to get the unique Logstail Enterprise key to setup Cloud SIEM. ')
             logstail_key = input(f'Enter your unique Logstail Enterprise key: ')
             result = extract_ports(logstail_key)
             if result:
                logs_port, auth_port = result
             else:
                print("Logstail Enterprise key not correct.\nContact support@logstail.com")
                return
             agent_name = input(f'Enter a name for your agent (If you have more that one agents make sure it\'s unique): ')
             rpm_install_siem(user_os, component, user_arch, logs_port, auth_port, agent_name)
          return
       elif option == '2':
          #status
          rpm_status(component)
          return
       elif option == '3':
          #show modules
          rpm_show_modules(component) #REMEMBER to change to vars
          return
       elif option == '4':
          #enable module
          rpm_enable_module(component) #REMEMBER to change to vars
          return
       elif option == '5':
          #disable module
          rpm_disable_module(component) #REMEMBER to change to vars
          return
       elif option == '6':
          #Restart
          rpm_restart(component)  #REMEMBER to change to vars
          return
       elif option == '7':
          if (input(f'You are about to unistall {component} collector. Are you sure? (Y/n): ') == 'Y'):
             if component == 'siem':
                rpm_uninstall_siem(user_os, component, user_arch)
             else:
                rpm_uninstall(component)
          return
       elif option == 'Q':
          #exit()
          return          
    
          
def agent_component_input():
   COMPONENTS_INPUTS = ['1', '2', '3', '4', '5', 'Q']
   user_input = ''
   while user_input != 'Q':
      print_agent_components()
      user_input = input(f'Select Component: ')
      while user_input not in COMPONENTS_INPUTS:
         print(f'Invalid input!')
         print_agent_components()
         user_input = input(f'Select Component: ')
      return user_input


if __name__ == "__main__":
   OS_INPUTS = ['1', '2', 'Q']
   welcome()
   print(ssl.OPENSSL_VERSION)
   print(f'Gathering System info...')
#   time.sleep(3)
   user_os = platform.system().lower()
   user_os_detail = platform.machine().lower()
   print(f'Detected {user_os} {user_os_detail}.')
   print(f'--------------------------------')
   is_correct = input(f'Is this the operating system type you want to install for? (Y/n): ')
   if is_correct == 'n':
      print(f'--------------------------------')
      user_os = input('Enter your Operating System name (linux, windows, etc): ')
      user_os_detail = input('Enter your Operating System Architecture: (aarch, x86_64 etc): ')
      print(f'--------------------------------')
   component = agent_component_input()
   while component != 'Q':
      #Print Descriptions
      if component == '1': #logs
         print(f'Logs component is a lightweight shipper for forwarding and centralizing log data. Installed as an agent on your servers, it monitors the log files or locations that you specify, collects log events, and forwards them to Logstail Servers for indexing.')
      elif component == '2': #metrics
         print(f'Metrics component is a lightweight shipper that you can install on your servers to periodically collect metrics from the operating system and from services running on the server. It takes the metrics and statistics that it collects and ships them to the Logstail Servers.')
      elif component == '3': #network
         print(f'Network component is a lightweight network packet analyzer that sends data from your hosts and containers to Logstail Servers. It supports many application layer protocols, from database to key-value stores to HTTP and low-level protocols. It provides visibility between the servers of your network')
      elif component == '4': #uptime
         print(f'Uptime component is a lightweight daemon that periodically checks the status and response time of your services using ICMP, TCP, or HTTP. Uptime monitors whether your services are available and reachable.')
      elif component == '5': #siem
         print(f'SIEM is a multi-platform component that runs on endpoints to monitor their security. It provides prevention, detection, and response capabilities for different threats. It can be deployed to various operating systems and devices, such as Linux, Windows, macOS, Solaris, AIX, laptops, desktops, servers, cloud instances, containers, or virtual machines. It communicates with the Logstail Correlation server, sending data in near real-time through an encrypted and authenticated channel.')
         print(f'---ATTENTION---')
         print(f'To access SIEM you must have an enterprise plan in Logstail Platform.\nContact us now at sales@logstail.com')
      option = 0 #Initialize   
      while option != 'Q':
         if component == '1': #logs
            option = collectors_options_input()
            collector_functions(option, user_os, user_os_detail, 'logs')
         elif component == '2': #metrics
            option = collectors_options_input()
            collector_functions(option, user_os, user_os_detail, 'metrics')
         elif component == '3': #network
            option = collectors_options_input()
            collector_functions(option, user_os, user_os_detail, 'network')
         elif component == '4': #uptime
            option = collectors_options_input()
            collector_functions(option, user_os, user_os_detail, 'uptime')
         elif component == '5': #siem
            option = collectors_options_input()
            collector_functions(option, 'debian', user_os_detail, 'siem')
      component = agent_component_input()
