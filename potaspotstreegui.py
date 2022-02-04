#!/usr/bin/env python3

# Displays activte POTA spots
# uses python3 and tkinter
# by W8MSC, Jan 25, 2022

import requests
import json
from tkinter import *
from tkinter import ttk

data = {}

win = Tk()
win.title("POTA Spots")

clear_before_refresh = False
ignore_QRT_spots = True

def clear():
    for i in tree.get_children():
        tree.delete(i)

def delete_selected():
    x=tree.selection()[0]
    tree.delete(x)

def details_callback():
    selected = tree.focus()
    print(tree.item(selected,'values'))

def item_detail(event = None):
    try:
        #print("inside item detail")
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

def fetch_spots_callback(event = None):
    print("inside fetch_spots_callback")
    
    for i in tree.get_children():
        tree.delete(i)
    
    url='https://api.pota.app/spot/activator'

    try:
        response=requests.get(url)
        results=response.json()
        num_spots=len(results)
        if num_spots>0:
            spots=sorted(results,key = lambda i : i['spotTime'])
            for spot in spots:
                print(spot)
                if 'QRT' in spot['comments'].upper():
                    print("Ignoring QRT spot")
                else:
                    spot_info=(spot['activator'],spot['frequency'],spot['mode'],spot['reference'],spot['locationDesc'],spot['name'],spot['comments'],spot['spotTime'])
                    #print(spot_info)
                    tree.insert('',END,values=spot_info)
        else:
            print("There are no active spots")
    except:
        print("Error")


    # try:
    #     response=requests.get(url)
    #     results=response.json()
    #     num_spots=len(results)
    #     if num_spots > 0:
    #         text.insert(INSERT,(f"There are {num_spots} spots at this time\n"))
    #         spots=sorted(results,key = lambda i : i['spotTime'])
    #         for spot in spots:
    #             msg=("Activator: {:12}  Freq: {:14}  Reference: {:8}  Location: {}  Park: {}\n".
    #                   format(spot['activator'], spot['frequency'],
    #                          spot['reference'], spot['locationDesc'],
    #                          spot['name']
    #                   )
    #             )
    #             text.insert(INSERT,msg)
            
    #     else:
    #         text.insert(INSERT,"There are no spots at this time\n")

    # except:
    #     print("Error")
    # #text.see(0,END)

callsign = StringVar()
top=Frame(win)
l=Label(top,text="Refresh in X seconds")

b=Button(top,text="Refresh Now",command=fetch_spots_callback)
c=Button(top,text="Clear",command=clear)
q=Button(top,text="Quit",command=quit)

l.pack(side=LEFT)
b.pack(side=LEFT)
c.pack(side=LEFT)
q.pack(side=LEFT)
top.pack(expand=YES,fill=BOTH)

bottom=Frame(win)
#s=Scrollbar(bottom)

columns=('1','2','3','4','5','6','7','8')

tree=ttk.Treeview(bottom,columns=columns,show='headings')
tree.heading('1',text='Activator')
tree.column('1',minwidth=0,width=100)
tree.heading('2',text='Frequency')
tree.column('2',minwidth=0,width=100)
tree.heading('3',text='Mode')
tree.column('3',minwidth=0,width=100)
tree.heading('4',text='Reference')
tree.column('4',minwidth=0,width=100)
tree.heading('5',text='Location')
tree.column('5',minwidth=0,width=100)
tree.heading('6',text='Park')
tree.column('6',minwidth=0,width=300)
tree.heading('7',text='Comments')
tree.column('7',minwidth=0,width=300)
tree.heading('8',text='Spot Time')
tree.column('8',minwidth=0,width=100)

# use this to only show summary info
# hiding columns for comments and spotTime
tree["displaycolumns"]=("1","2", "3", "4", "5", "6")


# s.config(command=text.yview)
# s.pack(side=RIGHT,fill=Y)
tree.pack(side=LEFT,expand=YES,fill=BOTH)
tree.bind("<Button-3>",item_detail)
bottom.pack(expand=YES,fill=BOTH)

m=Menu(win,tearoff=0)
m.add_command(label='Details',command=details_callback)
#m.add_command(label='Edit')
#m.add_command(label='Delete',command=delete_selected)

win.bind("<Return>",fetch_spots_callback)


mainloop()
