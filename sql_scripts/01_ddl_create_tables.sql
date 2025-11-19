-- 1. Tabla CARGO
CREATE TABLE Cargo (
    id_cargo   VARCHAR2(20)  PRIMARY KEY,
    nombre     VARCHAR2(50)  NOT NULL
);

-- 2. Tabla ROL
CREATE TABLE Rol (
    id_rol        INT     PRIMARY KEY,
    nombre        VARCHAR2(50)  UNIQUE NOT NULL,
    descripcion   VARCHAR2(200),
    nivel_permisos INT
);

-- 3. Tabla PROYECTO
CREATE TABLE Proyecto (
    id_proyecto    INT    PRIMARY KEY,
    nombre         VARCHAR2(50)  UNIQUE NOT NULL,
    descripcion    VARCHAR2(200),
    fecha_inicio   DATE          NOT NULL,
    fecha_creacion DATE          DEFAULT SYSDATE
);

-- 4. Tabla empleado
CREATE TABLE Empleado (
    id_empleado          VARCHAR2(20)  PRIMARY KEY,
    id_cargo             VARCHAR2(20),
    id_departamento      INT,
    nombre               VARCHAR2(50)  NOT NULL,
    direccion            VARCHAR2(200),
    telefono             VARCHAR2(20),
    email                VARCHAR2(100) UNIQUE NOT NULL, -- UNIQUE para asegurar la unicidad
    fecha_inicio_contrato DATE          NOT NULL,
    salario              NUMBER(12, 2), -- Precisión mejorada
    
    -- Claves Foráneas
    CONSTRAINT fk_emp_cargo FOREIGN KEY (id_cargo) REFERENCES Cargo(id_cargo)
);

-- 5. Tabla DEPARTAMENTO (Depende de Empleado para el Gerente)
CREATE TABLE Departamento (
    id_departamento INT    PRIMARY KEY,
    nombre          VARCHAR2(50)  UNIQUE NOT NULL,
    gerente_id      VARCHAR2(20),  -- FK que referencia a Empleado
    fecha_creacion  DATE          DEFAULT SYSDATE,
    activo          NUMBER     DEFAULT 1,
    
    -- Clave Foránea a Empleado (Relación Recursiva)
    CONSTRAINT fk_depto_gerente FOREIGN KEY (gerente_id) REFERENCES Empleado(id_empleado)
);

-- 6. Tabla USUARIO (Depende de Empleado y Rol)
CREATE TABLE Usuario (
    id_usuario    VARCHAR2(20)  PRIMARY KEY,
    id_empleado   VARCHAR2(20),
    nombre        VARCHAR2(20)  UNIQUE NOT NULL,
    contraseña    VARCHAR2(300) NOT NULL,        -- CRÍTICO: Suficiente longitud para el Hash (ej. bcrypt)
    id_rol        INT,
    
    -- Claves Foráneas
    CONSTRAINT fk_user_empleado FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado),
    CONSTRAINT fk_user_rol FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);

-- Ahora actualizamos la FK de Empleado a Departamento
ALTER TABLE Empleado
ADD CONSTRAINT fk_emp_depto FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento);

-- 7. Tabla EMPLEADO_PROYECTO (Relación N:M)
CREATE TABLE Empleado_Proyecto (
    id_empleado VARCHAR2(20),
    id_proyecto INT,
    
    -- Clave Primaria Compuesta
    PRIMARY KEY (id_empleado, id_proyecto),
    
    -- Claves Foráneas
    CONSTRAINT fk_ep_empleado FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado),
    CONSTRAINT fk_ep_proyecto FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id_proyecto)
);

-- 8. Tabla REGISTRO_TIEMPO
CREATE TABLE Registro_Tiempo (
    id_registro           INT   PRIMARY KEY,
    id_empleado           VARCHAR2(20) NOT NULL,
    id_proyecto           INT   NOT NULL,
    fecha_trabajo         DATE         NOT NULL,
    horas_trabajadas      NUMBER(3, 1) NOT NULL,
    descripcion_tareas    VARCHAR2(200),
    fecha_registro        DATE         DEFAULT SYSDATE,
    
    -- Claves Foráneas
    CONSTRAINT fk_rt_empleado FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado),
    CONSTRAINT fk_rt_proyecto FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id_proyecto)
);

-- Secuencias para IDs numéricos
CREATE SEQUENCE seq_rol START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_departamento START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_proyecto START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_registro_tiempo START WITH 1 INCREMENT BY 1;