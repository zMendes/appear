import matplotlib.pyplot as plt
import cv2
from keras.models import Model, Sequential
from keras.layers import (
    Convolution2D,
    ZeroPadding2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout,
    Activation,
)
import numpy as np
import sqlite3


class FaceFinder:
    def __init__(self):
        self.prototxt = "model/deploy.prototxt"
        self.model = "model/res10_300x300_ssd_iter_140000.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

    def find_faces(self, image):
        (h, w) = image.shape[:2]
        self.net.setInput(
            cv2.dnn.blobFromImage(
                cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
            )
        )
        return self.net.forward(), h, w
