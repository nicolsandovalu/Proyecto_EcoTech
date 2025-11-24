import tkinter as tk
from tkinter import messagebox
from ..datos.empleado_dao import EmpleadoDAO
from .mainWindow import MainWindow 

class LoginScreen:
    """Interfaz de Usuario para autenticación segura."""
    
    def __init__(self, db_manager):
        self.root = tk.Tk()
        self.root.title("EcoTech Solutions - Acceso seguro")
        self.root.geometry("400x300")
        
        # El DAO usa la conexión de la BD
        self.empleado_dao = EmpleadoDAO()
        self._create_widgets()
        
    def _create_widgets(self):
        # Etiqueta de título
        # CORRECCIÓN: Usar 'font=' en lugar de 'front='
        tk.Label(self.root, text="Iniciar sesión", font=("Arial", 16)).pack(pady=20)
        
        # campo usuario/email
        tk.Label(self.root, text="Usuario/Email: ").pack(pady=(10, 0))
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()
        
        # campo contrasñea
        tk.Label(self.root, text="Contraseña").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self.root, width=30, show="*") 
        self.password_entry.pack()
        
        # botón de inicio de sesión
        tk.Button(self.root, text="Iniciar sesión", command=self._handle_login, width=20).pack(pady=20)
        
    def _handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validación de Entradas Seguras
        if not username or not password:
            messagebox.showerror("Error de Validación", "Ambos campos son obligatorios.")
            return
        
        # CORRECCIÓN: Llamada a la lógica de autenticación (Capa de Datos)
        user_info = self.empleado_dao.authenticate_user(username, password)
        
        # Lógica de Autorización/Resultado
        if user_info:
            # Destruir la ventana de login y abrir la ventana principal
            self.root.destroy()
            self._open_main_window(user_info)
        else:
            messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")
            
    def _open_main_window(self, user_info):
        """Abre la ventana principal del sistema."""
        main_root = tk.Tk()
        MainWindow(main_root, user_info)
        main_root.mainloop()
            
    def run(self):
        self.root.mainloop()