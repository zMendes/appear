import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from face_register import FaceRegister
from presence_manager import PresenceManager


if __name__ == "__main__":
    print("Please choose the desired mode:")
    print("1. Presence Manager")
    print("2. Face Register")
    mode = int(input(""))
    if mode == 1:
        fc = PresenceManager()
        fc.run()
    elif mode == 2:
        name = input("Name: ")
        fr = FaceRegister()
        fr.register(name)
    else:
        print("Mode not recognized, please try again.")
