from time import sleep
from face_model import FaceModel
from face_finder import FaceFinder

import sqlite3
import cv2
import numpy as np
from dtos import RegistrationData
from utils import preprocess, adapt_array, convert_array

import numpy as np

class FaceRegister(FaceModel):
    def __init__(self):
        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)
        self.con : sqlite3.Connection = sqlite3.connect("data.db", detect_types=sqlite3.PARSE_DECLTYPES)
        self.con.execute(
            f"CREATE TABLE IF NOT EXISTS FACES(name TEXT NOT NULL, code TEXT NOT NULL, phone_number TEXT, chatID TEXT NOT NULL, img array NOT NULL)"
        )

    def register(self, registrationData : RegistrationData) -> bool:
        vgg_face_descriptor = self.setupModel()
        ff = FaceFinder()
        found_face = False
        faces, h, w = ff.find_faces(registrationData.image)
        if len(faces):
            found_face = True
        if not found_face:
            return False
        for i in range(0, faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence > 0.5:
                box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = registrationData.image[startY:endY, startX:endX]
                face_color = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        img_representation = vgg_face_descriptor.predict(preprocess(face_color))
        params = (registrationData.name, registrationData.id, registrationData.phone_number, registrationData.image, img_representation)
        self.con.execute("INSERT INTO FACES VALUES (?, ?, ?, ?, ?)", params)
        self.con.commit()
        return True

def Countdown(timer: int) -> None:
    for i in range(timer, 0, -1):
        print(f"{i}...")
        sleep(1)
    print("Cheese!")