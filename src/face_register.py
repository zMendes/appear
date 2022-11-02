from face_model import FaceModel
from face_finder import FaceFinder

import sqlite3
import cv2
import numpy as np
from utils import preprocess, adapt_array, convert_array

import sqlite3
import numpy as np
import io


class FaceRegister(FaceModel):
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)
        self.con = sqlite3.connect("data.db", detect_types=sqlite3.PARSE_DECLTYPES)
        self.con.execute(
            f"CREATE TABLE IF NOT EXISTS FACES(name TEXT NOT NULL, img array NOT NULL)"
        )

    def register(self, name):
        vgg_face_descriptor = self.setupModel()
        ff = FaceFinder()
        found_face = False
        while not found_face:
            ret, image = self.camera.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            faces, h, w = ff.find_faces(image)
            if len(faces):
                found_face = True
        for i in range(0, faces.shape[2]):

            confidence = faces[0, 0, i, 2]
            if confidence > 0.5:
                box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = image[startY:endY, startX:endX]
                face_color = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        img_representation = vgg_face_descriptor.predict(preprocess(face_color))
        params = (name, img_representation)
        self.con.execute("INSERT INTO FACES VALUES (?, ?)", params)
        self.con.commit()
