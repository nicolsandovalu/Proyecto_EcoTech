import oracledb
from ..dominio.proyecto import Proyecto
from .db_connector import DatabaseConnector
from datetime import date, datetime 
from typing import Optional

class ProyectoDAO:
    
    def __init__(self):
        self.db = DatabaseConnector()
    
    # --- MÉTODO: CREATE ---
    def create_proyecto(self, proyecto_obj: Proyecto) -> bool:
        """Inserta nuevo proyecto en BD (Operación CREATE)."""
        conn = self.db.connect()
        if not conn: return False
        
        cursor = conn.cursor()
        data = proyecto_obj.to_dict() 
        
        try:
            # Eliminación de claves generadas por Oracle (secuencia y SYSDATE)
            if 'id_proyecto' in data:
                del data['id_proyecto']
            if 'fecha_creacion' in data:
                del data['fecha_creacion']
                
            sql = """
                INSERT INTO PROYECTO (ID_PROYECTO, NOMBRE, DESCRIPCION, FECHA_INICIO, FECHA_CREACION)
                VALUES (seq_proyecto.NEXTVAL, :nombre, :descripcion, TO_DATE(:fecha_inicio, 'YYYY-MM-DD'), SYSDATE)
            """
            cursor.execute(sql, data)
            conn.commit()
            return True
        except oracledb.Error as e:
            conn.rollback()
            print(f"Error ORA-{e.args[0].code} al crear proyecto: {e.args[0].message}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    # --- MÉTODO: READ (BUSCAR POR ID) ---
    def get_proyecto_by_id(self, proyecto_id: int) -> Optional[Proyecto]:
        """Busca y retorna un proyecto por su ID."""
        conn = self.db.connect()
        if not conn: return None
        
        cursor = conn.cursor()
        
        try:
            sql = "SELECT ID_PROYECTO, NOMBRE, DESCRIPCION, FECHA_INICIO, FECHA_CREACION FROM PROYECTO WHERE ID_PROYECTO = :id"
            cursor.execute(sql, {'id': proyecto_id})
            fila = cursor.fetchone()
            
            if fila:
                # CORRECCIÓN: Convertir explícitamente a objeto date si es datetime, eliminando la hora (00:00:00)
                fecha_inicio_limpia = fila[3].date() if fila[3] and isinstance(fila[3], datetime) else fila[3]
                fecha_creacion_limpia = fila[4].date() if fila[4] and isinstance(fila[4], datetime) else fila[4]
                
                return Proyecto(
                    id_proyecto=fila[0],
                    nombre=fila[1],
                    descripcion=fila[2],
                    fecha_inicio=fecha_inicio_limpia, 
                    fecha_creacion=fecha_creacion_limpia
                )
            return None
        except oracledb.Error as e:
            print(f"Error ORA-{e.args[0].code} al buscar proyecto: {e.args[0].message}")
            return None
        finally:
            cursor.close()

    # --- MÉTODO: READ (LISTAR TODOS) ---
    def get_all_proyectos(self) -> list:
        """Obtiene todos los proyectos y los retorna como una lista de objetos Proyecto."""
        conn = self.db.connect()
        if not conn: return []
        
        cursor = conn.cursor()
        proyectos_list = []
        
        try:
            sql = "SELECT ID_PROYECTO, NOMBRE, DESCRIPCION, FECHA_INICIO, FECHA_CREACION FROM PROYECTO ORDER BY FECHA_CREACION DESC"
            cursor.execute(sql)
            
            for fila in cursor.fetchall():
                # CORRECCIÓN: Limpieza de fecha al listar
                fecha_inicio_limpia = fila[3].date() if fila[3] and isinstance(fila[3], datetime) else fila[3]
                fecha_creacion_limpia = fila[4].date() if fila[4] and isinstance(fila[4], datetime) else fila[4]

                proyectos_list.append(Proyecto(
                    id_proyecto=fila[0],
                    nombre=fila[1],
                    descripcion=fila[2],
                    fecha_inicio=fecha_inicio_limpia,
                    fecha_creacion=fecha_creacion_limpia
                ))
            return proyectos_list
        except oracledb.Error as e:
            print(f"Error ORA-{e.args[0].code} al obtener proyectos: {e.args[0].message}")
            return []
        finally:
            cursor.close()
            
    # --- MÉTODO: UPDATE (CORRECCIÓN FINAL DPY-1001) ---
    def update_proyecto(self, proyecto_obj: Proyecto) -> bool:
        
        conn = self.db.connect()
        if not conn: 
            return False

        cursor = conn.cursor()
        data = proyecto_obj.to_dict() 
        
        try:
           # CORRECCIÓN DPY-4008: Eliminar clave no usada en el UPDATE
            if 'fecha_creacion' in data:
                del data['fecha_creacion']

            # CORRECCIÓN DEFINITIVA: Convertir el valor de la fecha a string
            fecha_inicio_val = data['fecha_inicio']
            
            # Si no es una cadena (es un date/datetime object), lo formateamos a string 'YYYY-MM-DD'.
            if fecha_inicio_val and not isinstance(fecha_inicio_val, str):
                data['fecha_inicio'] = fecha_inicio_val.strftime('%Y-%m-%d')
                
            sql = """
                UPDATE PROYECTO
                SET NOMBRE = :nombre, 
                    DESCRIPCION = :descripcion,
                    FECHA_INICIO = TO_DATE(:fecha_inicio, 'YYYY-MM-DD')
                WHERE ID_PROYECTO = :id_proyecto
            """
            cursor.execute(sql, data)
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
            
        except oracledb.Error as e:
            conn.rollback()
            print(f"Error ORA-{e.args[0].code} al actualizar proyecto: {e.args[0].message}")
            return False
            
        finally:
            cursor.close()

    # --- MÉTODO: DELETE (NUEVO) ---
    def delete_proyecto(self, proyecto_id: int) -> bool:
        """Elimina un proyecto, incluyendo sus dependencias (Operación DELETE)."""
        conn = self.db.connect()
        if not conn: 
            return False

        cursor = conn.cursor()
        
        try:
            # 1. Eliminar entradas dependientes (Registro de Tiempo)
            cursor.execute("DELETE FROM REGISTRO_TIEMPO WHERE ID_PROYECTO = :id", {'id': proyecto_id})

            # 2. Eliminar entradas dependientes (Asignación a Proyectos)
            cursor.execute("DELETE FROM EMPLEADO_PROYECTO WHERE ID_PROYECTO = :id", {'id': proyecto_id})
            
            # 3. Eliminar el Proyecto
            cursor.execute("DELETE FROM PROYECTO WHERE ID_PROYECTO = :id", {'id': proyecto_id})
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
            
        except oracledb.Error as e:
            conn.rollback()
            print(f"Error ORA-{e.args[0].code} al eliminar proyecto: {e.args[0].message}")
            return False
            
        finally:
            cursor.close()
            
    # --- MÉTODOS: ASIGNACIÓN N:M ---
    def assign_empleado(self, id_proyecto: int, id_empleado: str) -> bool:
        """Asigna empleado a proyecto (Implementa la lógica N:M)."""
        conn = self.db.connect()
        if not conn: return False

        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO EMPLEADO_PROYECTO (ID_EMPLEADO, ID_PROYECTO) VALUES (:emp_id, :proj_id)", [id_empleado, id_proyecto])
            conn.commit()
            return True
        except oracledb.IntegrityError:
            return True
        except oracledb.Error as e:
            conn.rollback()
            print(f"Error ORA-{e.args[0].code} al asignar empleado: {e.args[0].message}")
            return False
        
        finally:
                cursor.close()