import cv2
import json

class FaceFinder:
    def __init__(self):
        with open("src/config.json") as f:
            config = json.load(f)["model"]
        self.prototxt : str = config["path_prototxt"]
        self.model : str = config["path_model"]
        self.net : cv2.dnn.Net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

    def find_faces(self, image) -> tuple[cv2.Mat, int, int]:
        (h, w) = image.shape[:2]
        self.net.setInput(
            cv2.dnn.blobFromImage(
                cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
            )
        )
        return self.net.forward(), h, w
