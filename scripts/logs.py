import logging
import os
from datetime import datetime

def setup_logger():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        filename = f'logs/email_errors_{datetime.now().strftime("%Y%m%d")}.log',
        level = logging.ERROR,
        format = '%(asctime)s - %(message)s',
        datefmt = '%d/%m/%Y %H:%M:%S'
    )
    return logging.getLogger(__name__)

def log_error(message: str):
    logger = logging.getLogger(__name__)
    logger.error(message)
