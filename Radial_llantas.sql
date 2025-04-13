CREATE DATABASE Radial_llantas;
USE Radial_llantas;

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre_cliente VARCHAR(25),
    apellidos VARCHAR(25),
    correo_cliente VARCHAR(50),
    direccion VARCHAR(100),
    codigo_postal VARCHAR(10),
    ciudad VARCHAR(25),
    telefono_cliente VARCHAR(15)
);

CREATE TABLE productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_producto VARCHAR(50),
    descripcion VARCHAR(255),
    precio DECIMAL(10,2) CHECK (precio >= 0),
    stock INT CHECK (stock >= 0),
    tipo_producto ENUM('llanta', 'servicio', 'poliza')
);

CREATE TABLE proveedores (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    nombre_proveedor VARCHAR(50),
    contacto_proveedor VARCHAR(50),
    telefono_proveedor VARCHAR(15)
);

CREATE TABLE compras (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    fecha DATE,
    total DECIMAL(10,2) CHECK (total >= 0),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE detalle_compras (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_compra INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT CHECK (cantidad > 0),
    subtotal DECIMAL(10,2) CHECK (subtotal >= 0),
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
);

CREATE TABLE promociones (
    id_promocion INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    descuento DECIMAL(5,2) CHECK (descuento >= 0 AND descuento <= 100),
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
);

CREATE TABLE metodos_pago (
    id_metodo_pago INT PRIMARY KEY AUTO_INCREMENT,
    metodo VARCHAR(50)
);
