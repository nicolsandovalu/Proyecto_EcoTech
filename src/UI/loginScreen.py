import tkinter as tk
from tkinter import messagebox
from ..datos.empleado_dao import EmpleadoDAO

class LoginScreen:
    #Interfaz de Usuario para autenticación segura
    
    def __init__(self, db_manager):
        self.root = tk.Tk()
        self.root.title("EcoTech Solutions - Acceso seguro")
        self.root.geometry("400x300")
        
        self.empleado_dao = EmpleadoDAO()
        self._create_widgets()
        
    def _create_widgets(self):
        #crea los elementos gráficos de la pantalla
        
        #Etiqueta de título
        tk.Label(self.root, text="Iniciar sesión", front= ("Arial", 16)).pack(pady=20)
        
        #campo usuario/email
        tk.Label(self.root, text="Usuario/Email: ").pack(pady=(10, 0))
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()
        
        #campo contrasñea
        tk.Label(self.root, text="Contraseña").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self.root, width=30, show="*") #show oculta la contraseña
        self.password_entry.pack()
        
        #botón de inicio de sesión
        tk.Button(self.root, text="Iniciar sesión", command=self._handle_login, width=20).pack(pady="20")
        
    def _handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
            
        #validación de entreda segura
        if not username or not password:
            messagebox.showerror("Error de Validación", "Ambos campos son obligatorios.")
            return
            #llamada a la lógica de autenticación(capa de datos)
        
        user_info: user_info = self.empleado_dao.authenticate_user(username, password)
        
        if user_info: 
            messagebox.showinfo("Éxito", f"Bienvenido, {user_info['nombre']}! Rold ID: {user_info['id_rol']}")
                
                # Si user_info['id_rol'] es 'Administrador', se abre la MainWindow completa.
                
        else:
            messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")
            
    def run(self):
         self.root.mainloop()