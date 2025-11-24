from .db_connector import DatabaseConnector
from ..dominio.rol import Rol
import oracledb

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

    # El método get_rol_by_id estaba sintácticamente correcto
    def get_rol_by_id(self, rol_id: int) -> Rol or None:
        # ... (código que ya tienes, que está correcto) ...
        pass