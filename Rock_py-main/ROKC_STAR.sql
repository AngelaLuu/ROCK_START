CREATE DATABASE ROCK_STAR;
USE ROCK_STAR;

CREATE TABLE Administrador (
    id int primary key auto_increment,
    nombre varchar(50),
    correo varchar(50),
    admin_password varchar (55),
    documento int
    );

CREATE TABLE Productos (
    id INT PRIMARY KEY auto_increment,
    nombre VARCHAR(255),
    descripcion TEXT,
    precio DECIMAL(10, 2),
    cantidad INT,
    imagen longblob
);

CREATE TABLE Pedidos (
    id INT PRIMARY KEY auto_increment,
    ciudad varchar (50),
    fecha_envio date,
    fecha_entrega DATE,	
    nombre_cliente VARCHAR(255),
    direccion_envio VARCHAR(255),
    total DECIMAL(10, 2)
);

insert into Productos (nombre, descripcion, precio, cantidad, imagen) values ('camisa', 'Camisa naranja talla XL', 50.000, 1, (load_file('/Descargas/image.png')));

select * from productos;

