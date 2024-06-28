import mysql.connector
import os
from mysql.connector import Error
from datetime import datetime
from dotenv import load_dotenv

class RobotExecution:
    """
    # Ejemplo de uso

    robot_execution = RobotExecution()

    robot_execution.createRecord(
        order_file='orden1234.txt',
        robot_status='completed',
        last_screenshot='screenshot123.png',
        error_msg='Ningunoooo'
    )
    """

    def __init__(self):
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()

        # Obtener los valores de las variables de entorno
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_name = os.getenv('DB_NAME')
        self.db_username = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')

    def createRecord(self, order_file: str, robot_status: str, last_screenshot: str = None, error_msg: str = None):
        try:
            # Establecer la conexión a la base de datos
            connection = mysql.connector.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_username,
                password=self.db_password
            )
            
            if connection.is_connected():
                cursor = connection.cursor()

                # Obtener la fecha y hora actual
                execution_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Crear la consulta SQL para reemplazar el registro
                sql_query = """
                REPLACE INTO robot_execution (execution_datetime, order_file, robot_status, last_screenshot, error_msg)
                VALUES (%s, %s, %s, %s, %s)
                """

                # Ejecutar la consulta
                cursor.execute(sql_query, (execution_datetime, order_file, robot_status, last_screenshot, error_msg))

                # Confirmar los cambios en la base de datos
                connection.commit()

                print("Registro creado o reemplazado exitosamente.")

        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Conexión a la base de datos cerrada.")

