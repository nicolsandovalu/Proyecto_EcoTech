from typing import List 

class Empleado:
    
    def __init__(self, id_empleado: str, nombre: str, email: str, salario: float,
                 id_departamento: int = None, id_cargo: str = None,
                 direccion: str = None, telefono: str = None,
                 fecha_inicio_contrato: str = None):
        
        #Atributos persistidos (Cargados desde la BD)
        self._id = id_empleado
        self._nombre = nombre
        self._email = email
        self._salario = salario 
        self._id_departamento = id_departamento
        self._id_cargo = id_cargo 
        self._direccion = direccion
        self._telefono = telefono 
        self._fecha_inicio_contrato = fecha_inicio_contrato
        
        #almacena los objetos Proyectos a los que está asignado
        self._proyectos_asignados: List = []
        
    def get_id(self) -> str:
        return self._id
    
    def get_nombre(self) -> str:
        return self._nombre
    
    def get_salario(self) -> float:
        return self._salario
    
    #método de negocio (requisitos del sistema)
    
    def asignar_departamento(self, nuevo_id_departamento: int):
        #permite reasignación de empleado a un depto. diferente
        
        #asigna empleado a un proyecto
        self._id_departamento = nuevo_id_departamento
        print(f"Empleado {self._nombre} reasignado al Dpto ID: {nuevo_id_departamento}")
        
    def desasignar_proyecto(self, proyecto_obj):
        #desasigna al empleado 
        if proyecto_obj in self._proyectos_asignados:
            self._proyectos_asignados.remove(proyecto_obj)
            return True
        return False
    
    def to_dict(self) -> dict:
        #convierte el objeto empelado a un diccionario para su uso en la capa de datos o UI
        
        return {
            'id_empleado': self._id,
            'nombre': self._nombre,
            'email': self._email,
            'salario': self._salario,
            'id_departamento': self._id_departamento,
            'id_cargo': self._id_cargo,
            'direccion': self._direccion,
            'telefono': self._telefono,
            'fecha_inicio_contrato': self._fecha_inicio_contrato
        }
        
    def __str__(self):
        return f"Empleado ID: {self._id} | Nombre: {self._nombre} | Salario: {self._salario}"