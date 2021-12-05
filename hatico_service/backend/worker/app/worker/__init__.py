from app.core.config import settings
from app.worker.processor import ImageProcessor

from pymongo import MongoClient


class ImageProcessorWorker:
    """
    Worker that process images in database
    """
    def run(self):
        """
        Run worker
        :return: void
        """
        database = MongoClient(host=settings.MONGO_DB_HOST)[settings.MONGO_DB_NAME]

        processor = ImageProcessor(database=database)
        processor.process_once()
        processor.watch_and_process_images()
