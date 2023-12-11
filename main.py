import tkinter as tk
from tkinter import ttk
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
timer = None
random_dict = None
data_dict = {}

try: 
    data = pandas.read_csv("./data/word_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    data_dict = original_data.to_dict(orient = "records")
else:
    data_dict = data.to_dict(orient = "records")

def next_card():
    global random_dict
    random_dict = random.choice(data_dict)
    french = random_dict["French"]
    canvas.itemconfig(card, image = card_front)
    canvas.itemconfig(title_text, text = "French", fill = "black")
    canvas.itemconfig(word_text, text = french, fill = "black")
    
    global timer
    timer = window.after(3000,flip)
    
def flip():
    english = random_dict["English"]
    canvas.itemconfig(card, image = card_back)
    canvas.itemconfig(title_text, text = "English", fill = "white")
    canvas.itemconfig(word_text, text = english, fil = "white")
    window.after_cancel(timer)
    
def is_known():
    try:
        data_dict.remove(random_dict)
    except:
        next_card()
    else:
        print(len(data_dict))
        
        new_data = pandas.DataFrame(data_dict)
        new_data.to_csv("./data/word_to_learn.csv", index=False)
        next_card()
    
    
window = tk.Tk()
window.title("Flash card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(window, width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
card_front = tk.PhotoImage(file="./images/card_front.png")
card_back = tk.PhotoImage(file="./images/card_back.png")
card = canvas.create_image(400, 263, image = card_front)
title_text = canvas.create_text(400, 160, text="Title", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.grid(column=0,row=0,columnspan=2)

right_img = tk.PhotoImage(file="./images/right.png")
right_button = ttk.Button(window, image=right_img, command = is_known)
right_button.grid(column=1, row=1)

wrong_img = tk.PhotoImage(file="./images/wrong.png")
wrong_button = ttk.Button(window, image=wrong_img, command = next_card)
wrong_button.grid(column=0, row=1)

window.mainloop()