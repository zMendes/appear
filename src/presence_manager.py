from genericpath import exists
import json
import os
import cv2
from utils import *
from face_model import FaceModel
from face_finder import FaceFinder
import sqlite3
import math
import csv
import time

class PresenceManager:
    def __init__(self):
        with open("src/config.json") as f:
            config = json.load(f)
        self.camera = cv2.VideoCapture(config["camera_index"])
        self.image_bus_path = "src/image_bus/"
        if exists(self.image_bus_path) == False:
            os.mkdir(self.image_bus_path)


    def run(self, file_path):
        ff = FaceFinder()
        presence_list = []
        last = 0
        while True:
            ret, image = self.camera.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            faces, h, w = ff.find_faces(image)

            for i in range(0, faces.shape[2]):

                confidence = faces[0, 0, i, 2]

                if confidence > 0.5 and time.time() - last >0.5:
                    box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cropped = image[startY:endY, startX:endX]
                    face_color = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(f"{self.image_bus_path}{time.time()}.png", face_color)
                    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    last = time.time()


            cv2.imshow("frame", image)
            if cv2.waitKey(1) == ord("q"):
                break
        self.camera.release()
        cv2.destroyAllWindows()
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["code", "name", "phone_number", "timestamp"])
            for person in presence_list:
                writer.writerow([person.code, person.name, person.phone_number, person.timestamp])



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
        for (name, code, p, chat, representation) in self.faces:
            similarity.append((name, code, p, chat,self.match(img_representation, representation[0])))
        for person in similarity:
            if person[-1] < s_max:
                final = person[:-1]
                s_max = person[-1]

        print(s_max)
        if s_max>25:
            return None
        return final

    def match(self, img1_representation, img2_representation):

        cosine_similarity = findCosineSimilarity(
            img1_representation, img2_representation
        )
        euclidean_distance = findEuclideanDistance(
            img1_representation, img2_representation
        )
        
        return euclidean_distance * cosine_similarity
