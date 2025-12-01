import oracledb
from .db_connector import DatabaseConnector
from ..dominio.departamento import Departamento
from typing import List, Optional

class DepartamentoDAO:
    
    #Gestiona la persistencia de los objetos Departamento.
    
    def __init__(self):
        self.db = DatabaseConnector()

    def create_departamento(self, departamento_obj: Departamento) -> int | None:
    
        #Registra un nuevo departamento en la base de datos (Operación CREATE).
        
        conn = self.db.connect()
        if not conn:
            return None

        cursor = conn.cursor()
        data = departamento_obj.to_dict()
        
        new_id_var = cursor.var(oracledb.NUMBER) 
        data['new_id'] = new_id_var
        
        try:
            # Usamos la secuencia de Oracle para obtener el ID (Asumimos que está definida: seq_departamento)
            sql = """
                INSERT INTO DEPARTAMENTO (ID_DEPARTAMENTO, NOMBRE, GERENTE_ID, ACTIVO)
                VALUES (seq_departamento.NEXTVAL, :nombre, :gerente_id, :activo)
                RETURNING ID_DEPARTAMENTO INTO :new_id
            """
            cursor.execute(sql, data)
            conn.commit()
            
            new_id = new_id_var.getvalue()[0]
            departamento_obj.id_departamento = new_id
            
            print(f"Departamento '{departamento_obj.nombre}' creado con ID: {new_id}")
            return new_id
            
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al crear departamento: {error.message}")
            return None
            
        finally:
            if cursor:
                cursor.close()

    def get_departamento_by_id(self, depto_id: int) -> Departamento | None:
        
        #Busca y retorna un departamento por su ID (Operación READ/Buscar).
        
        conn = self.db.connect()
        if not conn:
            return None
        
        cursor = conn.cursor()
        
        try:
            sql = "SELECT ID_DEPARTAMENTO, NOMBRE, GERENTE_ID, FECHA_CREACION, ACTIVO FROM DEPARTAMENTO WHERE ID_DEPARTAMENTO = :id"
            cursor.execute(sql, {'id': depto_id})
            row = cursor.fetchone()
            
            if row:
                # Mapeo de tupla de Oracle a objeto Departamento (POO)
                return Departamento(
                    id_departamento=row[0],
                    nombre=row[1],
                    gerente_id=row[2],
                    fecha_creacion=row[3],
                    activo=int(row[4])
                )
            return None
            
        except oracledb.Error as e:
            error, = e.args
            print(f"Error ORA-{error.code} al buscar departamento: {error.message}")
            return None
            
        finally:
            if cursor:
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
            if cursor:
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
            if cursor:
                cursor.close()
            
# MÉTODO: READ (LISTAR)
    def get_all_departamentos(self) -> List:
    
    #Recupera y retorna una lista de todos los departamentos registrados 
        conn = self.db.connect()
        if not conn:
            return []

        cursor = None
        departamentos_list = []
    
        try:
            cursor = conn.cursor()
            sql = """
                SELECT ID_DEPARTAMENTO, NOMBRE, GERENTE_ID, FECHA_CREACION, ACTIVO 
                FROM DEPARTAMENTO 
                ORDER BY NOMBRE"""
    
            cursor.execute(sql)
            results = cursor.fetchall()
        
        # Mapea todas las filas a objetos del dominio
            for row in results:
                departamentos_list.append(Departamento(
                    id_departamento=row[0],
                    nombre=row[1],
                    gerente_id=row[2],
                    fecha_creacion=row[3],
                    activo=int(row[4])
                )
            )
        
            return departamentos_list
        
        except oracledb.Error as e:
            error, = e.args
            print(f"Error ORA-{error.code} al listar departamentos: {error.message}")
            return []
        
        finally:
            if cursor:
                cursor.close()
            