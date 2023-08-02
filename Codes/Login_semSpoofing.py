import os.path
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import time
from time import sleep
from pymata4 import pymata4

servo_pin = 10
LedTrancado_pin = 4
LedLiberado_pin = 5
triggerPin = 8
echo_pin = 9
board = pymata4.Pymata4()

db_dir = './db'

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        self.add_webcam(self.webcam_label)

        self.sensor()
        self.the_callback()
        self.the_callback1()

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
        name = util.recognize(self.most_recent_capture_arr, db_dir)

        while name in ['unknown_person', 'no_persons_found']:
            print('Ops...', 'Usuário desconhecido. Por favor, registre-se ou tente novamente.')
            self.process_webcam()
            temp_img = './temp.jpg'
            cv2.imwrite(temp_img, self.most_recent_capture_arr)
            name = util.recognize(self.most_recent_capture_arr, db_dir)
            util.LedTrancado(board, LedTrancado_pin, 1)
            time.sleep(5)
                    
        else:
            print('Acesso permitido !', 'Bem-vindo, {}.'.format(name))
            util.LedTrancado(board, LedTrancado_pin, 0)
            util.LedLiberado(board, LedLiberado_pin, 1)
            util.rotateServo(board, servo_pin, 180)
            os.remove(temp_img)
            time.sleep(10)
    
    def the_callback(self, data):
        distance = data[2]
        util.LedTrancado(board, LedTrancado_pin, 0)
        util.LedLiberado(board, LedLiberado_pin, 1)
        print(distance, 'cm')

        if distance < 6:
            print('Porta Fechada!')
            util.rotateServo(board, servo_pin, 0)
            util.LedLiberado(board, LedLiberado_pin, 0)
            self.login()

    def the_callback1(self, data):
        distance = data[2]
        util.LedTrancado(board, LedTrancado_pin, 0)
        util.LedLiberado(board, LedLiberado_pin, 1)
        print(distance, 'cm')

        if distance < 6:
            print('Porta Fechada!')
            util.rotateServo(board, servo_pin, 0)
            util.LedLiberado(board, LedLiberado_pin, 0)
            self.login()

    def sensor(self):
        board.set_pin_mode_sonar(triggerPin, echo_pin, self.the_callback)
        time.sleep(2)

        while True:
            board.sonar_read(triggerPin)
            time.sleep(5)

            
if __name__ == "__main__":
    app = App()
    app.start()
 