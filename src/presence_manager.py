import matplotlib.pyplot as plt
import cv2
import numpy as np
from utils import *
from face_model import FaceModel
from face_finder import FaceFinder
import sqlite3
import math


class PresenceManager:
    def __init__(self):
        self.camera = cv2.VideoCapture(4)

    def run(self):
        ff = FaceFinder()
        fm = FaceMatcher()
        while True:
            ret, image = self.camera.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            faces, h, w = ff.find_faces(image)

            for i in range(0, faces.shape[2]):

                confidence = faces[0, 0, i, 2]

                if confidence > 0.5:
                    box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cropped = image[startY:endY, startX:endX]
                    face_color = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                    name = fm.find_in_db(face_color)
                    text = "{} - {:.2f}%".format(name, confidence * 100)

                    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    cv2.putText(
                        image,
                        text,
                        (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (0, 0, 255),
                        2,
                    )
                cv2.imshow("frame", image)
                if cv2.waitKey(1) == ord("q"):
                    break
        self.camera.release()
        cv2.destroyAllWindows()


class FaceMatcher(FaceModel):
    def __init__(self, epsilon=0.40):
        self.model = self.setupModel()
        self.epsilon = epsilon
        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)
        self.con = sqlite3.connect("data.db", detect_types=sqlite3.PARSE_DECLTYPES)
        faces = self.con.execute("SELECT * FROM FACES")
        self.faces = faces.fetchall()
    def find_in_db(self, img):
        similarity = []
        img_representation = self.model.predict(preprocess((img)))[0, :]
        s_max = math.inf
        name_final = ""
        for (name, representation) in self.faces:
            similarity.append((name,self.match(img_representation, representation[0])))
        for person in similarity:
            if person[1] < s_max:
                name_final = person[0]
                s_max = person[1]
        #if s_max>45:
        #    return "?"
        


        return name_final

    def match(self, img1_representation, img2_representation):

        cosine_similarity = findCosineSimilarity(
            img1_representation, img2_representation
        )
        euclidean_distance = findEuclideanDistance(
            img1_representation, img2_representation
        )
        
        return euclidean_distance * cosine_similarity#< self.epsilon:
            #return True
        #return False
