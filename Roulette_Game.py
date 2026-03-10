from tkinter import *
from random import randint

# ------------------ WINDOW ------------------
screen = Tk()
screen.title("Roulette")
screen.configure(bg="#88BDF2")
screen.geometry("1300x780")

# ------------------ VARIABLES ------------------
balance = 3000
bet = 100

selected_numbers = set()
selected_types = set()

number_buttons = {}
type_buttons = {}

r_clr = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
b_clr = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

conflict_groups = [
    {"Even", "Odd"},
    {"red", "black"},
    {"1-18", "19-36"},
    {"1st12", "2nd12", "3rd12"}
]

# ------------------ INFO BOX ------------------
box = Frame(screen, width=500, height=330, bg="pink")
box.place(x=450, y=420)

Label(box, text="GAME INFO", font=("arial",20,"bold"),bg="pink").place(x=160, y=10)

box_balance = Label(box, text=f"Balance : {balance}",font=("arial",16,"bold"), bg="pink")
box_balance.place(x=50, y=60)

box_selected = Label(box, text="Selected : -",font=("arial",15,"bold"),bg="pink")
box_selected.place(x=50, y=100)

box_result = Label(box, text="Result Number : -",font=("arial",16,"bold"), bg="pink")
box_result.place(x=50, y=155)

box_status = Label(box, text="",font=("arial",20,"bold"), bg="pink")
box_status.place(x=240, y=230)

# ------------------ FUNCTIONS ------------------
def update_selected_label():
    text = ""
    if selected_numbers:
        text += "Numbers : " + ",".join(map(str, sorted(selected_numbers))) + "\n"
    if selected_types:
        text += "Bets : " + ",".join(selected_types)
    box_selected.config(text=text if text else "Selected : -")

# -------- NUMBER TOGGLE --------
def mychoice_no(n):
    btn = number_buttons[n]
    if n in selected_numbers:
        selected_numbers.remove(n)
        reset_colors()
    else:
        selected_numbers.add(n)
        btn.config(bg="yellow")
    update_selected_label()

# -------- TYPE TOGGLE --------
def mychoice_type(t):
    btn = type_buttons[t]

    if t in selected_types:
        selected_types.remove(t)
        btn.config(bg="green")
        update_selected_label()
        return

    for group in conflict_groups:
        if t in group:
            for other in group:
                if other in selected_types:
                    selected_types.remove(other)
                    type_buttons[other].config(bg="green")

    selected_types.add(t)
    btn.config(bg="yellow")
    update_selected_label()

# -------- RESET NUMBER COLORS --------
def reset_colors():
    for n, btn in number_buttons.items():
        if n == 0:
            btn.config(bg="green", fg="white")
        elif n in r_clr:
            btn.config(bg="red", fg="white")
        else:
            btn.config(bg="black", fg="white")

# -------- CHECK TYPE WIN --------
def is_type_win(t, result):
    if t == "red" and result in r_clr: return True
    if t == "black" and result in b_clr: return True
    if t == "Even" and result % 2 == 0 and result != 0 : return True
    if t == "Odd" and result % 2 == 1: return True
    if t == "1-18" and 1 <= result <= 18: return True
    if t == "19-36" and 19 <= result <= 36: return True
    if t == "1st12" and 1 <= result <= 12: return True
    if t == "2nd12" and 13 <= result <= 24: return True
    if t == "3rd12" and 25 <= result <= 36: return True
    return False

# -------- SPIN --------
def spin():
    global balance

    if not selected_numbers and not selected_types:
        box_status.config(text="PLEASE SELECT BET", fg="red")
        return

    reset_colors()

    result = randint(0, 36)
    box_result.config(text=f"Result Number : {result}")
    number_buttons[result].config(bg="yellow", fg="black")

    total_bet = bet * (len(selected_numbers) + len(selected_types))
    total_win = 0
    win = False

    for n in selected_numbers:
        if n == result:
            total_win += bet * 36
            win = True

    winning_types = []

    for t in selected_types:
        if is_type_win(t, result):
            total_win += bet * 2
            winning_types.append(t)
            win = True

    # reset all type buttons
    for t, btn in type_buttons.items():
        btn.config(bg="green")

    # highlight only winning types
    for t in winning_types:
        type_buttons[t].config(bg="yellow")

    balance += total_win - total_bet
    box_balance.config(text=f"Balance : {balance}")

    box_status.config(text="YOU WIN" if win else "YOU LOSE",
                      fg="green" if win else "red")

# ------------------ NUMBER BUTTONS ------------------
def create_row(start, y):
    x = 100
    for i in range(start, 37, 3):
        clr = "red" if i in r_clr else "black"
        btn = Button(screen, text=i, bg=clr, fg="white",
                     width=6, height=2, font=('arial',19,'bold'),
                     command=lambda n=i: mychoice_no(n))
        btn.place(x=x, y=y)
        number_buttons[i] = btn
        x += 100

def zero():
    btn = Button(screen, text=0, bg="green", fg="white",
                 width=6, height=7, font=('arial',19,'bold'),
                 command=lambda: mychoice_no(0))
    btn.place(x=5, y=10)
    number_buttons[0] = btn

# ------------------ TYPE BUTTONS ------------------
def bottom_buttons():
    first = [("1st12",104),("2nd12",500),("3rd12",900)]
    second = [
        ("1-18",104),("Even",295),("red",500),
        ("black",700),("Odd",900),("19-36",1096)
    ]

    for txt,x in first:
        btn = Button(screen,text=txt,bg="green",fg="white",
                     width=26,height=2,font=('arial',19,'bold'),
                     command=lambda t=txt: mychoice_type(t))
        btn.place(x=x,y=242)
        type_buttons[txt] = btn

    for txt,x in second:
        btn = Button(screen,
                     text=txt if txt not in ("red","black") else "",
                     bg=txt if txt in ("red","black") else "green",
                     fg="white",width=13,height=2,
                     font=('arial',19,'bold'),
                     command=lambda t=txt: mychoice_type(t))
        btn.place(x=x,y=320)
        type_buttons[txt] = btn

# ------------------ SPIN BUTTON ------------------
Button(screen,text="SPIN",bg="gold",
       font=('arial',25,'bold'),
       width=10,command=spin).place(x=450,y=630)

# ------------------ INIT ------------------
create_row(3,10)
create_row(2,85)
create_row(1,160)
zero()
bottom_buttons()

screen.mainloop()