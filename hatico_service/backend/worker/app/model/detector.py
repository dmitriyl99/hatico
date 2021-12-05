from typing import Tuple
import os

from imageai.Detection import ObjectDetection
import pandas as pd
import numpy as np

from app.core.config import settings


class ObjectDetectionModel:
    retina_detector: ObjectDetection
    retina_custom_objects: ObjectDetection.CustomObjects
    yolo_detector: ObjectDetection
    yolo_custom_objects: ObjectDetection.CustomObjects

    def __init__(self):
        # Load RetinaNet model
        self.retina_detector, self.retina_custom_objects = self._configure_retina_detector()

        # Load YOLO model
        self.yolo_detector, self.yolo_custom_objects = self._configure_yolo_detector()

    def _configure_retina_detector(self) -> Tuple[ObjectDetection, ObjectDetection.CustomObjects]:
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join(settings.DATA_DIR, 'resnet50_coco_best_v2.1.0.h5'))
        custom_objects = detector.CustomObjects(person=True, dog=True)
        detector.loadModel()

        return detector, custom_objects

    def _configure_yolo_detector(self) -> Tuple[ObjectDetection, ObjectDetection.CustomObjects]:
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(settings.DATA_DIR, 'yolo.h5'))
        custom_objects = detector.CustomObjects(person=True, dog=True)
        detector.loadModel()

        return detector, custom_objects

    def predict(self, image) -> dict:
        """
        Detect dogs and person on image
        :param image: matplotlib.image instance
        :return: list of predicted dogs
        """
        is_animal_there = 0
        is_it_a_dog = 0
        is_the_owner_there = 0
        is_animal_there_retina = 0
        is_it_a_dog_retina = 0
        is_the_owner_there_retina = 0
        is_animal_there_yolo = 0
        is_it_a_dog_yolo = 0
        is_the_owner_there_yolo = 0

        # Detect with RetinaNet
        _, retina_objects = self.retina_detector.detectObjectsFromImage(
            custom_objects=self.retina_custom_objects,
            input_image=image,
            input_type='array',
            minimum_percentage_probability=5,
            output_type='array'
        )
        if len(retina_objects) > 0:
            retina_objects = pd.DataFrame(retina_objects)
            retina_objects.columns = ['name', 'percentage_prob', 'box_points']
            animal_mask = (retina_objects['name'] == 'dog') & (retina_objects['percentage_prob'] >= 7)
            is_animal_there_retina = 1 if retina_objects[animal_mask].shape[0] > 0 else 0
            mask_dog = (retina_objects["name"] == "dog") & (
                    retina_objects["percentage_prob"] >= 9
            )
            is_it_a_dog_retina = 1 if retina_objects[mask_dog].shape[0] > 0 else 0
            mask_person = (retina_objects["name"] == "person") & (
                    retina_objects["percentage_prob"] >= 52
            )
            is_the_owner_there_retina = (
                1 if retina_objects[mask_person].shape[0] > 0 else 0
            )
            objs_retina = retina_objects[mask_dog]
            objs_retina["source"] = "retina"

        # Detect with YOLOv3
        _, yolo_objects = self.yolo_detector.detectObjectsFromImage(
            custom_objects=self.yolo_custom_objects,
            input_image=image,
            input_type='array',
            minimum_percentage_probability=5,
            output_type='array'
        )
        if len(yolo_objects) > 0:
            yolo_objects = pd.DataFrame(yolo_objects)
            yolo_objects.columns = [
                'name', 'perc_prob', 'box_points'
            ]
            mask_animal = ((yolo_objects["name"] == "dog") & (yolo_objects["perc_prob"] >= 5))
            is_animal_there_yolo = 1 if yolo_objects[mask_animal].shape[0] > 0 else 0
            mask_dog = ((yolo_objects['name'] == 'dog') & yolo_objects['perc_prob'] >= 5)
            is_it_a_dog_yolo = 1 if yolo_objects[mask_dog].shape[0] > 0 else 0
            mask_person     = (yolo_objects["name"] == "person") & (
                    yolo_objects["perc_prob"] >= 60
            )
            is_the_owner_there_yolo = 1 if yolo_objects[mask_person].shape[0] > 0 else 0
            yolo_objects = yolo_objects[mask_dog]
            yolo_objects['source'] = 'yolo'

        objects_df = pd.DataFrame()
        # concatenate yolo and retina objects
        if len(retina_objects) > 0 and len(yolo_objects) > 0:
            objects_df = pd.concat([retina_objects, yolo_objects])
        else:
            if len(retina_objects) > 0:
                objects_df = retina_objects
            elif len(yolo_objects) > 0:
                objects_df = yolo_objects

        # is_animal_there, is_it_a_dog, is_the_owner_there aggregate
        is_animal_there = np.max([is_animal_there_retina, is_animal_there_yolo])
        if is_animal_there > 0:
            is_it_a_dog = np.max([is_it_a_dog_retina, is_it_a_dog_yolo])
            if is_it_a_dog > 0:
                is_the_owner_there = np.max(
                    [is_the_owner_there_retina, is_the_owner_there_yolo]
                )

        predicted_objects = []
        if len(objects_df) > 0 and is_it_a_dog:
            # crop images
            for box in objects_df['box_points']:
                cropped_image = image[
                    box[1] : (box[1] + box[3]), box[0] : (box[0] + box[2])
                ]
                predicted_objects.append(cropped_image)

        return {
            'objects': predicted_objects,
            "is_animal_there": is_animal_there,
            "is_it_a_dog": is_it_a_dog,
            "is_the_owner_there": is_the_owner_there,
        }
