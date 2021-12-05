from .detector import ObjectDetectionModel
from .color import ColorDetectionModel
from .breed import BreedDetectionModel

import io

import matplotlib.image as mpimg


class Model:
    def predict(self, image):
        color = None
        breed = None
        tail = None

        data, ext = image['data'], image['ext']
        with io.BytesIO(data) as file:
            image = mpimg.imread(file, format=ext)

        detection_result = ObjectDetectionModel().predict(image)
        objects = detection_result['objects']
        if len(objects) > 0:
            color = ColorDetectionModel().predict(objects)
            breed, tail = BreedDetectionModel().predict(objects)

        return {
            'is_animal_there': detection_result['is_animal_there'],
            'is_it_a_dog': detection_result['is_it_a_dog'],
            'is_the_owner_there': detection_result['is_the_owner_there'],
            'color': color,
            'breed': breed,
            'tail': 1 if tail == "short" else 2
        }
