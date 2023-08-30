from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as MessageBox
import pygame.mixer as mixer
import main_file
import json

mixer.init()
click = mixer.Sound('assets/sounds/click.wav')
userdata_json_path = 'assets/data/userdata.json'
appinfo_json_path = 'assets/data/appinfo.json'
def getJSONdata(path):
    try:
        with open(path, mode='r') as f:
            data = json.load(f)
            f.close()
        return data
    except Exception:
        print("Unable to fetch data from path")
def clear(windows):
    for widget in windows.winfo_children():
        widget.forget()

def addUserData(data) -> dict:
    with open('assets/data/userdata.json', mode='w') as f:
        json.dump(data, f, indent=2)
        f.close()
def finishJSON(username, lvl):
        print(lvl)
        if lvl == 'Level 1':
            lvl = 1
        elif lvl == "Level 2":
            lvl = 2
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
        return True
def home(root):
    root.destroy()
    main_file.mn_menu()
def change_learning_level(root, username):
    clear(root)
    data = getJSONdata('assets/data/userdata.json')
    learning_lvl = data["learning_lvl"]
    lbl = Label(root, text="Choose a Learning Level", font=("sans", 30), bg='LightBlue', fg='red')
    lbl.pack(pady=60)
    choice = StringVar()
    options = ['Level 1', 'Level 2', 'Level 3']
    level = OptionMenu(root, choice, *options)
    level.pack()
    choice.set(f"Level {learning_lvl}")
    root.unbind("<Return>")
    root.bind("<Return>", func= lambda event: [finishJSON(username, choice.get()), root.destroy(), main_gui()])
    go = Button(root, text="Next", font=("Tahoma", 15), width=10, height=1, relief="solid", command= lambda : [click.play(), finishJSON(username, choice.get()), root.destroy(), main_gui()])
    go.pack(pady=20)
    Label(root, text='Made By TheSpikyHedgehog (c) 2023', bg='lightblue').pack()

def change_username(root, learninglvl):
    clear(root)
    lbl = Label(root, text="Input A Username", font=("sans", 30), bg='LightBlue', fg='red')
    lbl.pack(pady=60)
    username_input = Entry(root, width=20, font=("Tahoma", 15), fg='green')
    username_input.pack()
    go = Button(root, relief="solid", text="Next", font=("Tahoma", 15), width=10, height=1, command= lambda : [click.play(), finishJSON(username_input.get(), learninglvl), root.destroy(), main_gui()])
    go.pack(pady=20)
    root.bind('<Return>', func = lambda event: [finishJSON(username_input.get(), learninglvl), root.destroy(), main_gui()])
    Label(root, text='Made By TheSpikyHedgehog (c) 2023', bg='lightblue').pack()

def show_userinfo(root, username, learning_lvl):
    clear(root)
    title_lb = Label(root,font=("Tahoma", 35, 'bold'), fg = "black",  text="User Info", bg='LightBlue').pack()
    username_lb = Label(root, font=("Tahoma", 20), text=f'Username: {username}', bg='lightblue').pack(pady=1)
    learning_lvl_lb = Label(root, font=("Tahoma", 20), text=f'Learning Level: {learning_lvl}', bg='lightblue').pack(pady=1)
    back = Button(root, text='Back', font=("Tahoma", 15), command= lambda : [root.destroy(), main_gui()]).pack(pady=1)

def show_appinfo(root, version, licence, versionid, author):
    clear(root)
    title_lb = Label(root,font=("Tahoma", 35, 'bold'), fg = "black",  text="App Info", bg='LightBlue').pack()
    version_ld = Label(root, font=("Tahoma", 20), text=f'Version: {version}', bg='lightblue').pack(pady=1)
    liccence_b = Label(root, font=("Tahoma", 20), text=f'Licence: {licence}', bg='lightblue').pack(pady=1)
    versionid_lb = Label(root, font=("Tahoma", 20), text=f'VersionID: {versionid}', bg='lightblue').pack(pady=1)
    authorlb = Label(root, font=("Tahoma", 20), text=f'Author: {author}', bg='lightblue').pack(pady=1)
    back = Button(root, text='Back', font=("Tahoma", 15), command= lambda : [root.destroy(), main_gui()]).pack(pady=1)
def about(root):
    MessageBox.showinfo(title='About', message='Avera is a English & Math practicing app. It was created by TheSpikyHedgehog. I created it because it might help my little sister learn math and english better but now I think everyone should be able to use it. Look at the README or App Info for more information.  ')
def main_gui():
    root = Tk()
    root.geometry('550x550')
    root.title("Avera: Settings")
    root.iconbitmap('assets/images/logo.ico')
    root.configure(bg='LightBlue')
    userdata = getJSONdata(userdata_json_path)
    appinfo = getJSONdata(appinfo_json_path)
    # userdata things
    try:
        learning_lvl = userdata["learning_lvl"]
        username = userdata["username"]
        # app data things
        version = appinfo['version']
        licence = appinfo['licence']
        versionid = appinfo['versionid']
        author = appinfo['author']
    except Exception as err:
        MessageBox.showerror(title=f"{err} Error", message=f"Tried to extract data from JSON but got \"{err}\" exception. Try deleting the JSON and try again or check if the JSON file exists.")
    #==-----GUI-----==#
    homeImg = PhotoImage(file='assets/images/home.png')
    home_btn = Button(root, image=homeImg, width=40, command= lambda : [click.play(), home(root)], relief="solid").pack()
    title_lb = Label(root,font=("Tahoma", 35, 'bold'), fg = "black",  text="Settings", bg='LightBlue').pack()
    hello = Label(root, text=f'Hello, {username}', font=("Tahoma", 20), bg='lightblue').pack()
    userinfo = Button(root, font=("Tahoma", 12), text="User Info", width=40, height=2, command = lambda: [click.play(), show_userinfo(root, username, learning_lvl)], relief="solid").pack(pady=0.1)
    appinfo = Button(root, font=("Tahoma", 12), text='App Info', width=40, height=2, command = lambda : [click.play(), show_appinfo(root, version, licence, versionid, author)], relief="solid").pack(pady=1)
    switchlvl = Button(root, font=("Tahoma", 12), text='Change Learning Level', width=40, height=2, command= lambda: [click.play(), change_learning_level(root, username)], relief="solid").pack(pady=1)
    switchuser = Button(root, font=("Tahoma", 12), text='Change Username', width=40, height=2, command= lambda: [click.play(), change_username(root, learning_lvl)], relief="solid").pack(pady=1)
    about_btn = Button(root, font=("Tahoma", 12), text="About", width=40, height=2, command = lambda: [click.play(), about(root)], relief="solid").pack(pady=1)
    root.mainloop()

if __name__ == '__main__':
    main_gui()
    print("[INFO] Executed")