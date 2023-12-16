import os
import pickle

import tkinter as tk
from tkinter import messagebox
import face_recognition

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox



def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 20)
                    )

    return button


def get_ctk_button(window, text, color, command):
    button = ctk.CTkButton(master=window,
                           width=120,
                           height=50,
                           text=text,
                           command=command,
                           fg_color='black',
                           corner_radius=50,
                           font=('Century Gothic', 16)
                           )
    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_img_label_with_text(window, text):
    label = ctk.CTkLabel(window, text=text)


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 16), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window, height=0.5, width=15, font=("Arial", 32))
    return inputtxt


'#custom tkinter input'


def get_entry_input(window, placeholder_text):
    inputtxt = ctk.CTkEntry(window, placeholder_text=placeholder_text, height=50, width=300, font=("Arial", 16),
                            placeholder_text_color='#676767', corner_radius=50)
    return inputtxt


'#custom tkinter label'


def get_information_text_ctk_label(window, text, fontsize, text_color):
    label = ctk.CTkEntry(window,
                         textvariable=text,
                         font=("Century Gothic", fontsize),
                         text_color=text_color,
                         height=300,
                         width=300,
                         justify='left',
                         state='disabled',
                         corner_radius=50
                         )
    return label

def get_text_ctk_label(window, text, fontsize, text_color):
    if text.__contains__('-1'):
        text = '0'
    label = ctk.CTkLabel(window,
                         text=text,
                         font=("Century Gothic", fontsize),
                         text_color=text_color,
                         )
    return label


'#custom tkinter comboBox'
def get_combobox(window):
    values = ['Computer science','Computer Engineering', 'Communications', 'Engineering', 'Business']
    combobox = ctk.CTkComboBox(window, values=values, width=300, height=50, font=("Arial", 16), corner_radius=50)
    return combobox


'#custom messagebox'


def show_error(text_message):
    CTkMessagebox(title="Error", message=text_message, icon="cancel")


def show_checkmark(text_message):
    CTkMessagebox(title="Notification", message=text_message,icon="check", option_1="Okay")

def empty_fields(window):
    name_entry_empty_label = get_text_ctk_label(window, 'Name is not correct.', 14, '#B00000')
    name_entry_empty_label.place(x=750, y=120)
    major_entry_empty_label = get_text_ctk_label(window, 'Major is not correct.', 14, '#B00000')
    major_entry_empty_label.place(x=750, y=240)
    starting_year_entry_empty_label = get_text_ctk_label(window, 'Starting year is not correct.', 14, '#B00000')
    starting_year_entry_empty_label.place(x=750, y=360)



def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'
