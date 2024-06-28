import os

class Files:
    @staticmethod
    def emptyDirectory(directory):
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

    
    @staticmethod
    def urlToFilename(url: str) -> str:
        # Eliminar http:// o https:// del comienzo
        if url.startswith("http://"):
            url = url[7:]
        elif url.startswith("https://"):
            url = url[8:]

        if url.startswith("www."):
            url = url[4:]
        
        # Eliminar .html o .htm del final
        if url.endswith(".html"):
            url = url[:-5]
        elif url.endswith(".htm"):
            url = url[:-4]
        
        # Reemplazar "/" con "-"
        url = url.replace("/", "-")
        
        # Reemplazar "." con "-"
        url = url.replace(".", "-")
        
        # Reemplazar "?" con "-"
        url = url.replace("?", "-")
        
        # Reemplazar "%" con "-"
        url = url.replace("%", "-")
        
        return url
