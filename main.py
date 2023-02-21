from tkinter import *

import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient='records')
current_card = {}
def next_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(current_title, text='French', fill = 'black')
    canvas.itemconfig(current_word, text = current_card['French'], fill = 'black')
    canvas.itemconfig(background_img, image = front_card_image)
    timer =  window.after(3000, flip_card)
def flip_card():
    canvas.itemconfig(current_title, text = 'English Translation', fill='white')
    canvas.itemconfig(current_word, text = current_card['English'], fill = 'white')
    canvas.itemconfig(background_img, image= back_card_image)

def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index= None)
    next_card()

window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg= BACKGROUND_COLOR)

timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_image = PhotoImage(file="images/card_front.png")
background_img = canvas.create_image(400, 263,image = front_card_image)
back_card_image = PhotoImage(file="images/card_back.png")
canvas.grid(row=0, column=0, columnspan=2)
current_title = canvas.create_text(400, 153, text='Title', font=('Ariel', 30, 'italic'))
current_word = canvas.create_text(400, 220, text = 'Word',font=('Ariel', 50, 'bold') )

cross_img = PhotoImage(file = "images/wrong.png")
cross_btn = Button(image=cross_img, highlightthickness=0, command=next_card)
cross_btn.grid(row=1, column=0)

mark_img = PhotoImage(file = "images/right.png")
mark_btn = Button(image=mark_img, highlightthickness=0, command=is_known)
mark_btn.grid(row=1, column=1)
next_card()
window.mainloop()