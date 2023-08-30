from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.font as font
import main_file
import pygame.mixer as mixer
import sys, random, time
import json

# sounds stuff
mixer.init()
click = mixer.Sound('assets/sounds/click.wav')
wrong_sound = mixer.Sound('assets/sounds/wrong.wav')
correct = mixer.Sound('assets/sounds/correct.wav')
results = mixer.Sound('assets/sounds/results.mp3')
def get_json(path):
    try:
        with open(path, mode='r') as f:
            data = json.load(f)
            return data
    except Exception:
        print("Unable to fetch data from path")
        return False

class TypeWord(object):
    def __init__(self):
        # gui stuff
        self.type = Tk()
        self.type.geometry("800x750")
        self.type.title("Type the Word - English")
        self.type.iconbitmap("assets/images/logo.ico")
        self.type.config(bg="lightblue")
        try:
            self.data = get_json("assets/data/userdata.json")
            self.username = self.data["username"]
            self.learning_lvl = self.data["learning_lvl"]
            
        except Exception:
            messagebox.showerror(title="Error", message="Couldn't get data. Check if the json file exists or if it's corrupted.")
            self.type.destroy()
            main()
        self.right_wrong = []
        self.times = []
        self.correct = 0
        self.wrong = 0
        self.amt_done = 0
        self.mainFont = font.nametofont("TkDefaultFont")
        self.mainFont.configure(family="Tahoma",
                                   size=20)
        # other things
        self.run()
        self.type.mainloop()

    def check_int(self, value):
        try:
            value = int(value)
            self.prepare(value)
            return True
        except Exception:
            messagebox.showerror(title="Only numbers", message="It seems you have entered a letter or word. Only numbers please!")
            return False
    def choose_amt(self):
        ready_lb = Label(self.type, text="Enter The Amount Of Questions", font=("Tahoma", 30), bg="lightblue")
        ready_lb.pack(pady=80)
        enter = Entry(self.type, font=('Tahoma', 25),relief="solid" , width="30")
        enter.pack()
        next_btn = Button(self.type, text="Next", font=("Tahoma", 20), command= lambda: [click.play(), self.check_int(enter.get())])
        next_btn.pack(pady=10)

    def prepare(self, amt):
        self.clear_widgets()
        ready_lb = Label(self.type, text="Press Start to Begin!", font=("Tahoma", 40), bg="lightblue")
        ready_lb.pack(pady=80)
        next_btn = Button(self.type, text="Start", font=("Tahoma", 20), command= lambda: [click.play(), self.show_q(amt)])
        next_btn.pack(pady=10)
    def clear_widgets(self):
        for widget in self.type.winfo_children():
            widget.forget()
            # print(f"Forgot {widget}")
    def next_q(self, correct_ans, user_ans, question_amt):
        print(f"crt = {correct_ans} | userans = {user_ans}")
        if user_ans == correct_ans:
            end = time.time()
            time_spent = round((end - start), 1)
            correct.play()
            self.times.append(time_spent)
            print(self.times)
            if self.wrg_limit >= 1:
                self.show_q(question_amt)
                self.amt_done += 1
                if self.amt_done >= question_amt:
                    self.show_results(question_amt=question_amt)
                print(self.amt_done)
            else:
                self.correct += 1
                self.right_wrong.append("Correct")
                self.show_q(question_amt)
                self.amt_done += 1
                if self.amt_done >= question_amt:
                    self.show_results(question_amt=question_amt)
                print(self.amt_done)
        else:
            wrong_sound.play()
            if self.wrg_limit >= 1:
                    wrong = Label(self.type, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.type.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
            else:
                    self.wrong += 1
                    self.right_wrong.append("Wrong")
                    wrong = Label(self.type, text="Wrong Answer. :( Try again.", font=("Tahoma", 20), bg="LightBlue", fg="red")
                    wrong.pack()
                    self.type.after(2000, wrong.forget)
                    self.wrg_limit += 1
                    self.wrg_cnt += 1
            
    def show_q(self, amt):
        self.clear_widgets()
        sentence, correct_word = self.generate_word()
        self.type.title("Type the word - English")
        global start
        start = time.time()
        self.wrg_limit = 0
        self.wrg_cnt = 0
        correct_wrng = Label(self.type, text=f"Correct: {self.correct} | Wrong: {self.wrong}", fg = "green" , bg = "lightblue", font=("Tahoma", 20))
        correct_wrng.pack(padx = 150)
        exit_btn = Button(self.type, text="Exit", font=("Tahoma", 14), command= lambda: [click.play(), sys.exit()])
        exit_btn.place(x=0, y=0)
        
        Label(self.type, text=f"{sentence}", font = ("Tahoma", 32), bg="LightBlue").pack(pady=140, padx = 120)
        self.type.bind("<Return>", lambda event: self.next_q(correct_word, user_ans=ansbox.get(), question_amt=amt))
        ansbox = Entry(self.type, font = ("Tahoma", 30))
        ansbox.pack()
        ansbox.focus()

        ans_btn = Button(self.type, command=  lambda : [click.play(),self.next_q(correct_word, user_ans=ansbox.get(), question_amt=amt)] ,text="Go", font=("Tahoma", 20), width=10).pack(pady=50, padx=1)

    def generate_word(self):
        if self.learning_lvl == 1:
            words = self.get_file("assets/data/words_lvl_1.txt")
            words = words.split("\n")
            length = len(words)
        elif self.learning_lvl == 2:
            words = self.get_file("assets/data/words_lvl_2.txt")
            words = words.split("\n")
            length = len(words)
        elif self.learning_lvl == 3:
            words = self.get_file("assets/data/words_lvl_3.txt")
            words = words.split("\n")
            length = len(words)
        else:
            messagebox.showerror(title="Faulty", message=f"Error: Faulty learning level.  The available levels are 1, 2, and 3.  Your level is {self.learning_lvl}. ")
            self.type.destroy()
            main()
            return False
        index = random.randint(1, length - 1)

        word = words[index]
        sentence = f"Type the word \"{word}\"."
        # print(index, words, word, sentence)
        return sentence, word
    
    def show_results(self, question_amt):
        self.clear_widgets()
        total_correct = 0
        total_q = question_amt
        scrollbar = Scrollbar(self.type)
        scrollbar.pack( side = RIGHT, fill = BOTH )
        display = Listbox(self.type, yscrollcommand = scrollbar.set )

        for i in self.right_wrong:
            if i == "Correct":
                total_correct += 1
            else:
                pass
        final_percent = total_correct/total_q
        final_percent_str = f'{final_percent:.2%}'
        self.type.title("Results - English")
        self.type.unbind("<Return>")
        total_time = 0     
        result = Label(self.type, text="Results", font=("Tahoma", 40), bg="lightblue", fg='green')
        result.pack()
        tm = Label(self.type, text="Question Info:", font=("Tahoma", 25), bg='Lightblue', fg="orange")
        tm.pack()
        for i in range(len(self.times)):
            display.insert(i, f"Question {i+1}: {self.times[i]} Seconds | {self.right_wrong[i]}")
    

        for i in range(len(self.times)):
            total_time += self.times[i]
        Label(self.type, text=f"Total Time: {round(total_time, 1)} Seconds", fg="red", bg='LightBlue', font=('Tahoma', 20)).pack()
        Label(self.type, text=f"{self.username}, you got {final_percent_str} correct!", fg="blue", bg='LightBlue', font=('Tahoma', 22)).pack()
        display.pack(padx = 10, pady = 10, expand = YES, fill = "both")
        scrollbar.config(command=display.yview)
        home = Button(self.type, text="Back to Home", bg='yellow', height=2, width=20, command =  lambda : [click.play(), self.type.destroy(), main()])
        home.pack(pady=40)
        results.play()
    def get_file(self, path):
        try:
            with open(path, mode='r') as f:
                data = f.read()
                return data
        except Exception:
            print("Unable to fetch data from path")
            return False
        
    def run(self):
        self.choose_amt()

#################################
typeword = TypeWord

def back_to_home(window):
    window.destroy()
    main_file.mn_menu()
def main():
    root = Tk()
    root.title("Avera: English Practice")
    root.iconbitmap('assets/images/logo.ico')
    root.geometry('550x550')
    root.config(bg="Lightblue")
    homeImg = PhotoImage(file='assets/images/home.png')
    home_btn = Button(root, image=homeImg, width=40, command= lambda : [click.play(), back_to_home(root)], relief="solid").pack()
    lb = Label(root, text="English", font=("Tahoma", 60, 'bold'), fg="yellow", bg='Lightblue').pack()
    typeword_btn = Button(root, font=("Tahoma", 12), text="Type the Word", width=40, height=4, command = lambda: [click.play(), root.destroy(), typeword()], relief="solid").pack(pady=10)
    root.mainloop()
    

if __name__ == "__main__": # testing purposes.
    main()