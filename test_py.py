import logging
import os
import sys

# Configuración de logging
log_file = '/var/www/store-scraper/logs/test_py.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)

try:
    logging.debug('Starting script...')
    logging.debug('Current directory: %s', os.getcwd())
    # Aquí va el resto del código de test_py.py
    # Por ejemplo, si el script simplemente imprime algo:
    logging.debug('Executing script content...')
    print("Hello from Python script")
    logging.debug('Script executed successfully.')
except Exception as e:
    logging.error('Error: %s', str(e))
    sys.exit(1)
