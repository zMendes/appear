import os
from registration_gui import RunRegisterAppAndGetRegistrationData
from dtos import RegistrationData
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from face_register import FaceRegister


if __name__ == "__main__":
    # name = input("Name: ")
    # code = input("Code: ")
    # phone_number = input("Phone number: ")
    # chat_id = input("chatID: ")
    registrationData : RegistrationData = RunRegisterAppAndGetRegistrationData()
    fr = FaceRegister()
    fr.register(registrationData)
