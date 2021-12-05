from loguru import logger

import os

from app.worker import ImageProcessorWorker

LOGS_DIRECTORY = 'storage/logs'

if not os.path.exists(LOGS_DIRECTORY):
    os.makedirs(LOGS_DIRECTORY)

logger.add(
    LOGS_DIRECTORY + '/logs-{time:YYYY-MM-DD}.log',
    level='INFO',
    format='{time:YYYY-MM-DD HH:mm:ss} - {level}: {message}',
    rotation='00:00'
)

worker = ImageProcessorWorker()
worker.run()
