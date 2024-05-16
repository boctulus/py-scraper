import os

class Files:
    @staticmethod
    def empty_directory(directory):
        # Verificar si el directorio existe
        if not os.path.exists(directory):
            print(f"El directorio '{directory}' no existe.")
            return

        # Obtener la lista de archivos en el directorio
        files = os.listdir(directory)

        # Eliminar cada archivo en el directorio
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Archivo '{file}' eliminado.")

        print(f"Se han eliminado todos los archivos de '{directory}'.")
