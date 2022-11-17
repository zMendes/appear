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


class FaceModel:
    def setupModel(self):
        def loadWights(model):
            model.load_weights("src/model/vgg_face_weights.h5")
            return model

        def buildModel():
            model = Sequential()
            model.add(ZeroPadding2D((1, 1), input_shape=(224, 224, 3)))
            model.add(Convolution2D(64, (3, 3), activation="relu"))
            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(64, (3, 3), activation="relu"))
            model.add(MaxPooling2D((2, 2), strides=(2, 2)))

            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(128, (3, 3), activation="relu"))
            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(128, (3, 3), activation="relu"))
            model.add(MaxPooling2D((2, 2), strides=(2, 2)))

            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(256, (3, 3), activation="relu"))
            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(256, (3, 3), activation="relu"))
            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(256, (3, 3), activation="relu"))
            model.add(MaxPooling2D((2, 2), strides=(2, 2)))

            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(512, (3, 3), activation="relu"))
            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(512, (3, 3), activation="relu"))
            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(512, (3, 3), activation="relu"))
            model.add(MaxPooling2D((2, 2), strides=(2, 2)))

            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(512, (3, 3), activation="relu"))
            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(512, (3, 3), activation="relu"))
            model.add(ZeroPadding2D((1, 1)))
            model.add(Convolution2D(512, (3, 3), activation="relu"))
            model.add(MaxPooling2D((2, 2), strides=(2, 2)))

            model.add(Convolution2D(4096, (7, 7), activation="relu"))
            model.add(Dropout(0.5))
            model.add(Convolution2D(4096, (1, 1), activation="relu"))
            model.add(Dropout(0.5))
            model.add(Convolution2D(2622, (1, 1)))
            model.add(Flatten())
            model.add(Activation("softmax"))
            return model

        model = loadWights(buildModel())
        return Model(inputs=model.layers[0].input, outputs=model.layers[-2].output)
