from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

try:
    to_learn = pandas.read_csv("data/words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError:
    to_learn = pandas.read_csv("data/french_words.csv").to_dict(orient="records")


def flip_card():
    canvas.itemconfig(canvas_img, image=canvas_back_img)
    canvas.itemconfig(title, fill="white", text="English")
    canvas.itemconfig(word, fill="white", text=current_card["English"])


def next_card():
    global current_card, flip_timer
    # Reset the flip_timer in case we click "next card" before the previous card was actually flipped
    window.after_cancel(flip_timer)
    # Start a new flip_timer so the card is flipped if you wait 3sec (if next card not pressed before)
    flip_timer = window.after(3000, flip_card)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_img, image=canvas_front_img)
    canvas.itemconfig(word, fill="black", text=current_card["French"])
    canvas.itemconfig(title, fill="black", text="French")


def got_it_next():
    to_learn.remove(current_card)
    pandas.DataFrame(to_learn).to_csv("data/words_to_learn.csv", index=False)
    next_card()






window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
canvas_front_img = PhotoImage(file="images/card_front.png")
canvas_back_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=canvas_front_img)
title = canvas.create_text(400, 150, text="French", fill="black", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="word", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightbackground=BACKGROUND_COLOR, command=got_it_next)
right_button.grid(column=1, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=1)


# Starting the game with a first card displaying:
next_card()


window.mainloop()

