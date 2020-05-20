import sys
import logging
import os
sys.path.append(r'D:\Users\Chris\Documents\Python')

module_path = os.path.dirname(__file__)

def setup_logger(name='default', loglevel=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)

    # Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)

    # Formatter
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # add handler
    logger.addHandler(console_handler)
    return logger

    # logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
    # End logging.