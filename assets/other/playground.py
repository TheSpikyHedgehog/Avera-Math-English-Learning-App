'''
Written by TheSpikyHedgehog
This file was first made to test and play with a bunch of different things.                    
Please ignore this file...
...or take a look (its kinda messy. may have nonsense variable names)
'''

import json
from tkinter import *
import tkinter.ttk as ttk
import customtkinter as ctk # better GUI dev
import random
# testing loading JSON files
test = {}
test['value'] = 'hi'
def addUserData(data):
    with open('assets/data/userdata.json', mode='w') as f:
        json.dump(data, f, indent=2)
        f.close()

addUserData('important')

with open('assets/data/userdata.json', mode='r') as f:

    val = json.load(f)

# print(val['username'])

# used to clear (actually forget) children of parent window to pave the way for new widgets
# can be used to switch frames without having to destroy current window
# Although when switching between main windows(like main menus), I prefer to destroy window.
def clear(window):
    for widget in window.winfo_children():
        widget.forget()


def theme_test():
    root = Tk()
    style = ttk.Style()
    style.theme_use("clam")
    label = Label(root, text="This is a test label").pack()
    tkklabel = ttk.Label(root, text="this is a ttk label").pack()
    btn = Button(root, text='btn').pack()
    ttkbtn = ttk.Button(root, text='btn ttk').pack()
    root.mainloop()
def ctk_test():
    root = ctk.CTk()
    button = ctk.CTkButton(root, text='This is a CTK button')
    button.pack()
    root.mainloop()
def test(func):
    print("HI")
    return func
def advanced_test(a, b):

    print(f"{a} and {b}")

def main_test(a, b):
    
    print("testing")
def get_file(path):
    try:
        with open(path, mode='r') as f:
                data = f.read()
                return data
    except Exception:
            print("Unable to fetch data from path")
            return False
        
if __name__ == "__main__":
    pass
