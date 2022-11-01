import matplotlib.pyplot as plt
import cv2
from keras.models import Model, Sequential
from keras.layers import  Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
import numpy as np
from utils import *

class FaceFinder():
    def __init__(self):
        self.prototxt = 'deploy.prototxt'
        self.model =  'res10_300x300_ssd_iter_140000.caffemodel'
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
    
    def find_faces(self, image):
        (h, w) = image.shape[:2]
        self.net.setInput(cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)))
        return self.net.forward(), h, w

class FaceRegister():
    def __init__(self):
        pass
    def register(self):
        pass

class PresenceListManager():
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
    def run(self):
        ff = FaceFinder()
        while True:
            ret, image = self.camera.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Find faces
            faces, h, w = ff.find_faces(image)

            print(f"{len(faces)} faces detected")
            for i in range(0, faces.shape[2]):
                
                # extract the confidence (i.e., probability) associated with the prediction
                confidence = faces[0, 0, i, 2]

                # filter out weak faces by ensuring the `confidence` is
                # greater than the minimum confidence threshold
                if confidence > 0.5:
                    # compute the (x, y)-coordinates of the bounding box for the object
                    box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
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
        self.camera.release()
        cv2.destroyAllWindows()

class FaceMatcher():
    def __init__(self, epsilon=0.40):
        self.model = self.setupModel()
        self.epsilon = epsilon

    def match(self, img1, img2):
        vgg_face_descriptor = Model(inputs=self.model.layers[0].input, outputs=self.model.layers[-2].output)
        img1_representation = vgg_face_descriptor.predict(preprocess_image((img1)))[0,:]
        img2_representation = vgg_face_descriptor.predict(preprocess_image((img2)))[0,:]
        
        print(img1_representation)
        
        
        cosine_similarity = findCosineSimilarity(img1_representation, img2_representation)
        euclidean_distance = findEuclideanDistance(img1_representation, img2_representation)
        
        print("Cosine similarity: ",cosine_similarity)
        print("Euclidean distance: ",euclidean_distance)
        
        if(cosine_similarity < self.epsilon):
            print("verified... they are same person")
        else:
            print("unverified! they are not same person!")
        
        f = plt.figure()
        f.add_subplot(1,2, 1)
        plt.imshow(img1)
        plt.xticks([]); plt.yticks([])
        f.add_subplot(1,2, 2)
        plt.imshow(img2)
        plt.xticks([]); plt.yticks([])
        plt.show(block=True)
        print("-----------------------------------------")

    def setupModel(self):
        def loadWights(model):
            model.load_weights('vgg_face_weights.h5')
            return model
        def buildModel():
            model = Sequential()
            model.add(ZeroPadding2D((1,1),input_shape=(224,224, 3)))
            model.add(Convolution2D(64, (3, 3), activation='relu'))
            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(64, (3, 3), activation='relu'))
            model.add(MaxPooling2D((2,2), strides=(2,2)))

            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(128, (3, 3), activation='relu'))
            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(128, (3, 3), activation='relu'))
            model.add(MaxPooling2D((2,2), strides=(2,2)))

            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(256, (3, 3), activation='relu'))
            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(256, (3, 3), activation='relu'))
            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(256, (3, 3), activation='relu'))
            model.add(MaxPooling2D((2,2), strides=(2,2)))

            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(512, (3, 3), activation='relu'))
            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(512, (3, 3), activation='relu'))
            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(512, (3, 3), activation='relu'))
            model.add(MaxPooling2D((2,2), strides=(2,2)))

            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(512, (3, 3), activation='relu'))
            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(512, (3, 3), activation='relu'))
            model.add(ZeroPadding2D((1,1)))
            model.add(Convolution2D(512, (3, 3), activation='relu'))
            model.add(MaxPooling2D((2,2), strides=(2,2)))

            model.add(Convolution2D(4096, (7, 7), activation='relu'))
            model.add(Dropout(0.5))
            model.add(Convolution2D(4096, (1, 1), activation='relu'))
            model.add(Dropout(0.5))
            model.add(Convolution2D(2622, (1, 1)))
            model.add(Flatten())
            model.add(Activation('softmax'))
            return model
        return loadWights(buildModel())