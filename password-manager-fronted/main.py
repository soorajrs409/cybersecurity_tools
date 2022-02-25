from tkinter import *
from tkinter import messagebox
import passwd_gen
import pyperclip
import json


def make_pass():
    passwd_entry.delete(0, END)
    generated_pass = passwd_gen.gen_pass()
    passwd_entry.insert(0, generated_pass)
    pyperclip.copy(generated_pass)
    # print(passwd_entry.get())   [For debugging ]


def save():
    website = website_entry.get()
    username = username_entry.get()
    passwd = passwd_entry.get()
    dict_data = {
        website: {
            "username": username,
            "password": passwd,
        }
    }

    if len(website) == 0 or len(username) == 0:
        messagebox.showinfo("OOPS", "Seems like you left some fields empty :(")
    else:

        is_ok = messagebox.askokcancel(title="Shall i save ??",
                                       message=f" Web Url : {website} \n Username : {username} \n "
                                               f"Password : {passwd}")
        if is_ok:

            try:
                with open("data.json", "r") as df:
                    data = json.load(df)
                    data.update(dict_data)
            except FileNotFoundError:
                with open("data.json", "w") as df:
                    json.dump(dict_data, df, indent=4)
            else:
                with open("data.json", "w") as df:
                    json.dump(data, df, indent=4)

            finally:
                website_entry.delete(0, END)
                username_entry.delete(0, END)
                passwd_entry.delete(0, END)


def search_data():
    website = website_entry.get()
    try:
        with open("data.json") as df:
            data = json.load(df)
    except FileNotFoundError:
        messagebox.showwarning("OOPS", "No entries on database.")
    else:
        if website in data:
            email = data[website]["username"]
            password = data[website]["password"]
            messagebox.showinfo(website, f"username : {email}\npassword : {password}")
        else:
            messagebox.showwarning("OOPS", f"seems like the data for {website} does not exist")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.resizable(0, 0)

# Canvas
canvas = Canvas(height=200, width=200)
logo_image = PhotoImage(file="rsz_electron.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)

passwd_label = Label(text="Password:")
passwd_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=24)
website_entry.grid(row=1, column=1)
website_entry.focus()

username_entry = Entry(width=40)
username_entry.grid(row=2, column=1, columnspan=2)
# username_entry.insert(0,"enter your email/username here ")

passwd_entry = Entry(width=24)
passwd_entry.grid(row=3, column=1)

# Button

gen_passwd_btn = Button(text="GeneratePassword", width=12, command=make_pass)
gen_passwd_btn.grid(row=3, column=2)

search_btn = Button(text="Search", width=12, command=search_data)
search_btn.grid(row=1, column=2)

add_btn = Button(text="Add", width=38, command=save)
add_btn.grid(row=4, column=1, columnspan=2)

window.mainloop()
