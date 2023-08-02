import os.path
import pickle
from tkinter import *
from tkinter import font
from tkinter import messagebox
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util

db_dir = './db'

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x620+350+100")
        self.main_window.overrideredirect(True)
        self.text_label_main_window_title = tk.Label(self.main_window, text = 'Reconhecimento Facial', font=("Arial", 30, "bold"))
        self.text_label_main_window_title.place(x = 400, y = 40)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=100, width=700, height=500)
        self.add_webcam(self.webcam_label)
        self.process_webcam()

        self.logout_button_main_window = util.get_button(self.main_window, 'Sair', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y= 450)
        self.logout_button_main_window.config(cursor="hand2")

        self.view_user_button_main_window = util.get_button(self.main_window, 'Visualizar usuários', 'gray', 
                                                                    self.view_user, fg = 'black')
        self.view_user_button_main_window.place(x=750, y=350)
        self.view_user_button_main_window.config(cursor="hand2")

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Registrar novo usuário', 'gray', 
                                                                    self.register_new_user, fg = 'black')
        self.register_new_user_button_main_window.place(x=750, y=250)
        self.register_new_user_button_main_window.config(cursor="hand2")

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'
    
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

    def logout(self):
        exit()

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x620+350+100")
        self.register_new_user_window.overrideredirect(True)
        self.text_label_register_new_user_window_title = tk.Label(self.register_new_user_window, text = 'Registro de usuários', font=("Arial", 30, "bold"))
        self.text_label_register_new_user_window_title.place(x = 400, y = 40)

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Aceitar', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=400)
        self.accept_button_register_new_user_window.config(cursor="hand2")

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Tentar Novamente', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=500)
        self.try_again_button_register_new_user_window.config(cursor="hand2")

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=100, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x = 750, y = 200)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Por favor, insira o nome:')
        self.text_label_register_new_user.place(x = 750, y = 150)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image = imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
        pickle.dump(embeddings, file)

        util.msg_box('Sucesso!', 'Usuário foi registrado com sucesso !')

        self.register_new_user_window.destroy()

    def view_user(self):
        self.view_user_window = tk.Toplevel(self.main_window)
        self.view_user_window.geometry("1200x620+350+100")
        self.view_user_window.overrideredirect(True)
        self.view_user_window_title = tk.Label(self.view_user_window, text = 'Visualização dos usuários', font=("Arial", 30, "bold"))
        self.view_user_window_title.place(x = 370, y = 40)
        self.view_user_window.grab_set()
        self.view_user_window.attributes("-topmost", True)

        self.delete_button_view_user_window = util.get_small_button(self.view_user_window, 'Deletar usuário', 'gray', self.delete_user, fg = 'black')
        self.delete_button_view_user_window.place(x=425, y=485)
        self.delete_button_view_user_window.config(cursor="hand2")

        self.return_button_view_user_window = util.get_small_button(self.view_user_window, 'Voltar', 'red', self.return_edit_user)
        self.return_button_view_user_window.place(x=425, y=550)
        self.return_button_view_user_window.config(cursor="hand2")

        flist = os.listdir(db_dir)
        self.lbox = tk.Listbox(self.view_user_window, height = 15, width = 35)
        self.lbox.pack(padx=10, pady=100)
        bolded = font.Font(weight='bold', size=16)
        self.lbox.config(font=bolded, cursor = "hand2", background="lightgray")
        for item in flist:
            self.lbox.insert(tk.END, item)

    def return_edit_user(self):
        self.view_user_window.destroy()

    def delete_user(self):
        selected_index = self.lbox.curselection()
        if selected_index:
            name = self.lbox.get(selected_index)
            index = int(selected_index[0])
            path = 'db/'
            file = path + name
            self.view_user_window.attributes('-disabled', 1)
            escolha = messagebox.askyesno(parent = self.view_user_window,title = 'Confirmação', message = 'Deseja realmente excluir esse usuário?')
            self.view_user_window.attributes('-disabled', 0)
            self.view_user_window.focus_force()
            if escolha:
                self.lbox.delete(index)
                os.remove(file)

if __name__ == "__main__":
    app = App()
    app.start()
 