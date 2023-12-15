import os.path
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import customtkinter as ctk

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class App:

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattendacerealtime-ffcf8-default-rtdb.firebaseio.com/"
    })

    ref = db.reference('Students')
    year = 2023
    student_id = 1

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.title("Face Recognition")

        self.login_button_main_window = util.get_button(self.main_window, "Login", "green", self.login, )
        self.login_button_main_window.place(x=750, y=300)

        self.register_button_main_window = util.get_button(self.main_window, "Register", "gray", self.register_new_user, fg='black')
        self.register_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label

        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        pass

    def register_new_user(self):
        # self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window = ctk.CTkToplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        self.register_new_user_window.resizable(False, False)
        self.register_new_user_window.title("Register New User")
        self.register_new_user_window.configure(bg='white')

        '#accept button'
        # self.accept_button_register_new_user_window = util.get_ctk_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window = util.get_ctk_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=345)

        '#try again button'
        # self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window = util.get_ctk_button(self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=930, y=345)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        # self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        # self.entry_text_register_new_user.place(x=750, y=150)
        #
        # self.name_entry_text_register_new_user = util.get_entry_name(self.register_new_user_window)
        # self.name_entry_text_register_new_user.place(x=750, y=60)
        #
        # self.name_entry_label_register_new_user = util.get_text_label(self.register_new_user_window, 'name:')
        # self.name_entry_label_register_new_user.place(x=750, y=40)

        # Name Field
        self.name_entry_label_register_new_user = util.get_text_ctk_label(self.register_new_user_window, 'Full name:')
        self.name_entry_label_register_new_user.place(x=750, y=40)

        self.name_entry_text_register_new_user = util.get_entry_input(self.register_new_user_window, 'Enter your name')
        self.name_entry_text_register_new_user.place(x=750, y=80)

        # Faculty Field
        self.faculty_entry_label_register_new_user = util.get_text_ctk_label(self.register_new_user_window, 'Faculty:')
        self.faculty_entry_label_register_new_user.place(x=750, y=140)

        self.faculty_entry_text_register_new_user = util.get_entry_input(self.register_new_user_window, 'Enter your faculty')
        self.faculty_entry_text_register_new_user.place(x=750, y=180)

        # Starting Year Field
        self.starting_year_label_register_new_user = util.get_text_ctk_label(self.register_new_user_window, text='Starting Year:')
        self.starting_year_label_register_new_user.place(x=750, y=240)

        self.starting_year_entry_text_register_new_user = util.get_entry_input(self.register_new_user_window, 'Enter your starting year')
        self.starting_year_entry_text_register_new_user.place(x=750, y=280)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def add_to_db(self,name, faculty, starting_year, student_id):
        ref= db.reference('Students')
        data = {
            'name': name,
            'faculty': faculty,
            'starting_year': starting_year,
            'year': 2023 - int(starting_year),
            'total_attendance': 0,
            'last_attendance': 'Never'
        }
        ref.child(str(student_id)).set(data)

    def accept_register_new_user(self):

        ref = db.reference('Students')
        name = self.name_entry_text_register_new_user.get()
        faculty = self.faculty_entry_text_register_new_user.get()
        starting_year = self.starting_year_entry_text_register_new_user.get()
        if not name or not faculty or not starting_year:
            print("Please fill in all fields.")
            return
        self.add_to_db(name, faculty, starting_year, self.student_id)
        self.student_id += 1


if __name__ == "__main__":
    app = App()
    app.start()