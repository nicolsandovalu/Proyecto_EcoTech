from .db_connector import DatabaseConnector
from ..dominio.rol import Rol
import oracledb
from typing import List, Optional

class RolDAO:
    
    def __init__(self):
        self.db = DatabaseConnector()
        
    def get_all_roles(self) -> list:
        # Recupera y retorna una lista de todos los roles disponibles en la BD
        conn = self.db.connect()
        if not conn:
            return []
        
        cursor = None
        roles_list = []
        
        try:
            cursor = conn.cursor()
            sql = "SELECT ID_ROL, NOMBRE, DESCRIPCION, NIVEL_PERMISOS FROM ROL ORDER BY NIVEL_PERMISOS DESC"
            
            # --- Indentación corregida ---
            cursor.execute(sql) 
            results = cursor.fetchall()
            # ---------------------------
            
            for row in results:
                # Mapeo a objeto Rol (POO) con comas corregidas
                roles_list.append(Rol(
                    id_rol=row[0],
                    nombre=row[1],
                    descripcion=row[2],
                    nivel_permisos=row[3]
                ))
                
            return roles_list
        
        except oracledb.Error as e:
            error, = e.args
            print(f"Error ORA-{error.code} al listar roles: {error.message}")
            return []

        finally:
            if cursor:
                cursor.close()

    
    def get_rol_by_id(self, id_rol: int) -> Optional[Rol]:
        conn = self.db.connect()
        cursor = None
        rol = None
        
        sql = "SELECT id_rol, nombre, descripcion, nivel_permisos FROM ROL WHERE id_rol = :id"
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, id=id_rol)
            
            row = cursor.fetchone()
            
            if row:
                # Mapeo de fila de BD a objeto de Dominio (Rol)
                rol = Rol(
                    id_rol=row[0],
                    nombre=row[1],
                    descripcion=row[2],
                    nivel_permisos=row[3]
                )
                
        except oracledb.Error as e:
            print(f"Error al obtener Rol por ID {id_rol}: {e}")
        finally:
            if cursor:
                cursor.close()
            
        return rol
    
    #crear rol 
    def create_rol(self, rol: Rol) -> bool:
        """Inserta un nuevo Rol en la base de datos."""
        conn = self.db.connect()
        cursor = None
        success = False
        
        sql = "INSERT INTO ROL (id_rol, nombre, descripcion, nivel_permisos) VALUES (:1, :2, :3, :4)"
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                rol.get_id(),
                rol.get_nombre(),
                rol.get_descripcion(),
                rol.get_nivel_permisos()
            ))
            conn.commit()
            success = True
            
        except oracledb.IntegrityError as e:
            print(f"Error de integridad (PK duplicada o FK): {e}")
            conn.rollback()
        except oracledb.Error as e:
            print(f"Error al crear Rol: {e}")
            conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return success
    
    #update
    def update_rol(self, rol: Rol) -> bool:
        """Actualiza la información de un Rol existente."""
        conn = self.db.connect()
        cursor = None
        success = False
        
        sql = """
            UPDATE ROL SET 
                nombre = :nombre, 
                descripcion = :descripcion, 
                nivel_permisos = :nivel_permisos 
            WHERE id_rol = :id_rol
        """
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, 
                nombre=rol.get_nombre(),
                descripcion=rol.get_descripcion(),
                nivel_permisos=rol.get_nivel_permisos(),
                id_rol=rol.get_id()
            )
            
            if cursor.rowcount > 0:
                conn.commit()
                success = True
            else:
                print(f"Advertencia: No se encontró el Rol con ID {rol.get_id()} para actualizar.")
                
        except oracledb.Error as e:
            print(f"Error al actualizar Rol: {e}")
            conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return success
    
    #delete
    def delete_rol(self, id_rol: int) -> bool:
        """Elimina un Rol por su ID. Falla si hay Usuarios asociados."""
        conn = self.db.connect()
        cursor = None
        success = False
        
        sql = "DELETE FROM ROL WHERE id_rol = :id"
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, id=id_rol)
            
            if cursor.rowcount > 0:
                conn.commit()
                success = True
            else:
                print(f"Advertencia: No se encontró el Rol con ID {id_rol} para eliminar.")
                
        except oracledb.IntegrityError as e:
            print(f"Error de Integridad: No se puede eliminar el Rol {id_rol} porque tiene usuarios asociados.")
            conn.rollback()
        except oracledb.Error as e:
            print(f"Error al eliminar Rol: {e}")
            conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return success