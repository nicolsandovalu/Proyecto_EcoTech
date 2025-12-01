from ..datos.registroTiempo_dao import RegistroTiempoDAO
from ..datos.empleado_dao import EmpleadoDAO
from ..datos.proyecto_dao import ProyectoDAO
from datetime import date

class GeneradorInforme:
   
   
    def __init__(self):
        #Inicializa los DAOs necesarios para obtener los datos de la BD.
        self.registro_dao = RegistroTiempoDAO()
        self.proyecto_dao = ProyectoDAO()
        self.empleado_dao = EmpleadoDAO()

    # ========================================================
    # MÉTODO DE REPORTE PRINCIPAL (HORAS POR PROYECTO)
    # ========================================================

    def generar_informe_horas_por_proyecto(self, fecha_inicio: date, fecha_fin: date) -> str:
        """
        Genera el informe de Horas Trabajadas por Proyecto en un rango de fechas.
        
        Args:
            fecha_inicio (date): Fecha de inicio del rango.
            fecha_fin (date): Fecha de fin del rango.
            
        Returns:
            str: El informe formateado listo para mostrar o exportar (PDF/Excel).
        """
        
        # 1. Delegar la consulta agregada a la Capa de Datos (DAO)
        # El DAO ejecuta la SUMA y GROUP BY directamente en Oracle.
        datos_agregados = self.registro_dao.get_total_horas_por_proyecto_en_rango(
            fecha_inicio, fecha_fin
        )
        
        if not datos_agregados:
            return f"No se encontraron registros de tiempo entre {fecha_inicio.strftime('%Y-%m-%d')} y {fecha_fin.strftime('%Y-%m-%d')}."
            
        # 2. Formateo y Generación del Resumen
        resumen = f"--- INFORME: HORAS POR PROYECTO (Del {fecha_inicio.strftime('%Y-%m-%d')} al {fecha_fin.strftime('%Y-%m-%d')}) ---\n"
        resumen += "-----------------------------------------------------------------\n"
        resumen += f"| {'ID Proyecto':<15} | {'Nombre Proyecto':<30} | {'Total Horas':<15} |\n"
        resumen += "-----------------------------------------------------------------\n"
        
        for proyecto_id, total_horas in datos_agregados:
            # En un sistema real, el Servicio buscaría el nombre del proyecto
            proyecto_obj = self.proyecto_dao.get_proyecto_by_id(proyecto_id)
            nombre_proyecto = proyecto_obj.get_nombre() if proyecto_obj else "Desconocido"

            resumen += f"| {proyecto_id:<15} | {nombre_proyecto:<30} | {total_horas:.2f} horas | \n"
            
        resumen += "-----------------------------------------------------------------\n"
        
        # (Aquí iría la lógica para EXPORTAR a PDF o Excel, cumpliendo el requisito de formatos exportables)
        # self.exportar_a_pdf(resumen)
        
        return resumen

    # ========================================================
    # MÉTODO DE REPORTE DE EMPLEADOS (Requisito General)
    # ========================================================

    def generar_informe_empleados(self) -> str:
        """Genera el informe de listado completo de empleados."""
        
        empleados = self.empleado_dao.get_all_empleados()
        
        if not empleados:
            return "No hay empleados registrados en el sistema."
            
        resumen = "--- INFORME DE LISTADO DE EMPLEADOS ---\n"
        resumen += "-----------------------------------------------------------------\n"
        resumen += f"| {'ID Empleado':<12} | {'Nombre':<25} | {'Email':<30} | {'Salario':<15} |\n"
        resumen += "-----------------------------------------------------------------\n"
        
        for emp in empleados:
            # Los métodos get_X() se usan para acceder a los atributos protegidos del objeto Dominio
            resumen += f"| {emp.get_id():<12} | {emp.get_nombre():<25} | {emp.get_email():<30} | {emp.get_salario():<15.2f} |\n"
            
        resumen += "-----------------------------------------------------------------\n"
        return resumen
