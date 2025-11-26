import tkinter as tk


class MainWindow:
    # Ventana principal del sistema. Muestra el dashboard y el menú de navegación.
    # Implementa la lógica de Autorización simplificada.

    # Niveles de Autorización (simplificados)
    ADMIN_ROLE = 99     # Acceso total a Gestión
    EMPLOYEE_ROLE = 10  # Acceso básico: Registro de Horas

    # -----------------------------------------------------
    # CONSTRUCTOR E INICIALIZACIÓN
    # -----------------------------------------------------

    def __init__(self, root, user_info: dict):
        self.root = root
        self.user_info = user_info
        # Asumimos que user_info['id_rol'] contiene 99 (Admin) o 10 (Empleado)
        self.rol_id = user_info['id_rol']

        self.root.title(
            f"EcoTech Solutions - Dashboard ({user_info['nombre']})")
        self.root.geometry("800x600")

        self._create_header()
        self._create_navigation()
        self._create_dashboard()

    def _create_header(self):
        """Crea la cabecera con el nombre del usuario y el rol."""
        header_frame = tk.Frame(self.root, bg="#34495E")
        header_frame.pack(fill='x', side='top')

        tk.Label(header_frame, text="Sistema de Gestión de Empleados", fg="white",
                 bg="#34495E", font=("Arial", 18, "bold")).pack(side='left', padx=10, pady=10)

        rol_name = self._get_rol_name(self.rol_id)
        tk.Label(header_frame, text=f"Usuario: {self.user_info['nombre']} ({rol_name})", fg="white", bg="#34495E").pack(
            side='right', padx=10, pady=10)

    def _get_rol_name(self, rol_id):
        """Traduce el ID del rol a un nombre legible (simulación)."""
        if rol_id == self.ADMIN_ROLE:
            return "Administrador"
        elif rol_id == self.EMPLOYEE_ROLE:
            return "Empleado"
        return "Desconocido"

    # -----------------------------------------------------
    # LÓGICA DE AUTORIZACIÓN (MENÚ)
    # -----------------------------------------------------

    def _create_navigation(self):
        """
        Crea la barra de navegación lateral, aplicando la Autorización.
        """
        nav_frame = tk.Frame(self.root, width=150, bg="#F0F0F0")
        nav_frame.pack(fill='y', side='left')

        tk.Label(nav_frame, text="MENÚ", font=(
            "Arial", 12, "bold")).pack(pady=10)

        # 1. Menú Exclusivo para ADMINISTRADOR (ID 99)
        if self.rol_id == self.ADMIN_ROLE:
            tk.Label(nav_frame, text="GESTIÓN", font=(
                "Arial", 10, "bold"), bg="#F0F0F0").pack(pady=(10, 0))

            # Gestión de Empleados (CRUD Empleados)
            tk.Button(nav_frame, text="Gestión de Empleados", width=20, anchor='w',
                      command=lambda: print("ADMIN: Abrir Empleados CRUD")).pack(pady=3, padx=5)

            # Gestión de Departamentos (CRUD Dptos)
            tk.Button(nav_frame, text="Gestión de Departamentos", width=20, anchor='w',
                      command=lambda: print("ADMIN: Abrir Dpto CRUD")).pack(pady=3, padx=5)

            # Gestión de Proyectos (CRUD Proyectos)
            tk.Button(nav_frame, text="Gestión de Proyectos", width=20, anchor='w',
                      command=lambda: print("ADMIN: Abrir Proyecto CRUD")).pack(pady=3, padx=5)

            # Asignar Empleados a Proyecto
            tk.Button(nav_frame, text="Asignar Proyecto", width=20, anchor='w',
                      command=lambda: print("ADMIN: Abrir Asignación Proyecto")).pack(pady=3, padx=5)

            # Generación de Informes (Solo Admin)
            tk.Button(nav_frame, text="Generación de Informes", width=20, anchor='w',
                      command=lambda: print("ADMIN: Abrir Informes")).pack(pady=3, padx=5)

        # 2. Menú para EMPLEADOS (Disponible para Admin y Empleado)
        # Usamos >= EMPLOYEE_ROLE para incluir a todos los que tengan permiso base
        if self.rol_id >= self.EMPLOYEE_ROLE:
            tk.Label(nav_frame, text="OPERACIONES", font=(
                "Arial", 10, "bold"), bg="#F0F0F0").pack(pady=(10, 0))

            # Registro de Tiempo (Empleado y Admin pueden registrar)
            tk.Button(nav_frame, text="Registro de Tiempo", width=20, anchor='w',
                      command=lambda: print("EMPLEADO: Abrir Registro de Tiempo")).pack(pady=3, padx=5)

            # El Empleado solo puede ver sus datos (simulación)
            tk.Button(nav_frame, text="Ver Mis Datos", width=20, anchor='w',
                      command=lambda: print("EMPLEADO: Abrir Mis Datos")).pack(pady=3, padx=5)

    def _create_dashboard(self):
        """Crea el área principal del dashboard."""
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Label(content_frame, text="Bienvenido al Dashboard",
                 font=("Arial", 20)).pack(pady=50)

        rol_name = self._get_rol_name(self.rol_id)
        tk.Label(content_frame, text=f"Su nivel de acceso es: {rol_name}", font=(
            "Arial", 14)).pack()
