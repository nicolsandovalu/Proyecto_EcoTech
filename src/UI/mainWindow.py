import tkinter as tk

class MainWindow:
    #Ventana principal del sistema. Muestra el dashboard y el menú de navegación.
    #Implementa la lógica de Autorización.
    
    
    # Niveles de Autorización (según los roles definidos en tu DML)
    ADMIN_ROLE = 99
    HR_ROLE = 50
    EMPLOYEE_ROLE = 10

    def __init__(self, root, user_info: dict):
        self.root = root
        self.user_info = user_info
        self.rol_id = user_info['id_rol']
        
        self.root.title(f"EcoTech Solutions - Dashboard ({user_info['nombre']})")
        self.root.geometry("800x600")
        
        self._create_header()
        self._create_navigation()
        self._create_dashboard()

    def _create_header(self):
        """Crea la cabecera con el nombre del usuario y el rol."""
        header_frame = tk.Frame(self.root, bg="#34495E")
        header_frame.pack(fill='x', side='top')
        
        tk.Label(header_frame, text="Sistema de Gestión de Empleados", fg="white", bg="#34495E", font=("Arial", 18, "bold")).pack(side='left', padx=10, pady=10)
        
        rol_name = self._get_rol_name(self.rol_id)
        tk.Label(header_frame, text=f"Usuario: {self.user_info['nombre']} ({rol_name})", fg="white", bg="#34495E").pack(side='right', padx=10, pady=10)

    def _get_rol_name(self, rol_id):
        """Traduce el ID del rol a un nombre legible (simulación)."""
        if rol_id == self.ADMIN_ROLE:
            return "Administrador"
        elif rol_id == self.HR_ROLE:
            return "Recursos Humanos"
        elif rol_id == self.EMPLOYEE_ROLE:
            return "Empleado"
        return "Desconocido"

    def _create_navigation(self):
        """
        Crea la barra de navegación lateral, aplicando la Autorización.
        """
        nav_frame = tk.Frame(self.root, width=150, bg="#F0F0F0")
        nav_frame.pack(fill='y', side='left')
        
        tk.Label(nav_frame, text="MENÚ", font=("Arial", 12, "bold")).pack(pady=10)

        # 1. Gestión de Empleados (Solo Admin/RR.HH.)
        if self.rol_id >= self.HR_ROLE:
            tk.Button(nav_frame, text="Gestión de Empleados", width=20, anchor='w', 
                      command=lambda: print("Abrir Empleados CRUD")).pack(pady=5, padx=5)

        # 2. Gestión de Departamentos y Proyectos (Solo Admin/RR.HH.)
        if self.rol_id >= self.HR_ROLE:
            tk.Button(nav_frame, text="Gestión de Departamentos", width=20, anchor='w', 
                      command=lambda: print("Abrir Dpto CRUD")).pack(pady=5, padx=5)
            tk.Button(nav_frame, text="Gestión de Proyectos", width=20, anchor='w', 
                      command=lambda: print("Abrir Proyecto CRUD")).pack(pady=5, padx=5)

        # 3. Registro de Tiempo (Todos los empleados)
        if self.rol_id >= self.EMPLOYEE_ROLE:
            tk.Button(nav_frame, text="Registro de Tiempo", width=20, anchor='w', 
                      command=lambda: print("Abrir Registro de Tiempo")).pack(pady=5, padx=5)

        # 4. Generación de Informes (Solo Admin/RR.HH.)
        if self.rol_id >= self.HR_ROLE:
            tk.Button(nav_frame, text="Generación de Informes", width=20, anchor='w', 
                      command=lambda: print("Abrir Informes")).pack(pady=5, padx=5)

    def _create_dashboard(self):
        """Crea el área principal del dashboard."""
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(content_frame, text="Bienvenido al Dashboard", font=("Arial", 20)).pack(pady=50)
        tk.Label(content_frame, text=f"Su nivel de acceso es: {self.rol_id}", font=("Arial", 12)).pack()