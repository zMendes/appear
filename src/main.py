from operator import truediv
import numpy as np
import cv2
from PIL import Image
from IPython.display import display, Javascript
from base64 import b64decode
import imutils
from time import sleep

fps = 30
camera = cv2.VideoCapture(0)

print("[INFO] loading model...")
prototxt = 'deploy.prototxt'
model = 'res10_300x300_ssd_iter_140000.caffemodel'
net = cv2.dnn.readNetFromCaffe(prototxt, model)
while True:
    ret, image = camera.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # resize it to have a maximum width of 400 pixels
    (h, w) = image.shape[:2]
    image = imutils.resize(image, width=500)
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (500, 500)), 1.0, (500, 500), (104.0, 177.0, 123.0))

    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    print(f"{len(detections)} faces detected")
    for i in range(0, detections.shape[2]):
        
        # extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence threshold
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # draw the bounding box of the face along with the associated probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            # cropped = image[startY:endY,startX:endX]
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
            cv2.putText(image, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        # gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', image)
        if cv2.waitKey(1) == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()