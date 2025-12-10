# src/datos/indicadores_api.py

import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any, List


class IndicadoresAPI:
    """Clase para la conexión y consulta de la API externa de indicadores."""

    def __init__(self):
        self.base_url = "https://mindicador.cl/api"

    def consultar_indicador(self, tipo: str, fecha: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Consulta un indicador económico por tipo y fecha.
        Utiliza la consulta por año para IVP, IPC, UTM, o por día para otros.
        Retorna el diccionario JSON deserializado de la API.
        """

        # Indicadores que NO soportan consulta diaria (DD-MM-YYYY) pero SÍ por año (YYYY)
        indicadores_sin_historial_diario = ["ipc", "utm", "ivp"]
        url = f"{self.base_url}/{tipo}"

        if fecha:
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                fecha_str_api = fecha_obj.strftime("%d-%m-%Y")
                year_str = str(fecha_obj.year)

                if tipo in indicadores_sin_historial_diario:

                    url = f"{self.base_url}/{tipo}/{year_str}"
                    print(
                        f"Consultando {tipo} por año: {year_str}")
                else:
                    # Estrategia 2: Consulta por FECHA diaria (para UF, Dolar, Euro)
                    url = f"{self.base_url}/{tipo}/{fecha_str_api}"
                    print(
                        f"Consultando {tipo} por fecha: {fecha_str_api}")

            except ValueError:
                print(
                    f"Formato de fecha incorrecto para {tipo}. Use YYYY-MM-DD.")
                return None
        else:
            print(
                f"Consultando {tipo} actual (sin fecha).")
            # URL ya está como /api/{tipo} para el valor actual

        try:
            # 1. Acceso a la fuente externa
            # <<< CORRECCIÓN: AUMENTAR TIMEOUT >>>
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Lanza excepción para códigos 4xx/5xx

            # 2. Deserialización JSON
            data = response.json()

            # <<< VERIFICACIÓN DE SERIE VACÍA >>>
            if 'serie' in data and not data['serie']:
                print(
                    f"Advertencia: No se encontró valor para {tipo} en la fecha solicitada.")
                return None
            # <<< FIN VERIFICACIÓN >>>

            return data

        except requests.exceptions.HTTPError as http_err:
            print(
                f"Error HTTP ({response.status_code}) al consultar {tipo} en {url}: {http_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Error de conexión de red: {req_err}")
            return None
        except Exception as e:
            print(
                f"Error inesperado durante la consulta: {e}")
            return None
