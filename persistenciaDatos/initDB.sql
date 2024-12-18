CREATE TABLE rol(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    nivel INT NOT NULL
);

CREATE TABLE carrera(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL
);

CREATE TABLE usuario(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    apellido VARCHAR NOT NULL,
    contrasena VARCHAR NOT NULL,
    id_rol INT NOT NULL,
    id_carrera INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol(id),
    FOREIGN KEY (id_carrera) REFERENCES carrera(id)
);

CREATE TABLE estadoPublicacion(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    estado INT NOT NULL
);

CREATE TABLE tipoPublicacion(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL
);

CREATE TABLE colores(
	id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
	color_1 VARCHAR NOT NULL,
	color_2 VARCHAR NOT NULL,
	color_3 VARCHAR NOT NULL
);



CREATE TABLE asignatura(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    prefijo VARCHAR NOT NULL,
    codigo INT NOT NULL,
    id_carrera INT NOT NULL,
    id_paleta INT,
    FOREIGN KEY (id_carrera) REFERENCES carrera(id),
    FOREIGN KEY (id_paleta) REFERENCES colores(id)
);

CREATE TABLE publicacion(
    id SERIAL PRIMARY KEY,
    titulo VARCHAR NOT NULL,
    descripcion VARCHAR NOT NULL,
    fecha_publicacion TIMESTAMP NOT NULL,
    id_usuario INT NOT NULL,
    id_estado INT NOT NULL,
    id_tipo INT NOT NULL,
    id_asignatura INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_estado) REFERENCES estadoPublicacion(id),
    FOREIGN KEY (id_tipo) REFERENCES tipoPublicacion(id),
    FOREIGN KEY (id_asignatura) REFERENCES asignatura(id)
);

CREATE TABLE archivo(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    id_drive VARCHAR NOT NULL,
    id_publicacion INT NOT NULL,
    FOREIGN KEY (id_publicacion) REFERENCES publicacion(id)
);

-- Insertar datos en la tabla carrera
INSERT INTO carrera(nombre) VALUES ('Ingeniería Civil Informática');
INSERT INTO carrera(nombre) VALUES ('Bachillerato en Ciencias Básicas');
INSERT INTO carrera(nombre) VALUES ('Ingeniería Civil Industrial');


INSERT INTO colores (color_1, color_2, color_3, nombre) VALUES
('#e82f2f', '#d65b62', '#dd8388', 'Rojo'),
('#f1831d', '#e1944d', '#e69f73', 'Naranjo'),
('#e3e30b', '#d9d934', '#d9d96c', 'Amarillo'),
('#55a630', '#80b918', '#aacc00', 'Verde'),
('#06bd9b', '#2bb39a', '#63ada0', 'Celeste'),
('#0077b6', '#0096c7', '#4095b0', 'Azul'),
('#7540df', '#957acb', '#c3b3e1', 'Morado'),
('#fb6f92', '#ff8fab', '#ffb3c6', 'Rosado'),
('#9c6644', '#b08968', '#cd9777', 'Cafe');

-- Insertar datos en la tabla rol
INSERT INTO rol(nombre, nivel) VALUES ('Estudiante', 1);
INSERT INTO rol(nombre, nivel) VALUES ('Moderador', 2);
INSERT INTO rol(nombre, nivel) VALUES ('Administrador', 3);

-- Insertar datos en la tabla usuario
INSERT INTO usuario(nombre, apellido, contrasena, id_rol, id_carrera) VALUES ('Andres', 'Mardones', '1234', 3, 1);
INSERT INTO usuario(nombre, apellido, contrasena, id_rol, id_carrera) VALUES ('Martin', 'Alvarado', '1234', 1, 1);
INSERT INTO usuario(nombre, apellido, contrasena, id_rol, id_carrera) VALUES ('Isaias', 'Cabrera', '1234', 1, 1);
INSERT INTO usuario(nombre, apellido, contrasena, id_rol, id_carrera) VALUES ('Osvaldo', 'Casas-Cordero', '1234', 1, 1);

-- Insertar datos en la tabla estadoPublicacion
INSERT INTO estadoPublicacion(nombre, estado) VALUES ('Publicado', 0);
INSERT INTO estadoPublicacion(nombre, estado) VALUES ('ESPERA', 1);
INSERT INTO estadoPublicacion(nombre, estado) VALUES ('No Publicado', 2);
-- INSERT INTO estadoPublicacion(nombre, estado) VALUES ('Eliminado', 3);

-- INSERT INTO tipoPublicacion(nombre) VALUES ('Apunte');
INSERT INTO tipoPublicacion(nombre) VALUES ('Examen');
INSERT INTO tipoPublicacion(nombre) VALUES ('Guía');
INSERT INTO tipoPublicacion(nombre) VALUES ('Libro');
INSERT INTO tipoPublicacion(nombre) VALUES ('Otro');

-- Insertar datos en la tabla asignatura
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Introducción a la programación', 'INFO', 101, 1, 1);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Taller 1', 'INFO', 102, 1, 2);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Programación', 'INFO', 103, 1, 3);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Base de Datos', 'INFO', 104, 1, 4);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Redes', 'INFO', 105, 1, 5);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Sistemas Operativos', 'INFO', 106, 1, 6);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Taller 2', 'INFO', 107, 1, 7);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Taller 3', 'INFO', 108, 1, 8);

INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Algebra Lineal', 'BAIN', 101, 2, 5);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Cálculo en una variable', 'BAIN', 102, 2, 6);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Química', 'BAIN', 103, 2, 7);

INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Mecanica de fluidos', 'INDU', 101, 3, 8);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Termodinamica', 'INDU', 102, 3, 9);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera, id_paleta) VALUES ('Investigación operativa', 'INDU', 103, 3, 5);