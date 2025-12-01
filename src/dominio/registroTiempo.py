# Archivo: src/dominio/registro_tiempo.py

from datetime import date


class RegistroTiempo:
 
    def __init__(self, id_registro: int = None, id_empleado: str = None,
                 id_proyecto: int = None, fecha_trabajo: date = None,
                 horas_trabajadas: float = None, descripcion_tareas: str = None,
                 fecha_registro: date = None):

        self._id_registro = id_registro         
        self._id_empleado = id_empleado         
        self._id_proyecto = id_proyecto          
        self._fecha_trabajo = fecha_trabajo     
        self._horas_trabajadas = horas_trabajadas
        self._descripcion_tareas = descripcion_tareas
        self._fecha_registro = fecha_registro

    def __str__(self):
        return (f"Registro ID: {self._id_registro} | Empleado: {self._id_empleado} | "
                f"Proyecto: {self._id_proyecto} | Fecha: {self._fecha_trabajo} | "
                f"Horas: {self._horas_trabajadas}")

    def to_dict(self):
        """Convierte el objeto a un diccionario para el DAO."""
        return {
            'id_registro': self._id_registro,
            'id_empleado': self._id_empleado,
            'id_proyecto': self._id_proyecto,
            'fecha_trabajo': self._fecha_trabajo,
            'horas_trabajadas': self._horas_trabajadas,
            'descripcion_tareas': self._descripcion_tareas,
            'fecha_registro': self._fecha_registro
        }
