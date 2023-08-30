###############################################################
# All GUI & logic for math.
# WARNING: I'm not the best programmer so there will be a lot of "bad spots"
# Other note: There might be some convention that I don't follow (because I don't know it).
# @Author: TheSpikyHedgehog
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
import random, sys, time
import tkinter.font as font
import main_file
import pygame.mixer as mixer
import json

mixer.init()
correct = mixer.Sound("assets/sounds/correct.wav")
wrong_sound = mixer.Sound("assets/sounds/wrong.wav")
click = mixer.Sound("assets/sounds/click.wav")
results = mixer.Sound("assets/sounds/results.mp3")

#First, some global functions.
def getJSONdata(path):
    try:
        with open(path, mode='r') as f:
            data = json.load(f)
            f.close()
        return data
    except Exception:
        print("Unable to fetch data from path")
userdata = getJSONdata('assets/data/userdata.json')

#Next, classes.
class Addition(object): #process Addition gui and logic
    def __init__(self):
        # set up variables and GUI
        root.destroy()
        self.add = Tk()
        self.add.geometry("800x750")
        self.add.title("Addition - Practice")
        self.add.configure(bg="LightBlue")
        self.add.iconbitmap('./assets/images/logo.ico')
        self.run()
        self.wrngRng = []
        self.times = []
        self.cardsNum = 0
        self.wrg_cnt = 0
        self.wrg_limit = 0
        self.correct = 0
        self.wrong = 0
        self.mainFont = font.nametofont("TkDefaultFont")
        self.mainFont.configure(family="Tahoma",
                                   size=20)
        self.username = userdata['username']
        self.learning_lvl = userdata['learning_lvl']
        self.add.mainloop()

    #-----------GUI SECTION-----------------
    def ask_mode(self):
        lb = Label(self.add, font=("Tahoma", 40), text="Select Mode", bg = "LightBlue")
        lb.pack()
        self.add.title("Select Mode - Addition - Practice")
        normal_mode = Button(self.add, text="Normal Mode", font=("Tahoma", 12), width=40, height=4, relief="solid", command= lambda: [click.play(),self.flashcardsAmt(whichGen='normal')])
        normal_mode.pack(pady=60)
        double_mode = Button(self.add, text="Doubles Mode", font=("Tahoma", 12), width=40, height=4, relief="solid", command= lambda: [click.play(),self.flashcardsAmt(whichGen='doubles')])
        double_mode.pack(pady=0)
    def flashcardsAmt(self, whichGen):
        self.clearWidgets()
        lb = Label(self.add, font=("Tahoma", 20), text="Select Amount of Math Facts to be Displayed", bg="LightBlue")
        lb.pack()
        self.add.title("Select Amount - Addition - Practice")
        #dropdown list things
        clicked = StringVar()
        options = [10, 20, 40, 50, 100]
        clicked.set(2)
        dropdown = OptionMenu(self.add, clicked, *options)
        dropdown.pack(pady=1)
        btn = Button(self.add, text="Select", font = ("Tahoma", 15), command= lambda : [click.play(),self.addNumRange(int(clicked.get()), whichGen)])
        btn.pack()

    def addNumRange(self, fcAmt, whichGen):
        self.clearWidgets()
        
        lb = Label(self.add, text="Select Range of Math Facts (ex. 10, 10)", font=("Tahoma", 20), bg="LightBlue")
        lb.pack()
        self.add.title("Select Range - Addition - Practice")
        #dropdown list things
        clicked = StringVar()
        options = ['-10, 10', '0, 10', '0, 20', '0, 40', '0, 50', '0, 100', '0, 200']
        clicked.set('0, 10')
        dropdown = OptionMenu(self.add, clicked, *options)
        dropdown.pack(pady=1)
        btn = Button(self.add, text="Begin", font = ("Tahoma", 15), command= lambda : [click.play(),self.addFactsGUIGen(clicked.get(), fcAmt, whichGen)])
        btn.pack()

    def next_q(self, correctAns, userAns, numRng, code, fcAmt, whichGen): #a bit too much paramaters
        print(f"crt = {correctAns} | userans = {userAns} |, {numRng}")
        userAns = int(userAns)
        
        if code == 'skip':
            end = time.time()
            time_spent = round((end - start), 1)
            self.cardsNum += 1
            self.wrngRng.append("Skipped")
            if self.cardsNum >= fcAmt + 1:
                self.showResults(self.times, self.wrngRng, fcAmt)
            else:
                self.times.append(time_spent)
                self.cardsNum +=1
                print(self.times)
                show = Label(self.add, text=f"Skipped!", fg = "red", font=("Tahoma", 20), bg="lightblue")
                show.pack()
                
                print(self.cardsNum)
                self.add.after(2000, lambda:self.addFactsGUIGen(numRng, fcAmt))
            
            if self.wrg_limit >= 1:
                pass
            else:
                self.wrong += 1
            
        else:
            if userAns == correctAns:
                end = time.time()
                time_spent = round((end - start), 1)
                correct.play()
                self.times.append(time_spent)
                
                if self.wrg_limit >= 1:
                    self.addFactsGUIGen(numRng, fcAmt, whichGen)
                    self.cardsNum += 1
                    if self.cardsNum >= fcAmt:
                        self.showResults(self.times, self.wrngRng, fcAmt)
                    
                else:
                    self.correct += 1
                    self.wrngRng.append("Correct")
                    self.addFactsGUIGen(numRng, fcAmt, whichGen)
                    self.cardsNum += 1
                    if self.cardsNum >= fcAmt:
                        self.showResults(self.times, self.wrngRng, fcAmt)
                    
            else:
                wrong_sound.play()
                if self.wrg_limit >= 1:
                    wrong = Label(self.add, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.add.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
                else:
                    self.wrong += 1
                    self.wrngRng.append("Wrong")
                    wrong = Label(self.add, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.add.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
        
       

            

    def addFactsGUIGen(self, numRng, fcAmt, whichGen):
        #print(f"[DEBUG]: FlashcardsAmt: {fcAmt}, Number Range: {numRng}")
        self.clearWidgets()

        self.add.title("Flashcards - Addition - Practice")
        global skip_btn
        global start
        start = time.time()
        skip_btn = Button(self.add, text="Skip", command = lambda: [click.play(),self.next_q(correctAns, correctAns, numRng, 'skip', fcAmt, whichGen)] , font=("Tahoma", 15))
        skip_btn.pack(pady=1, padx=0)
        self.wrg_limit = 0
        self.wrg_cnt = 0
        correct_wrng = Label(self.add, text=f"Correct: {self.correct} | Wrong: {self.wrong}", fg = "green" , bg = "lightblue", font=("Tahoma", 20))
        correct_wrng.pack(padx = 150)
        exit_btn = Button(self.add, text="Exit", font=("Tahoma", 14), command= lambda:[click.play(),sys.exit()])
        exit_btn.place(x=0, y=0)
        if whichGen == "normal":
            correctAns, add1, add2 = self.genFacts(numRng)
        elif whichGen == "doubles":
            correctAns, add1, add2 = self.genDoublesFacts(numRng)
        
        Label(self.add, text=f"{add1} + {add2} = ", font = ("Tahoma", 60), bg="LightBlue").pack(pady=140, padx = 120)
        self.add.bind("<Return>", lambda event: [click.play(),self.next_q(correctAns, ansbox.get(), numRng, 'userinput', fcAmt, whichGen)])
        ansbox = Entry(self.add, font = ("Tahoma", 30))
        ansbox.pack()
        ansbox.focus()

        ans_btn = Button(self.add, command=  lambda : [click.play(),self.next_q(correctAns, ansbox.get(), numRng, 'userinput', fcAmt, whichGen)] ,text="Go", font=("Tahoma", 20), width=10).pack(pady=50, padx=1)

    
    def genFacts(self, numRng):
       
        numRngMin = int(numRng.split(',')[0])
        numRngMax = int(numRng.split(',')[1])
        #since this is ONLY addition, no need to think about other operations.
        add1 = random.randint(numRngMin, numRngMax)
        add2 = random.randint(numRngMin, numRngMax)
        # print(add1, add2)
        correctAns = add1 + add2
        # print(correctAns)
        return correctAns, add1, add2
    
    def genDoublesFacts(self, numRng):
       
        numRngMin = int(numRng.split(',')[0])
        numRngMax = int(numRng.split(',')[1])
        #since this is double's, all the addends are the same
        add = random.randint(numRngMin, numRngMax)
        
        
        correctAns = add + add
        add1 = add
        add2 = add
        return correctAns, add1, add2
        
    def showResults(self, times, rightorwrong, fcAmt):
        self.clearWidgets()
        total_correct = 0
        total_questions = fcAmt
        for i in self.wrngRng:
            print(i)
            if i == "Correct":
                total_correct += 1
                print('correct')
            else:
                print('wrong')
        print(total_correct)
        final_percent = total_correct/total_questions
        final_percent_str = f'{final_percent:.2%}'
        print(final_percent, final_percent_str)
        scrollbar = Scrollbar(self.add)
        scrollbar.pack( side = RIGHT, fill = BOTH )
        display = Listbox(self.add, yscrollcommand = scrollbar.set )

        self.add.title("Results - Addition - Practice")
        self.add.unbind("<Return>")
        
        result = Label(self.add, text="Results", font=("Tahoma", 40), bg="lightblue", fg='green')
        result.pack()
        tm = Label(self.add, text="Question Info:", font=("Tahoma", 25), bg='Lightblue', fg="orange")
        tm.pack() 
        for i in range(len(times)):
            display.insert(i, f"Question {i+1}: {times[i]} Seconds | {self.wrngRng[i]}")
        
        total_time = 0

        for i in range(len(times)):
            total_time += times[i]
        Label(self.add, text=f"Total Time: {round(total_time, 1)} Seconds", fg="red", bg='LightBlue', font=('Tahoma', 20)).pack()
        Label(self.add, text=f"{self.username}, you got {final_percent_str} correct!", fg="blue", bg='LightBlue', font=('Tahoma', 22)).pack()
        display.pack(padx = 10, pady = 10, expand = YES, fill = "both")
        scrollbar.config(command=display.yview)
        home = Button(self.add, text="Back to Home", bg='yellow', height=2, width=20, command =  lambda : [click.play(),mn_menu(self, selectclass='addclass')])
        home.pack(pady=40)
        results.play()
    def destroyWindow(self):
        self.add.destroy()

    def clearWidgets(self): #Very important, forgets widgets and paves the way for new window
        for widget in self.add.winfo_children():
            widget.forget()
            
    def run(self):
        
        self.ask_mode()
        
        
        
class Subtraction(object):
    def __init__(self):
        root.destroy()
        self.sub = Tk()
        self.sub.iconbitmap('./assets/images/logo.ico')
        self.sub.geometry("800x700")
        self.sub.title("Subtraction - Practice")
        self.sub.configure(bg="LightBlue")
        self.sub.iconbitmap('./assets/images/logo.ico')
        self.run()
        self.wrngRng = []
        self.times = []
        self.cardsNum = 0
        self.wrg_cnt = 0
        self.wrg_limit = 0
        self.correct = 0
        self.wrong = 0
        self.mainFont = font.nametofont("TkDefaultFont")
        self.mainFont.configure(family="Tahoma",
                                   size=20)
        self.username = userdata['username']
        self.learning_lvl = userdata['learning_lvl']
        self.sub.mainloop()
    #--------GUI SECTION----------
    def flashcardsAmt(self):
    
        lb = Label(self.sub, font=("Tahoma", 20), text="Select Amount of Math Facts to be Displayed", bg="LightBlue")
        lb.pack()
        self.sub.title("Select Amount - Subtraction - Practice")
            #dropdown list things
        clicked = StringVar()
        options = [10, 20, 40, 50, 100]
        clicked.set(10)
        dropdown = OptionMenu(self.sub, clicked, *options)
        dropdown.pack(pady=1)
        btn = Button(self.sub, text="Select", font = ("Tahoma", 15), command= lambda : [click.play(),self.addNumRange(int(clicked.get()))])
        btn.pack()

    def addNumRange(self, fcAmt):
        self.clearWidgets()
        #print(f"[DEBUG]: {fcAmt}")
        print(fcAmt)
        lb = Label(self.sub, text="Select Range of Math Facts (ex. 10, 10)", font=("Tahoma", 20), bg="LightBlue")
        lb.pack()
        self.sub.title("Select Range - Subtraction - Practice")
        #dropdown list things
        clicked = StringVar()
        options = ['-10, 10', '0, 10', '0, 20', '0, 40', '0, 50', '0, 100', '0, 200']
        clicked.set('0, 10')
        dropdown = OptionMenu(self.sub, clicked, *options)
        dropdown.pack(pady=1)
        btn = Button(self.sub, text="Begin", font = ("Tahoma", 15), command= lambda : [click.play(),self.subFactsGUIGen(clicked.get(), fcAmt)])
        btn.pack()

    def next_q(self, correctAns, userAns, numRng, code, fcAmt):
        print(f"crt = {correctAns} | userans = {userAns} |, {numRng}")
        userAns = int(userAns)
        
        if code == 'skip':
            end = time.time()
            time_spent = round((end - start), 1)
            self.cardsNum += 1
            self.wrngRng.append("Skipped")
            if self.cardsNum >= fcAmt + 1:
                self.showResults(self.times, self.wrngRng, fcAmt)
            else:
                self.times.append(time_spent)
                self.cardsNum +=1
                print(self.times)
                show = Label(self.sub, text=f"Skipped!", fg = "red", font=("Tahoma", 20), bg="lightblue")
                show.pack()
                
                print(self.cardsNum)
                self.sub.after(2000, lambda:self.subFactsGUIGen(numRng, fcAmt))
            
            if self.wrg_limit >= 1:
                pass
            else:
                self.wrong += 1
            
        else:
            if userAns == correctAns:
                end = time.time()
                time_spent = round((end - start), 1)
                correct.play()
                self.times.append(time_spent)
                print(self.times)
                if self.wrg_limit >= 1:
                    self.subFactsGUIGen(numRng, fcAmt)
                    self.cardsNum += 1
                    if self.cardsNum >= fcAmt:
                        self.showResults(self.times, self.wrngRng, fcAmt)
                    print(self.cardsNum)
                else:
                    self.correct += 1
                    self.wrngRng.append("Correct")
                    self.subFactsGUIGen(numRng, fcAmt)
                    self.cardsNum += 1
                    if self.cardsNum >= fcAmt:
                        self.showResults(self.times, self.wrngRng, fcAmt)
                    print(self.cardsNum)
            else:
                wrong_sound.play()
                if self.wrg_limit >= 1:
                    wrong = Label(self.sub, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.sub.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
                else:
                    self.wrong += 1
                    self.wrngRng.append("Wrong")
                    wrong = Label(self.sub, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.sub.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
        
       

            

    def subFactsGUIGen(self, numRng, fcAmt):
        #print(f"[DEBUG]: FlashcardsAmt: {fcAmt}, Number Range: {numRng}")
        self.clearWidgets()

        self.sub.title("Flashcards - Subtraction - Practice")
        global skip_btn
        global start
        start = time.time()
        skip_btn = Button(self.sub, text="Skip", command = lambda: self.next_q(correctAns, correctAns, numRng, 'skip', fcAmt) , font=("Tahoma", 15))
        skip_btn.pack(pady=1, padx=0)
        self.wrg_limit = 0
        self.wrg_cnt = 0
        correct_wrng = Label(self.sub, text=f"Correct: {self.correct} | Wrong: {self.wrong}", fg = "green" , bg = "lightblue", font=("Tahoma", 20))
        correct_wrng.pack(padx = 150)
        exit_btn = Button(self.sub, text="Exit", font=("Tahoma", 14), command= lambda : [click.play(), sys.exit()])
        exit_btn.place(x=0, y=0)
        correctAns, eq = self.genFacts(numRng)
        
        Label(self.sub, text=f"{eq} = ", font = ("Tahoma", 60), bg="LightBlue").pack(pady=140, padx = 120)
        self.sub.bind("<Return>", lambda event: [click.play(),self.next_q(correctAns, ansbox.get(), numRng, 'userinput', fcAmt)])
        ansbox = Entry(self.sub, font = ("Tahoma", 30))
        ansbox.pack()
        ansbox.focus()

        ans_btn = Button(self.sub, command=  lambda : [click.play(),self.next_q(correctAns, ansbox.get(), numRng, 'userinput', fcAmt)] ,text="Go", font=("Tahoma", 20), width=10).pack(pady=50, padx=1)

        

    def genFacts(self, numRng):
       
        numRngMin = int(numRng.split(',')[0])
        numRngMax = int(numRng.split(',')[1])
        #since this is ONLY addition, no need to think about other operations.
        add1 = random.randint(numRngMin, numRngMax)
        add2 = random.randint(numRngMin, numRngMax)
        # print(add1, add2)
        if add1 > add2:
            correctAns = add1 - add2
            eq = f'{add1} - {add2}'
        else:
            correctAns = add2 - add1
            eq = f'{add2} - {add1}'
        # print(correctAns)
        return correctAns, eq
        
    def showResults(self, times, rightorwrong, fcAmt):
        self.clearWidgets()
        total_correct = 0
        total_questions = fcAmt
        scrollbar = Scrollbar(self.sub)
        scrollbar.pack( side = RIGHT, fill = BOTH )
        display = Listbox(self.sub, yscrollcommand = scrollbar.set )
        for i in self.wrngRng:
            print(i)
            if i == "Correct":
                total_correct += 1
                print('correct')
            else:
                print('wrong')
        final_percent = total_correct/total_questions
        final_percent_str = f'{final_percent:.2%}'
        self.sub.title("Results - Subtraction - Practice")
        self.sub.unbind("<Return>")
        
        result = Label(self.sub, text="Results", font=("Tahoma", 40), bg="lightblue", fg='green')
        result.pack()
        tm = Label(self.sub, text="Question Info:", font=("Tahoma", 25), bg='Lightblue', fg="orange")
        tm.pack()
        for i in range(len(times)):
            display.insert(i, f"Question {i+1}: {times[i]} Seconds | {self.wrngRng[i]}")
        
        total_time = 0

        for i in range(len(times)):
            total_time += times[i]
        Label(self.sub, text=f"Total Time: {round(total_time, 1)} Seconds", fg="red", bg='LightBlue', font=('Tahoma', 20)).pack()
        Label(self.sub, text=f"{self.username}, you got {final_percent_str} correct!", fg="blue", bg='LightBlue', font=('Tahoma', 22)).pack()
        display.pack(padx = 10, pady = 10, expand = YES, fill = "both")
        scrollbar.config(command=display.yview)
        home = Button(self.sub, text="Back to Home", bg='yellow', height=2, width=20, command =  lambda : [click.play(),mn_menu(self, 'subclass')])
        home.pack(pady=40)
        results.play()
    def destroyWindow(self):
        self.sub.destroy()
    def clearWidgets(self):
        for widget in self.sub.winfo_children():
            widget.forget()
            
    def run(self):
        self.flashcardsAmt()
        

class Multiplication(object):
    def __init__(self):
        root.destroy()
        self.mul = Tk()
        self.mul.iconbitmap('./assets/images/logo.ico')
        self.mul.geometry("800x700")
        self.mul.title("Multiplication - Practice")
        self.mul.configure(bg="LightBlue")
        self.mul.iconbitmap('./assets/images/logo.ico')
        self.run()
        self.wrngRng = []
        self.times = []
        self.cardsNum = 0
        self.wrg_cnt = 0
        self.wrg_limit = 0
        self.correct = 0
        self.wrong = 0
        self.mainFont = font.nametofont("TkDefaultFont")
        self.mainFont.configure(family="Tahoma",
                                   size=20)
        self.username = userdata['username']
        self.learning_lvl = userdata['learning_lvl']
        self.mul.mainloop()
    #--------GUI SECTION----------
    def flashcardsAmt(self):
    
        lb = Label(self.mul, font=("Tahoma", 20), text="Select Amount of Math Facts to be Displayed", bg="LightBlue")
        lb.pack()
        self.mul.title("Select Amount - Multiplication - Practice")
            #dropdown list things
        clicked = StringVar()
        options = [10, 20, 40, 50, 100]
        clicked.set(10)
        dropdown = OptionMenu(self.mul, clicked, *options)
        dropdown.pack(pady=1)
        btn = Button(self.mul, text="Select", font = ("Tahoma", 15), command= lambda : [click.play(),self.mulNumRange(int(clicked.get()))])
        btn.pack()

    def mulNumRange(self, fcAmt):
        self.clearWidgets()
        
        print(fcAmt)
        lb = Label(self.mul, text="Select Range of Math Facts (ex. 10, 10)", font=("Tahoma", 20), bg="LightBlue")
        lb.pack()
        self.mul.title("Select Range - Multiplication - Practice")
        #dropdown list things
        clicked = StringVar()
        options = ['-10, 10', '0, 10', '0, 20', '0, 40', '0, 50', '0, 100', '0, 200']
        clicked.set('0, 10')
        dropdown = OptionMenu(self.mul, clicked, *options)
        dropdown.pack(pady=1)
        btn = Button(self.mul, text="Begin", font = ("Tahoma", 15), command= lambda : [click.play(),self.mulFactsGUIGen(clicked.get(), fcAmt)])
        btn.pack()

    def next_q(self, correctAns, userAns, numRng, code, fcAmt):
        print(f"crt = {correctAns} | userans = {userAns} |, {numRng}")
        userAns = int(userAns)
        
        if code == 'skip':
            end = time.time()
            time_spent = round((end - start), 1)
            self.cardsNum += 1
            self.wrngRng.append("Skipped")
            if self.cardsNum >= fcAmt + 1:
                self.showResults(self.times, self.wrngRng, fcAmt)
            else:
                self.times.append(time_spent)
                self.cardsNum +=1
                print(self.times)
                show = Label(self.mul, text=f"Skipped!", fg = "red", font=("Tahoma", 20), bg="lightblue")
                show.pack()
                
                print(self.cardsNum)
                self.mul.after(2000, lambda:self.mulFactsGUIGen(numRng, fcAmt))
            
            if self.wrg_limit >= 1:
                pass
            else:
                self.wrong += 1
            
        else:
            if userAns == correctAns:
                end = time.time()
                time_spent = round((end - start), 1)
                correct.play()
                self.times.append(time_spent)
                print(self.times)
                if self.wrg_limit >= 1:
                    self.mulFactsGUIGen(numRng, fcAmt)
                    self.cardsNum += 1
                    if self.cardsNum >= fcAmt:
                        self.showResults(self.times, self.wrngRng, fcAmt)
                    print(self.cardsNum)
                else:
                    self.correct += 1
                    self.wrngRng.append("Correct")
                    self.mulFactsGUIGen(numRng, fcAmt)
                    self.cardsNum += 1
                    if self.cardsNum >= fcAmt:
                        self.showResults(self.times, self.wrngRng, fcAmt)
                    print(self.cardsNum)
            else:
                wrong_sound.play()
                if self.wrg_limit >= 1:
                    wrong = Label(self.mul, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.mul.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
                else:
                    self.wrong += 1
                    self.wrngRng.append("Wrong")
                    wrong = Label(self.mul, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.mul.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
        
       

            

    def mulFactsGUIGen(self, numRng, fcAmt):
        #print(f"[DEBUG]: FlashcardsAmt: {fcAmt}, Number Range: {numRng}")
        self.clearWidgets()

        self.mul.title("Flashcards - Multiplication - Practice")
        global skip_btn
        global start
        start = time.time()
        skip_btn = Button(self.mul, text="Skip", command = lambda: [click.play(),self.next_q(correctAns, correctAns, numRng, 'skip', fcAmt)] , font=("Tahoma", 15))
        skip_btn.pack(pady=1, padx=0)
        self.wrg_limit = 0
        self.wrg_cnt = 0
        correct_wrng = Label(self.mul, text=f"Correct: {self.correct} | Wrong: {self.wrong}", fg = "green" , bg = "lightblue", font=("Tahoma", 20))
        correct_wrng.pack(padx = 150)
        exit_btn = Button(self.mul, text="Exit", font=("Tahoma", 14), command= lambda : [click.play(),sys.exit()])
        exit_btn.place(x=0, y=0)
        correctAns, eq = self.genFacts(numRng)
        
        Label(self.mul, text=f"{eq} = ", font = ("Tahoma", 60), bg="LightBlue").pack(pady=140, padx = 120)
        self.mul.bind("<Return>", lambda event: [click.play(),self.next_q(correctAns, ansbox.get(), numRng, 'userinput', fcAmt)])
        ansbox = Entry(self.mul, font = ("Tahoma", 30))
        ansbox.pack()
        ansbox.focus()

        ans_btn = Button(self.mul, command=  lambda : [click.play(),self.next_q(correctAns, ansbox.get(), numRng, 'userinput', fcAmt)] ,text="Go", font=("Tahoma", 20), width=10).pack(pady=50, padx=1)

        

    def genFacts(self, numRng):
       
        numRngMin = int(numRng.split(',')[0])
        numRngMax = int(numRng.split(',')[1])
        #since this is ONLY addition, no need to think about other operations.
        mul1 = random.randint(numRngMin, numRngMax)
        mul2 = random.randint(numRngMin, numRngMax)
        # print(add1, add2)
        correctAns = mul1 * mul2
        print(type(correctAns))
        print(type(1/2))
        if type(1/2) == int:
            print("LOLOLOL")
        eq = f'{mul1} x {mul2}'
        # print(correctAns)
        return correctAns, eq
        
    def showResults(self, times, rightorwrong, fcAmt):
        self.clearWidgets()
        total_correct = 0
        total_questions = fcAmt
        scrollbar = Scrollbar(self.mul)
        scrollbar.pack( side = RIGHT, fill = BOTH )
        display = Listbox(self.mul, yscrollcommand = scrollbar.set )
        for i in self.wrngRng:
            print(i)
            if i == "Correct":
                total_correct += 1
                print('correct')
            else:
                print('wrong')

        final_percent = total_correct/total_questions
        final_percent_str = f'{final_percent:.2%}'
        self.mul.title("Results - Multiplication - Practice")
        self.mul.unbind("<Return>")
        
        result = Label(self.mul, text="Results", font=("Tahoma", 40), bg="lightblue", fg='green')
        result.pack()
        tm = Label(self.mul, text="Question Info:", font=("Tahoma", 25), bg='Lightblue', fg="orange")
        tm.pack()
        for i in range(len(times)):
            display.insert(i, f"Question {i+1}: {times[i]} Seconds | {self.wrngRng[i]}")
        
        total_time = 0

        for i in range(len(times)):
            total_time += times[i]
        Label(self.mul, text=f"Total Time: {round(total_time, 1)} Seconds", fg="red", bg='LightBlue', font=('Tahoma', 20)).pack()
        Label(self.mul, text=f"{self.username}, you got {final_percent_str} correct!", fg="blue", bg='LightBlue', font=('Tahoma', 22)).pack()
        display.pack(padx = 10, pady = 10, expand = YES, fill = "both")
        scrollbar.config(command=display.yview)
        home = Button(self.mul, text="Back to Home", bg='yellow', height=2, width=20, command =  lambda : [click.play(),mn_menu(self, 'mulclass')])
        home.pack(pady=40)
        results.play()
    def destroyWindow(self):
        self.mul.destroy()
    def clearWidgets(self):
        for widget in self.mul.winfo_children():
            widget.forget()
            
    def run(self):
        self.flashcardsAmt()
class Division(object):
    def __init__(self):
        root.destroy()
        self.div = Tk()
        self.div.iconbitmap('./assets/images/logo.ico')
        self.div.geometry("800x700")
        self.div.title("Division")
        self.div.configure(bg="LightBlue")
        self.div.iconbitmap('./assets/images/logo.ico')
        self.run()
        self.wrngRng = []
        self.times = []
        self.cardsNum = 0
        self.wrg_cnt = 0
        self.wrg_limit = 0
        self.correct = 0
        self.wrong = 0
        self.mainFont = font.nametofont("TkDefaultFont")
        self.mainFont.configure(family="Tahoma",
                                   size=20)
        self.username = userdata['username']
        self.learning_lvl = userdata['learning_lvl']
        self.div.mainloop()
    #--------GUI SECTION----------
    def flashcardsAmt(self):
    
        lb = Label(self.div, font=("Tahoma", 20), text="Select Amount of Math Facts to be Displayed", bg="LightBlue")
        lb.pack()
        self.div.title("Select Amount - Division - Practice")
            #dropdown list things
        clicked = StringVar()
        options = [10, 20, 40, 50, 100]
        clicked.set(10)
        dropdown = OptionMenu(self.div, clicked, *options)
        dropdown.pack(pady=1)
        btn = Button(self.div, text="Select", font = ("Tahoma", 15), command= lambda : [click.play(),self.addNumRange(int(clicked.get()))])
        btn.pack()

    def addNumRange(self, fcAmt):
        self.clearWidgets()
        #print(f"[DEBUG]: {fcAmt}")
        print(fcAmt)
        lb = Label(self.div, text="Select Range of Math Facts (ex. 10, 10)", font=("Tahoma", 20), bg="LightBlue")
        lb.pack()
        self.div.title("Select Range - Division - Practice")
        #dropdown list things
        clicked = StringVar()
        options = ['-10, 10', '1, 10', '1, 20']
        clicked.set('1, 10')
        dropdown = OptionMenu(self.div, clicked, *options)
        dropdown.pack(pady=1)
        btn = Button(self.div, text="Begin", font = ("Tahoma", 15), command= lambda : [click.play(),self.divFactsGUIGen(clicked.get(), fcAmt)])
        btn.pack()

    def next_q(self, correctAns, userAns, numRng, code, fcAmt):
        print(f"crt = {correctAns} | userans = {userAns} |, {numRng}")
        userAns = int(userAns)
        
        if code == 'skip':
            end = time.time()
            time_spent = round((end - start), 1)
            self.cardsNum += 1
            self.wrngRng.append("Skipped")
            if self.cardsNum >= fcAmt + 1:
                self.showResults(self.times, self.wrngRng)
            else:
                self.times.append(time_spent)
                self.cardsNum +=1
                print(self.times)
                show = Label(self.div, text=f"Skipped!", fg = "red", font=("Tahoma", 20), bg="lightblue")
                show.pack()
                
                print(self.cardsNum)
                self.div.after(2000, lambda:self.divFactsGUIGen(numRng, fcAmt))
            
            if self.wrg_limit >= 1:
                pass
            else:
                self.wrong += 1
            
        else:
            if userAns == correctAns:
                end = time.time()
                time_spent = round((end - start), 1)
                correct.play()
                self.times.append(time_spent)
                print(self.times)
                if self.wrg_limit >= 1:
                    self.divFactsGUIGen(numRng, fcAmt)
                    self.cardsNum += 1
                    if self.cardsNum >= fcAmt:
                        self.showResults(self.times, self.wrngRng, fcAmt)
                    print(self.cardsNum)
                else:
                    self.correct += 1
                    self.wrngRng.append("Correct")
                    self.divFactsGUIGen(numRng, fcAmt)
                    self.cardsNum += 1
                    if self.cardsNum >= fcAmt:
                        self.showResults(self.times, self.wrngRng, fcAmt)
                    print(self.cardsNum)
            else:
                wrong_sound.play()
                if self.wrg_limit >= 1:
                    wrong = Label(self.div, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.div.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
                else:
                    self.wrong += 1
                    self.wrngRng.append("Wrong")
                    wrong = Label(self.div, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.div.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
        
       

            

    def divFactsGUIGen(self, numRng, fcAmt):
        #print(f"[DEBUG]: FlashcardsAmt: {fcAmt}, Number Range: {numRng}")
        self.clearWidgets()

        self.div.title("Flashcards - Division - Practice")
        global skip_btn
        global start
        start = time.time()
        skip_btn = Button(self.div, text="Skip", command = lambda: self.next_q(correctAns, correctAns, numRng, 'skip', fcAmt) , font=("Tahoma", 15))
        skip_btn.pack(pady=1, padx=0)
        self.wrg_limit = 0
        self.wrg_cnt = 0
        correct_wrng = Label(self.div, text=f"Correct: {self.correct} | Wrong: {self.wrong}", fg = "green" , bg = "lightblue", font=("Tahoma", 20))
        correct_wrng.pack(padx = 150)
        exit_btn = Button(self.div, text="Exit", font=("Tahoma", 14), command= lambda: [click.play(), sys.exit()])
        exit_btn.place(x=0, y=0)
        correctAns, eq = self.genFacts(numRng)
        
        Label(self.div, text=f"{eq} = ", font = ("Tahoma", 60), bg="LightBlue").pack(pady=140, padx = 120)
        self.div.bind("<Return>", lambda event: self.next_q(correctAns, ansbox.get(), numRng, 'userinput', fcAmt))
        ansbox = Entry(self.div, font = ("Tahoma", 30))
        ansbox.pack()
        ansbox.focus()

        ans_btn = Button(self.div, command=  lambda : [click.play(),self.next_q(correctAns, ansbox.get(), numRng, 'userinput', fcAmt)] ,text="Go", font=("Tahoma", 20), width=10).pack(pady=50, padx=1)

        

    def genFacts(self, numRng):
       
        numRngMin = int(numRng.split(',')[0])
        numRngMax = int(numRng.split(',')[1])
        #since this is ONLY addition, no need to think about other operations.
        add1 = random.randint(numRngMin, numRngMax)
        add2 = random.randint(numRngMin, numRngMax)
        
       
        mul = add1 * add2
        choice = random.randint(0, 1)
        if choice == 0:
            eq = f'{mul} ÷ {add1}'
            correctAns = mul / add1
        else:
            eq = f'{mul} ÷ {add2}'
            correctAns = mul / add2
        return correctAns, eq
        
    def showResults(self, times, rightorwrong, fcAmt):
        self.clearWidgets()
        total_correct = 0
        total_questions = fcAmt
        for i in self.wrngRng:
            print(i)
            if i == "Correct":
                total_correct += 1
                print('correct')
            else:
                print('wrong')
        final_percent = total_correct/total_questions
        final_percent_str = f'{final_percent:.2%}'
        scrollbar = Scrollbar(self.div)
        scrollbar.pack( side = RIGHT, fill = BOTH )
        display = Listbox(self.div, yscrollcommand = scrollbar.set )

        self.div.title("Results - Division - Practice")
        self.div.unbind("<Return>")
        
        result = Label(self.div, text="Results", font=("Tahoma", 40), bg="lightblue", fg='green')
        result.pack()
        tm = Label(self.div, text="Question Info:", font=("Tahoma", 25), bg='Lightblue', fg="orange")
        tm.pack()
        for i in range(len(times)):
            display.insert(i, f"Question {i+1}: {times[i]} Seconds | {self.wrngRng[i]}")
        
        total_time = 0

        for i in range(len(times)):
            total_time += times[i]
        Label(self.div, text=f"Total Time: {round(total_time, 1)} Seconds", fg="red", bg='LightBlue', font=('Tahoma', 20)).pack()
        Label(self.div, text=f"{self.username}, you got {final_percent_str} correct!", fg="blue", bg='LightBlue', font=('Tahoma', 22)).pack()
        display.pack(padx = 10, pady = 10, expand = YES, fill = "both")
        scrollbar.config(command=display.yview)
        home = Button(self.div, text="Back to Home", bg='yellow', height=2, width=20, command =  lambda : [click.play(),mn_menu(self, 'divclass')])
        home.pack(pady=40)
        results.play()
    def destroyWindow(self):
        self.div.destroy()
    def clearWidgets(self):
        for widget in self.div.winfo_children():
            widget.forget()
            
    def run(self):
        self.flashcardsAmt()
# classes
addclass = Addition
subclass = Subtraction
mulclass = Multiplication
divclass = Division
def back_to_home():
    root.destroy()
    main_file.mn_menu()
def mn_menu(self, selectclass): #this is main menu for after the first one has been executed
    if selectclass == 'addclass':
        addclass.destroyWindow(self)
    elif selectclass == 'subclass':
        subclass.destroyWindow(self)
    elif selectclass == 'mulclass':
        mulclass.destroyWindow(self)
    elif selectclass == 'divclass':
        divclass.destroyWindow(self)
    global root
    root = Tk()
    root.geometry("550x550")
    root.title("Avera: Math Practice")
    root.iconbitmap('./assets/images/logo.ico')
    root.configure(bg='LightBlue')
    homeImg = PhotoImage(file='assets/images/home.png')
    home_btn = Button(root, image=homeImg, width=40, command= lambda : [click.play(),back_to_home()], relief="solid").pack()
    title_lb = Label(root,font=("Tahoma", 60, 'bold'), fg = "yellow",  text="Math", bg='LightBlue').pack()
    add_btn = Button(root, font=("Tahoma", 12), text="Addition", width=40, height=4, command = lambda: [click.play(), addclass().run], relief="solid").pack(pady=1)
    sub_btn = Button(root, font=("Tahoma", 12), text='Subtraction', width=40, height=4, command = lambda : [click.play(),subclass().run], relief="solid").pack(pady=2)
    div_btn = Button(root, font=("Tahoma", 12), text='Division', width=40, height=4, command= lambda: [click.play(),divclass().run], relief="solid").pack(pady=3)
    mul_btn = Button(root, font=("Tahoma", 12), text="Multiplication", width=40, height=4, command = lambda: [click.play(),mulclass().run], relief="solid").pack(pady=4)
    root.mainloop()

def main():
    global root
    root = Tk()
    root.geometry("550x550")
    root.title("Avera: Math Practice")
    root.iconbitmap('assets/images/logo.ico')
    root.configure(bg='LightBlue')
    homeImg = PhotoImage(file='assets/images/home.png')
    home_btn = Button(root, image=homeImg, width=40, command= lambda : [click.play(), back_to_home()], relief="solid").pack()
    title_lb = Label(root,font=("Tahoma", 60, 'bold'), fg = "yellow",  text="Math", bg='LightBlue').pack()
    add_btn = Button(root, font=("Tahoma", 12), text="Addition", width=40, height=4, command = lambda: [click.play(), addclass().run], relief="solid").pack(pady=1)
    sub_btn = Button(root, font=("Tahoma", 12), text='Subtraction', width=40, height=4, command = lambda : [click.play(),subclass().run], relief="solid").pack(pady=2)
    div_btn = Button(root, font=("Tahoma", 12), text='Division', width=40, height=4, command= lambda: [click.play(),divclass().run], relief="solid").pack(pady=3)
    mul_btn = Button(root, font=("Tahoma", 12), text="Multiplication", width=40, height=4, command = lambda: [click.play(),mulclass().run], relief="solid").pack(pady=4)
    root.mainloop()

if __name__ == "__main__": # testing purposes
    main()