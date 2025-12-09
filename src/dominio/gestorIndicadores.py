# src/dominio/gestor_indicadores.py (Versión Completa y Corregida)

from src.datos.indicador_api import IndicadoresAPI
from src.datos.indicadores_dao import IndicadoresDAO
from src.dominio.indicador import Indicador
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List


class GestorIndicadores:
    """
    Gestiona la lógica de negocio para la consulta, validación y registro de indicadores.
    """

    def __init__(self):
        self.api_data = IndicadoresAPI()
        self.dao_oracle = IndicadoresDAO()
        self.sitio_proveedor = "mindicador.cl"

    def _deserializar_y_validar_data(self, tipo: str, data_cruda: Dict[str, Any], fecha_consulta_usuario: Optional[str]) -> Optional[Indicador]:
        """
        Procesa el JSON de la API, valida los datos y retorna un objeto Indicador.
        Aplica la lógica de búsqueda de fecha exacta/mensual y valida solo la positividad de UF/UTM.
        """
        if not data_cruda:
            return None

        try:
            nombre = data_cruda.get("nombre", tipo.upper())
            unidad = data_cruda.get("unidad_medida", "")
            item_encontrado = None

            # Indicadores que tienen valores mensuales (generalmente al día 1)
            indicadores_mensuales = ["ipc", "utm", "ivp"]
            # Indicadores que deben ser estrictamente positivos (unidades de valor)
            indicadores_positivos_estrictos = ['uf', 'utm']

            if "serie" in data_cruda and data_cruda["serie"]:

                if fecha_consulta_usuario:
                    fecha_buscada = fecha_consulta_usuario

                    # 1. Intentamos buscar el día exacto ingresado
                    for item in data_cruda["serie"]:
                        if item.get("fecha", "")[:10] == fecha_buscada:
                            item_encontrado = item
                            break

                    # 2. Búsqueda Tolerante (solo para indicadores mensuales)
                    if not item_encontrado and tipo in indicadores_mensuales:
                        try:
                            fecha_obj = datetime.strptime(
                                fecha_buscada, '%Y-%m-%d')
                            fecha_primer_dia_mes = fecha_obj.strftime(
                                '%Y-%m-01')

                            for item in data_cruda["serie"]:
                                if item.get("fecha", "")[:10] == fecha_primer_dia_mes:
                                    item_encontrado = item

                                    # <<< NOTIFICACIÓN DE BÚSQUEDA MENSUAL >>>
                                    print(
                                        f"    🔔 Nota: El valor para {tipo.upper()} se registra al 1ro del mes. Usando valor de: {fecha_primer_dia_mes}")

                                    break
                        except ValueError:
                            pass  # Ignorar si la fecha no se puede parsear

                # 3. Si sigue sin encontrar (o si no se pasó fecha), tomamos el primer elemento (más reciente/cercano)
                if not item_encontrado:
                    item_encontrado = data_cruda["serie"][0]

            # Caso especial para valores directos (si se consulta el actual sin serie)
            elif "valor" in data_cruda:
                valor = data_cruda["valor"]
                fecha_valor_str = datetime.today().strftime('%Y-%m-%d')

            else:
                raise ValueError(
                    "Estructura de datos de API no reconocida o vacía.")

            # Si el item_encontrado fue definido, extraemos los datos de él
            if item_encontrado:
                valor = item_encontrado["valor"]
                fecha_valor_str = item_encontrado["fecha"][:10]

            # --- VALIDACIÓN FINAL (CORRECCIÓN OBTENIDA) ---
            # 1. Asegurar que sea numérico
            if not isinstance(valor, (int, float)):
                print(
                    f"ERROR DE VALIDACIÓN: Valor '{valor}' del indicador {tipo.upper()} no es numérico.")
                return None

            # 2. Asegurar positividad solo para UF y UTM (ya que IPC puede ser negativo)
            if valor <= 0 and tipo in indicadores_positivos_estrictos:
                print(
                    f"ERROR DE VALIDACIÓN: Valor '{valor}' del indicador {tipo.upper()} no puede ser cero o negativo.")
                return None

            fecha_valor = datetime.strptime(fecha_valor_str, '%Y-%m-%d').date()

            return Indicador(
                codigo=tipo,
                nombre=nombre,
                valor=float(valor),
                fecha_valor=fecha_valor,
                unidad=unidad,
                sitio_proveedor=self.sitio_proveedor
            )

        except ValueError as ve:
            print(f"ERROR DE DESERIALIZACIÓN/FECHA para {tipo}: {ve}")
            return None
        except Exception as e:
            print(f"ERROR INESPERADO al procesar data de {tipo}: {e}")
            return None

    def obtener_y_registrar_indicador(self, tipo: str, fecha: Optional[str], id_usuario_registro: str, registrar: bool = False) -> Optional[Indicador]:
        """
        1. Consulta la API. 2. Deserializa/Valida. 3. (Opcional) Registra en Oracle.
        """

        # 1. CONSULTA A LA API (Capa de Datos: indicadores_api.py)
        data_cruda = self.api_data.consultar_indicador(tipo, fecha)

        # 2. PROCESAMIENTO Y VALIDACIÓN (Capa de Dominio)
        # Se pasa la fecha para que la deserialización busque el día exacto
        indicador_obj = self._deserializar_y_validar_data(
            tipo, data_cruda, fecha)

        if indicador_obj and registrar:
            # 3. REGISTRO EN ORACLE (Capa de Datos: indicadores_dao.py)
            success = self.dao_oracle.registrar_indicador(
                indicador=indicador_obj,
                id_usuario=id_usuario_registro,  # Pasa el ID del empleado
                sitio_proveedor=self.sitio_proveedor
            )
            if not success:
                print(f"Advertencia: Falló el registro de {tipo} en la BD.")

        return indicador_obj

    def obtener_serie_por_rango(self, tipo: str, fecha_inicio: str, fecha_fin: str) -> List[Indicador]:
        """
        Consulta la API, iterando día a día en el rango, y devuelve una lista de objetos Indicador.
        """
        valores_serie = []
        try:
            start = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            end = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except ValueError:
            print("ERROR: Formato de fecha de rango incorrecto. Use YYYY-MM-DD.")
            return []

        current_date = start

        # Iterar sobre las fechas del rango
        while current_date <= end:
            fecha_str = current_date.strftime('%Y-%m-%d')

            # Usar el método existente de día único (que maneja las restricciones de la API)
            # Pasamos un ID temporal ya que solo estamos obteniendo datos, no registrando.
            indicador_obj = self.obtener_y_registrar_indicador(
                tipo=tipo, fecha=fecha_str, id_usuario_registro='TEMP', registrar=False
            )

            # Solo agregar si el valor corresponde al día consultado
            if indicador_obj and indicador_obj.get_fecha_valor().strftime('%Y-%m-%d') == fecha_str:
                valores_serie.append(indicador_obj)

            # Mover al siguiente día
            current_date = current_date + timedelta(days=1)

        return valores_serie
