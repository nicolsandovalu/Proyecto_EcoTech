import sys
from src.datos.db_connector import DatabaseConnector
from src.datos.empleado_dao import EmpleadoDAO
from src.dominio.empleado import Empleado
from datetime import date # Necesario para crear fechas

def display_menu(user_info):
    """Muestra el menú principal basado en el rol del usuario."""
    print("\n=============================================")
    print(f"Bienvenido, {user_info['nombre']}! | Rol ID: {user_info['id_rol']}")
    print("=============================================")
    
    # Lógica de Autorización simplificada
    if user_info['id_rol'] == 99: # ADMINISTRADOR
        print("1. [ADMIN] Registrar Nuevo Empleado")
        print("2. [ADMIN] Listar Todos los Empleados")
        print("3. [ADMIN] Asignar Proyecto a Empleado")
        print("4. [ADMIN] Eliminar Empleado")
    
    print("9. Cerrar Sesión")
    print("0. Salir del Sistema")
    return input("Seleccione una opción: ")

def register_new_employee():
    """Función para registrar un empleado a través de la consola."""
    print("\n--- REGISTRO DE NUEVO EMPLEADO ---")
    
    # Nota: En una app real, esto sería input() y se validaría la entrada (Validación Segura)
    try:
        data = {
            'id_empleado': input("ID Empleado (ej: E001): "),
            'nombre': input("Nombre: "),
            'email': input("Email: "),
            'salario': float(input("Salario: ")),
            'id_departamento': int(input("ID Departamento (ej: 1): ")),
            'id_cargo': input("ID Cargo (ej: DEV): "),
            'direccion': "Ejemplo Calle",
            'telefono': "555-1234",
            'fecha_inicio_contrato': '2025-01-01'
        }
        password = input("Contraseña inicial: ")
        
        # Crear objeto de dominio Empleado
        nuevo_empleado = Empleado(**data)
        
        # Usar el DAO para la persistencia
        dao = EmpleadoDAO()
        
        # Se asume un método que une create_empleado y create_user (que usa SeguridadDAO)
        # Aquí simplificamos, pero en la app real usarías un Service layer:
        if dao.create_empleado(nuevo_empleado):
            print("✅ EMPLEADO REGISTRADO CON ÉXITO.")
            # Faltaría aquí llamar a UsuarioDAO.create_user con la contraseña hasheada
        else:
            print("❌ FALLO AL REGISTRAR EMPLEADO.")
            
    except Exception as e:
        print(f"Error en la entrada de datos: {e}")

def list_all_employees():
    """Muestra la lista de empleados en consola."""
    dao = EmpleadoDAO()
    empleados = dao.get_all_empleados()
    
    if empleados:
        print("\n--- LISTADO DE EMPLEADOS ---")
        for emp in empleados:
            print(f"{emp.get_id()} | {emp.get_nombre()} | Depto: {emp.get_id_departamento()} | Salario: {emp.get_salario()}")
    else:
        print("No hay empleados registrados o la conexión falló.")

def main():
    print("--- Iniciando Sistema de Gestión de Empleados (Consola) ---")

    db_manager = DatabaseConnector()
    db_conn = db_manager.connect()
    
    if db_conn is None:
        print("Crítico: No se pudo establecer la conexión a la base de datos Oracle. Cerrando aplicación")
        sys.exit(1)
        
    user_session = None
    
    # 1. Simulación de LOGIN
    # En una UI real, esto se manejaría en LoginScreen
    print("\n--- SIMULACIÓN DE LOGIN ---")
    while user_session is None:
        username = input("Usuario (simulación): ")
        password = input("Contraseña (simulación): ")
        
        # Simulación de la autenticación: Asume que "admin" con cualquier pass es Rol 99
        if username == "admin":
            user_session = {'nombre': 'ADMINISTRADOR', 'id_rol': 99}
            break
        else:
            print("Usuario o contraseña incorrectos (Usar 'admin' por ahora).")
    
    # 2. Bucle Principal del Sistema (Autorización)
    while True:
        choice = display_menu(user_session)
        
        if choice == '1' and user_session['id_rol'] == 99:
            register_new_employee()
        elif choice == '2' and user_session['id_rol'] == 99:
            list_all_employees()
        elif choice == '9':
            user_session = None # Simulación de logout
            print("Sesión cerrada.")
            break
        elif choice == '0':
            break
        elif user_session['id_rol'] != 99 and choice in ['1', '2', '3', '4']:
             print("❌ AUTORIZACIÓN DENEGADA. No tiene permisos para esta acción.")
        elif choice not in ['0', '9']:
            print("Opción no válida.")

    db_manager.disconnect()
    print("Aplicación finalizada y conexión a DB cerrada.")

if __name__ == "__main__":
    main()