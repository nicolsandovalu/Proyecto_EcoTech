# src/datos/indicadores_dao.py

import oracledb
from src.datos.db_connector import DatabaseConnector
# Asumimos que el modelo Indicador se importará desde el dominio
# Importación necesaria para el tipado/modelo
from ..dominio.indicador import Indicador
from datetime import datetime
from typing import Optional


class IndicadoresDAO:
    """Gestiona el registro de indicadores económicos en la BD Oracle."""

    def __init__(self):
        # CONSTRUCTOR SIMPLE: La inicialización se realiza aquí.
        # Si hay un error, el 'db_connector.py' debe lanzar la excepción.
        self.db = DatabaseConnector()

    def registrar_indicador(self, indicador: Indicador, id_usuario: str, sitio_proveedor: str) -> bool:
        """
        Almacena el valor de un indicador consultado en la base de datos.
        """
        # La conexión se intenta aquí. Si falla, 'conn' será None y retornará False.
        conn = self.db.connect()
        if not conn:
            return False

        cursor = conn.cursor()

        # Requisitos de registro:
        # - Nombre del indicador (ej: UF, Dolar Observado)
        # - Fecha en que registra el valor (fecha_valor)
        # - Fecha en que el usuario realiza la consulta (fecha_consulta, que es hoy)
        # - Usuario que la realiza (id_usuario)
        # - Sitio que provee los indicadores (sitio_proveedor)

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

            # Mapeo de datos del objeto Indicador y datos adicionales
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
