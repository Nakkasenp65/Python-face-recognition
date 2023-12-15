import os
import pickle

import tkinter as tk
from tkinter import messagebox
import face_recognition

import customtkinter as ctk


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
                           height=35,
                           text=text,
                           command=command,
                           fg_color='black',
                           corner_radius=20,
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


def get_entry_input(window, placeholder_text):
    inputtxt = ctk.CTkEntry(window, placeholder_text=placeholder_text, height=50, width=300, font=("Arial", 16))
    return inputtxt


def get_text_ctk_label(window, text):
    label = ctk.CTkLabel(window,
                         text=text,
                         font=("Century Gothic", 16),
                         text_color="black",
                         )
    return label

def msg_box(title, description):
    messagebox.showinfo(title, description)


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
