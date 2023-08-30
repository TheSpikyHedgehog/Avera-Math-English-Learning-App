###############################################################
#
# Avera App.
# This file is the main GUI part of the main app.
# By TheSpikyHedgehog
#--------------------------------------------------------------
#   Copyright (C) 2023  @TheSpikyHedgehog
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------



from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as MessageBox
#- import needed files
import learn_math
import learn_english
import settings
#- 
import time
import pygame.mixer as mixer
import json
import os

mixer.init()
click = mixer.Sound('assets/sounds/click.wav')
def clear(windows):
    for widget in windows.winfo_children():
        widget.forget()



def addUserData(data) -> dict: # Used to add data to JSON
    with open('assets/data/userdata.json', mode='w') as f:
        json.dump(data, f, indent=2)
        f.close()

def getJSONdata(path) -> str: #Function used to retrive data from JSON
    try:
        with open(path, mode='r') as f:
            data = json.load(f)
            f.close()
        return data
    except Exception:
        print("Unable to fetch data from path")

def getUserData():
    with open('assets/data/userdata.json', mode='r') as f:
        userdata = json.load(f)
        f.close()
    return userdata

def whole():
    root = Tk() 
    root.geometry('600x600')
    root.config(bg='lightblue')
    root.title("Avera: Math & English Practicing App")
    root.iconbitmap('./assets/images/logo.ico')
    Progress_Bar= ttk.Progressbar(root,orient=HORIZONTAL,length=250,mode='determinate')
    def Slide():
        Progress_Bar['value']=0
        root.update_idletasks()
        # root.config(bg='lightblue')
        time.sleep(0.5)
        for i in range(100):
            Progress_Bar['value'] += 1
            root.update_idletasks()
            time.sleep(0.01)

    logo = PhotoImage(file='assets/images/logo_enlarged.png')
    logo_original =  PhotoImage(file='assets/images/logo_original.png')
    main_logo =  Label(root, image=logo_original)
    main_logo.pack(pady=50)
    Progress_Bar.pack(pady=160)
    Slide()
    Progress_Bar.forget()
    main_logo.forget()
    appinfo = getJSONdata(path='assets/data/appinfo.json')
    root.config(bg='lightblue')
    def math_boot():
        root.destroy()
        learn_math.main()
    
    def main():
        version = appinfo["version"]
        main_logo =  Label(root, image=logo, bg='lightblue')
        main_logo.pack()
        Label(root, text="Select")
        math = Button(root, text="Math", font=("Tahoma", 20), width=25, height=2, command= lambda : [click.play(), math_boot()], relief="solid")
        english = Button(root, text="English", font=("Tahoma", 20), width=25, height=2, command = lambda: [click.play(), root.destroy(), learn_english.main()], relief="solid")
        math.pack(pady=20)
        english.pack()
        setting = Button(root, text="Settings", font=("Tahoma", 20), width=25, height=2, command = lambda : [click.play(), root.destroy(), settings.main_gui()], relief="solid")
        setting.pack(pady=20)
        Label(root, text=f'Made By TheSpikyHedgehog (c) 2023 || Version {version}', bg='lightblue').pack()
    
    def create_account(root):
        data_file_path = 'assets/data/userdata.json'
        try:
            if os.path.exists(data_file_path):

                with open(file=data_file_path, mode='r') as f:
                    userdata = json.load(f)
                    f.close()
                main()
                return userdata
            else:
                with open(file=data_file_path, mode='w') as f:
                    print("JSON data file created")
                    get_username()

        except Exception:
            MessageBox.showerror(title="Error", message="Error loading/writing data to userdata.json.  If an existing JSON file named 'userdata.json' exists under ./assets/data, please delete that file and try again.")
            return False
        
    def get_username():
        lbl = Label(root, text="Input A Username", font=("sans", 30), bg='LightBlue', fg='red')
        lbl.pack(pady=60)
        username_input = Entry(root, width=20, font=("Tahoma", 15), fg='green')
        username_input.pack()
        go = Button(root, text="Next", font=("Tahoma", 15), width=10, height=1, relief="solid", command= lambda : [click.play(), getLevel(username_input.get(), root)])
        go.pack(pady=20)
        root.bind('<Return>', func = lambda event: getLevel(username_input.get(), root))
        Label(root, text='Made By TheSpikyHedgehog (c) 2023', bg='lightblue').pack()
    
    def getLevel(username, root):
        clear(root)
        print(username)
        lbl = Label(root, text="Choose a Learning Level", font=("sans", 30), bg='LightBlue', fg='red')
        lbl.pack(pady=60)
        choice = StringVar()
        options = ['Level 1', 'Level 2', 'Level 3']
        level = OptionMenu(root, choice, *options)
        level.pack()
        choice.set('Level 1')
        root.unbind("<Return>")
        root.bind("<Return>", func= lambda event: finishJSON(username, choice.get()))
        go = Button(root, text="Next", relief="solid", font=("Tahoma", 15), width=10, height=1, command= lambda : [click.play(), finishJSON(username, choice.get())])
        go.pack(pady=20)
        Label(root, text='Made By TheSpikyHedgehog (c) 2023', bg='lightblue').pack()
    create_account(root)

    def finishJSON(username, lvl):
        print(lvl)
        if lvl == 'Level 1':
            lvl = 1
        elif lvl == "Level 2":
            lvl = 1
        elif lvl == "Level 3":
            lvl = 3
        else:
            print("NONE!")

        userdata = {
            "username":username,
            "learning_lvl":lvl
        }
        print(userdata)
        addUserData(userdata)
        clear(root)
        main()

    
    # root.config(bg='gray')
    # root.after(200, func= lambda:root.config(bg='black'))
    # root.after(1000, func= lambda:root.config(bg='gray'))
    # root.after(1100, func = lambda : root.config(bg='lightblue'))
    # root.after(1200, func = main)
    root.mainloop()

def mn_menu():
    root = Tk() 
    root.geometry('600x600')
    root.config(bg='lightblue')
    root.title("Avera: Math & English Practicing App")
    root.iconbitmap('assets/images/logo.ico')
    logo = PhotoImage(file='assets/images/logo_enlarged.png')
    appinfo = getJSONdata("assets/data/appinfo.json")
    def math_boot():
        root.destroy()
        learn_math.main()
    def main():
        version = appinfo["version"]
        main_logo =  Label(root, image=logo, bg='lightblue')
        main_logo.pack()
        Label(root, text="Select")
        math = Button(root, text="Math", font=("Tahoma", 20), width=25, height=2, command= lambda :[click.play(), math_boot()], relief="solid")
        english = Button(root, text="English", font=("Tahoma", 20), width=25, height=2, command= lambda : [click.play(), root.destroy(), learn_english.main()], relief="solid")
        math.pack(pady=20)
        english.pack()
        setting_btn =  Button(root, text="Settings", font=("Tahoma", 20), width=25, height=2, command= lambda : [click.play(), root.destroy(), settings.main_gui()], relief="solid")
        setting_btn.pack(pady=20)
        Label(root, text=f'Made By TheSpikyHedgehog (c) 2023 || Version {version}', bg='lightblue').pack()
    main()
    root.mainloop()
if __name__ == '__main__':
    whole()