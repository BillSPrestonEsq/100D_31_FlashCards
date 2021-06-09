from tkinter import *
import pandas as pd
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 20, "italic")
WORD_FONT = ("Arial", 40, "bold")
timer = None

# ----------- NEXT CARD ------------ #
def next_card():
    global card_front
    global window
    global timer
    global current_card

    window.after_cancel(timer)
    canvas.create_image(400, 263, image=card_front)
    current_card = choose_rand_card()
    update_card("French")
    auto_timer(3)

# --------- UPDATE CARD ----------- #
def update_card(new_language):
    global current_language
    global current_word
    global current_card
    global df
    global language
    global word

    current_word = current_card[new_language].to_string(index=False)
    current_language = new_language
    language = canvas.create_text(400, 100, text=current_language, font=LANGUAGE_FONT)
    word = canvas.create_text(400, 200, text=current_word, font=WORD_FONT)

# -------- CORRECT BUTTON --------- #
def correct_answer():
    remove_card()
    if not df.size == 0:
        next_card()
    else:
        right_button.config(state=DISABLED)
        wrong_button.config(state=DISABLED)
        messagebox.showinfo(title="Congratulations!", message="You have completed all the flash cards!")


# --------- WRONG BUTTON ---------- #
def wrong_answer():
    next_card()
    pass

# ------------- TIMER ------------- #
def auto_timer(countdown):
    global card_back
    global window
    global timer

    if countdown <= 0:
        canvas.create_image(400, 263, image=card_back)
        update_card("English")
    else:
        timer = window.after(1000, auto_timer, countdown - 1)

# ---------- CHOOSE CARD ---------- #
def choose_rand_card():
    global df
    return df.sample()

# ---------- REMOVE CARD ---------- #
def remove_card():
    global df
    df = df.drop(current_card.index)
    df.to_csv('data/words_to_learn.csv',index=False)


# ---------- IMPORT DATA ---------- #
try:
    df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    print("words_to_learn not found")
    df = pd.read_csv("data/french_words.csv")
finally:
    current_card = df.sample()
    current_language = "French"
    current_word = current_card["French"].to_string(index=False)

# -------------- UI --------------- #

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
answer_right = PhotoImage(file="images/right.png")
answer_wrong = PhotoImage(file="images/wrong.png")

right_button = Button(image=answer_right, highlightthickness=0, command=correct_answer)
wrong_button = Button(image=answer_wrong, highlightthickness=0, command=wrong_answer)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 100, text=current_language, font=LANGUAGE_FONT)
word = canvas.create_text(400, 200, text=current_word, font=WORD_FONT)

right_button.grid(row=1, column=0)
wrong_button.grid(row=1, column=1)
canvas.grid(row=0, column=0, columnspan=2)

auto_timer(3)

window.mainloop()