-- DML - Datos Iniciales para Pruebas (EcoTech Solutions)

-- ========================================================
-- 1. ROLES (Requisito de Autorización)
-- ========================================================

-- Se recomienda usar valores fijos (ej. 10, 99) en lugar de secuencias para roles de sistema
INSERT INTO Rol (id_rol, nombre, descripcion, nivel_permisos) VALUES (10, 'EMPLEADO', 'Usuario estándar con acceso a registro de tiempo', 10);
INSERT INTO Rol (id_rol, nombre, descripcion, nivel_permisos) VALUES (99, 'ADMINISTRADOR', 'Acceso total y gestión de CRUD', 99);


-- ========================================================
-- 2. CARGOS (Para Empleado)
-- ========================================================

INSERT INTO Cargo (id_cargo, nombre) VALUES ('DEV', 'Desarrollador de Software');
INSERT INTO Cargo (id_cargo, nombre) VALUES ('HR_MGR', 'Gerente de Recursos Humanos');
INSERT INTO Cargo (id_cargo, nombre) VALUES ('VENTAS', 'Ejecutivo de Ventas');
INSERT INTO Cargo (id_cargo, nombre) VALUES ('GERENTE', 'Gerente de Proyectos');
INSERT INTO Cargo (id_cargo, nombre) VALUES ('FIN_ANA', 'Analista Financiero');



-- ========================================================
-- 3. DEPARTAMENTOS (Para Empleado)
-- ========================================================

-- ID 100: RRHH
INSERT INTO Departamento (id_departamento, nombre, activo) VALUES (100, 'Recursos Humanos', 1);
-- ID 200: Desarrollo Sostenible
INSERT INTO Departamento (id_departamento, nombre, activo) VALUES (200, 'Desarrollo Sostenible', 1);


-- ========================================================
-- 4. EMPLEADO Y USUARIO (Autenticación Segura)
-- ========================================================

-- Empleado 1: Administrador (ID: A100)
INSERT INTO Empleado (id_empleado, id_cargo, id_departamento, nombre, email, salario, fecha_inicio_contrato, direccion, telefono)
VALUES ('A100', 'HR_MGR', 100, 'Nicol Sandoval', 'nicol.admin@ecotech.com', 75000.00, DATE '2025-01-15', 'Calle Falsa 123', '555-0001');

-- USUARIO 1: Administrador (Login: 'admin')
-- Contraseña almacenada: El hash que corresponde a la palabra 'admin123'
INSERT INTO Usuario (id_usuario, id_empleado, nombre, contraseña, id_rol)
VALUES ('A100', 'A100', 'admin', '$2b$12$Ea2267Gv33g4kH4vT9bAHe2/22t/P/2Jm7p/S.F7a8O.F7/2N/0P.', 99); 


-- Empleado 2: Empleado Estándar (ID: E200)
INSERT INTO Empleado (id_empleado, id_cargo, id_departamento, nombre, email, salario, fecha_inicio_contrato, direccion, telefono)
VALUES ('E200', 'DEV', 200, 'Joaquín Mendoza', 'joaquin.m@ecotech.com', 45000.00, DATE '2025-03-20', 'Av. Siempre Viva 456', '555-0002');

-- USUARIO 2: Empleado Estándar (Login: 'joaquin')
-- Contraseña almacenada: El hash que corresponde a la palabra 'admin123'
INSERT INTO Usuario (id_usuario, id_empleado, nombre, contraseña, id_rol)
VALUES ('E200', 'E200', 'joaquin', '$2b$12$Ea2267Gv33g4kH4vT9bAHe2/22t/P/2Jm7p/S.F7a8O.F7/2N/0P.', 10);

--- EN CASO DE ERROR EN CONTRASEÑA JOAQUIN, INGRESAR:
-- -- Reemplaza 'COPIA_AQUI_EL_HASH_GENERADO' por la cadena que te dio Python.
-- Contraseña Plana: admin123
-- UPDATE USUARIO
-- SET CONTRaseña = '$2b$12$qM.gZPhh9Ff1Y72aAfh4f.hbXJgTlyj0lKVEgYxOuZmRUSjB0o2gu'
-- WHERE NOMBRE = 'admin' OR NOMBRE = 'joaquin';

-- COMMIT;


-- ========================================================
-- 5. PROYECTOS
-- ========================================================

-- ID 1000: Proyecto Activo
INSERT INTO Proyecto (id_proyecto, nombre, descripcion, fecha_inicio)
VALUES (1000, 'Proyecto Sostenible Alpha', 'Desarrollo de aplicación para monitoreo de carbono.', DATE '2025-11-01');


-- ========================================================
-- 6. ASIGNACIÓN DE PROYECTOS (N:M)
-- ========================================================

-- Asignar Joaquín (E200) al Proyecto Alpha (1000)
INSERT INTO Empleado_Proyecto (id_empleado, id_proyecto) VALUES ('E200', 1000);


-- ========================================================
-- 7. REGISTRO DE TIEMPO (Para Informes)
-- ========================================================

-- Registro 1: Empleado E200 trabajó 8 horas en Proyecto 1000
INSERT INTO Registro_Tiempo (id_registro, id_empleado, id_proyecto, fecha_trabajo, horas_trabajadas, descripcion_tareas)
VALUES (1, 'E200', 1000, DATE '2025-11-28', 8.0, 'Implementación de módulo de reportes.');

-- Registro 2: Empleado E200 trabajó 4.5 horas en Proyecto 1000
INSERT INTO Registro_Tiempo (id_registro, id_empleado, id_proyecto, fecha_trabajo, horas_trabajadas, descripcion_tareas)
VALUES (2, 'E200', 1000, DATE '2025-11-29', 4.5, 'Revisión y corrección de bugs.');


COMMIT;