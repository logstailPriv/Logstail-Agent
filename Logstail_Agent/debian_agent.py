'''
Unless explicitly stated otherwise all files in this repository are licensed
under the Apache License Version 2.0.
This product includes software developed at Logstail (https://logstail.com/).
Copyright 2023-present Logstail
'''

import os
import re
import platform
import urllib.request
import subprocess
from defs import URLS
from defs import MAPPINGS
from defs import CERT
from reporthook import reporthook
from logger import write_to_log

def uptime_monitors(component):
   options = ['1', '2', '3', 'Q']
   #print available monitors:
   print(f'--------------------------------')
   print('Available Monitors')
   print('1: HTTP Monitor (Regularly checks the availability of a website or service by sending periodic requests)')
   print('2: TCP Monitor (Checks the availability of a TCP-based service by establishing and maintaining a connection.)')
   print('3: ICMP Monitor (Checks the availability of a network host using ICMP (Internet Control Message Protocol) echo requests.)')
   print('Q: Quit')
   monitor = input('Enter option: ')
   while monitor not in options:
      print('Error! Enter a correct option')
      monitor = input('Enter option: ')
   if monitor == '1':
      print(f'--------------------------------')
      print('HTTP Monitor Configuration')
      HOST_ID = input('Enter an ID for the monitor: ')
      HOST_NAME = input('Enter a name for the monitor: ')
      HOST_URL = input('Enter the url: ')
      print(f'--------------------------------')
      configure_uptime('http', HOST_ID, HOST_NAME, HOST_URL, -1, component)
   elif monitor == '2':
      print(f'--------------------------------')
      print('HTTP Monitor Configuration')
      HOST_ID = input('Enter an ID for the monitor: ')
      HOST_NAME = input('Enter a name for the monitor: ')
      HOST_URL = input('Enter the url: ')
      HOST_PORT = input('Enter the port: ')
      print(f'--------------------------------')
      configure_uptime('tcp', HOST_ID, HOST_NAME, HOST_URL, HOST_PORT, component)
   elif monitor == '3':
      print(f'--------------------------------')
      print('HTTP Monitor Configuration')
      HOST_ID = input('Enter an ID for the monitor: ')
      HOST_NAME = input('Enter a name for the monitor: ')
      HOST_URL = input('Enter the url: ')
      print(f'--------------------------------')
      configure_uptime('icmp', HOST_ID, HOST_NAME, HOST_URL, -1, component)
   elif monitor == 'Q':
      print('Exiting monitor setup..')
      return

def configure_uptime(name, HOST_ID, HOST_NAME, HOST_URL, HOST_PORT, component):
#   cwd_cert = 'C:/Program Files/Logstail-Agent'
   beat = map_to_beats(component)
   file = '/etc/{beat}/{beat}.yml'
   conf_file = os.getcwd() + f'/configs/{name}-monitor.yml'
   with open(file, 'r') as yaml_file:
      lines = yaml_file.readlines()
   for i,line in enumerate(lines):
      if '#New Monitor' in line:
         with open(conf_file, 'r') as mon_file:
            mon_lines = mon_file.readlines()
         #replace variables
            for j, mon_line in enumerate(mon_lines):
               if 'HOST_ID' in mon_line:
                  mon_lines[j] = re.sub('HOST_ID', HOST_ID, mon_line)
               if 'HOST_NAME' in mon_line:
                  mon_lines[j] = re.sub('HOST_NAME', HOST_NAME, mon_line)
               if 'HOST_URL' in mon_line:
                  mon_lines[j] = re.sub('HOST_URL', HOST_URL, mon_line)
               if 'HOST_PORT' in mon_line:
                  mon_lines[j] = re.sub('HOST_PORT', HOST_PORT, mon_line)
         #replace in yaml
         print(mon_lines)
         lines[i:i+1] = mon_lines
         break
   #save
   with open(file, 'w') as output_file:
      output_file.writelines(lines)
   write_to_log(f'{component} collector {name} monitor enabled', '/var/log/Logstail/agent.log')
   print(f'--------------------------------')
   print(f'{name} monitor configured!')
   print(f'--------------------------------')
   return

def map_to_beats(component):
   #map the components to the beats
   return MAPPINGS[component]

def replace_string(data, search_string, r_string):
   new_lines = []
   for line in data:
      if search_string in line:
         new_line = line.replace(search_string, r_string)
         new_lines.append(new_line)
      else:
         new_lines.append(line)
   return new_lines

def install(user_os, component, architecture, user_token):
   url = URLS[user_os][architecture][component]
   cwd = os.getcwd()
   cwd = cwd + '/output'
   #make output directory for the agent download file
   os.makedirs(cwd, exist_ok=True)
   print(f'--------------------------------')
   print(f'Downloading Logstail certificate for secure communication...')
   if not os.path.exists('/etc/certs/logstail'):
      os.makedirs('/etc/certs/logstail')
   urllib.request.urlretrieve(CERT, '/etc/certs/logstail/SectigoRSADomainValidationSecureServerCA.crt', reporthook=reporthook)
   print(f'Certificate successfully downloaded')
   print(f'--------------------------------')
   filepath = cwd + '/' + component + '-logstail.deb'
   #download .deb from Logstail github
   urllib.request.urlretrieve(url, filepath, reporthook=reporthook)
   #install .deb file
   subprocess.call(["dpkg", "-i", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'--------------------------------')
   print(f'Cleaining up...')
   subprocess.call(["rm", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'{component} Collector Successfully installed!')
   if not os.path.exists('/var/log/Logstail'):
      os.makedirs('/var/log/Logstail/')
   write_to_log(f'{component} collector installed', '/var/log/Logstail/agent.log')
   print(f'--------------------------------')
   beat = map_to_beats(component)
   #replace Token with user's Token
   conf_file = os.getcwd() + f'/configs/{beat}.yml'
   with open(conf_file, 'r') as file:
      yaml_data = file.readlines()
   yaml_data = replace_string(yaml_data, "USER_TOKEN", user_token)
   yaml_data = replace_string(yaml_data, "LOGSTAIL_CERT", '/etc/certs/logstail/SectigoRSADomainValidationSecureServerCA.crt')
   with open(conf_file, 'w') as file:
      file.writelines(yaml_data)
   #replace in the instalation directory and restart the collector
   subprocess.call(["cp", conf_file, f'/etc/{beat}/{beat}.yml'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'--------------------------------')
   print(f'Starting {component} collector...')
   subprocess.call(["service", beat, "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'{component} collector started!')
   print(f'--------------------------------')
   return


#Install SIEM
def install_siem(user_os, component, architecture, logs_port, auth_port, agent_name):
   url = URLS[user_os][architecture][component]
   cwd = os.getcwd()
   cwd = cwd + '/output'
   #make output directory for the agent download file
   os.makedirs(cwd, exist_ok=True)
   filepath = cwd + '/' + component + '-logstail.deb'
   #download .deb from Logstail github
   urllib.request.urlretrieve(url, filepath, reporthook=reporthook)
   #install .deb file
   subprocess.call(["dpkg", "-i", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'--------------------------------')
   print(f'Cleaining up...')
   subprocess.call(["rm", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'{component} Successfully installed!')
   write_to_log(f'{component} collector installed', '/var/log/Logstail/agent.log')
   print(f'--------------------------------')
   if user_os == 'debian':
      conf_file = os.getcwd() + f'/configs/ossec_deb.conf'
   with open(conf_file, 'r') as file:
      yaml_data = file.readlines()
   yaml_data = replace_string(yaml_data, "LOGS_PORT", logs_port)
   yaml_data = replace_string(yaml_data, "AUTH_PORT", auth_port)
   yaml_data = replace_string(yaml_data, "AGENT_NAME", agent_name)
   with open(conf_file, 'w') as file:
      file.writelines(yaml_data)
   #replace in the instalation directory and restart the collector
   subprocess.call(["cp", conf_file, '/var/ossec/etc/ossec.conf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'--------------------------------')
   print(f'Starting {component}...')
   subprocess.call(["service", 'logstail-siem', "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #change to logstail agent later
   print(f'{component} started!')
   print(f'--------------------------------')
   return

def show_modules(component):
   #for siem this option isnt available and has to be configured manually!
   if component == 'siem':
      print(f'--------------------------------')
      print(f'To view the modules in SIEM open the \'/var/ossec/etc/ossec.conf\' file.\nContact Logstail Support team for guidance!\nsupport@logstail.com')
      print(f'--------------------------------')
      return
   #print all the modules for the collector and their status (enabled # disabled)
   beat = map_to_beats(component)
   #read conf file
   #conf_file = os.getcwd() + f'/configs/{beat}.yml'
   conf_file = f'/etc/{beat}/{beat}.yml'
   if beat == 'metricbeat':
      module_keyword = '- module:'
      status_keyword = 'enabled:'
   if beat == 'packetbeat':
      module_keyword = '- type:'
      status_keyword = 'enabled:'
   if beat == 'filebeat':
      module_keyword = '#module'
      status_keyword = 'enabled:'
   with open(conf_file, 'r') as file:
      yaml_data = file.readlines()
   module_name = ''
   module_status = ''
   for line in yaml_data:
      if module_keyword in line:
         module_status = ''
         module_name = line.replace(module_keyword, '')
      if status_keyword in line:
         module_status = line.replace(status_keyword, '')
         #if beat == 'filebeat' : module_name = ''
      #if beat == 'filebeat' and '    type:' in line:
         #module_name = line.replace('    type:', '')
      if module_name != '' and module_status != '':
         module_status = re.sub(r'\s+', '', module_status)
         module_name = re.sub(r'\s+', '', module_name)
         symbol = '✅' if module_status == 'true' else '❌'
         module_status = 'Enabled' if module_status == 'true' else 'Not enabled'
         module_name = module_name.rstrip('\n')
         print(f'{module_name:<12}: {symbol} {module_status}')
         module_name = ''
         module_status = ''
   return

def enable_module(component):
   #for siem this option isnt available and has to be configured manually!
   if component == 'siem':
      print(f'--------------------------------')
      print(f'To enable modules in SIEM edit the \'/var/ossec/etc/ossec.conf\' file.\nContact Logstail Support team for guidance!\nsupport@logstail.com')
      return
   #We suppose that user first ran the show_modules operation to view all the modules so after that we ask him to provide with the name of the module he wishes to enable.
   print(f'--------------------------------')
   module_name = input(f'Enter module name you want to enable: ')
   new_lines = []
   beat = map_to_beats(component)
   conf_file = f'/etc/{beat}/{beat}.yml'
   if component == 'uptime':
      uptime_monitors(component)
      test_config(component, cwd_cert + '/Logstail-' + component)
      print(f'--------------------------------')
      print(f'Restarting {component} collector...')
      subprocess.call(["service", beat, "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      print(f'{component} collector restarted!')
      print(f'--------------------------------')
      return
   if beat == 'metricbeat':
      module_keyword = '- module:'
      status_keyword = 'enabled:'
   if beat == 'packetbeat':
      module_keyword = '- type:'
      status_keyword = 'enabled:'
   if beat == 'filebeat':
      module_keyword = '#module'
      status_keyword = 'enabled:'
   with open(conf_file, 'r') as file:
      yaml_data = file.readlines()
   found = False
   exist = False
   for line in yaml_data:
      if module_keyword in line and re.search(r'\b' + re.escape(module_name) + r'\b', line):
#module_name in line:
         found = True
         exist = True
      if status_keyword in line and found:
         new_line = line.replace('false', 'true')
         new_lines.append(new_line)
         found = False
      else:
         new_line = line
         new_lines.append(new_line)
   with open(conf_file, 'w') as file:
      file.writelines(new_lines)
   if exist:
      print(f'Enabled {module_name}.')
      print(f'--------------------------------')
      print(f'Restarting {component} collector...')
      subprocess.call(["service", beat, "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      print(f'{component} collector restarted!')
      print(f'Further configuration might be needed for module to work!\nOpen the configuration file ({conf_file}) locate the {module_name} module and validate the configuration!\nRestart is required for changes to Apply!')
      print(f'--------------------------------')
   else:
      print(f'--------------------------------')
      print(f'Module {module_name} is not valid!')
      print(f'--------------------------------')
   return

def disable_module(component):
   #for siem this option isnt available and has to be configured manually!
   if component == 'siem':
      print(f'--------------------------------')
      print(f'To disable modules in SIEM open the \'/var/ossec/etc/ossec.conf\' file.\nContact Logstail Support team for guidance!\nsupport@logstail.com')
      print(f'--------------------------------')
      return
   #We suppose that user first ran the show_modules operation to view all the modules so after that we ask him to provide with the name of the module he wishes to enable.
   module_name = input(f'Enter module name you want to disable: ')
   new_lines = []
   beat = map_to_beats(component)
   conf_file = f'/etc/{beat}/{beat}.yml'
   if beat == 'metricbeat':
      module_keyword = '- module:'
      status_keyword = 'enabled:'
   if beat == 'packetbeat':
      module_keyword = '- type:'
      status_keyword = 'enabled:'
   if beat == 'filebeat':
      module_keyword = '#module'
      status_keyword = 'enabled:'
   with open(conf_file, 'r') as file:
      yaml_data = file.readlines()
   found = False
   exist = False
   for line in yaml_data:
      if module_keyword in line and re.search(r'\b' + re.escape(module_name) + r'\b', line):
#module_name in line:
         found = True
         exist = True
      if status_keyword in line and found:
         new_line = line.replace('true', 'false')
         new_lines.append(new_line)
         found = False
      else:
         new_line = line
         new_lines.append(new_line)
   with open(conf_file, 'w') as file:
      file.writelines(new_lines)
   if exist:
      print(f'--------------------------------')
      print(f'Disabled {module_name}.')
      print(f'Restarting {component} collector...')
      subprocess.call(["service", beat, "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      print(f'{component} collector restarted!')
      print(f'--------------------------------')
   else:
      print(f'--------------------------------')
      print(f'Module {module_name} is not valid!')
      print(f'--------------------------------')
   return



def show_status(component):
   beat = map_to_beats(component)
   process = subprocess.Popen(['service', f'{beat}', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   output, error = process.communicate()
   output = output.decode('utf-8')
   error = output.encode('utf-8')
   #print(f'{output}, {error}')
   pattern = r'Active: (.*)'
   match = re.search(pattern, output)
   print(f'Status: {match.group(1)}')
   return

def restart(component):
   beat = map_to_beats(component)
   print(f'--------------------------------')
   print(f'Restarting {component} collector...')
   subprocess.call(["service", beat, "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'{component} collector restarted!')
   print(f'--------------------------------')
   return

def uninstall(component):
   beat = map_to_beats(component)
   print(f'--------------------------------')
   print(f'Stopping {component} collector...')
   subprocess.call(["service", beat, "stop"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'{component} collector restarted!')
   print(f'Uninstalling {component} collector...')
   subprocess.call(["apt", 'remove', beat], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'Deleting files...')
   subprocess.call(['rm', '-r', f'/etc/{beat}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print(f'Uninstall successfull!')
   print(f'--------------------------------')
