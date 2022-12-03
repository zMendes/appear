'''
The ideia of this program is consume the images in the folder "image_bus" and match it with the database
'''

import csv
import datetime
import glob
import os
from time import sleep
import cv2
from presence_manager import FaceMatcher
from public_env import SERVICE_BUS_BATCH_SIZE, IDENTIFICATION_MAXIMUM_TIMES, DELTATIME_BETWEEN_IDENTIFICATIONS
from presence import Presence
from telegram_handler import TelegramHandler
import uuid
import sqlite3

class Identification():
    def __init__(self, code, name, timestamp):
        self.code = code
        self.name = name
        self.last_appearence = timestamp
        self.times = 0


class ImageBusConsumer:
    def __init__(self):
        #generate uuid
        self.classID = str(uuid.uuid4())
        self.fm = FaceMatcher()
        self.telegram = TelegramHandler()
        self.search_dir = "src/image_bus/"
        self.identifications = {}
        self.con = sqlite3.connect("data.db", detect_types=sqlite3.PARSE_DECLTYPES)
        self.con.execute(
            f"CREATE TABLE IF NOT EXISTS LISTS(classID STRING NOT NULL, name TEXT NOT NULL, code TEXT NOT NULL, timestamp TIMESTAMP NOT NULL, PRIMARY KEY(classID, code, timestamp))"
        )
        self.con.execute("")


    def run(self):
        files = list(filter(os.path.isfile, glob.glob(self.search_dir + "*.png")))
        while len(files) <= 0:
            print("Waiting for images")
            sleep(1)
            files = list(filter(os.path.isfile, glob.glob(self.search_dir + "*.png")))
        presence_list = []
        files.sort(key=lambda x: os.path.getmtime(x))
        print("Time: ",datetime.datetime.fromtimestamp(os.path.getmtime(files[0])))
        for i in range(min(len(files), SERVICE_BUS_BATCH_SIZE)):
            db_res = self.fm.find_in_db(cv2.imread(files[i]))
            if db_res != None:
                name,code,phone_number, chat_id = db_res
                if code in self.identifications:
                    if (datetime.datetime.fromtimestamp(os.path.getmtime(files[i])) - self.identifications[code].last_appearence) > datetime.timedelta(seconds=DELTATIME_BETWEEN_IDENTIFICATIONS):
                        self.identifications[code].times = 1
                        self.identifications[code].last_appearence = datetime.datetime.fromtimestamp(os.path.getmtime(files[i]))
                        if self.identifications[code].times >= IDENTIFICATION_MAXIMUM_TIMES:
                            presence_list.append(Presence(code, name, phone_number, datetime.datetime.fromtimestamp(os.path.getmtime(files[i]))))
                            self.identifications[code].times = 0
                            self.telegram.send_message(f"Olá {name}, você foi identificado!",chat_id=chat_id)

                    self.identifications[code].times += 1
                    self.identifications[code].last_appearence = datetime.datetime.fromtimestamp(os.path.getmtime(files[i]))

                    if self.identifications[code].times == IDENTIFICATION_MAXIMUM_TIMES:
                        presence_list.append(Presence(code, name, phone_number, datetime.datetime.fromtimestamp(os.path.getmtime(files[i]))))
                        self.telegram.send_message(f"Olá {name}, você está presente!",chat_id=chat_id)

                else:
                    self.identifications[code] = Identification(code, name, datetime.datetime.fromtimestamp(os.path.getmtime(files[i])))
            else:
                print("Person not in database")
            os.remove(files[i])
            
        for person in presence_list:
            params = (
                self.classID,
                person.name,
                person.code,
                person.timestamp
            )
            self.con.execute("INSERT INTO LISTS VALUES (?, ?, ?, ?)", params)
        self.con.commit()


        self.run()

if __name__ == "__main__":
    ImageBusConsumer().run()