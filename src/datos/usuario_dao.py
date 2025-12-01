from .db_connector import DatabaseConnector
from .seguridad_dao import SeguridadDAO
from ..dominio.usuario import Usuario
import oracledb

class UsuarioDAO:
    
    def __init__(self):
        self.db = DatabaseConnector()
        
    def create_usuario(self, usuario_obj: Usuario, contrasena_plana: str) -> bool:
        conn = self.db.connect()
        if not conn:
            return False
        
        cursor = None
        
        try:
            cursor = conn.cursor()
            
            hashed_password = SeguridadDAO.hash_password(contrasena_plana)
            
            sql = """
                INSERT INTO USUARIO (ID_USUARIO, ID_EMPLEADO, NOMBRE, CONTRASEÑA, ID_ROL)
                VALUES (:id_usuario, :id_empleado, :nombre, :contrasena, :id_rol)
                """
            
            data = {
                'id_usuario': usuario_obj.get_id(),
                'id_empleado': usuario_obj.get_id_empleado(),
                'nombre': usuario_obj.get_nombre_usuario(),
                'contrasena': hashed_password,
                'id_rol': usuario_obj.get_id_rol()
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
                
                # MÉTODO: AUTENTICACIÓN (Login)

    def authenticate_user(self, username: str, password_plana: str) -> dict or None:
        """
        Busca al usuario por nombre/email y verifica la contraseña hasheada.
        (Cumple el requisito de Autenticación Segura).
        """
        conn = self.db.connect()
        if not conn:
            return None

        cursor = None

        try:
            cursor = conn.cursor()

            # La consulta busca al usuario por nombre de usuario (USUARIO.NOMBRE) o por Email (EMPLEADO.EMAIL)
            sql = """
                SELECT u.CONTRaseña, e.NOMBRE, u.ID_ROL, e.ID_EMPLEADO
                FROM USUARIO u
                JOIN EMPLEADO e ON u.ID_EMPLEADO = e.ID_EMPLEADO
                WHERE u.NOMBRE = :user_input OR e.EMAIL = :user_input
            """
            cursor.execute(sql, {'user_input': username})
            
            user_record = cursor.fetchone()

            if not user_record:
                return None  # Usuario no encontrado

            hashed_password = user_record[0] # El hash almacenado
            
            # 1. VERIFICACIÓN DEL HASH (Seguridad)
            if SeguridadDAO.check_password(password_plana, hashed_password):
                # Autenticación exitosa
                return {
                    'nombre': user_record[1],
                    'id_rol': user_record[2],
                    'id_empleado': user_record[3]
                }
            else:
                return None  # Contraseña incorrecta

        except oracledb.Error as e:
            error, = e.args
            print(f"Error ORA-{error.code} durante la autenticación: {error.message}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()