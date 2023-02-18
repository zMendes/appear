import tkinter as tk
from tkinter import  ttk
import cv2
import numpy as np
from dtos import RegistrationData

def CaptureImage(show : bool = False) -> np.ndarray:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        _, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        if show:
            cv2.imshow("frame", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return frame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Setting up the window
        self.title('Register')
        self.geometry('400x150')
        self.resizable(0, 0)
        self.attributes('-toolwindow', True)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.__create_widgets()

        # Setting up the variables
        self.registration = None

    

    def __create_widgets(self):
        ttk.Label(self, text='Name:').grid(
            column=0,
            row=0, 
            sticky=tk.W
        )
        name = ttk.Entry(self, width=30)
        name.focus()
        name.grid(column=1, row=0, sticky=tk.W)

        ttk.Label(self, text='Id:').grid(
            column=0,
            row=1, 
            sticky=tk.W
        )
        id = ttk.Entry(self, width=30)
        id.focus()
        id.grid(column=1, row=1, sticky=tk.W)

        ttk.Label(self, text='Phone Number:').grid(
            column=0,
            row=2, 
            sticky=tk.W
        )
        phone_number = ttk.Entry(self, width=30)
        phone_number.focus()
        phone_number.grid(column=1, row=2, sticky=tk.W)
        
        ttk.Label(self, text='Telegram Chat Id:').grid(
            column=0,
            row=3, 
            sticky=tk.W
        )
        telegram_chat_id = ttk.Entry(self, width=30)
        telegram_chat_id.focus()
        telegram_chat_id.grid(column=1, row=3, sticky=tk.W)
        
        show_image_on_capture = tk.IntVar()
        tk.Checkbutton(self, text="Show image on capture", variable=show_image_on_capture, onvalue=True, offvalue=False).grid(column=1, row=4, sticky=tk.W)

        ttk.Button(self, text='Take Picture',command=lambda :self.Register(name.get(), id.get(), telegram_chat_id.get(), phone_number.get(), show_image_on_capture)).grid(column=2, row=0)
        ttk.Button(self, text='Submit',command=lambda : self.Submit()).grid(column=2, row=1)

    def Register(self, name: str, id: str, telegram_chat_id: str, phone_number: str, show_image_on_capture: bool = False):
        self.registration = RegistrationData(name, id, telegram_chat_id, CaptureImage(show_image_on_capture.get()), phone_number)

    def Submit(self):
        if(self.AbleToSubmit()):
            self.destroy()
            return
        print("Unable to submit")
    
    def AbleToSubmit(self):
        return (self.registration is not None) or (self.registration.name is not None) or (self.registration.id is not None) or (self.registration.telegram_chat_id is not None) or (self.registration.image is not None)

    def Start(self) -> RegistrationData:
        self.mainloop()
        return self.registration

def RunRegisterAppAndGetRegistrationData():
    app = App()
    return app.Start()

if __name__ == "__main__":
    app = App()
    registration = app.Start()
    print(registration)