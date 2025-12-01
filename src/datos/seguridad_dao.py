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
        
        

# --- Bloque de prueba para generar hash e insertarlo en Oracle ---

if __name__ == "__main__":
    # La clase SeguridadDAO ya está definida en este archivo, la usamos directamente
    
    # 1. Definimos la contraseña plana que queremos usar
    CONTRASENA_PLANA = "admin123" 
    
    # 2. Generamos el hash cifrado usando bcrypt
    fresh_hash = SeguridadDAO.hash_password(CONTRASENA_PLANA)
    
    print("\n=============================================")
    print("HASH GENERADO PARA ORACLE (admin123):")
    print(fresh_hash)
    print("=============================================")
    
    # 3. Prueba de verificación (opcional)
    if SeguridadDAO.check_password(CONTRASENA_PLANA, fresh_hash):
        print("VERIFICACIÓN INTERNA: ÉXITO (El hash es válido para la clave plana).")
    else:
        print("VERIFICACIÓN INTERNA: FALLO. Algo salió mal con la generación del hash.")