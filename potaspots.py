#!/usr/bin/env python3

from tkinter import *
import requests
import json

spots_URL = "https://api.pota.app/spot/activator"

try:
    response = requests.get(spots_URL)
    results = response.json()
    if len(results) > 0:
        spots=sorted(results,key = lambda i : i['spotTime'])
        table_headers=print("{:>12} {:>10} {:>10} {}  {}".format("Activator","Frequency","Reference","Location","Park"))
        for spot in spots:
            if "QRT" not in spot['comments'].upper():
                print("{:>12} {:>10} {:>10} {}  {}".
                      format(spot['activator'], spot['frequency'],
                             spot['reference'], spot['locationDesc'],
                             spot['name']
                             ))
    else:
        print("There are no spots at the moment")
except:
    print("error")
