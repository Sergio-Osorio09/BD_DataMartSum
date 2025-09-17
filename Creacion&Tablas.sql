DROP DATABASE IF EXISTS DataMartSUM;
CREATE DATABASE DataMartSUM;

USE DataMartSUM;

-- DIMENSIONES

-- DimEstudiante
CREATE TABLE DimEstudiante (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    genero CHAR(1),
    fecha_nacimiento DATE,
    dni CHAR(8) UNIQUE,
    codigo_estudiante CHAR(8) UNIQUE,
    nombre VARCHAR(100),
    apellido_paterno VARCHAR(50),
    apellido_materno VARCHAR(50),
    distrito VARCHAR(50),
    provincia VARCHAR(50),
    departamento VARCHAR(50),
    estado_estudiante VARCHAR(20),
    anio_ingreso YEAR,
    modalidad_ingreso VARCHAR(50),
    email_institucional VARCHAR(100),
    celular CHAR(9),
    discapacidad CHAR(2)
);

-- DimCurso
CREATE TABLE DimCurso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    codigo_curso VARCHAR(20) UNIQUE,
    nombre_curso VARCHAR(100),
    creditos INT,
    horas_teoria INT,
    horas_practica INT,
    ciclo_curso INT,
    tipo_curso VARCHAR(20),
    estado_curso VARCHAR(20)
);

-- DimCarrera
CREATE TABLE DimCarrera (
    id_carrera INT AUTO_INCREMENT PRIMARY KEY,
    codigo_carrera VARCHAR(20) UNIQUE,
    nombre_carrera VARCHAR(100),
    duracion INT,
    creditos_totales INT,
    plan_estudios VARCHAR(20)
);

-- DimPeriodo
CREATE TABLE DimPeriodo (
    id_periodo INT AUTO_INCREMENT PRIMARY KEY,
    codigo_periodo VARCHAR(10) UNIQUE,
    anio YEAR,
    semestre VARCHAR(5),
    fecha_inicio DATE,
    fecha_fin DATE
);

-- DimDocente
CREATE TABLE DimDocente (
    id_docente INT AUTO_INCREMENT PRIMARY KEY,
    codigo_docente VARCHAR(20) UNIQUE,
    nombre VARCHAR(100),
    apellido_paterno VARCHAR(50),
    apellido_materno VARCHAR(50),
    genero CHAR(1),
    facultad VARCHAR(100),
    grado_academico VARCHAR(50),
    categoria VARCHAR(20)
);

-- TABLA DE HECHOS
CREATE TABLE FactInscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT,
    id_carrera INT,
    id_curso INT,
    id_docente INT,
    id_periodo INT,
    nota_final DECIMAL(5,2),
    curso_aprobado BOOLEAN,
    veces_curso INT,
    CONSTRAINT fk_estudiante FOREIGN KEY (id_estudiante) REFERENCES DimEstudiante(id_estudiante),
    CONSTRAINT fk_carrera FOREIGN KEY (id_carrera) REFERENCES DimCarrera(id_carrera),
    CONSTRAINT fk_curso FOREIGN KEY (id_curso) REFERENCES DimCurso(id_curso),
    CONSTRAINT fk_docente FOREIGN KEY (id_docente) REFERENCES DimDocente(id_docente),
    CONSTRAINT fk_periodo FOREIGN KEY (id_periodo) REFERENCES DimPeriodo(id_periodo)
);
