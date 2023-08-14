import os.path
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import utility
from time import sleep
from pyfirmata import Arduino, util
import time

servo_pin = 10
LedLiberado_pin = 5
reed_pin = 8

PORT = 'COM3'
board = Arduino(PORT) 
it = util.Iterator(board)
it.start()
servo = board.get_pin('d:{}:s'.format(10))
led1 = board.digital[5]

db_dir = './db'

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.webcam_label = utility.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        self.add_webcam(self.webcam_label)

        self.sensor()

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

    def login(self):
        temp_img = './temp.jpg'
        self.process_webcam()
        cv2.imwrite(temp_img, self.most_recent_capture_arr)
        name = utility.recognize(self.most_recent_capture_arr, db_dir)

        while name in ['unknown_person', 'no_persons_found']:
            print('Ops...', 'Usuário desconhecido. Por favor, registre-se ou tente novamente.')
            self.process_webcam()
            temp_img = './temp.jpg'
            cv2.imwrite(temp_img, self.most_recent_capture_arr)
            name = utility.recognize(self.most_recent_capture_arr, db_dir)
            time.sleep(5)
                    
        else:
            servo.write(0)
            led1.write(1)
            print('Acesso permitido !', 'Bem-vindo, {}.'.format(name))
            os.remove(temp_img)
            time.sleep(10)

    def sensor(self):
        reed_pin_mode = board.get_pin('d:{}:i'.format(reed_pin))
        reed_pin_mode.enable_reporting()

        while True:
            # Leia o estado do pino do reed switch (0 para aberto, 1 para fechado)
            self.reed_state = reed_pin_mode.read()
            
            if self.reed_state == 1:
                print("Porta fechada")
                led1.write(0)
                servo.write(180)
                self.login()
            else:
                print("Porta aberta")
                led1.write(1)        
            time.sleep(0.1)  # Pequeno atraso para evitar leituras rápidas repetidas
     
if __name__ == "__main__":
    app = App()
    app.start()
 