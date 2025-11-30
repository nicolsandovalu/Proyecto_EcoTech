import cx_Oracle
from proyecto import Proyecto

class ProyectoDAO:
    def __init__(self, connection):
        self.connection = connection
    
    def crear(self, proyecto: Proyecto) -> bool:
        """Inserta nuevo proyecto en BD"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO proyecto (id_proyecto, nombre, descripcion, fecha_inicio, fecha_creacion)
                    VALUES (:1, :2, :3, :4, :5)
                """, [proyecto.id_proyecto, proyecto.nombre, proyecto.descripcion, 
                      proyecto.fecha_inicio, proyecto.fecha_creacion])
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Error crear proyecto: {e}")
            return False
    
    def obtener_por_id(self, id_proyecto: int) -> Proyecto:
        """Obtiene proyecto por ID"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM proyecto WHERE id_proyecto = :1", [id_proyecto])
                fila = cursor.fetchone()
                return Proyecto(fila[0], fila[1], fila[2], fila[3], fila[4]) if fila else None
        except Exception as e:
            print(f"Error obtener proyecto: {e}")
            return None
    
    def obtener_todos(self) -> list:
        """Obtiene todos los proyectos"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM proyecto ORDER BY fecha_creacion DESC")
                return [Proyecto(fila[0], fila[1], fila[2], fila[3], fila[4]) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error obtener proyectos: {e}")
            return []
    
    def actualizar(self, proyecto: Proyecto) -> bool:
        """Actualiza proyecto existente"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE proyecto SET nombre = :1, descripcion = :2, fecha_inicio = :3 
                    WHERE id_proyecto = :4
                """, [proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.id_proyecto])
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Error actualizar proyecto: {e}")
            return False
    
    def eliminar(self, id_proyecto: int) -> bool:
        """Elimina proyecto por ID"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM empleado_proyecto WHERE id_proyecto = :1", [id_proyecto])
                cursor.execute("DELETE FROM proyecto WHERE id_proyecto = :1", [id_proyecto])
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Error eliminar proyecto: {e}")
            return False
    
    def asignar_empleado(self, id_proyecto: int, id_empleado: str) -> bool:
        """Asigna empleado a proyecto"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO empleado_proyecto VALUES (:1, :2)", [id_empleado, id_proyecto])
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Error asignar empleado: {e}")
            return False