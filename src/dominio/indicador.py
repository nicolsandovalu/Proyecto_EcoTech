# src/dominio/indicador.py

from datetime import date
from typing import Optional


class Indicador:
    """Modelo de datos para un indicador económico, usado por la Capa de Dominio."""

    def __init__(self, nombre: str, valor: float, fecha_valor: date, unidad: str,
                 codigo: str = None, sitio_proveedor: str = "mindicador.cl"):

        self._nombre = nombre
        self._valor = valor
        self._fecha_valor = fecha_valor
        self._unidad = unidad
        self._codigo = codigo  # Ej: 'uf', 'dolar'
        self._sitio_proveedor = sitio_proveedor

    # --- GETTERS ---

    def get_nombre(self) -> str:
        return self._nombre

    def get_valor(self) -> float:
        return self._valor

    def get_fecha_valor(self) -> date:
        return self._fecha_valor

    def get_unidad(self) -> str:
        return self._unidad

    def get_sitio_proveedor(self) -> str:
        return self._sitio_proveedor

    # --- MÉTODO PARA EL DAO ---

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario para el uso en la Capa de Datos."""
        return {
            'nombre': self._nombre,
            'valor': self._valor,
            'fecha_valor': self._fecha_valor.strftime('%Y-%m-%d'),
            'unidad': self._unidad,
            'codigo': self._codigo,
            'sitio_proveedor': self._sitio_proveedor
        }

    def __str__(self):
        return f"{self._nombre} ({self._fecha_valor.strftime('%Y-%m-%d')}): {self._valor} {self._unidad}"
