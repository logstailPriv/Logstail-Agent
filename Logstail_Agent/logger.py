'''
Unless explicitly stated otherwise all files in this repository are licensed
under the Apache License Version 2.0.
This product includes software developed at Logstail (https://logstail.com/).
Copyright 2023-present Logstail
'''


def write_to_log(message, filepath):
   try:
      with open(filepath, 'a') as log_file:
         log_file.write(f'{message}\n')
   except Exception as e:
      print('Error writing to log file.\nContact us at support@logstail.com')