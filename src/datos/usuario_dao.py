# Archivo: src/dao/usuario_dao.py

from .db_connector import DatabaseConnector
from ..dominio.usuario import Usuario  # Asumimos que tiene este modelo
import oracledb


class UsuarioDAO:

    def __init__(self):
        self.db = DatabaseConnector()

    def create_usuario(self, usuario: Usuario) -> bool:
        """
        Inserta un nuevo registro de login en la tabla USUARIO.
        """
        conn = self.db.connect()
        if not conn:
            return False

        cursor = None

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO USUARIO (ID_EMPLEADO, CONTRASENA, ID_ROL)
                VALUES (:id_empleado, :contrasena, :id_rol)
            """
            # El modelo Usuario debe tener getters o to_dict para acceder a los datos
            data = {
                # Usamos el ID del empleado como nombre de usuario
                'id_empleado': usuario.get_nombre_usuario(),
                'contrasena': usuario.get_contrasena(),
                'id_rol': usuario.get_id_rol()
            }

            cursor.execute(sql, data)
            conn.commit()
            return True

        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(f"Error ORA-{error.code} al crear usuario: {error.message}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
