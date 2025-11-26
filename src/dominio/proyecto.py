from datetime import date
from typing import List

class Proyecto:
    def __init__(self, id_proyecto: int, nombre: str, descripcion: str, fecha_inicio: date, fecha_creacion: date = None):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_creacion = fecha_creacion or date.today()
        self.empleados: List['Empleado'] = []
    
    def crear(self) -> 'Proyecto':
        """Crea un nuevo proyecto"""
        return self
    
    def editar(self, nombre: str = None, descripcion: str = None) -> None:
        """Edita los datos del proyecto"""
        if nombre:
            self.nombre = nombre
        if descripcion:
            self.descripcion = descripcion
    
    def eliminar(self) -> bool:
        """Elimina el proyecto"""
        return True
    
    def asignar_empleados(self, empleado: 'Empleado') -> 'Empleado':
        """Asigna un empleado al proyecto"""
        if empleado not in self.empleados:
            self.empleados.append(empleado)
        return empleado

    def __str__(self) -> str:
        return f"Proyecto({self.id_proyecto}): {self.nombre}"