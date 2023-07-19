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
from defs import URLS_WIN
from defs import MAPPINGS
from defs import CERT
from reporthook import reporthook
import zipfile
import shutil
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
   cwd_cert = 'C:/Program Files/Logstail-Agent'  
   beat = map_to_beats(component)
   file = cwd_cert + '/Logstail-' + component + f'/{beat}.yml'
   conf_file = os.getcwd() + f'\\configs\\{name}-monitor.yml'
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
   write_to_log(f'{component} collector {name} monitor enabled', cwd_cert + '/logs/agent.log')
   print(f'{name} monitor configured!')
   return
      
def install_npcap():
    download_url = "https://nmap.org/npcap/dist/npcap-1.75.exe"
    cwd = os.getcwd()
    cwd = cwd + '\\output\\npcap_installer.exe'
    # Download the Npcap installer
    print(f'--------------------------------')
    print(f'Downloading Npcap')
    urllib.request.urlretrieve(download_url, cwd, reporthook=reporthook)
    try:
       # Run the Npcap installer silently
       print(f'Installing Npcap...')
       subprocess.check_call([cwd])
       print("Npcap installation successful.")
    except subprocess.CalledProcessError as e:
       print(f"Npcap installation failed. Error: {str(e)}\nContact as at support@logstail.com")
    # Clean up the installer file
    subprocess.run(["del", cwd], shell=True)
    return



def is_service_installed(service_name):
    try:
        output = subprocess.check_output(['sc', 'query', service_name])
        return b'STATE' in output
    except subprocess.CalledProcessError:
        return False

def test_config(component, path):
   beat = map_to_beats(component)
   print(f'--------------------------------')
   print('Checking configuration...')
   print(f'--------------------------------')
   try:
      output = subprocess.check_output(f'{beat}.exe test config', shell=True, cwd=path).decode("utf-8")
   except subprocess.CalledProcessError as e:
      print(f'--------------------------------')
      print(f"Configuration test failed with exit code {e.returncode}.\nContact support@logstail.com")
      print(f'--------------------------------')
      return      
   if 'Config OK' in output:
      print(f'--------------------------------')
      print(output)
      print(f'--------------------------------')
   else:
      print(f'--------------------------------')
      print(output)
      print('If error is not resolved, try reinstalling the agent component.\nIf further help is needed contact us at support@logstail.com')
      print(f'--------------------------------')
      
      
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

def uninstall(component):
   cwd_cert = 'C:/Program Files/Logstail-Agent'
   beat = map_to_beats(component) 
   try:
      print(f'--------------------------------')
      print(f'Stopping {component} collector...')
      subprocess.call(["sc", "stop", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      print(f'{component} collector stoped!')
      print(f'--------------------------------')
   except subprocess.CalledProcessError as e:   
      print(f'--------------------------------')
      print(f"Agent stop failed with exit code {e.returncode}.\nContact support@logstail.com")
      print(f'--------------------------------')       
   print(f'--------------------------------')
   print(f'Uninstall {component} collector service...')
   ps_file = cwd_cert + '/Logstail-' + component + f'/uninstall-service-{beat}.ps1'
   try:
      subprocess.call(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      print(f'{component} collector service uninstalled!')
      print(f'--------------------------------')
      print(f'Removing files...')
      write_to_log(f'{component} collector uninstalled', cwd_cert + '/logs/agent.log')
      try:
         shutil.rmtree(cwd_cert + '/Logstail-' + component)
         print(f'--------------------------------')
      except Exception as e:
         print(f"An error occurred while deleting the folder: {str(e)}\nTry manually deleting the folder {cwd_cert + '/Logstail-' + component}")
         print(f'--------------------------------')
   except subprocess.CalledProcessError as e:
      print(f'--------------------------------')
      print(f"Remove failed with exit code {e.returncode}.\nContact support@logstail.com")
      print(f'--------------------------------')
   return      
   
def install(user_os, component, architecture, user_token):
   url = URLS_WIN[component]
   cwd = os.getcwd()
   cwd = cwd + '\\output'
   #make output directory for the agent download file
   os.makedirs(cwd, exist_ok=True)
   #cert download path
   cwd_cert = 'C:/Program Files/Logstail-Agent'
   os.makedirs(cwd_cert, exist_ok=True)
   #make logs folder
   os.makedirs(cwd_cert + '/logs', exist_ok=True)
   print(f'--------------------------------')
   print(f'Downloading Logstail certificate for secure communication...')
   urllib.request.urlretrieve(CERT, cwd_cert + '/SectigoRSADomainValidationSecureServerCA.crt', reporthook=reporthook)
   print(f'Certificate successfully downloaded')
   print(f'--------------------------------')
   filepath = cwd + '\\' + component + '-logstail.zip'
   #download .zip from Logstail github
   urllib.request.urlretrieve(url, filepath, reporthook=reporthook)
   #unzip zip file to C:/Program files/Logstail
   with zipfile.ZipFile(filepath, 'r') as zip_ref:
      zip_ref.extractall(cwd_cert)
   beat = map_to_beats(component) 
   matches = os.listdir(cwd_cert)
   for match in matches:
      if beat in match:
         os.rename(cwd_cert + '/' + match, cwd_cert + '/Logstail-' + component)
   #edit yaml
   conf_file = os.getcwd() + f'\\configs\\{beat}_windows.yml'
   with open(conf_file, 'r') as file:
      yaml_data = file.readlines()
   yaml_data = replace_string(yaml_data, "USER_TOKEN", user_token)
   yaml_data = replace_string(yaml_data, "LOGSTAIL_CERT", cwd_cert + '/SectigoRSADomainValidationSecureServerCA.crt')
   with open(conf_file, 'w') as file:
      file.writelines(yaml_data)
   shutil.copy2(conf_file, cwd_cert + '/Logstail-' + component + f'/{beat}.yml')
   print(f'--------------------------------')
   print(f'Install {component} collector service...')
   ps_file = cwd_cert + '/Logstail-' + component + f'/install-service-{beat}.ps1'
   try:
      subprocess.call(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      print(f'{component} collector service installed!')
      write_to_log(f'{component} collector installed', cwd_cert + '/logs/agent.log')
      print(f'--------------------------------')
      print(f'Starting {component} collector...')
      if component == 'network':
         if not (is_service_installed('npcap') or is_service_installed('npf')):
            print(f'--------------------------------')
            print('WinPcap or Npcap is required to run the Network Collector!')
            print(f'--------------------------------')
            print('Npcap is a packet sniffing and network analysis tool for Windows, providing raw packet capturing capabilities with features and improvements over its predecessor, WinPcap.')
            if (input('Do you want to continue with installing Npcap? (Y/n): ') == 'Y'):
               install_npcap()
               write_to_log(f'Npcap installed', cwd_cert + '/logs/agent.log')
            else:
               print('Network collector could not be configured correctly.\nContact us at support@logstail.com')
         else:
            print(f'--------------------------------')
            print('Required service is Installed!')
            print(f'--------------------------------')
      try:
         print(f'Starting {component} collector...')
         subprocess.call(["sc", "start", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
         print(f'{component} collector started!')
         print(f'--------------------------------')
      except subprocess.CalledProcessError as e:   
         print(f'--------------------------------')
         print(f"Agent start failed with exit code {e.returncode}.\nContact support@logstail.com")
         print(f'--------------------------------') 
   except subprocess.CalledProcessError as e:
      print(f'--------------------------------')
      print(f"Installation failed with exit code {e.returncode}.\nContact support@logstail.com")
      print(f'--------------------------------') 
   os.remove(filepath)
   return
   
def install_siem(user_os, component, architecture, logs_port, auth_port, agent_name):
   url = URLS_WIN[component]
   cwd = os.getcwd()
   cwd = cwd + '\\output'
   #make output directory for the agent download file
   os.makedirs(cwd, exist_ok=True)
   #cert download path
   cwd_cert = 'C:/Program Files/Logstail-Agent'
   os.makedirs(cwd_cert, exist_ok=True)
   filepath = cwd + '\\logstail-siem.msi'
   #download siem agent from Logstail github
   urllib.request.urlretrieve(url, filepath, reporthook=reporthook)
   if component == 'siem':
      beat = 'LogstailSvc'
   else:
      beat = map_to_beats(component)
   #execute msi installer to install Logstail-siem
   try:
      subprocess.run(['msiexec', '/i', cwd + '\\logstail-siem.msi'], check=True)
      write_to_log(f'{component} collector installed', cwd_cert + '/logs/agent.log')
   except subprocess.CalledProcessError as e:
      print(f'--------------------------------')
      print(f"MSI installer execution failed with exit code {e.returncode}.\nContact support@logstail.com")
      print(f'--------------------------------')
   #edit yaml
   conf_file = os.getcwd() + f'\configs\ossec_win.conf'
   with open(conf_file, 'r') as file:
      yaml_data = file.readlines()
   yaml_data = replace_string(yaml_data, "LOGS_PORT", logs_port)
   yaml_data = replace_string(yaml_data, "AUTH_PORT", auth_port)
   yaml_data = replace_string(yaml_data, "AGENT_NAME", agent_name)
   with open(conf_file, 'w') as file:
      file.writelines(yaml_data)
   shutil.copy2(conf_file, 'C:\Program Files (x86)\ossec-agent\ossec.conf')
   subprocess.call(["sc", "start", beat], shell=True)
   print(f'{component} collector started!')
   print(f'--------------------------------')
   return

def uninstall_siem(user_os, component, architecture):
   url = URLS_WIN[component]
   cwd = os.getcwd()
   cwd = cwd + '\\output'
   #make output directory for the agent download file
   os.makedirs(cwd, exist_ok=True)
   #cert download path
   cwd_cert = 'C:/Program Files/Logstail-Agent'
   os.makedirs(cwd_cert, exist_ok=True)
   filepath = cwd + '\\logstail-siem.msi'
   #download siem agent from Logstail github
   #urllib.request.urlretrieve(url, filepath, reporthook=reporthook) NEED TO UNCOMMENT!!!!!!!
   if component == 'siem':
      beat = 'LogstailSvc'
   else:
      beat = map_to_beats(component)
   #execute msi installer to install Logstail-siem
   subprocess.call(["sc", "stop", beat], shell=True)
   print(f'{component} collector stoped!')
   print(f'--------------------------------')
   try:
      subprocess.run(['msiexec', '/i', cwd + '\\logstail-siem.msi'], check=True)
      write_to_log(f'{component} collector uninstalled', cwd_cert + '/logs/agent.log')
      print(f'{component} collector uninstalled!')
      print(f'--------------------------------')
   except subprocess.CalledProcessError as e:
      print(f'--------------------------------')
      print(f"MSI installer execution failed with exit code {e.returncode}.\nContact support@logstail.com")
      print(f'--------------------------------')
   return

def show_modules(component):
   #print all the modules for the collector and their status (enabled # disabled)
   beat = map_to_beats(component)
   cwd_cert = 'C:/Program Files/Logstail-Agent'
   #read conf file
   #conf_file = os.getcwd() + f'/configs/{beat}.yml'
   conf_file = cwd_cert + '/Logstail-' + component + f'/{beat}.yml'
   #for siem this option isnt available and has to be configured manually!
   if component == 'siem':
      print(f'--------------------------------')
      print(f'To view and configure the modules in SIEM open the \'C:\Program Files (x86)\ossec-agent\ossec.conf\' file.\nContact Logstail Support team for guidance!\nsupport@logstail.com')
      return
   if component == 'uptime':
      print(f'--------------------------------')
      print(f'To view your configured monitors visit your apps.logstail.com or open the {conf_file} file!')
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
   try:   
      with open(conf_file, 'r') as file:
         yaml_data = file.readlines()
   except FileNotFoundError:
       print(f'--------------------------------')
       print("Configuration file not found. Try installing the collector.")
       print(f'--------------------------------')
       return
   except PermissionError:
       print(f'--------------------------------')
       print("Permission denied. Unable to open file. Execute script with Administrator Privilages")
       print(f'--------------------------------')
       return
   except Exception as e:
       print(f'--------------------------------')
       print("An error occurred while opening the file:", str(e))
       print(f'--------------------------------')
       return
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
         print(f'{module_name:<17}: {symbol} {module_status}')
         module_name = ''
         module_status = ''
   return
   
def enable_module(component):
   #We suppose that user first ran the show_modules operation to view all the modules so after that we ask him to provide with the name of the module he wishes to enable.
   beat = map_to_beats(component)
   cwd_cert = 'C:/Program Files/Logstail-Agent'
   #read conf file
   conf_file = cwd_cert + '/Logstail-' + component + f'/{beat}.yml'
   #for siem this option isnt available and has to be configured manually!
   if component == 'siem':
      print(f'--------------------------------')
      print(f'Available SIEM windows add-ons')
      print(f'1: Sysmon (System service that provides advanced monitoring and logging capabilities, enabling detailed visibility into system activity for threat detection and incident response.)')
      module = input('Enter the module you want to install: ')
      print(f'--------------------------------')
      if module == '1':
         cwd = os.getcwd()
         cwd = cwd + '\\scripts'
         try:
            subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', cwd + '\\sysmon.ps1'], check=True)
            print(f'--------------------------------')
            print("PowerShell script executed successfully.\nSysmon is now enabled!")
            print(f'--------------------------------')
         except subprocess.CalledProcessError as e:
            print(f'--------------------------------')
            print(f"PowerShell script execution failed with exit code {e.returncode}. Contact as at support@logstail.com")
            print(f'--------------------------------')
      print(f'To view and configure the modules in SIEM open the \'C:\Program Files (x86)\ossec-agent\ossec.conf\' file.\nContact Logstail Support team for guidance!\nsupport@logstail.com')
      return
   if component == 'uptime':
      uptime_monitors(component)
      test_config(component, cwd_cert + '/Logstail-' + component)
      print(f'Restarting {component} collector...')
      subprocess.call(["sc", "stop", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      subprocess.call(["sc", "start", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      print(f'{component} collector restarted!')
      print(f'--------------------------------')
      return
   module_name = input(f'Enter module name you want to enable: ')
   new_lines = []
   if beat == 'metricbeat':
      module_keyword = '- module:'
      status_keyword = 'enabled:'
   if beat == 'packetbeat':
      module_keyword = '- type:'
      status_keyword = 'enabled:'
   if beat == 'filebeat':
      module_keyword = '#module'
      status_keyword = 'enabled:'
   try:   
      with open(conf_file, 'r') as file:
         yaml_data = file.readlines()
   except FileNotFoundError:
       print(f'--------------------------------')
       print("Configuration file not found. Try installing the collector.")
       print(f'--------------------------------')
       return
   except PermissionError:
       print(f'--------------------------------')
       print("Permission denied. Unable to open file. Execute script with Administrator Privilages")
       print(f'--------------------------------')
       return
   except Exception as e:
       print(f'--------------------------------')
       print("An error occurred while opening the file:", str(e))
       print(f'--------------------------------')
       return
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
      print(f'--------------------------------')
      print(f'Enabled {module_name}.')
      write_to_log(f'{component} collector {module_name} enabled', cwd_cert + '/logs/agent.log')
      test_config(component, cwd_cert + '/Logstail-' + component)
      print(f'Restarting {component} collector...')
      subprocess.call(["sc", "stop", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      subprocess.call(["sc", "start", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      print(f'Further configuration might be needed for module to work!\nOpen the configuration file ({conf_file}) locate the {module_name} module and validate the configuration!\nRestart is required for changes to Apply!')
      print(f'{component} collector restarted!')
      print(f'--------------------------------')
   else:
      print(f'--------------------------------')
      print(f'Module {module_name} is not valid!')
      print(f'--------------------------------')
   return
   
def disable_module(component):
   #We suppose that user first ran the show_modules operation to view all the modules so after that we ask him to provide with the name of the module he wishes to enable.
   new_lines = []
   beat = map_to_beats(component)
   cwd_cert = 'C:/Program Files/Logstail-Agent'
   #read conf file
   conf_file = cwd_cert + '/Logstail-' + component + f'/{beat}.yml'
   #for siem this option isnt available and has to be configured manually!
   if component == 'siem':
      print(f'--------------------------------')
      print(f'To disable modules in SIEM edit the \'C:\Program Files (x86)\ossec-agent\ossec.conf\' file.\nContact Logstail Support team for guidance!\nsupport@logstail.com')
      print(f'--------------------------------')
      return
   if component == 'uptime':
      print(f'--------------------------------')
      print(f'To delete a monitor you have to go to {conf_file} and delete the specific lines.\nThen restart the collector!')   
      return
   module_name = input(f'Enter module name you want to disable: ')
   if beat == 'metricbeat':
      module_keyword = '- module:'
      status_keyword = 'enabled:'
   if beat == 'packetbeat':
      module_keyword = '- type:'
      status_keyword = 'enabled:'
   if beat == 'filebeat':
      module_keyword = '#module'
      status_keyword = 'enabled:'
   try:   
      with open(conf_file, 'r') as file:
         yaml_data = file.readlines()
   except FileNotFoundError:
       print(f'--------------------------------')
       print("Configuration file not found. Try installing the collector.")
       print(f'--------------------------------')
       return
   except PermissionError:
       print(f'--------------------------------')
       print("Permission denied. Unable to open file. Execute script with Administrator Privilages")
       print(f'--------------------------------')
       return
   except Exception as e:
       print(f'--------------------------------')
       print("An error occurred while opening the file:", str(e))
       print(f'--------------------------------')
       return
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
      write_to_log(f'{component} collector {module_name} disabled', cwd_cert + '/logs/agent.log')
      test_config(component, cwd_cert + '/Logstail-' + component)
      print(f'Restarting {component} collector...')
      subprocess.call(["sc", "stop", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      subprocess.call(["sc", "start", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      print(f'{component} collector restarted!')
      print(f'--------------------------------')
      #print(f'Further configuration might be needed for module to work!\nOpen the configuration file ({conf_file}) locate the {module_name} module and validate the configuration!\nRestart is required for changes to Apply!')
   else:
      print(f'--------------------------------')
      print(f'Module {module_name} is not valid!')
      print(f'--------------------------------')
   return
   
def restart(component):
   if component == 'siem':
      beat = 'LogstailSvc'
   else:
      beat = map_to_beats(component)
   if component != 'siem':
      try:
         cwd_cert = 'C:/Program Files/Logstail-Agent'
         test_config(component, cwd_cert + '/Logstail-' + component)
         print(f'--------------------------------')
         print(f'Restarting {component} collector...')
      except Exception as e:
         print("Failed to check configuration.\nInstall collector, if error continues contact us at support@logstail.com")
   try:
      subprocess.call(["sc", "stop", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      subprocess.call(["sc", "start", beat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
      print(f'{component} collector restarted!')
      print(f'--------------------------------')
   except subprocess.CalledProcessError as e:
      print(f'--------------------------------')
      print(f'Failed to restart {component} collector.\nInstall collector, if error continues contact us at support@logstail.com')   
      print(f'--------------------------------')
   return
   
def show_status(component):
   if component == 'siem':
      beat = 'LogstailSvc'
   else:
      beat = map_to_beats(component)
      try:
         cwd_cert = 'C:/Program Files/Logstail-Agent'
         test_config(component, cwd_cert + '/Logstail-' + component)
      except Exception as e:
         print("Failed to test configuration.\nInstall collector, if error continues contact us at support@logstail.com")   
   try:   
      output = subprocess.check_output(f'sc query {beat}', shell=True).decode('utf-8')
      if 'STATE' in output:
         start_index = output.index("STATE") + 7
         end_index = output.index("\n", start_index)
         state = output[start_index:end_index].strip().split()[-1]
         print(f'--------------------------------')
         print(f'Status: {state}')
         print(f'--------------------------------')
   except subprocess.CalledProcessError as e:
      print(f'--------------------------------')
      print("Component does not exist or an Error occured.\nTry installing component. If error continues contact support@logstail.com")
      print(f'--------------------------------')
   return
