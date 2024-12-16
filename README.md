# Nombre del Proyecto


**BICUN** es un sitio web diseñado para estudiantes de distintas carreras que buscan compartir y acceder a material académico como guías, pruebas, apuntes, entre otros recursos. Su propósito es fomentar la colaboración y el acceso a materiales educativos dentro de la comunidad universitaria.

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Funcionalidades](#funcionalidades)
- [Por Hacer](#por-hacer)
- [Contribuidores](#contribuidores)


---

## Requisitos Previos

Antes de instalar el proyecto, asegúrate de tener instalado lo siguiente:

- [Node.js](https://nodejs.org/) v20.x o superior.
- [npm](https://www.npmjs.com/) v6.x o superior.
- [PostgreSQL](https://www.postgresql.org/download/) v13.x o superior.
- [Python](https://www.python.org/) v3.x o superior.

--- 


## Instalación

Instrucciones para clonar el repositorio y configurar el entorno.

```bash
# Clona el repositorio
git clone https://github.com/AndresMardonesUACH/BICUN.git

# Entra en el directorio del proyecto
cd BICUN

# Instala las dependencias de python
pip install -r requirements.txt

# Entra en el directorio de la interfaz
cd interfaz

# Instala las dependencias
npm install

# Entra en el directorio de la API
cd ../persistenciaDatos

# Ejecuta el script de creación de la base de datos
python3 init.py


```

---

## Uso

Instrucciones para ejecutar el proyecto en un entorno local.
Dentre de la carpeta interfaz ejecutar el siguiente comando:

```bash
# Ejecuta el proyecto
cd BICUN/interfaz
npm run dev

cd ../api
python3 gestionPublicaciones.py -m flask
```

---

## Funcionalidades

- **Publicación de Recursos**: Los usuarios pueden publicar y compartir material académico en la plataforma.
- **Búsqueda de Recursos**: Los usuarios pueden buscar y acceder a material académico publicado por otros estudiantes.
- **Descarga de Recursos**: Los usuarios pueden descargar el material académico disponible en la plataforma.

---

## Por Hacer

- **Sistema de Perfiles**: Implementar un sistema de perfiles para que los usuarios puedan personalizar su información y configuración en la plataforma.
- **Sistema de Reportes**: Implementar un sistema de reportes para que los usuarios puedan denunciar contenido inapropiado o irregular en la plataforma.
- **Sistema de Administración**: Implementar un sistema de administración para que los moderadores y administradores puedan gestionar y supervisar el contenido en la plataforma.
- **Sistema de Seguridad**: Implementar un sistema de seguridad para proteger la integridad y privacidad de los usuarios en la plataforma.

---

## Contribuidores

- Andrés Mardones
- Isaias Cabrera
- Martín Alvarado
- Osvaldo Casas-Cordero