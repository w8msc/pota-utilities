#!/usr/bin/env python3

import os
import requests
import datetime

"""
Downloads the current list of all POTA parks and saves as CSV

Parks on the Air
Amateur radio portable operations activities

May 2021, W8MSC

"""

print("Downloading park data...")

# need to switch to pota.app once it's implemented
url='http://pota.us/all_parks.csv'
r=requests.get(url)

with open('temp.csv','wb') as f:
    f.write(r.content)

print("Result code = {}".format(r.status_code))
temp_filesize=os.stat('temp.csv').st_size
print("Temp filesize = {}".format(temp_filesize))

if os.path.exists('all_parks.csv'):
    current_filesize=os.stat('all_parks.csv').st_size
    print("Current filesize = {}".format(current_filesize))
    if temp_filesize==current_filesize:
        print("Files are the same, keeping current park data file")
        os.remove('temp.csv')
    else:
        print("Files are not the same, keep the new file")
        os.remove('all_parks.csv')
        os.rename('temp.csv','all_parks.csv')
else:
    os.rename('temp.csv','all_parks.csv')
    