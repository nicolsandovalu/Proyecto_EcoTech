from .db_connector import DatabaseConnector
from ..dominio.departamento import Departamento
import oracledb

class DepartamentoDAO:
    
    #Gestiona la persistencia de los objetos Departamento.
    
    def __init__(self):
        self.db = DatabaseConnector()

    def create_departamento(self, departamento_obj: Departamento) -> bool:
    
        #Registra un nuevo departamento en la base de datos (Operación CREATE).
        
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        data = departamento_obj.to_dict()
        
        try:
            # Usamos la secuencia de Oracle para obtener el ID (Asumimos que está definida: seq_departamento)
            sql = """
                INSERT INTO DEPARTAMENTO (ID_DEPARTAMENTO, NOMBRE, GERENTE_ID, ACTIVO)
                VALUES (seq_departamento.NEXTVAL, :nombre, :gerente_id, :activo)
            """
            cursor.execute(sql, data)
            conn.commit()
            print(f"Departamento '{data['nombre']}' creado exitosamente.")
            return True
            
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al crear departamento: {error.message}")
            return False
            
        finally:
            cursor.close()

    def get_departamento_by_id(self, depto_id: int) -> Departamento or None:
        
        #Busca y retorna un departamento por su ID (Operación READ/Buscar).
        
        conn = self.db.connect()
        if not conn:
            return None
        
        cursor = conn.cursor()
        
        try:
            sql = "SELECT ID_DEPARTAMENTO, NOMBRE, GERENTE_ID, ACTIVO FROM DEPARTAMENTO WHERE ID_DEPARTAMENTO = :id"
            cursor.execute(sql, {'id': depto_id})
            row = cursor.fetchone()
            
            if row:
                # Mapeo de tupla de Oracle a objeto Departamento (POO)
                return Departamento(
                    id_departamento=row[0],
                    nombre=row[1],
                    gerente_id=row[2],
                    activo=(row[3] == 1) # Mapeo de NUMBER(1) a booleano
                )
            return None
            
        except oracledb.Error as e:
            error, = e.args
            print(f"Error ORA-{error.code} al buscar departamento: {error.message}")
            return None
            
        finally:
            cursor.close()

    def update_departamento(self, departamento_obj: Departamento) -> bool:
        
        #Actualiza la información de un departamento existente (Operación UPDATE/Editar).
        
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        data = departamento_obj.to_dict()
        
        try:
            sql = """
                UPDATE DEPARTAMENTO
                SET NOMBRE = :nombre, 
                    GERENTE_ID = :gerente_id,
                    ACTIVO = :activo
                WHERE ID_DEPARTAMENTO = :id_departamento
            """
            cursor.execute(sql, data)
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
            
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al actualizar departamento: {error.message}")
            return False
            
        finally:
            cursor.close()

    def delete_departamento(self, depto_id: int) -> bool:
        
        #Elimina (o desactiva) un departamento (Operación DELETE/Eliminar).
        #Nota: Se recomienda un 'soft delete' (cambiar ACTIVO=0) en lugar de DELETE físico si hay FKs.
        
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        
        try:
            # Opción más segura: Soft Delete (si la empresa lo permite)
            sql = "UPDATE DEPARTAMENTO SET ACTIVO = 0 WHERE ID_DEPARTAMENTO = :id"
            
            # Opción requerida (si no hay datos dependientes): Hard Delete
            # sql = "DELETE FROM DEPARTAMENTO WHERE ID_DEPARTAMENTO = :id"
            
            cursor.execute(sql, {'id': depto_id})
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
            
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al eliminar departamento: {error.message}")
            # El error ORA-02292 (restricción de integridad violada) ocurriría aquí si usamos DELETE físico
            return False
            
        finally:
            cursor.close()