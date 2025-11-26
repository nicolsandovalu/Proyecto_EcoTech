class Rol:
    # Representa un rol de usuario con su respectivo nivel de permisos

    def __init__(self, id_rol: int, nombre: str, descripcion: str = None, nivel_permisos: int = 0):
        self._id = id_rol
        self._nombre = nombre
        self._descripcion = descripcion
        self._nivel_permisos = nivel_permisos

    def get_id(self) -> str:
        # Retorna el ID del rol
        return self._id

    def get_nombre(self) -> str:
        # Retorna el nombre del rol
        return self._nombre

    def get_nivel_permisos(self) -> int:
        # Retorna el nivel de autorización asociado
        return self._nivel_permisos

    def to_dict(self) -> dict:
        # Convierte el objeto a un diccionario
        return {
            'id_rol': self._id,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'nivel_permisos': self._nivel_permisos
        }

    def __str__(self):
        # representación en cadena
        return f"Rol ID: {self._id}, Nombre: {self._nombre}, Nivel de Permisos: {self._nivel_permisos}"
