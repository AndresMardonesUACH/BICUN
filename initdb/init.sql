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

CREATE TABLE asignatura(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    prefijo VARCHAR NOT NULL,
    codigo INT NOT NULL,
    id_carrera INT NOT NULL,
    FOREIGN KEY (id_carrera) REFERENCES carrera(id)
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
    ruta VARCHAR NOT NULL,
    id_publicacion INT NOT NULL,
    FOREIGN KEY (id_publicacion) REFERENCES publicacion(id)
);

-- Insertar datos en la tabla carrera
INSERT INTO carrera(nombre) VALUES ('Ingeniería Civil Informática');

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
-- INSERT INTO tipoPublicacion(nombre) VALUES ('Tarea');
INSERT INTO tipoPublicacion(nombre) VALUES ('Examen');
INSERT INTO tipoPublicacion(nombre) VALUES ('Guía');
INSERT INTO tipoPublicacion(nombre) VALUES ('Libro');
INSERT INTO tipoPublicacion(nombre) VALUES ('Otro');

-- Insertar datos en la tabla asignatura
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera) VALUES ('Programación', 'INF', 111, 1);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera) VALUES ('Base de Datos', 'INF', 112, 1);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera) VALUES ('Redes', 'INF', 113, 1);
INSERT INTO asignatura(nombre, prefijo, codigo, id_carrera) VALUES ('Sistemas Operativos', 'INF', 114, 1);