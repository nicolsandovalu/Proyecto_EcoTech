import oracledb
from ..dominio.proyecto import Proyecto
from .db_connector import DatabaseConnector
from datetime import date 

class ProyectoDAO:
    
    def __init__(self, connection):
        self.db = DatabaseConnector()
    
    def create_proyecto(self, proyecto_obj: Proyecto) -> bool:
        """Inserta nuevo proyecto en BD (Operación CREATE)."""
        conn = self.db.connect()
        if not conn: return False
        
        cursor = conn.cursor()
        data = proyecto_obj.to_dict() # Obtenemos el diccionario con los datos del objeto
        
        try:
            # La sentencia SQL usa la secuencia y parámetros vinculados por nombre
            sql = """
                INSERT INTO PROYECTO (ID_PROYECTO, NOMBRE, DESCRIPCION, FECHA_INICIO, FECHA_CREACION)
                VALUES (seq_proyecto.NEXTVAL, :nombre, :descripcion, TO_DATE(:fecha_inicio, 'YYYY-MM-DD'), SYSDATE)
            """
            cursor.execute(sql, data)
            conn.commit() # Confirma la transacción
            return True
        except oracledb.Error as e:
            conn.rollback() # Deshace la transacción en caso de error
            print(f"Error ORA-{e.args[0].code} al crear proyecto: {e.args[0].message}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    # --- MÉTODO: READ (LISTAR TODOS) ---
    def get_all_proyectos(self) -> list:
        """Obtiene todos los proyectos y los retorna como una lista de objetos Proyecto."""
        conn = self.db.connect()
        if not conn: return []
        
        cursor = conn.cursor()
        proyectos_list = []
        
        try:
            sql = "SELECT ID_PROYECTO, NOMBRE, DESCRIPCION, FECHA_INICIO, FECHA_CREACION FROM PROYECTO ORDER BY FECHA_CREACION DESC"
            cursor.execute(sql)
            
            for fila in cursor.fetchall():
                # Mapeo de fila a objeto Proyecto (POO)
                proyectos_list.append(Proyecto(
                    id_proyecto=fila[0],
                    nombre=fila[1],
                    descripcion=fila[2],
                    fecha_inicio=fila[3], # oracledb mapea a date
                    fecha_creacion=fila[4]
                ))
            return proyectos_list
        except oracledb.Error as e:
            print(f"Error ORA-{e.args[0].code} al obtener proyectos: {e.args[0].message}")
            return []
        finally:
            cursor.close()
            conn.close()
            
    # --- MÉTODOS: ASIGNACIÓN N:M (DELEGADO) ---
    
    def assign_empleado(self, id_proyecto: int, id_empleado: str) -> bool:
        """Asigna empleado a proyecto (Implementa la lógica N:M)."""
        conn = self.db.connect()
        if not conn: return False

        cursor = conn.cursor()
        
        try:
            # Utiliza la tabla intermedia EMPLEADO_PROYECTO
            cursor.execute("INSERT INTO EMPLEADO_PROYECTO (ID_EMPLEADO, ID_PROYECTO) VALUES (:emp_id, :proj_id)", [id_empleado, id_proyecto])
            conn.commit()
            return True
        except oracledb.IntegrityError:
            # Captura si ya está asignado
            return True
        except oracledb.Error as e:
            conn.rollback()
            print(f"Error ORA-{e.args[0].code} al asignar empleado: {e.args[0].message}")
            return False
        finally:
            cursor.close()
            conn.close()