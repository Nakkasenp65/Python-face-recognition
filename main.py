import os.path
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import face_recognition
import customtkinter as ctk

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


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

        self.title_text_main_window = util.get_text_ctk_label(self.main_window, "Face Recognition", 48, "black")
        self.title_text_main_window.place(x=750, y=20)

        # self.login_button_main_window = util.get_button(self.main_window, "Login", "green", self.login, )
        self.login_button_main_window = util.get_ctk_button(self.main_window, "Login", "black", self.login )
        self.login_button_main_window.place(x=750, y=300)

        # self.register_button_main_window = util.get_button(self.main_window, "Register", "gray", self.register_new_user, fg='black')
        self.register_button_main_window = util.get_ctk_button(self.main_window, "Register", "black", self.register_new_user )
        self.register_button_main_window.place(x=890, y=300)

        self.show_profile_button_new_user_window = util.get_ctk_button(self.main_window, 'Show Profile','blue', self.show_profile)
        self.show_profile_button_new_user_window.place(x=1030, y=300)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        self.student_id = 1
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

    def show_profile(self):
        pass

    def register_new_user(self):

        '#custom tkinter window'
        # self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window = ctk.CTkToplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        self.register_new_user_window.resizable(False, False)
        self.register_new_user_window.title("Register New User")
        self.register_new_user_window.configure(bg='white')

        '#accept button'
        # self.accept_button_register_new_user_window = util.get_ctk_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window = util.get_ctk_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=450)

        '#try again button'
        # self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window = util.get_ctk_button(self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=930, y=450)

        '#capture label'
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

        '# Name Field'
        self.name_entry_label_register_new_user = util.get_text_ctk_label(self.register_new_user_window, 'Full name:', 16, 'white')
        self.name_entry_label_register_new_user.place(x=750, y=40)

        self.name_entry_text_register_new_user = util.get_entry_input(self.register_new_user_window, 'Your name')
        self.name_entry_text_register_new_user.place(x=750, y=70)

        '# Faculty Field'
        self.major_entry_label_register_new_user = util.get_text_ctk_label(self.register_new_user_window, 'Faculty:', 16, 'white')
        self.major_entry_label_register_new_user.place(x=750, y=160)

        # self.major_entry_text_register_new_user = util.get_entry_input(self.register_new_user_window, 'Your faculty')
        self.major_entry_text_register_new_user = util.get_combobox(self.register_new_user_window)
        self.major_entry_text_register_new_user.place(x=750, y=190)

        '# Starting Year Field'
        self.starting_year_label_register_new_user = util.get_text_ctk_label(self.register_new_user_window, 'Starting Year:', 16, 'white')
        self.starting_year_label_register_new_user.place(x=750, y=280)

        self.starting_year_entry_text_register_new_user = util.get_entry_input(self.register_new_user_window, 'Starting year')
        self.starting_year_entry_text_register_new_user.place(x=750, y=310)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def add_to_db(self,name, major, starting_year, student_id):
        ref= db.reference('Students')
        data = {
            'name': name,
            'major': major,
            'starting_year': starting_year,
            'year': 2023 - int(starting_year),
            'total_attendance': 0,
            'last_attendance': 'Never'
        }
        # ref.child(str(student_id)).set(data)
        ref.child("1").set(data)

    def accept_register_new_user(self):

        ref = db.reference('Students')
        name = self.name_entry_text_register_new_user.get()
        major = self.major_entry_text_register_new_user.get()
        starting_year = self.starting_year_entry_text_register_new_user.get()

        loc = face_recognition.face_locations(self.register_new_user_capture)
        encoding_img = face_recognition.face_encodings(self.register_new_user_capture, loc)
        if len(encoding_img) == 0:
            util.show_error("No face detected.")
            return
        else:

            if not name or not major or not starting_year:
                util.empty_fields(self.register_new_user_window)
                print("Please fill in all fields.")
                return

            else:
                util.show_checkmark("Face detected.")
                encoding_img = encoding_img[0]

                self.add_to_db(name, major, starting_year, self.student_id)
                cv2.imwrite(os.path.join(self.db_dir, str(self.student_id) + '.jpg'), self.register_new_user_capture)

                print(encoding_img)
                self.student_id += 1




if __name__ == "__main__":
    app = App()
    app.start()