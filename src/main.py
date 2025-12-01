import sys
from src.datos.db_connector import DatabaseConnector
from src.datos.empleado_dao import EmpleadoDAO
from src.datos.proyecto_dao import ProyectoDAO
from .datos.usuario_dao import UsuarioDAO
from src.datos.seguridad_dao import SeguridadDAO
from src.dominio.empleado import Empleado
from src.dominio.usuario import Usuario
from src.dominio.proyecto import Proyecto
from datetime import date 


def display_menu(user_info):
    """Muestra el menú principal basado en el rol del usuario."""
    print("\n=============================================")
    print(f"Bienvenido, {user_info['nombre']}! | Rol ID: {user_info['id_rol']}")
    print("=============================================")
    
    # Lógica de Autorización
    if user_info['id_rol'] == 99: # ADMINISTRADOR
        print("1. [ADMIN] Registrar Nuevo Empleado")
        print("2. [ADMIN] Listar Todos los Empleados")
        print("3. [ADMIN] Asignar Proyecto a Empleado")
        print("4. [ADMIN] Eliminar Empleado")
        print("5. [ADMIN] Listar Proyectos") # Añadimos listar proyectos para la opción 3
    
    print("9. Cerrar Sesión")
    print("0. Salir del Sistema")
    return input("Seleccione una opción: ")

def register_new_employee():
    print("\n--- REGISTRO DE NUEVO EMPLEADO ---")
    
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
        
        # 1. Crear Objeto Empleado y Persistir
        nuevo_empleado = Empleado(**data)
        
        if not dao.create_empleado(nuevo_empleado):
            print("FALLO AL REGISTRAR EMPLEADO (Verifique FKs y Conexión).")
            return
            
        # 2. Crear Objeto Usuario (Rol 10 por defecto) y Persistir
        nuevo_usuario = Usuario(
            id_usuario=data['id_empleado'],
            nombre_usuario=data['id_empleado'],
            contrasena_hash="", # El hash se genera en el DAO
            id_rol=10, 
            id_empleado=data['id_empleado'] 
        )

        if usuario_dao.create_usuario(nuevo_usuario, contrasena_plana):
             print("EMPLEADO Y USUARIO REGISTRADOS CON ÉXITO.")
        else:
             print("FALLO AL REGISTRAR USUARIO. (Debería implementarse el rollback del Empleado)")
            
    except ValueError:
        print("Error de tipo: El salario y el ID de departamento deben ser números.")
    except Exception as e:
        print(f"Error en la entrada de datos: {e}")

def list_all_employees():
    dao = EmpleadoDAO()
    empleados = dao.get_all_empleados()
    
    if empleados:
        print("\n--- LISTADO DE EMPLEADOS ---")
        for emp in empleados:
            print(f"ID: {emp.get_id():<5} | Nombre: {emp.get_nombre():<20} | Depto ID: {emp.get_id_departamento()} | Salario: {emp.get_salario():.2f}")
    else:
        print("No hay empleados registrados o la conexión falló.")

# --- ASIGNAR PROYECTO (Opción 3) ---
def assign_project_console():
    print("\n--- ASIGNACIÓN DE EMPLEADO A PROYECTO ---")
    
    empleado_id = input("Ingrese el ID del Empleado a asignar: ")
    proyecto_id_str = input("Ingrese el ID del Proyecto (ej: 1000): ")
    
    try:
        proyecto_id = int(proyecto_id_str)
    except ValueError:
        print("Error: El ID del proyecto debe ser un número entero.")
        return

    dao_emp = EmpleadoDAO() 
    dao_proj = ProyectoDAO()
    
    # 1. Verificar si el empleado y proyecto existen (Validación Segura)
    if dao_emp.get_empleado_by_id(empleado_id) is None:
        print(f"Error de Validación: El Empleado ID '{empleado_id}' no existe.")
        return
        
    # Verifica si el proyecto existe
    if dao_proj.get_proyecto_by_id(proyecto_id) is None:
        print(f"Error de Validación: El Proyecto ID '{proyecto_id}' no existe.")
        return
    
    # 2. Llamar al DAO para realizar la asignación N:M
    if dao_emp.assign_empleado_to_proyecto(empleado_id, proyecto_id):
        print(f"ÉXITO: Empleado {empleado_id} asignado al Proyecto {proyecto_id}.")
    else:
        print("FALLO: La asignación falló (Verifique IDs o conexión).")

def list_all_projects():
        dao = ProyectoDAO()
        proyectos = dao.get_all_proyectos()
        
        if proyectos:
            print ("n\ --- LISTADO DE PROYECTOS ---")
            for proj in proyectos:
                print(f"ID: {proj.get_id():<5} | Nombre: {proj.get_nombre():<30} | Inicio: {proj.get_fecha_inicio()}")
        else:
            print("No hay proyectos registrados o la conexión falló.")

# ---  ELIMINAR EMPLEADO (Opción 4) ---
def delete_employee_console():
    print("\n--- ELIMINACIÓN DE EMPLEADO ---")
    
    empleado_id = input("Ingrese el ID del Empleado a ELIMINAR (Esta acción es permanente): ")
    confirm = input(f"¿Confirma la eliminación del empleado {empleado_id}? (S/N): ").upper()
    
    if confirm != 'S':
        print("Operación cancelada.")
        return

    dao = EmpleadoDAO()
    
    # Llamar al DAO para eliminar empleado (elimina Usuario, Empleado_Proyecto y Empleado)
    if dao.delete_empleado(empleado_id):
        print(f"ÉXITO: Empleado {empleado_id} eliminado exitosamente.")
    else:
        print("FALLO: La eliminación falló (El empleado podría tener registros de tiempo dependientes).")




# ========================================================
# FUNCIÓN PRINCIPAL (MAIN)
# ========================================================

def main():
    print("--- Iniciando Sistema de Gestión de Empleados (Consola) ---")

    db_manager = DatabaseConnector()
    db_conn = db_manager.connect()
    
    if db_conn is None:
        print("Crítico: No se pudo establecer la conexión a la base de datos Oracle. Cerrando aplicación")
        sys.exit(1)
        
    user_session = None
    
    # 1. Simulación de LOGIN
    print("\n---LOGIN ---")
    
    
    # SIMULACIÓN DE AUTENTICACIÓN
    while user_session is None:
        username = input("Usuario (Login/Email): ")
        password = input("Contraseña: ")
        
        # Llamada a la Capa de Datos para la Autenticación Segura
        usuario_dao = UsuarioDAO()
        user_info = usuario_dao.authenticate_user(username, password)
        
        if user_info:
            user_session = user_info
            print(f"\nBienvenido, {user_session['nombre']}! | Rol ID: {user_session['id_rol']}")
        else:
            print("Usuario o contraseña incorrectos.")
    
    # 2. Bucle Principal del Sistema (Autorización)
    while True:
        choice = display_menu(user_session)
        
        if choice == '1' and user_session['id_rol'] == 99:
            register_new_employee() # CRUD: Crear
        elif choice == '2' and user_session['id_rol'] == 99:
            list_all_employees() # CRUD: Leer
        elif choice == '3' and user_session['id_rol'] == 99:
            assign_project_console() #  Asignar Proyecto
        elif choice == '4' and user_session['id_rol'] == 99:
            delete_employee_console() #  Eliminar Empleado
        elif choice == '5' and user_session['id_rol'] == 99:
            list_all_projects() #Listar proyectos
            print("--- Listar Proyectos (Pendiente de lógica de ProyectoDAO) ---")
        elif choice == '9':
            user_session = None # Simulación de logout
            print("Sesión cerrada.")
            break
        elif choice == '0':
            break
        elif user_session['id_rol'] != 99 and choice in ['1', '2', '3', '4', '5']:
             print("AUTORIZACIÓN DENEGADA. No tiene permisos para esta acción.")
        else:
            print("Opción no válida.")
    
    
            
    # El bloque finally ahora es solo una limpieza final (la lógica de cierre va al final de main)
    db_manager.disconnect()
    print("Aplicación finalizada y conexión a DB cerrada.")

if __name__ == "__main__":
    main()