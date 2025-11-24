#Módulo para el manejo de seguridad de contraseñas mediante hashing (bcrypt). Crucial para la Autenticación Segura y Protección de Datos Sensibles
import bcrypt

class SeguridadDAO:
    #implementa técnicas de cifrado, hashing, para la seguridad de contraseñas
    
    @staticmethod
    def hash_password(password: str) -> str:
        #cifra contraseña en texto usando bcrypt. Retorna el hashs codigicado en str
    
        if not password:
            return ""
        
        # Genera el hash con un salt aleatorio, codificando la entrada a bytes
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        #devuelve el hash como string
        return hashed.decode('utf-8')
    
    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        #verifica si la contrasñea ingresada coindice con el hash almacenado en la BD
        
        if not password or not hashed_password:
            return False
        
        try:
            # Compara la contraseña (bytes) con el hash almacenado (bytes).  Retorna True si coinciden, False en caso contrario.
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except ValueError:
            return False   
        
        
