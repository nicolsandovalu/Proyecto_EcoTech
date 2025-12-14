-- TABLA REGISTRO INDICADOR 
create table registro_indicador (
   id_registro      number(10) primary key,
   nombre_indicador varchar2(50) not null,
   valor            number(20,4) not null,
   fecha_valor      date not null,
   fecha_consulta   date not null,
   id_empleado      varchar2(5) not null,
   sitio_proveedor  varchar2(100) not null,
   constraint fk_reg_emp foreign key ( id_empleado )
      references empleado ( id_empleado )
);

-- Sentencia para crear la secuencia 
create sequence seq_registro_indicador start with 1 increment by 1;