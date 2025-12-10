# src/datos/indicadores_dao.py

import oracledb
from src.datos.db_connector import DatabaseConnector
from ..dominio.indicador import Indicador
from datetime import datetime
from typing import Optional


class IndicadoresDAO:
    """Gestiona el registro de indicadores económicos en la BD Oracle."""

    def __init__(self):
        self.db = DatabaseConnector()

    def registrar_indicador(self, indicador: Indicador, id_usuario: str, sitio_proveedor: str) -> bool:
        """
        Almacena el valor de un indicador consultado en la base de datos.
        """

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
                'nombre': indicador.get_nombre(),
                'valor': indicador.get_valor(),
                # Aseguramos que la fecha_valor sea string en 'YYYY-MM-DD' para TO_DATE
                'fecha_valor': indicador.get_fecha_valor().strftime('%Y-%m-%d'),
                'id_empleado_val': id_usuario,
                'sitio': sitio_proveedor
            }

            cursor.execute(sql, data)
            conn.commit()
            print(
                f"LOG [IndicadoresDAO]: Registro de {indicador.get_nombre()} completado en Oracle.")
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
