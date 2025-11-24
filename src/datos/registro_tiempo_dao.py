# Archivo: src/dao/registro_tiempo_dao.py

from ..db_connector import DatabaseConnector
from ..dominio.registro_tiempo import RegistroTiempo
import oracledb
from datetime import date  # Necesario para el mapeo de fechas


class RegistroTiempoDAO:
    """
    Gestiona la persistencia de los objetos RegistroTiempo.
    Implementa las operaciones CRUD y las consultas necesarias para los informes.
    """

    def __init__(self):
        self.db = DatabaseConnector()

    def create_registro(self, registro_obj: RegistroTiempo) -> bool:
        """
        Registra una nueva entrada de tiempo en la base de datos (Operación CREATE).
        """
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        data = registro_obj.to_dict()

        try:
            # Usamos la secuencia para obtener el ID: seq_registro_tiempo.NEXTVAL
            sql = """
                INSERT INTO REGISTRO_TIEMPO (ID_REGISTRO, ID_EMPLEADO, ID_PROYECTO, 
                                            FECHA_TRABAJO, HORAS_TRABAJADAS, DESCRIPCION_TAREAS)
                VALUES (seq_registro_tiempo.NEXTVAL, :id_empleado, :id_proyecto, 
                        :fecha_trabajo, :horas_trabajadas, :descripcion_tareas)
            """
            # Eliminamos id_registro y fecha_registro del diccionario 'data' si están presentes
            # para evitar pasarlos a la consulta INSERT que los genera automáticamente.
            params = {k: data[k] for k in data if k in ('id_empleado', 'id_proyecto',
                                                        'fecha_trabajo', 'horas_trabajadas',
                                                        'descripcion_tareas')}

            cursor.execute(sql, params)
            conn.commit()
            print(
                f"Registro de {data['horas_trabajadas']} horas creado exitosamente.")
            return True

        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(
                f"Error ORA-{error.code} al crear registro de tiempo: {error.message}")
            return False

        finally:
            cursor.close()
            conn.close()

    def get_registros_by_empleado(self, empleado_id: str) -> list[RegistroTiempo]:
        """
        Busca y retorna todos los registros de tiempo para un empleado específico (READ para informes).
        """
        conn = self.db.connect()
        if not conn:
            return []

        cursor = conn.cursor()
        registros = []

        try:
            # Consulta para traer los registros de un empleado
            sql = """
                SELECT ID_REGISTRO, ID_EMPLEADO, ID_PROYECTO, FECHA_TRABAJO, HORAS_TRABAJADAS, 
                       DESCRIPCION_TAREAS, FECHA_REGISTRO
                FROM REGISTRO_TIEMPO 
                WHERE ID_EMPLEADO = :id 
                ORDER BY FECHA_TRABAJO DESC
            """
            cursor.execute(sql, {'id': empleado_id})

            for row in cursor:
                # Mapeo de la fila de Oracle a objeto RegistroTiempo (POO)
                registros.append(RegistroTiempo(
                    id_registro=row[0],
                    id_empleado=row[1],
                    id_proyecto=row[2],
                    # oracledb mapea fechas de Oracle a objetos date/datetime de Python
                    fecha_trabajo=row[3],
                    horas_trabajadas=row[4],
                    descripcion_tareas=row[5],
                    fecha_registro=row[6]
                ))

            return registros

        except oracledb.Error as e:
            error, = e.args
            print(
                f"Error ORA-{error.code} al buscar registros: {error.message}")
            return []

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------
    # Funciones de consulta específicas para INFORMES (READ)
    # ----------------------------------------------------

    def get_total_horas_por_proyecto_en_rango(self, fecha_inicio: date, fecha_fin: date) -> list:
        """
        Consulta para obtener datos agregados (horas sumadas por proyecto) para el GeneradorInforme.
        Retorna una lista de tuplas o diccionarios con (ID_PROYECTO, SUMA_HORAS).
        """
        conn = self.db.connect()
        if not conn:
            return []

        cursor = conn.cursor()

        try:
            # Esta consulta SQL hace la agregación directamente en la DB, lo cual es más eficiente
            sql = """
                SELECT 
                    ID_PROYECTO, 
                    SUM(HORAS_TRABAJADAS) AS TOTAL_HORAS
                FROM 
                    REGISTRO_TIEMPO
                WHERE 
                    FECHA_TRABAJO BETWEEN :inicio AND :fin
                GROUP BY 
                    ID_PROYECTO
                ORDER BY 
                    TOTAL_HORAS DESC
            """

            cursor.execute(sql, {'inicio': fecha_inicio, 'fin': fecha_fin})

            # Retorna una lista de tuplas: [(id_proyecto, total_horas), ...]
            return cursor.fetchall()

        except oracledb.Error as e:
            error, = e.args
            print(
                f"Error ORA-{error.code} en consulta de informe: {error.message}")
            return []

        finally:
            cursor.close()
            conn.close()

    # Nota: Los métodos UPDATE y DELETE (por ID_REGISTRO) se omiten para brevedad,
    # pero seguirían la misma estructura que los del DepartamentoDAO.
