from .db_connector import DatabaseConnector
from ..dominio.rol import Rol
import oracledb


class RolDAO:

    def __init__(self):
        self.db = DatabaseConnector()

    # --- [MÉTODO EXISTENTE] ---
    def get_all_roles(self) -> list:
        # ... (código que ya tienes para listar todos los roles) ...
        pass

    # --- [MÉTODO EXISTENTE] ---
    def get_rol_by_id(self, rol_id: int) -> Rol or None:
        # ... (código que ya tienes, que está correcto) ...
        pass

    # --- [NUEVO MÉTODO] ---
    def get_rol_by_name(self, rol_name: str) -> Rol or None:
        """
        Recupera un objeto Rol buscando por su nombre (ej. 'EMPLEADO', 'ADMINISTRADOR').
        Esto es crucial para la lógica de registro de usuarios.
        """
        conn = self.db.connect()
        if not conn:
            return None

        cursor = conn.cursor()

        try:
            sql = """
                SELECT ID_ROL, NOMBRE, DESCRIPCION, NIVEL_PERMISOS 
                FROM ROL 
                WHERE NOMBRE = UPPER(:rol_name)
            """

            # Usamos UPPER() en el SQL para hacer la búsqueda insensible a mayúsculas/minúsculas
            cursor.execute(sql, {'rol_name': rol_name.upper()})
            row = cursor.fetchone()

            if row:
                # Mapeo a objeto Rol
                return Rol(
                    id_rol=row[0],
                    nombre=row[1],
                    descripcion=row[2],
                    nivel_permisos=row[3]
                )
            return None  # Retorna None si no se encuentra el rol

        except oracledb.Error as e:
            error, = e.args
            print(
                f"Error ORA-{error.code} al buscar rol por nombre: {error.message}")
            return None

        finally:
            if cursor:
                cursor.close()
