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
    stock INT,
    imagen varchar (255)
);

CREATE TABLE Pedidos (
    id INT PRIMARY KEY auto_increment,
    nombre_cliente VARCHAR(255),
    direccion_envio VARCHAR(255),
    numero_cliente VARCHAR (255),
    total DECIMAL(10, 2),
    metodo_pago VARCHAR (20)
);

CREATE TABLE Detalle_Pedidos (
	id_detalle int primary key auto_increment,
    cantidad int,
    precio decimal (10, 2),
    id_pedido int,
    id_producto int,
    talla char,
    foreign key (id_producto) references Productos (id),
    foreign key (id_pedido) references Pedidos (id)
);


