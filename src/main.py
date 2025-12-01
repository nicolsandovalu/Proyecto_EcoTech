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
from datetime import date, datetime
from typing import Optional




def display_menu(user_info):
    #Muestra el menú principal basado en el rol del usuario.
    print("\n=============================================")
    print(f"Bienvenido, {user_info['nombre']}! | Rol ID: {user_info['id_rol']}")
    print("=============================================")
    
    if user_info['id_rol'] == 99:
        print("1. [ADMIN] Gestión de Empleados")
        print("2. [ADMIN] Gestión de Proyectos")
        print("3. [ADMIN] Gestión de Departamentos")
        print("4. [ADMIN] Generar Informes")
        print("5. [ADMIN] Gestión de Roles")
    
    print("6. Registrar horas trabajadas")
    print("9. Cerrar sesión")
    print("0. Salir del sistema") 
    return input("Seleccione una opción: ")

#Empleado

def menu_empleado_admin():
    print("\n--- GESTIÓN DE EMPLEADOS ---")
    print("1. Registrar Nuevo Empleado (Create)")
    print("2. Listar Todos los Empleados (Read)")
    print("3. Eliminar Empleado (Delete)")
    print("4. Asignar/Desasignar Proyecto a Empleado (N:M)")
    print("5. Volver al Menú Principal")
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
            'id_cargo': input("ID Cargo (ej: DEV): "),
            'direccion': input("Dirección: "),
            'telefono': input("Teléfono: "),
            'fecha_inicio_contrato': input("Fecha Inicio (YYYY-MM-DD): ")
        }
        
        contrasena_plana = input("Contraseña inicial: ")
        
        #Crear objeto Empleaado y Persistir
        nuevo_empleado = Empleado(**data)
        
        if not dao.create_empleado(nuevo_empleado):
            print("FALLO AL REGISTRAR EMPLEADO (Verifique FKs y Conexión).")
            return
        
        #Crear objeto usuario
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
            dao.delete_empleado(data['id_empleado']) #rollbackmanual
        
    except ValueError:
        print("Error de tipo: El salario y el ID de departamento deben ser números o la fecha no tiene el formato YYYY-MM-DD")
    except Exception as es:
        print(f"Error en la entrada de datos: {e}")

def list_all_employees():
    dao = EmpleadoDAO()
    empleados = dao.get_all_empleados()
    
    if empleados:
        print("n\--- LISTADO DE EMPLEADOS ---")
        for emp in empleados:
            print(f"ID: {emp.get_id():<5}  | Nombre: {emp.get_nombre():<20} | Depto ID: {emp.get_id_departamento()}  | Salario: {emp.get_salario():.2f}")
    else:
        print("No hay empleados registrados o la conexión falló.")

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
        print(f"ÉXITO: Empleado {empleado_id} asignado al Proyecto {proyecto_id}.")
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
    
#PROYECTOS, OPCIÓN 2 ADMIN

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
        nuevo_proyecto = Proyecto(id_proyecto=None, nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio)
        
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
        print ("\n--- LISTADO DE PROYECTOS ---")
        for proj in proyectos:
            print(f"ID: {proj.get_id():<5} | Nombre: {proj.get_nombre():<30} | Inicio: {proj.get_fecha_inicio()}")
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
        
        nuevo_nombre = input(f"Nuevo Nombre (Actual: {proyecto_obj.get_nombre()}): ") or proyecto_obj.get_nombre()
        nueva_descripcion = input(f"Nueva Descripción (Actual: {proyecto_obj.get_descripcion()}): ") or proyecto_obj.get_descripcion()
        nueva_fecha_str = input(f"Nueva Fecha de Inicio (YYYY-MM-DD, Actual: {proyecto_obj.get_fecha_inicio()}): ")

        # Validar y actualizar la fecha
        fecha_inicio_nueva = proyecto_obj.get_fecha_inicio()
        if nueva_fecha_str:
            fecha_inicio_nueva = datetime.strptime(nueva_fecha_str, '%Y-%m-%d').date()

        # Actualizar objeto de dominio
        proyecto_obj.editar(nombre=nuevo_nombre, descripcion=nueva_descripcion)
        # La fecha no tiene un setter en dominio, se actualiza directamente para la persistencia
        proyecto_obj._fecha_inicio = fecha_inicio_nueva 
        
        if dao.update_proyecto(proyecto_obj):
            print(f"ÉXITO: Proyecto ID {proyecto_id} modificado correctamente.")
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
            
        confirm = input(f"¿Confirma la eliminación del proyecto {proyecto_obj.get_nombre()} (ID: {proyecto_id})? (S/N): ").upper()
        
        if confirm == 'S':
            # Llama al método del DAO que maneja la eliminación en cascada (FKs)
            if dao.delete_proyecto(proyecto_id): 
                print(f"ÉXITO: Proyecto ID {proyecto_id} eliminado correctamente.")
            else: 
               print("FALLO: El proyecto podría tener asignaciones de tiempo o empleados dependientes, o fallo de conexión.")
        else:
            print("Operación cancelada.")
            
    except ValueError:
        print("Error: El ID debe ser numérico.")
    except Exception as e:
        print(f"Error inesperado al eliminar proyecto: {e}")

#DEPARTAMENTOS OPCIÓN 3 ADMIN

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
        nuevo_departamento = Departamento(nombre=nombre, gerente_id=gerente_id or None)
        nuevo_departamento.nombre = nombre # Asegurar el nombre está asignado para la validación
        
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
        print ("\n--- LISTADO DE DEPARTAMENTOS ---")
        for dpto in departamentos:
            estado = "Activo" if dpto.activo else "Inactivo"
            print(f"ID: {dpto.id_departamento:<5} | Nombre: {dpto.nombre:<30} | Gerente ID: {dpto.gerente_id or 'N/A'} | Estado: {estado}")
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
        
        nuevo_nombre = input(f"Nuevo Nombre (Actual: {depto_obj.nombre}): ") or depto_obj.nombre
        activo_str = input(f"Estado Activo (1/0, Actual: {1 if depto_obj.activo else 0}): ")

        if nuevo_nombre:
            depto_obj.nombre = nuevo_nombre
        if activo_str in ['0', '1']:
            depto_obj.activo = (activo_str == '1')
        
        if dao.update_departamento(depto_obj):
            print(f"ÉXITO: Departamento ID {depto_id} modificado correctamente.")
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
        confirm = input(f"¿Confirma la desactivación (Soft Delete) del departamento ID {depto_id}? (S/N): ").upper()

        if confirm == 'S':
            if dao.delete_departamento(depto_id): # Este método hace un UPDATE ACTIVO=0
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
        gerente_id = input("ID del nuevo Gerente (debe ser un Empleado existente): ")
        
        depto_obj: Optional[Departamento] = dao.get_departamento_by_id(depto_id)
        
        if depto_obj:
            depto_obj.gerente_id = gerente_id
            if dao.update_departamento(depto_obj):
                print(f"ÉXITO: Gerente {gerente_id} asignado al Departamento ID {depto_id}.")
            else:
                print("FALLO: No se pudo actualizar el departamento (Verifique si el Gerente ID existe).")
        else:
            print(f"Error: Departamento ID {depto_id} no encontrado.")
            
    except ValueError:
        print("Error: El ID del Departamento debe ser numérico.")   

#REPORTES OPCION 4

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
            
        print(f"\nModificando Rol: {rol_obj.get_nombre()} (Nivel: {rol_obj.get_nivel_permisos()})")
        
        nuevo_nombre = input(f"Nuevo Nombre (Actual: {rol_obj.get_nombre()}): ") or rol_obj.get_nombre()
        nueva_descripcion = input(f"Nueva Descripción (Actual: {rol_obj.get_descripcion()}): ") or rol_obj.get_descripcion()
        nuevo_nivel_str = input(f"Nuevo Nivel de Permisos (Actual: {rol_obj.get_nivel_permisos()}): ")
        
        nuevo_nivel = int(nuevo_nivel_str) if nuevo_nivel_str else rol_obj.get_nivel_permisos()
        
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

        confirm = input(f"¿Confirma la eliminación del Rol '{rol_obj.get_nombre()}' (ID: {id_rol})? (S/N): ").upper()
        
        if confirm == 'S':
            if dao.delete_rol(id_rol):
                print(f"ÉXITO: Rol ID {id_rol} eliminado correctamente.")
            else:
                print("FALLO: La eliminación falló (El Rol podría tener usuarios asociados).")
        else:
            print("Operación cancelada.")
            
    except ValueError:
        print("Error: El ID del Rol debe ser un número entero.")
    except Exception as e:
        print(f"Error inesperado al eliminar Rol: {e}")


#Registro de Tiempo opción 6

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
            print(f"ÉXITO: {horas_trabajadas} horas registradas para el Proyecto {proyecto_id}.")
        else:
            print("FALLO: No se pudo registrar el tiempo (Verifique ID de Proyecto o Empleado).")
            
    except ValueError:
        print("Error: La fecha debe ser YYYY-MM-DD y las horas/ID deben ser números.")
    except Exception as e:
        print(f"Error al registrar tiempo: {e}") 

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
        password = input("Contraseña: ")
        
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
            if choice == '1': # Gestión Empleados
                sub_choice = menu_empleado_admin()
                if sub_choice == '1': register_new_employee()
                elif sub_choice == '2': list_all_employees()
                elif sub_choice == '3': delete_employee_console()
                elif sub_choice == '4': assign_project_console()
                elif sub_choice == '5': continue
                else: print("Opción no válida en el menú de Empleados.")

            elif choice == '2': # Gestión Proyectos
                sub_choice = menu_proyectos_admin()
                if sub_choice == '1': create_proyecto_console()
                elif sub_choice == '2': list_all_projects()
                elif sub_choice == '3': update_proyecto_console()
                elif sub_choice == '4': delete_proyecto_console()
                elif sub_choice == '5': continue
                else: print("Opción no válida en el menú de Proyectos.")

            elif choice == '3': # Gestión Departamentos
                sub_choice = menu_departamentos_admin()
                if sub_choice == '1': create_departamento_console()
                elif sub_choice == '2': list_all_departamentos()
                elif sub_choice == '3': update_departamento_console()
                elif sub_choice == '4': delete_departamento_console()
                elif sub_choice == '5': assign_gerente_console()
                elif sub_choice == '6': continue
                else: print("Opción no válida en el menú de Departamentos.")
            
            elif choice == '4': # Generación de Informes
                generate_report_console()
            
            elif choice == '5': # Gestión de Roles
                sub_choice = menu_roles_admin()
                if sub_choice == '1': create_rol_console()
                elif sub_choice == '2': list_all_roles()
                elif sub_choice == '3': update_rol_console()
                elif sub_choice == '4': delete_rol_console()
                elif sub_choice == '5': continue
                else: print("Opción no válida en el menú de Roles.")

        # Opción Común (Rol 10 o 99)
        if choice == '6':
            if rol_id == 10 or rol_id == 99:
                 register_time_console(user_session) # Requisito Registro de Tiempo
            else:
                print("AUTORIZACIÓN DENEGADA. No tiene permisos para esta acción.")

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
