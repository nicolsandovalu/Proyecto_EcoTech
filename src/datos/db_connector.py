import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnector:
    
    def __init__(self):
        self.user = os.getenv("DB_USER", "usuario_por_defecto")
        self.password = os.getenv("DB_PASS", "contasena_por_defecto")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "1521")
        self.service_name = os.getenv("DB_SERVICE", "XEPDB1")
        self._connection = None 
        self._dsn = f"{self.host}:{self.port}/{self.service_name}"
    
    def connect(self):
        if self._connection:
            return self._connection
        
        try:
            self._connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self._dsn)
            print("Conexión a Oracle establecida con éxito.")
            return self._connection
        
        except oracledb.Error as e:
            error, = e.args
            print(f"Error de conexión a Oracle ({error.code}): {error.message}")
            self._connection = None 
            return None
    
    def disconnect(self):
        if self._connection:
            try:
                self._connection.close()
                print("Conexión a Oracle cerrada.")
            except oracledb.Error as e:
                print(f"Error al cerrar la conexión: {e}")
            self._connection = None
    
    # Devuelve el objeto de conexión para ser usado por los DAOs.
    def get_connection(self):
        return self._connection