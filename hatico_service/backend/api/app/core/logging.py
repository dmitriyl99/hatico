import os
import logging

from loguru import logger

LOGS_DIRECTORY = 'storage/logs'


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def configure():
    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)

    logger.add(
        LOGS_DIRECTORY + '/logs-{time:YYYY-MM-DD}.log',
        level='INFO',
        format='{time:YYYY-MM-DD HH:mm:ss} - {level}: {message}',
        rotation='00:00'
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
