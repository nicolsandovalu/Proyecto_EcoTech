import oracledb
from src.datos.db_connector import DatabaseConnector
from ..dominio.indicador import Indicador
from datetime import datetime
from typing import Optional


class IndicadoresDAO:
    #Gestiona el registro de indicadores económicos en la BD Oracle.

    def __init__(self):
        self.db = DatabaseConnector()

    def registrar_indicador(self, indicador: Indicador, id_usuario: str, sitio_proveedor: str, nombre_a_guardar: str) -> bool:
        
        #Almacena el valor de un indicador consultado en la base de datos.

        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()

        try:
            sql = """
                INSERT INTO REGISTRO_INDICADOR (
                    ID_REGISTRO, NOMBRE_INDICADOR, VALOR, FECHA_VALOR, 
                   FECHA_CONSULTA, ID_EMPLEADO, SITIO_PROVEEDOR
                )
                VALUES (
                    seq_registro_indicador.NEXTVAL, :nombre, :valor, TO_DATE(:fecha_valor, 'YYYY-MM-DD'),
                    SYSDATE, :id_empleado_val, :sitio
                )
            """

            data = {
                'nombre': nombre_a_guardar,
                'valor': indicador.get_valor(),
                'fecha_valor': indicador.get_fecha_valor().strftime('%Y-%m-%d'),
                'id_empleado_val': id_usuario,
                'sitio': sitio_proveedor
            }

            cursor.execute(sql, data)
            conn.commit()
            print(
                f"LOG [IndicadoresDAO]: Registro de {nombre_a_guardar} completado en Oracle.")
            return True

        except oracledb.Error as e:
            conn.rollback()
            error, = e.args
            print(
                f"Error ORA-{error.code} al registrar indicador: {error.message}")
            return False

        finally:
            if cursor:
                cursor.close()

    def get_indicadores_by_range(self, tipo_indicador: str, fecha_inicio: date, fecha_fin: date) -> List[Indicador]:
        """
        Obtiene una lista de objetos Indicador registrados en la DB en un rango de fechas,
        para un tipo específico.
        """
        conn = None
        cursor = None
        try:
            conn = self.db.connect()
            if not conn:
                return []

            cursor = conn.cursor()

            sql = """
            SELECT NOMBRE_INDICADOR, VALOR, FECHA_VALOR, SITIO_PROVEEDOR
            FROM REGISTRO_INDICADOR
            WHERE NOMBRE_INDICADOR = :tipo_indicador 
            AND FECHA_VALOR >= TO_DATE(:inicio_str, 'YYYY-MM-DD') 
            AND FECHA_VALOR < TO_DATE(:fin_str, 'YYYY-MM-DD')
            ORDER BY FECHA_VALOR ASC
        """

            fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
            fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

            cursor.execute(sql,
                           tipo_indicador=tipo_indicador,
                           inicio_str=fecha_inicio_str,
                           fin_str=fecha_fin_str)

            resultados = cursor.fetchall()
            lista_indicadores = []
            for row in resultados:
                indicador = Indicador(
                    nombre=row[0],
                    valor=row[1],
                    fecha_valor=row[2],
                    sitio_proveedor=row[3],
                    unidad="Pesos"
                )
                lista_indicadores.append(indicador)

            return lista_indicadores

        except oracledb.Error as e:
            error, = e.args
            print(
                f"Error ORA-{error.code} al consultar historial: {error.message}")
            return []

        except Exception as e:
            print(
                f"Error inesperado al obtener indicadores por rango desde Oracle: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
