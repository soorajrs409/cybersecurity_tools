from tkinter import *
from tkinter import messagebox
import math

CYAN = "#00ffff"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
COUNTER = None
STATUS = False


def reset():
    window.after_cancel(COUNTER)
    canvas.itemconfigure(timer_text, text="00:00")
    check_mark.config(text="")
    global reps, STATUS
    reps = 0
    STATUS = False


def start_process():
    global STATUS
    if not STATUS:
        start_timer()


def start_timer():
    global STATUS
    STATUS = True
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        messagebox.showwarning("Long Break", "Time for a long break")
        timer(long_break_sec)

    elif reps % 2 == 0:
        messagebox.showwarning("Short Break", "Time for a short break")
        timer(short_break_sec)

    else:
        messagebox.showwarning("Break over", "Cmon start working")
        timer(work_sec)



def timer(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfigure(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global COUNTER
        COUNTER = window.after(1000, timer, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
            check_mark.config(text=marks)


window = Tk()
window.title("Electron's Timer")
window.resizable(0, 0)

canvas = Canvas(width=512, height=512, bg=CYAN)
electron_img = PhotoImage(file="electron.png")
canvas.create_image(256, 256, image=electron_img)
timer_text = canvas.create_text(256, 300, text="00:00", font=(FONT_NAME, 40, "bold"), fill="#000fff000")
canvas.pack()

start_btn = Button(text="Start", command=start_process)
start_btn.place(x=10, y=480)

reset_btn = Button(text="Reset", command=reset)
reset_btn.place(x=440, y=480)

check_mark = Label(fg=CYAN)
check_mark.place(x=250, y=480)

window.mainloop()
