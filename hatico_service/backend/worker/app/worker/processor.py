from pymongo.database import Database
from loguru import logger

from app.core.utils import Timer
from app.model import Model

import traceback


class ImageProcessor:
    """
    Service that process image with ML models and find attributes
    """
    _database: Database
    _attributes: list
    model: Model

    def __init__(self, database: Database):
        self._database = database
        self._attributes = [a for a in self._database.attributes.find({}, {'_id': False})]

    def process_once(self):
        """
        Process all current pending images
        :return: void
        """
        logger.info('Process all current pending images')
        images = self._database.images.find({'status': 'PENDING'})
        for image in images:
            self._process_image(image['_id'])

    def watch_and_process_images(self):
        """
        Watch for new images and process every inserted image
        :return: idle
        """
        logger.info('Start watching for new images...')
        pipeline = [{'$match': {'operationType': 'insert'}}]
        with self._database.images.watch(pipeline) as stream:
            for change in stream:
                image_id = change['fullDocument']['_id']
                self._process_image(image_id)

    def _process_image(self, image_id):
        image = self._database.images.find_one_and_update(
            {'_id': image_id, 'status': 'PENDING'}, {'$set': {'status': 'PROCESSING'}}
        )
        if not image:
            return
        logger.info(f'Processing image with id {image_id}')
        timer = Timer()
        timer.start()
        try:
            result = Model().predict(image)
        except Exception as e:
            result = None
            logger.error(f'Error while processing image with id {image_id}: {e}. Traceback: {traceback.format_tb(e.__traceback__)}')
        timer.finish()
        elapsed_time = timer.elapsed
        if result:
            attribute_values = {
                a['name']: a['values'][result[a['name']]]['raw'] if 'values' in a and result[a['name']] is not None else result[a['name']]
                for a in self._attributes
            }
            camera = self._get_random_camera()  # Only for presentation
            address = {
                'cam_id': camera['ID'],
                'address': camera['Address'],
                'district': camera['District'],
                'geoData': camera['geoData']
            }
            attribute_values['address'] = address

            query = {'_id': image_id}
            statement = {'$set': {'status': 'PROCESSED', 'attribute_values': attribute_values, 'elapsed_time': elapsed_time}}
            self._database.images.update_one(
                query, statement
            )
            logger.info(f'Image with id {image_id} - success')
        else:
            query = {'_id': image_id}
            statement = {'$set': {'status': 'FAILED', 'elapsed_time': elapsed_time}}
            self._database.images.update_one(
                query, statement
            )

    def _get_random_camera(self):
        # Only for presentation
        items = [item for item in self._database.cameras.aggregate([{'$sample': {'size': 1}}])]
        return items[0]
