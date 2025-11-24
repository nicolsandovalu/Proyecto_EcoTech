class Cargo:
    
    def __init__(self, id_cargo: str, nombre: str):
        self._id = id_cargo
        self._nombre = nombre
    
    def to_dict(self):
        return {'id_cargo': self._id, 'nombre': self._nombre}