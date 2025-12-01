from datetime import date
from typing import List

class Proyecto:
    
    def __init__(self, id_proyecto: int, nombre: str, descripcion: str, fecha_inicio: date, fecha_creacion: date = None):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self._fecha_creacion = fecha_creacion or date.today()
        self._empleados: List = []
    
    def get_id(self) -> int:
        """Retorna el ID del proyecto (acceso público al atributo _id_proyecto)."""
        return self._id_proyecto

    def get_nombre(self) -> str:
        """Retorna el nombre del proyecto."""
        return self._nombre

    def get_descripcion(self) -> str:
        """Retorna la descripción del proyecto."""
        return self._descripcion
        
    def get_fecha_inicio(self) -> date:
        """Retorna la fecha de inicio del proyecto."""
        return self._fecha_inicio
    
    def crear(self) -> int:
        # Método lógico para la capa de servicio
        return self._id_proyecto
    
    def editar(self, nombre: str = None, descripcion: str = None) -> None:
        """Edita los datos del proyecto (Validación de Entradas Seguras)."""
        if nombre:
            self._nombre = nombre
        if descripcion:
            self._descripcion = descripcion
    
    def eliminar(self) -> bool:
        # Método lógico para la capa de servicio
        return True
    
    def asignar_empleados(self, empleado: 'Empleado'):
        """Asigna un empleado al proyecto (Relación N:M)."""
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            return True
        return False
    
    def desasignar_empleados(self, empleado: 'Empleado'):
        if empleado in self._empleados:
            self._empleados.remove(empleado)
            return True
        return False
    
    # --- MÉTODO PARA EL DAO ---
    
    def to_dict(self) -> dict:
        """Convierte el objeto Proyecto a un diccionario para que el DAO lo use en las operaciones SQL."""
        fecha_inicio_str = self._fecha_inicio.strftime('%Y-%m-%d') if self._fecha_inicio else None
        fecha_creacion_str = self._fecha_creacion.strftime('%Y-%m-%d') if self._fecha_creacion else None
        
        return {
            'id_proyecto': self._id_proyecto,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'fecha_inicio': fecha_inicio_str,
            'fecha_creacion': fecha_creacion_str
        }
        
    def __str__(self) -> str:
        return f"Proyecto({self._id_proyecto}): {self._nombre}"