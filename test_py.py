import logging
import os
import sys
import time

# Configuración de logging
log_file = './logs/test_py.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)

current_directory = os.getcwd()
logging.debug(current_directory)

try:
    logging.debug('Starting script...')
    logging.debug('Current directory: %s', os.getcwd())

    for i in range(4):
        logging.debug(f'Executing script content... #{i}')
        print(f"Hello from Python script #{i}")
        time.sleep(1)
    
    logging.debug('Script executed successfully.')

except Exception as e:
    logging.error('Error: %s', str(e))
    sys.exit(1)
