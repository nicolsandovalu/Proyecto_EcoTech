# Archivo: src/dominio/departamento.py

class Departamento:
    """
    Clase que representa la entidad Departamento dentro del sistema EcoTech Solutions.
    Corresponde al modelo de dominio (POO).
    """

    def __init__(self, id_departamento: int = None, nombre: str = None,
                gerente_id: str = None, activo: bool = True, fecha_creacion=None):

        # Atributos de persistencia
        # PK, puede ser None al crear (usando secuencia)
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente_id = gerente_id            # FK a Empleado (Gerente)
        self.activo = activo   # Para Soft Delete (True/False)
        self.fecha_creacion = fecha_creacion

        # Notas: Se puede agregar la fecha_creacion si es necesaria en el objeto.

    def __str__(self):
        """Representación amigable del objeto."""
        estado = "Activo" if self.activo else "Inactivo"
        return f"Departamento ID: {self.id_departamento} | Nombre: {self.nombre} | Gerente ID: {self.gerente_id} | Estado: {estado}"

    def to_dict(self):
        """
        Convierte el objeto Departamento a un diccionario compatible con las consultas SQL
        del DepartamentoDAO.
        """
        return {
            'id_departamento': self.id_departamento,
            'nombre': self.nombre,
            'gerente_id': self.gerente_id,
            # El DAO espera un valor numérico (0 o 1) para el campo ACTIVO en Oracle
            'activo': 1 if self.activo else 0
        }

    # =============================
    # Métodos de Negocio (Ejemplo)
    # =============================

    def desactivar(self):
        """Marca el departamento como inactivo (Soft Delete)."""
        self.activo = False

    def validar_nombre(self) -> bool:
        """Verifica que el nombre tenga una longitud válida antes de la persistencia."""
        if self.nombre is None: 
            return False
        return 3 <= len(self.nombre) <= 50
