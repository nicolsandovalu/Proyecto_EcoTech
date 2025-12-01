import oracledb
from ..dominio.empleado import Empleado
from .db_connector import DatabaseConnector


class EmpleadoDAO:

    def __init__(self):
        self.db = DatabaseConnector()

    # ----------------------------------------------------
    # MÉTODO: CREATE
    # ----------------------------------------------------
    def create_empleado(self, empleado: Empleado) -> bool:

        #Inserta un nuevo registro en la tabla EMPLEADO.

        conn = self.db.connect()
        if not conn:
            return False

        cursor = None

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO EMPLEADO (ID_EMPLEADO, ID_CARGO, ID_DEPARTAMENTO, NOMBRE, EMAIL, SALARIO, FECHA_INICIO_CONTRATO)
                VALUES (:id_empleado, :id_cargo, :id_departamento, :nombre, :email, :salario, TO_DATE(:fecha_inicio_contrato, 'YYYY-MM-DD'))
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
            if cursor:
                cursor.close()
            if conn:
                conn.close()  # <- Corrección: Asegurar el cierre de la conexión

    # ----------------------------------------------------
    # MÉTODO: READ (LISTAR)
    # ----------------------------------------------------

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
            if cursor:
                cursor.close()
            if conn:
                conn.close()  # <- Corrección: Asegurar el cierre de la conexión

    # ----------------------------------------------------
    # MÉTODOS: ASIGNACIÓN DE PROYECTOS (N:M)
    # ----------------------------------------------------

    def assign_empleado_to_proyecto(self, empleado_id: str, proyecto_id: int) -> bool:
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()

        try:
            sql = """
                    INSERT INTO EMPLEADO_PROYECTO (EMPLEADO_ID, PROYECTO_ID)
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
            if cursor:
                cursor.close()
            if conn:
                conn.close()  # <- Corrección: Asegurar el cierre de la conexión

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
            cursor.execute(sql, {'emp_id': empleado_id, 'proj_id': proyecto_id})
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
        
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al desasignar proyecto: {error.message}")
            
        finally:
            if cursor: 
                cursor.close()
            if conn:
                conn.close()
                
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
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            