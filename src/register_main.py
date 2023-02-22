import os
from registration_gui import RunRegisterAppAndGetRegistrationData
from dtos import RegistrationData
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from face_register import FaceRegister


if __name__ == "__main__":
    registrationData : RegistrationData = RunRegisterAppAndGetRegistrationData()
    fr = FaceRegister()
    fr.register(registrationData)
