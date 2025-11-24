import oracledb
from ..dominio.empleado import Empleado
from .db_connector import DatabaseConnector


class EmpleadoDAO:
    
    def __init__(self):
        self.db = DatabaseConnector()
    
    def get_all_empleados(self) -> list:
        #retorna una lista de todos los objetos Empleado activos en el sistema
        conn = self.db.connect()
        if not conn:
            return[]
        
        cursor = conn.cursor()
        empleados_list = []
        
        try:
            cursor = conn.cursor()
            sql = """
                        SELECT ID_EMPLEADO, ID_CARGO, ID_DEPARTAMENTO, NOMBRE, EMAIL, SALARIO, FECHA_INICIO_CONTRATO 
                        FROM EMPLEADO
                        ORDER BY NOMBRE """
                        
            cursor.execute(sql)
            results = cursor.fetchall()
            
            #mapeo a objetos Empleado
            for row in results:
                empleados_list.append(Empleado( 
                    id_empleado=row[0], 
                    id_cargo=row[1],
                    id_departamento=row[2],
                    nombre=row[3],
                    email=row[4],
                    salario=row[5],
                    fecha_inicio_contrato=row[6].strftime('%Y-%m-%d') if row[6] else None
                ))
                
            return empleados_list

        except oracledb.Error as e:
            error, = e.args
            print(f"Error ORA-{error.code} al listar empleados: {error.message}")
            return []

        finally:
            if cursor:
                cursor.close()

    def assign_empleado_to_proyecto(self, empleado_id: str, proyecto_id: int) -> bool:
        conn = self.db.connect()
        if not conn: 
            return False 
        
        cursor = conn.cursor()
        
        try:
            #manejo de excepciones de FK garantiza que no se dupliquen
            sql = """
                    INSERT INTO EMPLEADO_PROYECTO (EMPLEADO_ID, PROYECTO_ID)
                    VALUES (:emp_id, :proj_id)
                """
            cursor.execute(sql, {'emp_id': empleado_id, 'proj_id': proyecto_id})
            conn.commit()
            return True
        
        except oracledb.IntegrityError:
            #captura si la combinación ya existe (PK DUPLICADA)
            print(f"El empleado {empleado_id} ya está asignado al proyecto {proyecto_id}.")
            return True #consideramos éxito si ya estaba asignado
        
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al asignar proyecto: {error.message}")
            return False
        
        finally:
            cursor.close()
            
    def deassign_empleado_from_proyecto(self, empleado_id: str, proyecto_id: int) -> bool:
        conn = self.db.connect()
        if not conn:
            return False
            
        cursor = conn.cursor()
            
        try:
            sql = """
                DELETE FROM EMPLEADO_PROYECTO 
                WHERE EMPLEADO_ID = :emp_id AND PROYECTO_ID = :proj_id
                """
            cursor.execute(sql,{'emp_id': empleado_id, 'proj_id': proyecto_id})
                
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
            
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al desasignar proyecto: {error.message}")
            return False
            
        finally:
            cursor.close()