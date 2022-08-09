#!/usr/bin/env python3

import os
import hashlib
import requests
import datetime

"""
Downloads the current list of all POTA parks and saves as CSV

Parks on the Air
Amateur radio portable operations activities

May 2021, W8MSC

"""

print("Downloading park data...")

# Swtiched to pota.app  Feb 6, 2022 W8MSC
url='http://pota.app/all_parks.csv'
r=requests.get(url)

with open('temp.csv','wb') as f:
    f.write(r.content)

print("Result code = {}".format(r.status_code))
temp_filesize=os.stat('temp.csv').st_size
print("Temp filesize = {}".format(temp_filesize))

if os.path.exists('all_parks.csv'):
    current_hash = hashlib.md5()
    current_file = open('all_parks.csv','rb')
    current_content = current_file.read()
    current_hash.update(current_content)
    current_digest = current_hash.hexdigest()

    print(f"Current file hash = {current_digest}")

    temp_hash = hashlib.md5()
    temp_file = open('temp.csv','rb')
    temp_content = temp_file.read()
    temp_hash.update(temp_content)
    temp_digest = temp_hash.hexdigest()

    print(f"Temp file hash = {temp_digest}")

    if current_digest == temp_digest:
        print("Files are the same, keeping the current park data file")
        os.remove('temp.csv')
    else:
        print("Files are not the same, updating current park data file")
        os.remove('all_parks.csv')
        os.rename('temp.csv','all_parks.csv')

    #current_filesize=os.stat('all_parks.csv').st_size
    # print("Current filesize = {}".format(current_filesize))
    # if temp_filesize==current_filesize:
    #     print("Files are the same, keeping current park data file")
    #     os.remove('temp.csv')
    # else:
    #     print("Files are not the same, keep the new file")
    #     os.remove('all_parks.csv')
    #     os.rename('temp.csv','all_parks.csv')
else:
    print("No previous park data file")
    os.rename('temp.csv','all_parks.csv')
    