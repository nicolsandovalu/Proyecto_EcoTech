from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .empleado import Empleado 

class Usuario:
    #Representa las credenciales de acceso asociadas a un Empleado.
    
    def __init__(self, id_usuario: str, nombre_usuario: str, contrasena_hash: str, id_rol: int, id_empleado: str):
        """
        Constructor de la clase Usuario.
        """
        
        # Atributos Persistidos (Visibilidad Protegida)
        self._id_usuario = id_usuario
        self._nombre_usuario = nombre_usuario
        self._contrasena_hash = contrasena_hash # CRÍTICO: Almacena el hash cifrado
        self._id_rol = id_rol
        self._id_empleado = id_empleado

    # --- MÉTODOS GETTERS ---
    
    def get_id(self) -> str:
        return self._id_usuario
        
    def get_nombre_usuario(self) -> str:
        return self._nombre_usuario
        
    def get_contrasena_hash(self) -> str:
        """Retorna el hash de la contraseña para la verificación."""
        return self._contrasena_hash
    
    def get_id_rol(self) -> int:
        return self._id_rol
        
    def get_id_empleado(self) -> str:
        return self._id_empleado

    # --- MÉTODO CRÍTICO PARA EL DAO ---
    def to_dict(self) -> dict:
        """Convierte el objeto Usuario a un diccionario para el DAO."""
        return {
            'id_usuario': self._id_usuario,
            'nombre_usuario': self._nombre_usuario,
            'contrasena_hash': self._contrasena_hash,
            'id_rol': self._id_rol,
            'id_empleado': self._id_empleado
        }