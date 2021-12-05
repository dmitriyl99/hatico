import gc
from collections import Counter
import os
from typing import List

import pandas as pd
import numpy as np
import cv2
import tensorflow as tf


import keras
from keras.models import Model
from keras.layers import GlobalAveragePooling2D, Lambda, Input
from keras.applications.inception_v3 import InceptionV3, preprocess_input as inception_preprocessor
from keras.applications.xception import Xception, preprocess_input as xception_preprocessor
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input as inc_resnet_preprocessor

from app.core.config import settings


class BreedDetectionModel:
    image_size: int = 331
    models: list = []
    breed_names: List[str]
    breed_tails: pd.DataFrame
    models_classes: list = [InceptionV3, InceptionResNetV2, Xception]
    preprocessors: list = [inception_preprocessor, xception_preprocessor, inc_resnet_preprocessor]

    def __init__(self):
        # load trained models
        for i in range(0, 3):
            model_filename = os.path.join(settings.DATA_DIR, f'models/model_{i}.h5')
            self.models.append(keras.models.load_model(model_filename))

        # Load breed names
        df = pd.read_csv(os.path.join(settings.DATA_DIR, 'datasets/breeds_labels.csv'))
        self.breed_names = sorted(df['breed'].unique())

        # Load breed tails
        df = pd.read_csv(os.path.join(settings.DATA_DIR, 'datasets/breeds_tails.csv'))
        self.breed_tails = df.set_index('breed')

    def _concat_features(self, feature_function, models, preprocessors, data) -> list:
        features_list = []

        for i in range(len(models)):
            features_list.append(feature_function(models[i], preprocessors[i], data))
        features_list = np.concatenate(features_list, axis=-1)
        del data
        gc.collect()

        return features_list

    def _get_features(self, model_class, preprocessor, data):
        dataset = tf.data.Dataset.from_tensor_slices(data)

        ds = dataset.batch(64)

        input_size = data.shape[1:]
        input_layer = Input(input_size)
        preprocessor = Lambda(preprocessor)(input_layer)

        model = model_class(
            weights='imagenet', include_top=False, input_shape=input_size
        )(preprocessor)

        avg = GlobalAveragePooling2D()(model)
        feature_extractor = Model(inputs=input_layer, outputs=avg)
        feature_maps = feature_extractor.predict(ds, verbose=False)
        return feature_maps

    def _most_frequent(self, ls):
        # most frequent element of code
        occurrences_count = Counter(ls)
        return occurrences_count.most_common(1)[0][0]

    def predict(self, objects) -> tuple:
        data = []
        i = 0
        for image in objects:
            original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            resized_image = cv2.resize(original_image, (self.image_size, self.image_size))
            data.append(resized_image)
            i += 1

        data_array = np.array(data)
        del data
        gc.collect()

        # Extract features
        features = self._concat_features(self._get_features, self.models_classes, self.preprocessors, data_array)
        del data_array
        gc.collect()

        predictions = self.models[0].predict(features, batch_size=128) / 3
        for model in self.models[1:]:
            predictions += model.predict(features, batch_size=128) / 3

        tmp = np.argmax(predictions, axis=1)
        tmp = pd.DataFrame(tmp, columns=['predicted_class'])
        tmp['predicted_class_name'] = tmp['predicted_class'].apply(
            lambda x: self.breed_names[x]
        )
        breed = self._most_frequent(tmp['predicted_class_name'])
        return breed, self.breed_tails.loc[breed, 'tail']
