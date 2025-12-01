import oracledb
from .db_connector import DatabaseConnector
from ..dominio.departamento import Departamento
from typing import List, Optional

class DepartamentoDAO:
    
    #Gestiona la persistencia de los objetos Departamento.
    
    def __init__(self):
        self.db = DatabaseConnector()

    # ========================================================
    # 1. MÉTODO: CREATE (Crear nuevo departamento)
    # ========================================================
    def create_departamento(self, departamento_obj: Departamento) -> int | None:
    
        conn = self.db.connect()
        if not conn:
            return None

        cursor = conn.cursor()
        data = departamento_obj.to_dict()
        
        # Eliminar ID de Python (resuelve DPY-4008)
        if 'id_departamento' in data:
            del data['id_departamento']
        
        new_id_var = cursor.var(oracledb.NUMBER) 
        data['new_id'] = new_id_var
        
        try:
            # SQL CORREGIDO: Usando GERENTE_ID
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

    # ========================================================
    # 2. MÉTODO: READ (Buscar por ID)
    # ========================================================
    def get_departamento_by_id(self, depto_id: int) -> Departamento | None:
        
        conn = self.db.connect()
        if not conn:
            return None
        
        cursor = conn.cursor()
        
        try:
            # SQL CORREGIDO
            sql = "SELECT ID_DEPARTAMENTO, NOMBRE, GERENTE_ID, FECHA_CREACION, ACTIVO FROM DEPARTAMENTO WHERE ID_DEPARTAMENTO = :id"
            cursor.execute(sql, {'id': depto_id})
            row = cursor.fetchone()
            
            if row:
                # Mapeo a objeto Departamento, usando gerente_id
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

    # ========================================================
    # 3. MÉTODO: UPDATE (Modificar departamento)
    # ========================================================
    def update_departamento(self, departamento_obj: Departamento) -> bool:
        
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        data = departamento_obj.to_dict()
        
        try:
            # SQL CORREGIDO: Usa GERENTE_ID
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

    # ========================================================
    # 4. MÉTODO: DELETE (Soft Delete)
    # ========================================================
    def delete_departamento(self, depto_id: int) -> bool:
        
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        
        try:
            # Implementa Soft Delete (cambiar ACTIVO=0)
            sql = "UPDATE DEPARTAMENTO SET ACTIVO = 0 WHERE ID_DEPARTAMENTO = :id"
            
            cursor.execute(sql, {'id': depto_id})
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
            
        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al eliminar departamento: {error.message}")
            return False
            
        finally:
            if cursor:
                cursor.close()
            
    # ========================================================
    # 5. MÉTODO: READ (Listar todos)
    # ========================================================
    def get_all_departamentos(self) -> List:
    
        conn = self.db.connect()
        if not conn:
            return []

        cursor = None
        departamentos_list = []
    
        try:
            cursor = conn.cursor()
            # SQL CORREGIDO
            sql = """
                SELECT ID_DEPARTAMENTO, NOMBRE, GERENTE_ID, FECHA_CREACION, ACTIVO 
                FROM DEPARTAMENTO 
                ORDER BY NOMBRE"""
    
            cursor.execute(sql)
            results = cursor.fetchall()
        
            for row in results:
                # Mapeo de retorno CORREGIDO
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