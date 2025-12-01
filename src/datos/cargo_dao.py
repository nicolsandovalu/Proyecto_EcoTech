from .db_connector import DatabaseConnector #Importa la clase Cargo
import oracledb

class CargoDAO:
    def __init__(self):
        self.db = DatabaseConnector()
     
    #recuperar todos los cargos de la base de datos   
    def get_all_cargos(self) -> list :
        conn = self.db.connect()
        if not conn: 
            return []
        
        cursor = None #se inicializa el cursor fuera del try
        
        try:
            cursor = conn.cursor()
            sql = "SELECT ID_CARGO, NOMBRE FROM CARGO"
            cursor.execute(sql)
            results = cursor.fetchall()
            
            #mapear los resultados a objetos Cargo de la Capa Dominio / en lista de tuplas
            cargos_list = []
            for row in results:
                cargos_list.append({'id_cargo': row[0], 'nombre': row[1]}) #(Cargo(row[0], row[1])) por ahora solo retornamos la tupla
                
            return cargos_list
        
        #manejo de excepciones: captura errores de Oracle o ejecución
        except oracledb.Error as e:
            error, = e.args
            print(f"Error ORA-{error.code} al listar cargos: {error.message}")
            return []
        
        except Exception as e:
            #captura errores genéricos como por ej. problemas de mapeo
            print(f"Error inesperado al listar cargos: {e}")
            return []
        
        finally:
            #asegura cerrar el cursor para liberar recursor. Finally se ejecuta siempre.
            if cursor:
                cursor.close()
            