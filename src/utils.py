import numpy as np

def findCosineSimilarity(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

def findEuclideanDistance(source_representation, test_representation):
    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance

def preporcess(image):
    from keras.utils import img_to_array
    from PIL import Image
    from keras.applications.imagenet_utils import preprocess_input
    if image.shape[0] != 224:
        img = img_to_array(Image.fromarray(image).resize((224,224)))
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img