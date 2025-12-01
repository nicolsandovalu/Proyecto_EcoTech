# # Archivo: src/servicio/gestion_usuarios_servicio.py

# import bcrypt
# from datetime import date  # Importamos por si los datos del empleado incluyen fechas

# # Importaciones de la capa DAO (DEBEN existir en src/dao/)
# from ..dao.rol_dao import RolDAO
# from ..dao.empleado_dao import EmpleadoDAO
# from ..dao.usuario_dao import UsuarioDAO

# # Importaciones de la capa de Dominio (DEBEN existir en src/dominio/)
# from ..dominio.empleado import Empleado
# # Asumimos que tiene un modelo Usuario con __init__(nombre_usuario, contrasena, id_rol)
# from ..dominio.usuario import Usuario


# class GestionUsuariosServicio:
#     """
#     Clase que encapsula la lógica de negocio para la gestión de usuarios y empleados.
#     Orquesta la creación de Empleado y su correspondiente registro de Usuario.
#     """

#     def __init__(self):
#         # Inicialización de todos los DAOs que esta clase de servicio va a utilizar
#         self.rol_dao = RolDAO()
#         self.empleado_dao = EmpleadoDAO()
#         self.usuario_dao = UsuarioDAO()

#     def crear_usuario_empleado(self, datos_empleado: dict, contrasena: str) -> bool:
#         """
#         Crea el registro de un nuevo empleado y su registro de login asociado (Usuario).
#         Requiere una transacción de dos pasos.
#         """

#         # 1. Obtener el objeto Rol 'EMPLEADO' del DAO
#         rol_empleado_obj = self.rol_dao.get_rol_by_name("EMPLEADO")

#         if not rol_empleado_obj:
#             print("ERROR FATAL: El rol 'EMPLEADO' no se encontró en la base de datos.")
#             return False

#         id_rol_empleado = rol_empleado_obj.get_id()
#         empleado_id = datos_empleado.get('id_empleado')

#         if not empleado_id:
#             print("Error: El ID del empleado es obligatorio.")
#             return False

#         # -----------------------------------------------
#         # PASO 2: Crear el objeto Empleado (Modelo)
#         # -----------------------------------------------
#         try:
#             nuevo_empleado = Empleado(
#                 id_empleado=empleado_id,
#                 nombre=datos_empleado['nombre'],
#                 email=datos_empleado['email'],
#                 salario=datos_empleado.get('salario', 0.0),
#                 id_departamento=datos_empleado.get('id_departamento'),
#                 id_cargo=datos_empleado.get('id_cargo'),
#                 # Otros campos del modelo Empleado deben ser pasados aquí...
#             )
#         except KeyError as e:
#             print(
#                 f"Error de datos: Falta un campo obligatorio en datos_empleado: {e}")
#             return False

#         # -----------------------------------------------
#         # PASO 3: Persistir el Empleado (Tabla EMPLEADO)
#         # -----------------------------------------------
#         # **Requiere que EmpleadoDAO tenga el método create_empleado**
#         if not self.empleado_dao.create_empleado(nuevo_empleado):
#             print("❌ Error: Fallo al persistir el registro del empleado.")
#             return False

#         # -----------------------------------------------
#         # PASO 4: Hashear Contraseña (Seguridad)
#         # -----------------------------------------------
#         hashed_password = bcrypt.hashpw(
#             contrasena.encode('utf-8'), bcrypt.gensalt())

#         # -----------------------------------------------
#         # PASO 5: Crear el objeto Usuario y Persistir (Tabla USUARIO)
#         # -----------------------------------------------
#         # Usamos el ID del empleado como nombre de usuario para el login
#         nuevo_usuario = Usuario(
#             nombre_usuario=empleado_id,
#             contrasena=hashed_password.decode('utf-8'),
#             id_rol=id_rol_empleado
#         )

#         # **Requiere que UsuarioDAO tenga el método create_usuario**
#         if not self.usuario_dao.create_usuario(nuevo_usuario):
#             # Lógica de rollback: En una aplicación real, si el usuario falla,
#             # DEBERÍAMOS ELIMINAR al empleado creado en el Paso 3.
#             print(
#                 "❌ Error: Fallo al crear el registro de USUARIO. Debería eliminar el empleado creado.")
#             return False

#         print(
#             f"✅ Éxito: Empleado '{nuevo_empleado.get_nombre()}' creado y usuario asignado con rol '{rol_empleado_obj.get_nombre()}'.")
#         return True
