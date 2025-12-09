import sys
from src.datos.db_connector import DatabaseConnector
from src.datos.empleado_dao import EmpleadoDAO
from src.datos.proyecto_dao import ProyectoDAO
from src.datos.departamento_dao import DepartamentoDAO
from src.datos.registroTiempo_dao import RegistroTiempoDAO
from src.dominio.informe import GeneradorInforme
from src.datos.usuario_dao import UsuarioDAO
from src.dominio.empleado import Empleado
from src.dominio.usuario import Usuario
from src.dominio.proyecto import Proyecto
from src.dominio.departamento import Departamento
from src.dominio.registroTiempo import RegistroTiempo
from src.datos.rol_dao import RolDAO
from src.dominio.rol import Rol
from datetime import datetime, timedelta
from datetime import date, datetime
import getpass
from typing import Optional
from src.dominio.gestorIndicadores import GestorIndicadores


def display_menu(user_info):
    # Muestra el menú principal basado en el rol del usuario.
    print("\n=============================================")
    print(
        f"Bienvenido, {user_info['nombre']}! | Rol ID: {user_info['id_rol']}")
    print("=============================================")

    if user_info['id_rol'] == 99:
        print("1. [ADMIN] Gestión de Empleados")
        print("2. [ADMIN] Gestión de Proyectos")
        print("3. [ADMIN] Gestión de Departamentos")
        print("4. [ADMIN] Generar Informes")
        print("5. [ADMIN] Gestión de Roles")

    print("6. Registrar horas trabajadas")
    print("7. Consultar y Registrar Indicadores Económicos")
    print("9. Cerrar sesión")
    print("0. Salir del sistema")
    return input("Seleccione una opción: ")

# Empleado


def menu_empleado_admin():
    print("\n--- GESTIÓN DE EMPLEADOS ---")
    print("1. Registrar Nuevo Empleado (Create)")
    print("2. Listar Todos los Empleados (Read)")
    print("3. Modificar Empleado (Update)")
    print("4. Eliminar Empleado (Delete)")
    print("5. Asignar Proyecto a Empleado (N:M)")
    print("6. Desasignar Proyecto a Empleado (N:M)")
    print("7. Volver al Menú Principal")
    return input("Seleccione una opción: ")


def register_new_employee():
    print("\n ---REGISTRO DE NUEVO EMPLEADO ---")
    dao = EmpleadoDAO()
    usuario_dao = UsuarioDAO()

    try:
        data = {
            'id_empleado': input("ID Empleado (ej: E001): "),
            'nombre': input("Nombre: "),
            'email': input("Email: "),
            'salario': float(input("Salario: ")),
            'id_departamento': int(input("ID Departamento (ej: 100): ")),
            'id_cargo': input("ID Cargo (DEV, HR_MGR, VENTAS, GERENTE, FIN_ANA): "),
            'direccion': input("Dirección: "),
            'telefono': input("Teléfono: "),
            'fecha_inicio_contrato': input("Fecha Inicio (YYYY-MM-DD): ")
        }

        contrasena_plana = getpass.getpass("Contraseña inicial: ")

        # Crear objeto Empleaado y Persistir
        nuevo_empleado = Empleado(**data)

        if not dao.create_empleado(nuevo_empleado):
            print("FALLO AL REGISTRAR EMPLEADO (Verifique FKs y Conexión).")
            return

        # Crear objeto usuario
        nuevo_usuario = Usuario(
            id_usuario=data['id_empleado'],
            nombre_usuario=data['id_empleado'],
            contrasena_hash="",
            id_rol=10,
            id_empleado=data['id_empleado']
        )

        if usuario_dao.create_usuario(nuevo_usuario, contrasena_plana):
            print("EMPLEADO Y USUARIO REGISTRADOS CON ÉXITO.")
        else:
            print("FALLO AL REGISTRAR USUARIO")
            dao.delete_empleado(data['id_empleado'])  # rollbackmanual

    except ValueError:
        print("Error de tipo: El salario y el ID de departamento deben ser números o la fecha no tiene el formato YYYY-MM-DD")
    except Exception as es:
        print(f"Error en la entrada de datos: {e}")


def list_all_employees():
    dao = EmpleadoDAO()
    empleados = dao.get_all_empleados()

    if empleados:
        print("\n--- LISTADO DE EMPLEADOS ---")
        for emp in empleados:
            print(f"ID: {emp.get_id():<5}  | Nombre: {emp.get_nombre():<20} | Depto ID: {emp.get_id_departamento()}  | Salario: {emp.get_salario():.2f}")
    else:
        print("No hay empleados registrados o la conexión falló.")


def update_empleado_console():
    print("\n--- MODIFICAR EMPLEADO ---")
    dao = EmpleadoDAO()

    empleado_id = input("Ingrese el ID del Empleado a modificar: ")
    empleado_obj = dao.get_empleado_by_id(empleado_id)

    if not empleado_obj:
        print(f"Error: Empleado ID '{empleado_id}' no encontrado.")
        return

    print(f"\nModificando: {empleado_obj.get_nombre()}")
    print("Presione Enter para mantener el valor actual.")

    try:
        # 1. Recopilar nuevos datos (actualizando el objeto existente)

        nuevo_nombre = input(f"Nombre (Actual: {empleado_obj.get_nombre()}): ")
        if nuevo_nombre:
            empleado_obj._nombre = nuevo_nombre

        nuevo_email = input(f"Email (Actual: {empleado_obj._email}): ")
        if nuevo_email:
            empleado_obj._email = nuevo_email

        nuevo_salario_str = input(
            f"Salario (Actual: {empleado_obj.get_salario():.2f}): ")
        if nuevo_salario_str:
            empleado_obj._salario = float(nuevo_salario_str)

        nueva_direccion = input(
            f"Dirección (Actual: {empleado_obj._direccion}): ")
        if nueva_direccion:
            empleado_obj._direccion = nueva_direccion

        nuevo_telefono = input(
            f"Teléfono (Actual: {empleado_obj._telefono}): ")
        if nuevo_telefono:
            empleado_obj._telefono = nuevo_telefono

        nuevo_id_cargo = input(
            f"ID Cargo (Actual: {empleado_obj._id_cargo}): ")
        if nuevo_id_cargo:
            empleado_obj._id_cargo = nuevo_id_cargo

        nuevo_id_depto_str = input(
            f"ID Departamento (Actual: {empleado_obj.get_id_departamento()}): ")
        if nuevo_id_depto_str:
            empleado_obj._id_departamento = int(nuevo_id_depto_str)

        nueva_fecha_str = input(
            f"Fecha Inicio (YYYY-MM-DD) (Actual: {empleado_obj._fecha_inicio_contrato}): ")
        if nueva_fecha_str:
            empleado_obj._fecha_inicio_contrato = nueva_fecha_str

        # 2. Llamar al DAO para persistir los cambios
        if dao.update_empleado(empleado_obj):
            print(f"ÉXITO: Empleado {empleado_id} modificado correctamente.")
        else:
            print("FALLO: No se pudo modificar el empleado en la base de datos.")

    except ValueError:
        print("Error de tipo: El salario, el ID de departamento deben ser números o la fecha no tiene el formato correcto.")
    except Exception as e:
        print(f"Error inesperado durante la modificación: {e}")


def assign_project_console():
    print("\n--- ASIGNACIÓN DE EMPLEADO A PROYECTO ---")
    empleado_id = input("Ingrese el ID del Empleado a asignar: ")
    proyecto_id_str = input("Ingrese el ID del proyecto (ej:1000): ")

    try:
        proyecto_id = int(proyecto_id_str)
    except ValueError:
        print("Error: El ID del proyecto debe ser un número entero.")
        return

    dao_emp = EmpleadoDAO()

    if dao_emp.assign_empleado_to_proyecto(empleado_id, proyecto_id):
        print(
            f"ÉXITO: Empleado {empleado_id} asignado al Proyecto {proyecto_id}.")
    else:
        print("ERROR: La asignación falló (Verifique IDs o conexión)")


def deassign_empleado_from_proyecto():
    print("\n--- DESASIGNACIÓN DE EMPLEADO A PROYECTO ---")
    empleado_id = input("Ingrese el ID del Empleado a desasignar: ")
    proyecto_id = input("Ingrese el ID del proyecto (ej:1000): ")

    try:
        proyecto_id = int(proyecto_id)
    except ValueError:
        print(f"Érror: El ID del proyecto debe ser un número entero.")

    dao_emp = EmpleadoDAO()

    if dao_emp.deassign_empleado_from_proyecto(empleado_id, proyecto_id):
        print(
            f"ÉXITO: Empleado {empleado_id} desasignado al Proyecto {proyecto_id}.")
    else:
        print("ERROR: La asignación falló (Verifique IDs o conexión)")


def delete_employee_console():
    print("\n--- ELIMINACIÓN DE EMPLEADO ---")
    empleado_id = input("Ingrese el ID del Empleado a ELIMINAR (Esta acción es permanente): ")
    confirm = input(f"¿Confirma la eliminación del empleado {empleado_id}? (S/N): ").upper()
    
    if confirm != 'S':
        print("Operación cancelada.")
        return

    dao = EmpleadoDAO()
    if dao.delete_empleado(empleado_id):
        print(f"ÉXITO: Empleado {empleado_id} eliminado exitosamente.")
    else:
        print("ERROR: La eliminación falló (El empleado podría tener registros de tiempo dependientes).")
            
# PROYECTOS, OPCIÓN 2 ADMIN


def menu_proyectos_admin():
    print("\n--- GESTIÓN DE PROYECTOS (CRUD) ---")
    print("1. Agregar Nuevo Proyecto (Create)")
    print("2. Listar Todos los Proyectos (Read)")
    print("3. Modificar Proyecto (Update)")
    print("4. Eliminar Proyecto (Delete)")
    print("5. Volver al Menú Principal")
    return input("Seleccione una opción: ")


def create_proyecto_console():
    print("\n--- AGREGAR NUEVO PROYECTO ---")
    dao = ProyectoDAO()
    try:
        nombre = input("Nombre del Proyecto: ")
        descripcion = input("Descripción: ")
        fecha_inicio_str = input("Fecha Inicio (YYYY-MM-DD): ")
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()

        # ID_PROYECTO se ignora, la secuencia de Oracle lo genera
        nuevo_proyecto = Proyecto(
            id_proyecto=None, nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio)

        if dao.create_proyecto(nuevo_proyecto):
            print("ÉXITO: Proyecto creado.")
        else:
            print("FALLO: No se pudo crear el proyecto.")
    except ValueError:
        print("Error: El formato de fecha debe ser YYYY-MM-DD.")
    except Exception as e:
        print(f"Error en la entrada de datos: {e}")


def list_all_projects():
    dao = ProyectoDAO()
    proyectos = dao.get_all_proyectos()

    if proyectos:
        print("\n--- LISTADO DE PROYECTOS ---")
        for proj in proyectos:
            print(
                f"ID: {proj.get_id():<5} | Nombre: {proj.get_nombre():<30} | Inicio: {proj.get_fecha_inicio()}")
    else:
        print("No hay proyectos registrados o la conexión falló.")


def update_proyecto_console():
    print("\n--- MODIFICAR PROYECTO ---")
    dao = ProyectoDAO()
    try:
        proyecto_id = int(input("ID del Proyecto a modificar: "))
        proyecto_obj = dao.get_proyecto_by_id(proyecto_id)

        if not proyecto_obj:
            print(f"Error: Proyecto ID {proyecto_id} no encontrado.")
            return

        print(f"Modificando: {proyecto_obj.get_nombre()}")

        nuevo_nombre = input(
            f"Nuevo Nombre (Actual: {proyecto_obj.get_nombre()}): ") or proyecto_obj.get_nombre()
        nueva_descripcion = input(
            f"Nueva Descripción (Actual: {proyecto_obj.get_descripcion()}): ") or proyecto_obj.get_descripcion()
        nueva_fecha_str = input(
            f"Nueva Fecha de Inicio (YYYY-MM-DD, Actual: {proyecto_obj.get_fecha_inicio()}): ")

        # Validar y actualizar la fecha
        fecha_inicio_nueva = proyecto_obj.get_fecha_inicio()
        if nueva_fecha_str:
            fecha_inicio_nueva = datetime.strptime(
                nueva_fecha_str, '%Y-%m-%d').date()

        # Actualizar objeto de dominio
        proyecto_obj.editar(nombre=nuevo_nombre, descripcion=nueva_descripcion)
        proyecto_obj._fecha_inicio = fecha_inicio_nueva

        if dao.update_proyecto(proyecto_obj):
            print(
                f"ÉXITO: Proyecto ID {proyecto_id} modificado correctamente.")
        else:
            print("FALLO: No se pudo modificar el proyecto en la base de datos.")

    except ValueError:
        print("Error: El ID debe ser numérico o el formato de fecha debe ser YYYY-MM-DD.")
    except Exception as e:
        print(f"Error al modificar proyecto: {e}")


def delete_proyecto_console():
    print("\n--- ELIMINAR PROYECTO ---")
    dao = ProyectoDAO()
    try:
        proyecto_id = int(input("ID del Proyecto a eliminar: "))

        proyecto_obj = dao.get_proyecto_by_id(proyecto_id)
        if not proyecto_obj:
            print(f"Error: Proyecto ID {proyecto_id} no encontrado.")
            return

        confirm = input(
            f"¿Confirma la eliminación del proyecto {proyecto_obj.get_nombre()} (ID: {proyecto_id})? (S/N): ").upper()

        if confirm == 'S':
            # Llama al método del DAO que maneja la eliminación en cascada (FKs)
            if dao.delete_proyecto(proyecto_id):
                print(
                    f"ÉXITO: Proyecto ID {proyecto_id} eliminado correctamente.")
            else:
                print(
                    "FALLO: El proyecto podría tener asignaciones de tiempo o empleados dependientes, o fallo de conexión.")
        else:
            print("Operación cancelada.")

    except ValueError:
        print("Error: El ID debe ser numérico.")
    except Exception as e:
        print(f"Error inesperado al eliminar proyecto: {e}")

# DEPARTAMENTOS OPCIÓN 3 ADMIN


def menu_departamentos_admin():
    print("\n--- GESTIÓN DE DEPARTAMENTOS (CRUD) ---")
    print("1. Agregar Nuevo Departamento (Create)")
    print("2. Listar Todos los Departamentos (Read)")
    print("3. Modificar Departamento (Update)")
    print("4. Eliminar Departamento (Soft Delete)")
    print("5. Asignar Gerente a Departamento")
    print("6. Volver al Menú Principal")
    return input("Seleccione una opción: ")


def create_departamento_console():
    print("\n--- AGREGAR NUEVO DEPARTAMENTO ---")
    dao = DepartamentoDAO()
    try:
        nombre = input("Nombre del Departamento: ")
        gerente_id = input("ID del Gerente (Opcional): ")

        # El ID_DEPARTAMENTO se asigna en el DAO con la secuencia
        nuevo_departamento = Departamento(
            nombre=nombre, gerente_id=gerente_id or None)
        # Asegurar el nombre está asignado para la validación
        nuevo_departamento.nombre = nombre

        if nuevo_departamento.validar_nombre():
            if dao.create_departamento(nuevo_departamento):
                print(f"ÉXITO: Departamento '{nombre}' creado.")
            else:
                print("FALLO: No se pudo crear el departamento.")
        else:
            print("Error: El nombre del departamento no es válido.")

    except Exception as e:
        print(f"Error en la entrada de datos: {e}")


def list_all_departamentos():
    dao = DepartamentoDAO()
    departamentos = dao.get_all_departamentos()

    if departamentos:
        print("\n--- LISTADO DE DEPARTAMENTOS ---")
        for dpto in departamentos:
            estado = "Activo" if dpto.activo else "Inactivo"
            print(
                f"ID: {dpto.id_departamento:<5} | Nombre: {dpto.nombre:<30} | Gerente ID: {dpto.gerente_id or 'N/A'} | Estado: {estado}")
    else:
        print("No hay departamentos registrados o la conexión falló.")


def update_departamento_console():
    print("\n--- MODIFICAR DEPARTAMENTO ---")
    dao = DepartamentoDAO()
    try:
        depto_id = int(input("ID del Departamento a modificar: "))
        depto_obj = dao.get_departamento_by_id(depto_id)

        if not depto_obj:
            print(f"Error: Departamento ID {depto_id} no encontrado.")
            return

        print(f"\nModificando: {depto_obj.nombre}")

        nuevo_nombre = input(
            f"Nuevo Nombre (Actual: {depto_obj.nombre}): ") or depto_obj.nombre
        activo_str = input(
            f"Estado Activo (1/0, Actual: {1 if depto_obj.activo else 0}): ")

        if nuevo_nombre:
            depto_obj.nombre = nuevo_nombre
        if activo_str in ['0', '1']:
            depto_obj.activo = (activo_str == '1')

        if dao.update_departamento(depto_obj):
            print(
                f"ÉXITO: Departamento ID {depto_id} modificado correctamente.")
        else:
            print("FALLO: No se pudo modificar el departamento.")

    except ValueError:
        print("Error: El ID debe ser numérico.")
    except Exception as e:
        print(f"Error al modificar departamento: {e}")


def delete_departamento_console():
    print("\n--- ELIMINAR DEPARTAMENTO (Soft Delete) ---")
    dao = DepartamentoDAO()
    try:
        depto_id = int(input("ID del Departamento a desactivar: "))
        confirm = input(
            f"¿Confirma la desactivación (Soft Delete) del departamento ID {depto_id}? (S/N): ").upper()

        if confirm == 'S':
            # Este método hace un UPDATE ACTIVO=0
            if dao.delete_departamento(depto_id):
                print(f"ÉXITO: Departamento ID {depto_id} desactivado.")
            else:
                print("FALLO: La desactivación falló (Verifique si el ID existe).")
        else:
            print("Operación cancelada.")

    except ValueError:
        print("Error: El ID del Departamento debe ser numérico.")
    except Exception as e:
        print(f"Error inesperado al eliminar departamento: {e}")


def assign_gerente_console():
    print("\n--- ASIGNAR GERENTE A DEPARTAMENTO ---")
    dao = DepartamentoDAO()
    try:
        depto_id = int(input("ID del Departamento: "))
        gerente_id = input(
            "ID del nuevo Gerente (debe ser un Empleado existente): ")

        depto_obj: Optional[Departamento] = dao.get_departamento_by_id(
            depto_id)

        if depto_obj:
            depto_obj.gerente_id = gerente_id
            if dao.update_departamento(depto_obj):
                print(
                    f"ÉXITO: Gerente {gerente_id} asignado al Departamento ID {depto_id}.")
            else:
                print(
                    "FALLO: No se pudo actualizar el departamento (Verifique si el Gerente ID existe).")
        else:
            print(f"Error: Departamento ID {depto_id} no encontrado.")

    except ValueError:
        print("Error: El ID del Departamento debe ser numérico.")

# REPORTES OPCION 4


def generate_report_console():
    print("\n--- GENERACIÓN DE INFORMES (REPORTE) ---")
    print("1. Listado Completo de Empleados")
    print("2. Horas Trabajadas por Proyecto (en rango de fechas)")
    print("3. Volver al Menú Principal")
    choice = input("Seleccione una opción de reporte: ")

    generador = GeneradorInforme()

    if choice == '1':
        print(generador.generar_informe_empleados())
    elif choice == '2':
        try:
            inicio_str = input("Fecha de Inicio del Rango (YYYY-MM-DD): ")
            fin_str = input("Fecha de Fin del Rango (YYYY-MM-DD): ")
            inicio = datetime.strptime(inicio_str, '%Y-%m-%d').date()
            fin = datetime.strptime(fin_str, '%Y-%m-%d').date()
            print(generador.generar_informe_horas_por_proyecto(inicio, fin))
        except ValueError:
            print("Error: El formato de fecha debe ser YYYY-MM-DD.")
    elif choice == '3':
        pass
    else:
        print("Opción no válida.")


def menu_roles_admin():
    print("\n--- GESTION DE ROLES ---")
    print("1. Agregar nuevo rol")
    print("2. Listar todos los roles")
    print("3. Modificar rol")
    print("4. Eliminar Rol")
    print("5. Volver al menú principal")
    return input("Seleccione una opción: ")


def list_all_roles():
    dao = RolDAO()
    roles = dao.get_all_roles()

    if roles:
        print("\n--- LISTADO DE ROLES ---")
        for rol in roles:
            print(f"ID: {rol.get_id():<5} | Nombre: {rol.get_nombre():<20} | Nivel: {rol.get_nivel_permisos()} | Descripción: {rol.get_descripcion()}")
    else:
        print("No hay roles registrados o la conexión falló.")


def create_rol_console():
    print("\n--- AGREGAR NUEVO ROL ---")
    dao = RolDAO()

    try:
        id_rol = int(input("ID del Rol (Debe ser único): "))
        nombre = input("Nombre del Rol (Ej. Gerente): ")
        descripcion = input("Descripción: ")
        nivel_permisos = int(input("Nivel de Permisos (99 o 10): "))

        nuevo_rol = Rol(
            id_rol=id_rol,
            nombre=nombre,
            descripcion=descripcion,
            nivel_permisos=nivel_permisos
        )

        if dao.create_rol(nuevo_rol):
            print(f"ÉXITO: Rol '{nombre}' creado.")
        else:
            print("ERROR: No se pudo crea el Rol (Verifique ID)")

    except ValueError:
        print("Error: Los IDs y el nivel de permisos deben ser números enteros.")
    except Exception as e:
        print(f"Error en la entrada de datos: {e}")


def update_rol_console():
    """Implementa la funcionalidad de Modificar Rol (Opción 3)."""
    print("\n--- MODIFICAR ROL ---")
    dao = RolDAO()
    try:
        id_rol = int(input("ID del Rol a modificar: "))
        rol_obj = dao.get_rol_by_id(id_rol)

        if not rol_obj:
            print(f"Error: Rol ID {id_rol} no encontrado.")
            return

        print(
            f"\nModificando Rol: {rol_obj.get_nombre()} (Nivel: {rol_obj.get_nivel_permisos()})")

        nuevo_nombre = input(
            f"Nuevo Nombre (Actual: {rol_obj.get_nombre()}): ") or rol_obj.get_nombre()
        nueva_descripcion = input(
            f"Nueva Descripción (Actual: {rol_obj.get_descripcion()}): ") or rol_obj.get_descripcion()
        nuevo_nivel_str = input(
            f"Nuevo Nivel de Permisos (Actual: {rol_obj.get_nivel_permisos()}): ")

        nuevo_nivel = int(
            nuevo_nivel_str) if nuevo_nivel_str else rol_obj.get_nivel_permisos()

        # Actualización de atributos del objeto
        rol_obj.set_nombre(nuevo_nombre)
        rol_obj.set_descripcion(nueva_descripcion)
        rol_obj.set_nivel_permisos(nuevo_nivel)

        if dao.update_rol(rol_obj):
            print(f"ÉXITO: Rol ID {id_rol} modificado correctamente.")
        else:
            print("FALLO: No se pudo modificar el Rol en la base de datos.")

    except ValueError:
        print("Error: El ID y el Nivel de Permisos deben ser números enteros.")
    except Exception as e:
        print(f"Error al modificar Rol: {e}")


def delete_rol_console():
    """Implementa la funcionalidad de Eliminar Rol (Opción 4)."""
    print("\n--- ELIMINAR ROL ---")
    dao = RolDAO()
    try:
        id_rol = int(input("ID del Rol a eliminar: "))

        rol_obj = dao.get_rol_by_id(id_rol)
        if not rol_obj:
            print(f"Error: Rol ID {id_rol} no encontrado.")
            return

        confirm = input(
            f"¿Confirma la eliminación del Rol '{rol_obj.get_nombre()}' (ID: {id_rol})? (S/N): ").upper()

        if confirm == 'S':
            if dao.delete_rol(id_rol):
                print(f"ÉXITO: Rol ID {id_rol} eliminado correctamente.")
            else:
                print(
                    "FALLO: La eliminación falló (El Rol podría tener usuarios asociados).")
        else:
            print("Operación cancelada.")

    except ValueError:
        print("Error: El ID del Rol debe ser un número entero.")
    except Exception as e:
        print(f"Error inesperado al eliminar Rol: {e}")


# Registro de Tiempo opción 6

def register_time_console(user_info):
    print("\n--- REGISTRO DE HORAS TRABAJADAS (REGISTRO TIEMPO) ---")
    dao = RegistroTiempoDAO()

    # Si es Rol 10 (Empleado), su ID es el que está en la sesión
    empleado_id = user_info['id_empleado']

    try:
        fecha_trabajo_str = input("Fecha de trabajo (YYYY-MM-DD): ")
        fecha_trabajo = datetime.strptime(fecha_trabajo_str, '%Y-%m-%d').date()
        horas_trabajadas = float(input("Horas trabajadas: "))
        proyecto_id = int(input("ID del Proyecto: "))
        descripcion_tareas = input("Descripción de las tareas: ")

        nuevo_registro = RegistroTiempo(
            id_empleado=empleado_id,
            id_proyecto=proyecto_id,
            fecha_trabajo=fecha_trabajo,
            horas_trabajadas=horas_trabajadas,
            descripcion_tareas=descripcion_tareas
        )

        if dao.create_registro(nuevo_registro):
            print(
                f"ÉXITO: {horas_trabajadas} horas registradas para el Proyecto {proyecto_id}.")
        else:
            print(
                "FALLO: No se pudo registrar el tiempo (Verifique ID de Proyecto o Empleado).")

    except ValueError:
        print("Error: La fecha debe ser YYYY-MM-DD y las horas/ID deben ser números.")
    except Exception as e:
        print(f"Error al registrar tiempo: {e}")

# main.py (Nueva Función para manejar la entrada de rango)


def menu_consulta_rangos(user_info):
    """Interfaz para seleccionar consulta por día o por rango."""
    print("\n--- SELECCIÓN DE CONSULTA DE INDICADORES ---")
    print("1. Consultar un día específico.")
    print("2. Consultar un rango de fechas. * Solo disponible para: UF, DOLAR, EURO.")
    choice = input("Seleccione el modo de consulta: ")

    # 1. Obtener ID del empleado
    empleado_id_registro = user_info['id_empleado']
    gestor = GestorIndicadores()

    if choice == '1':
        # Consulta por día
        fecha_consulta = input("Ingrese la fecha (YYYY-MM-DD): ").strip()
        if not fecha_consulta:
            print("Fecha no puede ser vacía.")
            return

        # Llama a la función que procesa un solo día (lógica actual)
        consultar_y_registrar_dia_unico(
            gestor, empleado_id_registro, fecha_consulta)

    elif choice == '2':
        # Consulta por rango de fechas
        fecha_inicio = input(
            "Ingrese la fecha de inicio (YYYY-MM-DD): ").strip()
        fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ").strip()

        if not fecha_inicio or not fecha_fin:
            print("Ambas fechas son requeridas para la consulta por rango.")
            return

        # Llama a la nueva función que procesa el rango
        consultar_y_registrar_rango(
            gestor, empleado_id_registro, fecha_inicio, fecha_fin)

    else:
        print("Opción no válida.")


# Función Auxiliar para Día Único (Se mueve la lógica original aquí)
def consultar_y_registrar_dia_unico(gestor, empleado_id, fecha_consulta):
    indicadores = ["uf", "ivp", "ipc", "utm", "dolar", "euro"]
    print("\n[ RESULTADOS DE LA CONSULTA DIARIA ]")

    for tipo in indicadores:
        # Lógica para obtener y registrar un solo día (ya corregida)
        indicador_obj = gestor.obtener_y_registrar_indicador(
            tipo=tipo, fecha=fecha_consulta, id_usuario_registro=empleado_id, registrar=False
        )
        if indicador_obj:
            print(f"  > {indicador_obj}")
            registrar = input(
                "  ¿Desea registrar este valor en Oracle? (S/N): ").lower()
            if registrar == 's':
                gestor.dao_oracle.registrar_indicador(
                    indicador=indicador_obj, id_usuario=empleado_id, sitio_proveedor=gestor.sitio_proveedor)
        else:
            print(
                f"  > No se pudo obtener la información para {tipo.upper()} en {fecha_consulta}.")


# Función Auxiliar para Rango
def consultar_y_registrar_rango(gestor, empleado_id, fecha_inicio_str, fecha_fin_str):
    # Solo estos soportan rangos según API
    indicadores = ["uf", "dolar", "euro"]

    # Esta función asume que solo UF, DÓLAR y EURO soportan rangos
    print("\n--- CONSULTA POR RANGO DE FECHAS ---")
    print(
        f"⚠️ Nota: El historial por rango solo está disponible para: {', '.join([i.upper() for i in indicadores])}.")
    print("\n[ RESULTADOS DE LA CONSULTA POR RANGO ]")

    for tipo in indicadores:
        print(f"\nConsultando {tipo.upper()} en el rango...")

        # El gestor debe tener un nuevo método para manejar rangos
        valores_serie = gestor.obtener_serie_por_rango(
            tipo=tipo, fecha_inicio=fecha_inicio_str, fecha_fin=fecha_fin_str
        )

        if valores_serie:
            print(f"  > {tipo.upper()} encontró {len(valores_serie)} valores.")

            for indicador_obj in valores_serie:
                print(f"    - {indicador_obj}")

                # Opcional: preguntar si quiere registrar toda la serie o solo algunos
                # Por simplicidad, asumiremos que no se pregunta por cada uno.

            # Si el usuario quiere registrar la serie completa
            registrar_serie = input(
                "  ¿Desea registrar toda esta serie en Oracle? (S/N): ").lower()
            if registrar_serie == 's':
                for indicador_obj in valores_serie:
                    gestor.dao_oracle.registrar_indicador(
                        indicador=indicador_obj, id_usuario=empleado_id, sitio_proveedor=gestor.sitio_proveedor)
                print(f"Serie de {tipo.upper()} registrada con éxito.")

        else:
            print(f"  > No se encontró serie para {tipo.upper()}.")


def main():
    print("--- Iniciando Sistema de Gestión de Empleados ---")

    db_manager = DatabaseConnector()
    db_conn = db_manager.connect()

    if db_conn is None:
        print("Crítico: No se pudo establecer la conexión a la base de datos Oracle. Cerrando aplicación")
        sys.exit(1)

    user_session = None

    # 1. Simulación de LOGIN
    print("\n---LOGIN ---")

    # Bucle de Autenticación
    while user_session is None:
        username = input("Usuario (Login/Email): ")
        password = getpass.getpass("Contraseña: ")

        # Llamada a la Capa de Datos para la Autenticación Segura (Requisito 9)
        usuario_dao = UsuarioDAO()
        user_info = usuario_dao.authenticate_user(username, password)

        if user_info:
            user_session = user_info
        else:
            print("Usuario o contraseña incorrectos.")

    # 2. Bucle Principal del Sistema (Autorización)
    while True:
        choice = display_menu(user_session)
        rol_id = user_session['id_rol']

        # Opciones de Administrador (Rol 99)
        if rol_id == 99:
            if choice == '1':  # Gestión Empleados
                sub_choice = menu_empleado_admin()
                if sub_choice == '1':
                    register_new_employee()
                elif sub_choice == '2':
                    list_all_employees()
                elif sub_choice == '3':
                    update_empleado_console()
                elif sub_choice == '4':
                    delete_employee_console()
                elif sub_choice == '5':
                    assign_project_console()
                elif sub_choice == '6':
                    deassign_empleado_from_proyecto()
                elif sub_choice == '7':
                    continue
                else:
                    print("Opción no válida en el menú de Empleados.")

            elif choice == '2':  # Gestión Proyectos
                sub_choice = menu_proyectos_admin()
                if sub_choice == '1':
                    create_proyecto_console()
                elif sub_choice == '2':
                    list_all_projects()
                elif sub_choice == '3':
                    update_proyecto_console()
                elif sub_choice == '4':
                    delete_proyecto_console()
                elif sub_choice == '5':
                    continue
                else:
                    print("Opción no válida en el menú de Proyectos.")

            elif choice == '3':  # Gestión Departamentos
                sub_choice = menu_departamentos_admin()
                if sub_choice == '1':
                    create_departamento_console()
                elif sub_choice == '2':
                    list_all_departamentos()
                elif sub_choice == '3':
                    update_departamento_console()
                elif sub_choice == '4':
                    delete_departamento_console()
                elif sub_choice == '5':
                    assign_gerente_console()
                elif sub_choice == '6':
                    continue
                else:
                    print("Opción no válida en el menú de Departamentos.")

            elif choice == '4':  # Generación de Informes
                generate_report_console()

            elif choice == '5':  # Gestión de Roles
                sub_choice = menu_roles_admin()
                if sub_choice == '1':
                    create_rol_console()
                elif sub_choice == '2':
                    list_all_roles()
                elif sub_choice == '3':
                    update_rol_console()
                elif sub_choice == '4':
                    delete_rol_console()
                elif sub_choice == '5':
                    continue
                else:
                    print("Opción no válida en el menú de Roles.")

        # Opción Común (Rol 10 o 99)
        if choice == '6':
            if rol_id == 10 or rol_id == 99:
                # Requisito Registro de Tiempo
                register_time_console(user_session)
            else:
                print("AUTORIZACIÓN DENEGADA. No tiene permisos para esta acción.")

        # Opción Común (Rol 10 o 99) - NUEVA OPCIÓN
        elif choice == '7':
            # Esta opción está disponible para TODOS los roles autenticados
            menu_consulta_rangos(user_session)

        # Opciones de control de sesión
        elif choice == '9':
            user_session = None
            print("Sesión cerrada.")
            break
        elif choice == '0':
            break

        # Control de acceso para opciones de Administrador
        elif rol_id != 99 and choice in ['1', '2', '3', '4', '5']:
            print("AUTORIZACIÓN DENEGADA. No tiene permisos para esta acción.")
        elif choice not in ['1', '2', '3', '4', '5', '6', '9', '0']:
            print("Opción no válida.")

    # Limpieza final
    db_manager.disconnect()
    print("Aplicación finalizada y conexión a DB cerrada.")


if __name__ == "__main__":
    main()
