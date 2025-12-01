from typing import Optional

class Rol:
    #Representa un rol de usuario con su respectivo nivel de permisos
    
    def __init__(self, id_rol: int, nombre: str, descripcion: str = None, nivel_permisos: int = 0):
        self._id = id_rol
        self._nombre = nombre
        self._descripcion = descripcion
        self._nivel_permisos = nivel_permisos
        
    def get_id(self) -> int:
        #Retorna el ID del rol
        return self._id
    
    def get_nombre(self) -> str:
        #Retorna el nombre del rol
        return self._nombre
    
    def get_descripcion(self) -> str:
        #Retorna la descripción del rol
        return self._descripcion
    
    def get_nivel_permisos(self) -> int:
        #Retorna el nivel de autorización asociado
        return self._nivel_permisos
    
    def set_nombre(self, nombre: str):
        #Establece el nuevo nombre del rol
        self._nombre = nombre

    def set_descripcion(self, descripcion: str):
        #Establece la nueva descripción del rol
        self._descripcion = descripcion

    def set_nivel_permisos(self, nivel_permisos: int):
        #Establece el nuevo nivel de permisos del rol
        self._nivel_permisos = nivel_permisos
    
    def to_dict(self) -> dict:
        #Convierte el objeto a un diccionario
        return {
            'id_rol': self._id,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'nivel_permisos': self._nivel_permisos
        }
    
    def __str__(self):
        #representación en cadena
        return f"Rol ID: {self._id}, Nombre: {self._nombre}, Nivel de Permisos: {self._nivel_permisos}"