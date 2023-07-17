'''
Unless explicitly stated otherwise all files in this repository are licensed
under the Apache License Version 2.0.
This product includes software developed at Logstail (https://logstail.com/).
Copyright 2023-present Logstail
'''

def reporthook(block_num, block_size, total_size):
#   downloaded = block_num * block_size
#   progress = (downloaded / total_size) * 100
#   print(f'Downloading... {progress:.2f}%')
   bar_width = 40
   downloaded = block_num * block_size
   percent = int(downloaded * 100 / total_size)
   filled_length = int(bar_width * percent / 100)
   bar = '#' + str(filled_length) + '-' * (bar_width - filled_length)
   print(f'Progress: [{bar}] {percent}% {downloaded}/{total_size}', end='\r', flush=True)
