"""
departamento.py
"""
import oracledb
from typing import List, Optional


class Departamento:
    """
    Clase que representa un Departamento en el sistema
    Incluye operaciones CRUD integradas según requisitos de la evaluación
    """

    # Variable de clase para la conexión a la base de datos
    _connection = None

    @classmethod
    def set_connection(cls, connection):
        """
        Método de clase para establecer la conexión a la base de datos
        Args:
            connection: Conexión a Oracle
        """
        cls._connection = connection

    def __init__(self, id_departamento: int = None, nombre: str = "",
                 gerente_id: str = None, activo: bool = True):
        """
        Constructor de la clase Departamento
        Args:
            id_departamento: ID único del departamento (PK)
            nombre: Nombre del departamento
            gerente_id: ID del empleado que es gerente (FK)
            activo: Estado del departamento (activo/inactivo)
        """
        self._id_departamento = id_departamento
        self._nombre = nombre
        self._gerente_id = gerente_id
        self._activo = activo

    # GETTERS Y SETTERS
    @property
    def id_departamento(self) -> int:
        """Getter para ID del departamento"""
        return self._id_departamento

    @property
    def nombre(self) -> str:
        """Getter para nombre del departamento"""
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        """
        Setter para nombre del departamento con validación
        Args:
            value: Nuevo nombre del departamento
        Raises:
            ValueError: Si el nombre está vacío
        """
        if not value or not value.strip():
            raise ValueError("El nombre del departamento no puede estar vacío")
        self._nombre = value.strip()

    @property
    def gerente_id(self) -> Optional[str]:
        """Getter para ID del gerente"""
        return self._gerente_id

    @gerente_id.setter
    def gerente_id(self, value: Optional[str]):
        """Setter para ID del gerente"""
        self._gerente_id = value

    @property
    def activo(self) -> bool:
        """Getter para estado activo/inactivo"""
        return self._activo

    @activo.setter
    def activo(self, value: bool):
        """Setter para estado activo/inactivo"""
        self._activo = value

    # OPERACIONES CRUD - Implementadas directamente en la clase

    def crear(self) -> bool:
        """
        CREATE - Insertar nuevo departamento en la base de datos
        Returns:
            bool: True si se creó correctamente, False si hubo error
        """
        try:
            if self._connection is None:
                raise Exception("No hay conexión a la base de datos")

            with self._connection.cursor() as cursor:
                # Obtener el próximo ID de la secuencia
                cursor.execute("SELECT seq_departamento.NEXTVAL FROM DUAL")
                self._id_departamento = cursor.fetchone()[0]

                # SQL para insertar nuevo departamento
                sql = """
                INSERT INTO Departamento (id_departamento, nombre, gerente_id, activo, fecha_creacion)
                VALUES (:1, :2, :3, :4, SYSDATE)
                """

                # Ejecutar inserción con parámetros
                cursor.execute(sql, [
                    self._id_departamento,
                    self._nombre,
                    self._gerente_id,
                    1 if self._activo else 0
                ])

                # Confirmar transacción
                self._connection.commit()
                print(
                    f"Departamento '{self._nombre}' creado exitosamente con ID: {self._id_departamento}")
                return True

        except oracledb.Error as e:
            print(f"Error al crear departamento: {e}")
            if self._connection:
                self._connection.rollback()
            return False

    @classmethod
    def obtener_por_id(cls, id_departamento: int) -> Optional['Departamento']:
        """
        READ - Obtener un departamento por su ID
        Args:
            id_departamento: ID del departamento a buscar
        Returns:
            Optional[Departamento]: Objeto Departamento o None si no existe
        """
        try:
            if cls._connection is None:
                raise Exception("No hay conexión a la base de datos")

            with cls._connection.cursor() as cursor:
                # SQL para buscar departamento por ID
                sql = """
                SELECT id_departamento, nombre, gerente_id, activo
                FROM Departamento 
                WHERE id_departamento = :1
                """

                cursor.execute(sql, [id_departamento])
                resultado = cursor.fetchone()

                # Si se encontró el departamento, crear y retornar objeto
                if resultado:
                    return cls(
                        id_departamento=resultado[0],
                        nombre=resultado[1],
                        gerente_id=resultado[2],
                        activo=bool(resultado[3])
                    )
                return None

        except oracledb.Error as e:
            print(f"Error al obtener departamento: {e}")
            return None

    @classmethod
    def obtener_todos(cls, solo_activos: bool = True) -> List['Departamento']:
        """
        READ - Obtener todos los departamentos
        Args:
            solo_activos: Si True, solo retorna departamentos activos
        Returns:
            List[Departamento]: Lista de objetos Departamento
        """
        try:
            if cls._connection is None:
                raise Exception("No hay conexión a la base de datos")

            with cls._connection.cursor() as cursor:
                # Construir SQL según filtro de activos
                if solo_activos:
                    sql = "SELECT id_departamento, nombre, gerente_id, activo FROM Departamento WHERE activo = 1 ORDER BY nombre"
                else:
                    sql = "SELECT id_departamento, nombre, gerente_id, activo FROM Departamento ORDER BY nombre"

                cursor.execute(sql)
                resultados = cursor.fetchall()

                # Convertir cada fila en objeto Departamento
                departamentos = []
                for resultado in resultados:
                    departamentos.append(cls(
                        id_departamento=resultado[0],
                        nombre=resultado[1],
                        gerente_id=resultado[2],
                        activo=bool(resultado[3])
                    ))
                return departamentos

        except oracledb.Error as e:
            print(f"Error al obtener departamentos: {e}")
            return []

    def actualizar(self) -> bool:
        """
        UPDATE - Actualizar el departamento actual en la base de datos
        Returns:
            bool: True si se actualizó correctamente, False si hubo error
        """
        try:
            if self._connection is None:
                raise Exception("No hay conexión a la base de datos")

            with self._connection.cursor() as cursor:
                # SQL para actualizar departamento
                sql = """
                UPDATE Departamento 
                SET nombre = :1, gerente_id = :2, activo = :3
                WHERE id_departamento = :4
                """

                cursor.execute(sql, [
                    self._nombre,
                    self._gerente_id,
                    1 if self._activo else 0,
                    self._id_departamento
                ])

                self._connection.commit()
                exito = cursor.rowcount > 0
                if exito:
                    print(
                        f"Departamento '{self._nombre}' actualizado exitosamente")
                return exito

        except oracledb.Error as e:
            print(f"Error al actualizar departamento: {e}")
            if self._connection:
                self._connection.rollback()
            return False

    def eliminar(self) -> bool:
        """
        DELETE - Eliminar el departamento actual (eliminación lógica)
        Returns:
            bool: True si se eliminó correctamente, False si hubo error
        """
        try:
            if self._connection is None:
                raise Exception("No hay conexión a la base de datos")

            with self._connection.cursor() as cursor:
                # Verificar si el departamento tiene empleados asignados
                cursor.execute(
                    "SELECT COUNT(*) FROM Empleado WHERE id_departamento = :1",
                    [self._id_departamento]
                )
                count_empleados = cursor.fetchone()[0]

                # No permitir eliminar si hay empleados asignados
                if count_empleados > 0:
                    print(
                        "No se puede eliminar el departamento porque tiene empleados asignados")
                    return False

                # Eliminación lógica (cambiar estado a inactivo)
                sql = "UPDATE Departamento SET activo = 0 WHERE id_departamento = :1"
                cursor.execute(sql, [self._id_departamento])
                self._connection.commit()
                exito = cursor.rowcount > 0
                if exito:
                    print(
                        f"Departamento '{self._nombre}' eliminado exitosamente")
                return exito

        except oracledb.Error as e:
            print(f"Error al eliminar departamento: {e}")
            if self._connection:
                self._connection.rollback()
            return False

    @classmethod
    def buscar_por_nombre(cls, nombre: str) -> List['Departamento']:
        """
        Búsqueda de departamentos por nombre (búsqueda parcial)
        Args:
            nombre: Texto a buscar en los nombres de departamentos
        Returns:
            List[Departamento]: Lista de departamentos que coinciden con la búsqueda
        """
        try:
            if cls._connection is None:
                raise Exception("No hay conexión a la base de datos")

            with cls._connection.cursor() as cursor:
                # SQL para búsqueda parcial por nombre
                sql = """
                SELECT id_departamento, nombre, gerente_id, activo
                FROM Departamento 
                WHERE UPPER(nombre) LIKE UPPER(:1) AND activo = 1
                ORDER BY nombre
                """

                cursor.execute(sql, [f'%{nombre}%'])
                resultados = cursor.fetchall()

                # Convertir resultados a objetos Departamento
                departamentos = []
                for resultado in resultados:
                    departamentos.append(cls(
                        id_departamento=resultado[0],
                        nombre=resultado[1],
                        gerente_id=resultado[2],
                        activo=bool(resultado[3])
                    ))
                return departamentos

        except oracledb.Error as e:
            print(f"Error al buscar departamentos: {e}")
            return []

    def __str__(self):
        """Representación en string del departamento"""
        gerente_info = f" - Gerente: {self._gerente_id}" if self._gerente_id else " - Sin gerente"
        estado = "Activo" if self._activo else "Inactivo"
        return f"Departamento {self._id_departamento}: {self._nombre} ({estado}){gerente_info}"


# Ejemplo de uso básico para pruebas
if __name__ == "__main__":
    """
    Bloque principal para pruebas de la clase Departamento
    """
    # Ejemplo de creación de un departamento
    depto_prueba = Departamento(nombre="Recursos Humanos")
    print(f"Departamento de prueba creado: {depto_prueba}")

    # Nota: Para usar con base de datos, primero establecer conexión:
    # Departamento.set_connection(conexion_oracle)
    # depto_prueba.crear()  # Esto insertaría en la base de datos
