import oracledb
from ..dominio.empleado import Empleado
from .db_connector import DatabaseConnector
from datetime import date, datetime
from typing import Optional


class EmpleadoDAO:

    def __init__(self):
        self.db = DatabaseConnector()

    def create_empleado(self, empleado: Empleado) -> bool:

        #Inserta un nuevo registro en la tabla EMPLEADO.

        conn = self.db.connect()
        if not conn:
            return False

        cursor = None

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO EMPLEADO (ID_EMPLEADO, ID_CARGO, ID_DEPARTAMENTO, NOMBRE, EMAIL, SALARIO, 
                                    FECHA_INICIO_CONTRATO, DIRECCION, TELEFONO)
                VALUES (:id_empleado, :id_cargo, :id_departamento, :nombre, :email, :salario, 
                        TO_DATE(:fecha_inicio_contrato, 'YYYY-MM-DD'), :direccion, :telefono)
            """

            # Usamos el to_dict del modelo Empleado para obtener los datos
            # El modelo Empleado.to_dict debe formatear la fecha a 'YYYY-MM-DD'
            data = empleado.to_dict()

            cursor.execute(sql, data)
            conn.commit()
            return True

        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al crear empleado: {error.message}")
            return False

        finally:
            cursor.close() 


    def get_all_empleados(self) -> list:
        # retorna una lista de todos los objetos Empleado activos en el sistema
        conn = self.db.connect()
        if not conn:
            return []

        cursor = None
        empleados_list = []

        try:
            cursor = conn.cursor()
            sql ="""
                SELECT ID_EMPLEADO, ID_CARGO, ID_DEPARTAMENTO, NOMBRE, EMAIL, SALARIO, FECHA_INICIO_CONTRATO, DIRECCION, TELEFONO 
                FROM EMPLEADO
                ORDER BY NOMBRE """

            cursor.execute(sql)
            results = cursor.fetchall()

            # mapeo a objetos Empleado
            for row in results:
                # La función strftime es necesaria aquí ya que row[6] es un objeto datetime de Python
                empleados_list.append(Empleado(
                   id_empleado=row[0],
                    id_cargo=row[1],
                    id_departamento=row[2],
                    nombre=row[3],
                    email=row[4],
                    salario=row[5],
                    fecha_inicio_contrato=row[6].strftime('%Y-%m-%d') if row[6] else None,
                    direccion=row[7],
                    telefono=row[8]
                ))

            return empleados_list

        except oracledb.Error as e:
            error, = e.args
            print(
                f"Error ORA-{error.code} al listar empleados: {error.message}")
            return []

        finally:
            cursor.close() 
    
    # READ (Buscar por ID)
    def get_empleado_by_id(self, empleado_id: str) -> Optional[Empleado]:
        """Busca y retorna un solo objeto Empleado por su ID."""
        conn = self.db.connect()
        if not conn: return None

        cursor = None
        try:
            cursor = conn.cursor()
            sql ="""
                SELECT ID_EMPLEADO, ID_CARGO, ID_DEPARTAMENTO, NOMBRE, EMAIL, SALARIO, FECHA_INICIO_CONTRATO, DIRECCION, TELEFONO 
                FROM EMPLEADO WHERE ID_EMPLEADO = :id"""

            cursor.execute(sql, {'id': empleado_id})
            row = cursor.fetchone()

            if row:
                return Empleado(
                    id_empleado=row[0],
                    id_cargo=row[1],
                    id_departamento=row[2],
                    nombre=row[3],
                    email=row[4],
                    salario=row[5],
                    fecha_inicio_contrato=row[6].strftime('%Y-%m-%d') if row[6] else None,
                    direccion=row[7],
                    telefono=row[8]
                )
            return None

        except oracledb.Error as e:
            return None
        
        finally:
            cursor.close()

    def update_empleado(self, empleado: Empleado) -> bool:
        """Actualiza todos los campos de un empleado en la BD."""
        conn = self.db.connect()
        if not conn: return False

        cursor = None
        try:
            cursor = conn.cursor()
            sql = """
                UPDATE EMPLEADO
                SET ID_CARGO = :id_cargo,
                    ID_DEPARTAMENTO = :id_departamento,
                    NOMBRE = :nombre,
                    EMAIL = :email,
                    SALARIO = :salario,
                    FECHA_INICIO_CONTRATO = TO_DATE(:fecha_inicio_contrato, 'YYYY-MM-DD'),
                    DIRECCION = :direccion,
                    TELEFONO = :telefono
                WHERE ID_EMPLEADO = :id_empleado
            """
            
            data = empleado.to_dict()

            if isinstance(data['fecha_inicio_contrato'], date):
                 data['fecha_inicio_contrato'] = data['fecha_inicio_contrato'].strftime('%Y-%m-%d')

            cursor.execute(sql, data)
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            else:
                conn.rollback() 
                return False 
                
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al actualizar empleado: {error.message}")
            return False

        finally:
            cursor.close()

    def assign_empleado_to_proyecto(self, empleado_id: str, proyecto_id: int) -> bool:
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()

        try:
            sql = """
                    INSERT INTO EMPLEADO_PROYECTO (ID_EMPLEADO, ID_PROYECTO)
                    VALUES (:emp_id, :proj_id)
                """
            cursor.execute(
                sql, {'emp_id': empleado_id, 'proj_id': proyecto_id})
            conn.commit()
            return True

        except oracledb.IntegrityError:
            print(
                f"El empleado {empleado_id} ya está asignado al proyecto {proyecto_id}.")
            return True

        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(
                f"Error ORA-{error.code} al asignar proyecto: {error.message}")
            return False

        finally:
            cursor.close()

    def deassign_empleado_from_proyecto(self, empleado_id: str, proyecto_id: int) -> bool:
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()

        try:
            # CORRECCIÓN CLAVE: Usamos los nombres de columna correctos (ID_EMPLEADO, ID_PROYECTO)
            sql = """
                DELETE FROM EMPLEADO_PROYECTO 
                WHERE ID_EMPLEADO = :emp_id AND ID_PROYECTO = :proj_id
            """
            cursor.execute(sql, {'emp_id': empleado_id, 'proj_id': proyecto_id})
            
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
                
    def delete_empleado(self, empleado_id: str) -> bool: 
    #elimina el registro de usuario y el registro de empleado
    
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()

        try:
            # 1. Eliminar entradas dependientes (Asignación a Proyectos)
            cursor.execute("DELETE FROM EMPLEADO_PROYECTO WHERE ID_EMPLEADO = :id", {'id': empleado_id})
            
            # 2. Eliminar el registro de Usuario (Asociado a la Autenticación)
            cursor.execute("DELETE FROM USUARIO WHERE ID_EMPLEADO = :id", {'id': empleado_id})

            # 3. Eliminar el Empleado
            cursor.execute("DELETE FROM EMPLEADO WHERE ID_EMPLEADO = :id", {'id': empleado_id})
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
            
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al eliminar empleado: {error.message}")
            return False
            
        finally:
            cursor.close()
            