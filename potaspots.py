#!/usr/bin/env python3

""" 

Pulls active spots from the POTA API

Parks on the Air
Amateur radio portable operations activities

May 2021, W8MSC

"""

import requests
import json

spots_URL = "https://api.pota.app/spot/activator"

try:
    response = requests.get(spots_URL)
    results = response.json()
    if len(results) > 0:
        spots = sorted(results, key=lambda i: i['spotTime'])
        print("{:>12}  {:>10}  {:>10}  {:15}  {}".format(
            "Activator", "Frequency", "Reference", "Location", "Park"))
        print("-"*100)
        for spot in spots:
            if "QRT" not in spot['comments'].upper():
                print("{:>12}  {:>10}  {:>10}  {:15}  {}".
                      format(spot['activator'], spot['frequency'],
                             spot['reference'], spot['locationDesc'],
                             spot['name']
                             ))
    else:
        print("There are no spots at the moment")
except Exception as e:
    print("Error: " + str(e))
