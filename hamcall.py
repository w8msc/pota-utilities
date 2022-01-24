#!/usr/bin/env python3

# Looks up US amateur radio callsign and displays result
# uses python3 and tkinter
# by W8MSC, Jan 23, 2022

import requests
import json
from tkinter import *

data = {}

win = Tk()
win.title("US Amateur Radio Callsign Lookup")

def clear():
    text.delete(1.0,END)

def fetch_callsign(callsign):
    url = ("https://callook.info/{}/json".format(callsign))
    r = requests.get(url, timeout=1)
    data = json.loads(r.text)
    return data

def search_callback(event = None):
    call=callsign.get().upper()
    fetch_callsign(call)
    
    data=fetch_callsign(callsign.get())
    text.insert(INSERT,(f"Status           : {data['status']}\n"))
    if data['status']=='VALID':
        text.insert(INSERT,(f"Current callsign : {data['current']['callsign']}\n"))
        text.insert(INSERT,(f"Name             : {data['name']}\n"))
        text.insert(INSERT,(f"Type             : {data['type']}\n"))
        if data['type']=='CLUB':
            text.insert(INSERT,(f"Trustee          : {data['trustee']['callsign']} ({data['trustee']['name']}\n"))
        else:
            text.insert(INSERT,(f"Class            : {data['current']['operClass']}\n"))
        text.insert(INSERT,(f"Address line 1   : {data['address']['line1']}\n"))
        text.insert(INSERT,(f"Address line 2   : {data['address']['line2']}\n"))
        text.insert(INSERT,(f"Expires          : {data['otherInfo']['expiryDate']}\n\n"))
        text.see("end")
    e.delete(0,END)

callsign = StringVar()
top=Frame(win)
l=Label(top,text="Search for callsign")
e=Entry(top,textvariable=callsign)
b=Button(top,text="Search",command=search_callback)
c=Button(top,text="Clear",command=clear)
q=Button(top,text="Quit",command=quit)

l.pack(side=LEFT)
e.pack(side=LEFT)
b.pack(side=LEFT)
c.pack(side=LEFT)
q.pack(side=LEFT)
top.pack()

bottom=Frame(win)
s=Scrollbar(bottom)
text=Text(bottom,bg='gray71',fg='black',yscrollcommand=s.set)
s.config(command=text.yview)
s.pack(side=RIGHT,fill=Y)
text.pack(side=LEFT)
bottom.pack()

win.bind("<Return>",search_callback)

mainloop()
