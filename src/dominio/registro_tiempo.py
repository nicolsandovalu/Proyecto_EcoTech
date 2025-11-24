# Archivo: src/dominio/registro_tiempo.py

from datetime import date


class RegistroTiempo:
    """
    Modelo de la entidad Registro_Tiempo, que almacena las horas dedicadas
    por un empleado a un proyecto en una fecha específica.
    """

    def __init__(self, id_registro: int = None, id_empleado: str = None,
                 id_proyecto: int = None, fecha_trabajo: date = None,
                 horas_trabajadas: float = None, descripcion_tareas: str = None,
                 fecha_registro: date = None):

        self.id_registro = id_registro          # PK (Usando secuencia)
        self.id_empleado = id_empleado          # FK a Empleado
        self.id_proyecto = id_proyecto          # FK a Proyecto
        self.fecha_trabajo = fecha_trabajo      # Fecha en que se realizó el trabajo
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_tareas = descripcion_tareas
        # Fecha de registro en el sistema (Default SYSDATE)
        self.fecha_registro = fecha_registro

    def __str__(self):
        return (f"Registro ID: {self.id_registro} | Empleado: {self.id_empleado} | "
                f"Proyecto: {self.id_proyecto} | Fecha: {self.fecha_trabajo} | "
                f"Horas: {self.horas_trabajadas}")

    def to_dict(self):
        """Convierte el objeto a un diccionario para el DAO."""
        return {
            'id_registro': self.id_registro,
            'id_empleado': self.id_empleado,
            'id_proyecto': self.id_proyecto,
            'fecha_trabajo': self.fecha_trabajo,
            'horas_trabajadas': self.horas_trabajadas,
            'descripcion_tareas': self.descripcion_tareas,
            'fecha_registro': self.fecha_registro
        }
