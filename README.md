# ⚙️ Sistema de Gestión de Empleados - EcoTech Solutions

El proyecto **EcoTech Solutions** implementa un sistema de gestión de recursos humanos y proyectos enfocado en el paradigma de **Programación Orientada a Objetos (POO)**. La persistencia de datos se realiza en **Oracle Database**, cumpliendo con altos estándares de seguridad y trazabilidad.

## ✨ Características Principales

El sistema cubre los siguientes requisitos de la evaluación:

* **CRUD Completo (POO/DAO):** Gestión de Empleados, Proyectos, Departamentos y Roles.
* **Seguridad:** Implementación de autenticación robusta con **Bcrypt** para el cifrado de contraseñas.
* **Autorización:** Control de acceso basado en roles (Administrador `99` y Empleado `10`).
* **Gestión de N:M:** Asignación y desasignación de Empleados a Proyectos.
* **Reporting:** Módulo para la generación de informes consolidados de tiempo, empleados y proyectos.
* **Conexión a Datos Externos:** Simulación de consumo de API (Módulo Clima).

---

## 🛠️ Requisitos y Configuración Inicial

### Requisitos de Software

* **Python:** Versión 3.8 o superior.
* **Base de Datos:** Acceso a una instancia de Oracle Database (servidor remoto o local/XE).

### Instalación y Dependencias

Navegue a la raíz del proyecto (`Proyecto_EcoTech`) y prepare el entorno virtual:

```bash
# 1. Crear y activar el entorno virtual
python -m venv .venv
source .venv/bin/activate  # Para macOS/Linux
# .venv\Scripts\activate   # Para Windows

# 2. Instalar librerías esenciales (oracledb, dotenv, bcrypt)
pip install oracledb python-dotenv bcrypt

```

### . Configuración de Conexión (.env)

El archivo .env debe contener las credenciales exactas de su base de datos.

```bash
# Ejemplo de configuración para Oracle (datos con fines académicos)
DB_USER=TU_USUARIO
DB_PASS=TU_CONTRASEÑA
DB_HOST=IP PÚBLICA O localhost
DB_PORT=1521 (Depende de tu configuración)
DB_SERVICE=XEPDB1
```

## 🗃️ Inicialización de la Base de Datos

Debe ejecutar los scripts SQL para crear el esquema y cargar los datos de prueba.

### Creación de Tablas (DDL)
Ejecute el script que define el esquema y las relaciones (FKs):

```bash
-- Ejecutar: Proyecto_EcoTech/sql_scripts/01_ddl_create_tables.sql
```

### Carga de Datos Iniciales (DML)
Este script carga los roles iniciales, cargos y los usuarios de prueba (admin, joaquin).

```bash
-- Ejecutar: Proyecto_EcoTech/sql_scripts/02_dml_initial_data.sql
```

## 🏃 Ejecución del Sistema
Asegúrese de que su entorno virtual esté activo ((.venv) en la terminal) y ejecute el módulo principal:

```bash
# Una vez en tu terminal aparezca, por ej. (.venv) PS C:\Users\nicol\Proyecto_EcoTech>, utiliza el comando para iniciar la aplicación de consola

python -m src.main

#o 

python.exe -m src.main
```
## Credenciales de Login
Utilice estos datos para probar la Autenticación y Autorización:


```bash
| **Usuario (Login/Email)** | **Contraseña Plana** | **Rol ID** | **Permiso** |
| :--- | :---: | :---: | :--- |
| `admin` | `admin123` | `99` | ADMINISTRADOR (Acceso total a CRUD, Informes y Gestión de Usuarios) |
| `joaquin` | `admin123` | `10` | EMPLEADO (Acceso solo a Registro de Tiempo y datos personales) |
```
