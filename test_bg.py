import os
import time
from datetime import datetime

def log_current_directory_and_time():
    # Obtén el directorio actual
    current_directory = os.getcwd()
    
    # Abre el archivo en modo append
    with open('D:\python\selenium\store-scraper\my-log.txt', 'a') as log_file:
        while True:
            # Obtén la fecha y hora actual
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Formatea el mensaje
            message = f"Directory: {current_directory} | Time: {current_time}"
            
            # Imprime en pantalla
            print(message)
            
            # Escribe en el archivo
            log_file.write(message + '\n')
            
            # Espera un segundo antes de la próxima iteración
            time.sleep(1)

if __name__ == "__main__":
    log_current_directory_and_time()
