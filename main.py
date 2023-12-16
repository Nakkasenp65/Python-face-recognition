import datetime
import os.path
import subprocess
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import face_recognition
import customtkinter as ctk
from customtkinter import CTkImage

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



class App:

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattendacerealtime-ffcf8-default-rtdb.firebaseio.com/"
    })


    def __init__(self):

        self.ref = db.reference('Students')
        self.total_student_object = self.ref.get()
        if self.total_student_object is None:
            self.student_id = 0
        else:
            self.student_id = len(self.ref.get())-1
        print(self.student_id)

        self.main_window = tk.Tk()
        self.main_window.geometry("980x520+350+100")
        self.main_window.title("Face Recognition")

        self.show_total_students_label = util.get_text_ctk_label(self.main_window, 'Total students: ', 16, 'black')
        self.show_total_students_label.place(x=750, y=70)

        self.show_total_students_label = util.get_text_ctk_label(self.main_window, str(self.student_id), 16, 'black')
        self.show_total_students_label.place(x=870, y=70)

        self.title_text_main_window = util.get_text_ctk_label(self.main_window, "Face Recognition", 24, "black")
        self.title_text_main_window.place(x=750, y=20)

        self.login_button_main_window = util.get_ctk_button(self.main_window, "Login", "black", self.login )
        self.login_button_main_window.place(x=820, y=300)

        self.register_button_main_window = util.get_ctk_button(self.main_window, "Register", "black", self.register_new_user )
        self.register_button_main_window.place(x=820, y=360)

        self.show_profile_button_new_user_window = util.get_ctk_button(self.main_window, 'Profile','blue', self.show_profile)
        self.show_profile_button_new_user_window.place(x=820, y=420)

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
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        print(output)
        static_student_id = output.split(',')[1][:-3]
        print(static_student_id)

        try:
            check_id = int(static_student_id)
            os.remove(unknown_img_path)
        except ValueError:
            util.show_error("No match found.")
            os.remove(unknown_img_path)
            return

        student_name = self.ref.child(static_student_id).get()['name']
        student_name = student_name.split(' ')[0]
        total_attendance = self.ref.child(static_student_id).get()['total_attendance']
        total_attendance += 1
        last_attendance = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.ref.child(static_student_id).update({'last_attendance': last_attendance,
                                                  'total_attendance': total_attendance})
        print('Student ID: ', static_student_id)
        notification = "Hello again, "+student_name+"\nDate: "+last_attendance
        util.show_checkmark(notification)

    def show_profile(self):
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        os.remove(unknown_img_path)
        print(output)
        static_student_id = output.split(',')[1][:-3]
        print(static_student_id)

        if static_student_id.__contains__("unknown_person"):
            util.show_error("Sorry, you are not registered.\n\nTry registering first.")
            return
        elif static_student_id.__contains__("no_persons_found"):
            util.show_error("Sorry, no face detected.\n\nPlease, Try again")
            return
        else:
            static_student_id

        student_name = self.ref.child(static_student_id).get()['name']
        student_major = self.ref.child(static_student_id).get()['major']
        student_starting_year = self.ref.child(static_student_id).get()['starting_year']
        student_year = self.ref.child(static_student_id).get()['year']
        student_total_attendance = self.ref.child(static_student_id).get()['total_attendance']
        student_last_attendance = self.ref.child(static_student_id).get()['last_attendance']
        student_information = ("Name: "+student_name
                         +"\nMajor: "+student_major
                         +"\nStarting year: "+student_starting_year
                         +"\nYear: "+str(student_year)
                         +"\nTotal attendance: "
                         +str(student_total_attendance)
                         +"\nLast attendance: "+student_last_attendance)

        self.register_new_user_window = ctk.CTkToplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        self.register_new_user_window.resizable(False, False)
        self.register_new_user_window.title("Register New User")
        self.register_new_user_window.configure(bg='white')

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_profile_img_to_label(static_student_id, self.capture_label)

        self.profile_label_register_new_user = util.get_text_ctk_label(self.register_new_user_window, 'Profile', 36, 'white')
        self.profile_label_register_new_user.place(x=750, y=20)

        self.information_label_register_new_user = util.get_information_text_ctk_label(self.register_new_user_window, student_information, 24, 'white')
        self.information_label_register_new_user.place(x=750, y=60)





    def register_new_user(self):

        is_no_face = False
        is_registered = False
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        print(output)
        os.remove(unknown_img_path)
        if output.__contains__("unknown_person"):
            is_registered = False
        elif output.__contains__("no_persons_found"):
            is_no_face = True
        else:
            is_registered = True

        if is_registered:
            print(is_registered)
            util.show_error("This person is already registered.")
            return
        elif is_no_face:
            print(is_no_face)
            util.show_error("No face detected.")
            return
        else:


            '#custom tkinter window'
            # self.register_new_user_window = tk.Toplevel(self.main_window)
            self.register_new_user_window = ctk.CTkToplevel(self.main_window)
            self.register_new_user_window.geometry("1200x520+370+120")
            self.register_new_user_window.resizable(False, False)
            self.register_new_user_window.title("Register New User")

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

    def add_profile_img_to_label(self, number_id, label):

        profile_img = cv2.imread(os.path.join(self.db_dir, str(number_id) + '.jpg'))
        img_ = cv2.cvtColor(profile_img, cv2.COLOR_BGR2RGB)
        profile_img = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=profile_img)
        label.imgtk = imgtk
        label.configure(image=imgtk)

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
        ref.child(str(student_id)).set(data)

    def accept_register_new_user(self):

        is_no_face = False
        is_registered = False
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.register_new_user_capture)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        print(output)
        os.remove(unknown_img_path)
        if output.__contains__("unknown_person"):
            is_registered = False
        elif output.__contains__("no_persons_found"):
            is_no_face = True
        else:
            is_registered = True

        if is_registered:
            print(is_registered)
            util.show_error("This person is already registered.")
            return
        elif is_no_face:
            print(is_no_face)
            util.show_error("No face detected.")
            return
        else:
            print("Face detected.")
            # ref = db.reference('Students')
            name = self.name_entry_text_register_new_user.get()
            major = self.major_entry_text_register_new_user.get()
            starting_year = self.starting_year_entry_text_register_new_user.get()

            if not name or not major or not starting_year:
                util.empty_fields(self.register_new_user_window)
                print("Please fill in all fields.")
                return

            else:
                util.show_checkmark("Registered success.")
                # encoding_img.append(encoding_img[0])

                self.student_id += 1
                self.add_to_db(name, major, starting_year, self.student_id)
                cv2.imwrite(os.path.join(self.db_dir, str(self.student_id) + '.jpg'), self.register_new_user_capture)
                self.show_total_students_label.configure(text=str(self.student_id))
                self.register_new_user_window.destroy()





if __name__ == "__main__":
    app = App()
    app.start()