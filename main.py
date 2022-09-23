# ---------------------------- PASSWORD GENERATOR ------------------------------- #
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------- #
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_random_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(LETTERS) for _ in range(nr_letters)]
    password_list += [random.choice(NUMBERS) for _ in range(nr_numbers)]
    password_list += [random.choice(SYMBOLS) for _ in range(nr_symbols)]

    random.shuffle(password_list)

    password_input.delete(0, END)
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def validate(website, email, password):
    return len(website) > 0 and len(email) > 0 and len(password) > 0


def save():
    website = website_input.get()
    email = user_name_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if validate(website, email, password):
        save_json_file(new_data)

        website_input.delete(0, END)
        password_input.delete(0, END)
        website_input.focus()
    else:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")


# ---------------------------- JSON READING WRITING ------------------------------- #
def read_json_file():
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
        return data


def save_json_file(new_data):
    try:
        data = read_json_file()
        data.update(new_data)
    except FileNotFoundError:
        data = new_data
    except json.decoder.JSONDecodeError:
        data = new_data
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)


def search_website():
    website = website_input.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave website field empty")
        return

    try:
        data = read_json_file()
        messagebox.showinfo(
            title=website,
            message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}"
        )
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No data.json file found")
    except json.decoder.JSONDecodeError:
        messagebox.showinfo(title="Oops", message="File data.json is empty")
    except KeyError:
        messagebox.showinfo(title="Oops", message=f"No password for {website}")


# ---------------------------- UI SETUP ------------------------------- #

# Window Object
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

# Displaying the image
canvas = Canvas(window, width=200, height=200)
logo_image = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo_image)  # 100, 100 means it will be centered in the canvas
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

user_name_label = Label(text="Email/Username:")
user_name_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Input text / Entries
website_input = Entry(width=21)
website_input.grid(row=1, column=1, columnspan=1)
website_input.focus()

user_name_input = Entry(width=35)
user_name_input.grid(row=2, column=1, columnspan=2)
user_name_input.insert(0, "andres@andrescourt.com")

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

# Buttons
generate_password = Button(text="Generate Password", width=12, command=generate_random_password)
generate_password.grid(row=3, column=2)

search_button = Button(text="Search", width=12, command=search_website)
search_button.grid(row=1, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
