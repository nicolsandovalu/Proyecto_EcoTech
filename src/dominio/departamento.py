class Departamento:


    def __init__(self, id_departamento: int = None, nombre: str = None,
                 gerente_id: str = None, activo: bool = True, fecha_creacion=None): # <-- Sincronizado a gerente_id
        
        # Atributos de persistencia
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente_id = gerente_id 
        self.activo = activo 
        self.fecha_creacion = fecha_creacion

    def __str__(self):
        """Representación amigable del objeto."""
        estado = "Activo" if self.activo else "Inactivo"
        return f"Departamento ID: {self.id_departamento} | Nombre: {self.nombre} | Gerente ID: {self.gerente_id} | Estado: {estado}"

    def to_dict(self):

        return {
            'id_departamento': self.id_departamento,
            'nombre': self.nombre,
            'gerente_id': self.gerente_id, # <-- KEY DE BINDING CORRECTA
            'activo': 1 if self.activo else 0
        }

    def desactivar(self):
        """Marca el departamento como inactivo (Soft Delete)."""
        self.activo = False

    def validar_nombre(self) -> bool:
        """Verifica que el nombre tenga una longitud válida antes de la persistencia."""
        if self.nombre is None: 
            return False
        return 3 <= len(self.nombre) <= 50