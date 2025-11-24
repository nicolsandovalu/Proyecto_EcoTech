# Archivo: src/servicio/informe.py (o src/dominio/informe.py, dependiendo de la arquitectura)

class GeneradorInforme:
    """
    Clase de utilidad para consolidar y preparar datos
    para la generación de informes (e.g., total de horas).
    """

    def __init__(self, tipo_informe: str, datos_consulta: list = None):
        """
        Inicializa el generador con el tipo de informe y los datos crudos
        obtenidos del RegistroTiempoDAO.
        """
        self.tipo_informe = tipo_informe
        self.datos_consulta = datos_consulta if datos_consulta is not None else []
        self.datos_procesados = {}

    def procesar_horas_por_proyecto(self):
        """
        Procesa los datos crudos (registros de tiempo) para calcular el total
        de horas por cada proyecto.
        """
        horas_por_proyecto = {}

        # Iterar sobre la lista de registros (ej. una lista de objetos RegistroTiempo)
        for registro in self.datos_consulta:
            proyecto = registro.id_proyecto
            horas = registro.horas_trabajadas

            # Sumar las horas al proyecto correspondiente
            horas_por_proyecto[proyecto] = horas_por_proyecto.get(
                proyecto, 0) + horas

        self.datos_procesados = horas_por_proyecto
        return self.datos_procesados

    def generar_resumen(self):
        """
        Devuelve una cadena de texto formateada para el informe final.
        """
        resumen = f"--- INFORME: {self.tipo_informe.upper()} ---\n"

        if not self.datos_procesados:
            resumen += "No hay datos para generar el informe. Ejecute un método de procesamiento primero.\n"
            return resumen

        if self.tipo_informe == "horas_proyecto":
            resumen += "Total de Horas Trabajadas por Proyecto:\n"
            for proyecto_id, total_horas in self.datos_procesados.items():
                # En un sistema real, aquí buscaríamos el nombre del proyecto por su ID
                resumen += f"  Proyecto ID {proyecto_id}: {total_horas:.1f} horas\n"

        resumen += "--------------------------------------\n"
        return resumen

    # Aquí se agregarían otros métodos de procesamiento, como:
    # def procesar_horas_por_empleado(self): ...
    # def procesar_productividad_departamento(self): ...
