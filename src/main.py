import sys
from src.datos.db_connector import DatabaseConnector
from src.UI.loginScreen import LoginScreen 

def main():
    print("Iniciando Sistema de gestión de empleado")
    
    db_manager = DatabaseConnector()
    db_conn = db_manager.connect()
    
    if db_conn is None:
        print("Crítico: No se pudo establecer la conexión a la base de datos Oracle. Cerrando aplicación")
        sys.exit(1)
        
    try:
        app = LoginScreen(db_manager)
        app.run()
    
    except Exception as e:
        print(f"Error inesperado al ejecutar la aplicación: {e}")
    
    finally:
        db_manager.disconnect()
        print("Aplicación finalizada y conexión a DB cerrada.")

if __name__ == "__main__":
    main()

