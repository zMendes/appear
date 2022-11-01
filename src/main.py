from operator import truediv
import sys
import numpy as np
import cv2
from PIL import Image
from time import sleep
from PresenceManager import PresenceManager
from FaceRegister import FaceRegister
if 'register' in sys.argv:
    fr = FaceRegister()
    fr.register()
else:
    fc = PresenceManager()
    fc.run()