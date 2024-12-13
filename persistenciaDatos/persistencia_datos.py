import sys
import psycopg2
from psycopg2 import Error
from datetime import datetime


# NUEVO
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from werkzeug.utils import secure_filename
import json
import os

import io

# Configuración de Google Drive API
CREDENTIALS_FILE = 'credentials.json'  # Tu archivo de credenciales JSON
SCOPES = ['https://www.googleapis.com/auth/drive.file']



# Función para autenticar y obtener servicio de Google Drive
def get_drive_service():
    """Crea un servicio de Google Drive a partir de un archivo de credenciales.
    Returns:
        Servicio de Google Drive.
    """
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service


# Función para crear o buscar una carpeta en Google Drive por asignatura
def get_or_create_folder(service, asignatura):
    """Obtiene o crea una carpeta en Google Drive para una asignatura.
    Args:
        service: Servicio de Google Drive.
        asignatura: ID de la asignatura.
        Returns:
            ID de la carpeta en Google Drive.
    """
    # Verificar si ya existe una carpeta para la asignatura
    query = f"name='{asignatura}' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)", pageSize=1).execute()
    items = results.get('files', [])

    # Si la carpeta ya existe, devuelve su ID
    if items:
        return items[0]['id']
    
    # Si no existe, crea una nueva carpeta
    file_metadata = {
        'name': asignatura,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder['id']


# --

# conectarse a la base de datos
def conectar():
    """Conectarse a la base de datos de PostgreSQL.
    Returns:
        Conexión a la base de datos.
    """
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="admin",
                                      host="localhost",
                                        database="arqui")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None
    

# desconectar de la base de datos
def disconnect(connection):
    """Desconectarse de la base de datos de PostgreSQL.
    Args:
        connection: Conexión a la base de datos.
    """
    if connection:
        connection.close()
        # print("PostgreSQL connection is closed")


def descargarArchivo(id_drive: str, output_path: str) -> None:
    """Descargar un archivo de Google Drive.
    Args:
        id_drive: ID del archivo en Google Drive.
        output_path: Ruta donde se guardará el archivo descargado.
    """

    service = get_drive_service()

    # Obtener el nombre del archivo
    try:
        file_metadata = service.files().get(fileId=id_drive, fields="name").execute()
        default_name = file_metadata['name']
    except Exception as e:
        print(f"Error al obtener el nombre del archivo: {e}")
        return

    # Descargar el archivo desde Google Drive
    try:
        request = service.files().get_media(fileId=id_drive)
        fh = io.BytesIO()  # Crear un buffer para almacenar los datos
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            _, done = downloader.next_chunk()

        output_path = os.path.join(output_path, default_name)
        # Guardar los datos descargados en el archivo seleccionado por el usuario
        with open(output_path, 'wb') as f:
            f.write(fh.getvalue())


    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        

def insertarPublicacion(titulo: str, descripcion: str, fecha: str, estado: str, publicador: str, tipo_publicacion: str, asignatura: str, drives_name: list) -> None:
    """Insertar una publicación en la base de datos y subir archivos a Google Drive.
    Args:
        titulo: Título de la publicación.
        descripcion: Descripción de la publicación.
        fecha: Fecha de publicación en formato ISO.
        estado: ID del estado de la publicación.
        publicador: ID del usuario que publica.
        tipo_publicacion: ID del tipo de publicación.
        asignatura: ID de la asignatura.
        drives_name: Lista de nombres de los archivos a subir.
    """

    print("Insertando publicación...")

    connect = conectar()
    cursor = connect.cursor()

    try:

        service = get_drive_service()

        # Obtener o crear la carpeta de la asignatura
        folder_id = get_or_create_folder(service, asignatura)


        # Insertar la publicación y obtener el id_publicacion
        cursor.execute("""
            INSERT INTO publicacion (titulo, descripcion, fecha_publicacion, id_estado, id_usuario, id_tipo, id_asignatura)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (titulo, descripcion, fecha, estado, publicador, tipo_publicacion, asignatura))
        # Obtener el id de la publicación insertada
        id_publicacion = cursor.fetchone()[0]
        
        # Insertar archivos en una sola consulta
        for file_name in drives_name:
            filepath = os.path.join('uploads', file_name)
            # Subir el archivo a la carpeta de la asignatura en Google Drive
            file_metadata = {
                'name': file_name,
                'parents': [folder_id],  # Colocar el archivo en la carpeta de la asignatura
                'description': f'Uploaded by {publicador}, Type: {tipo_publicacion}, Asignatura: {asignatura}',
                'properties': {
                    'user': publicador,
                    'type': tipo_publicacion,
                    'asignatura': asignatura
                }
            }
            media = MediaFileUpload(filepath, mimetype='application/octet-stream')
            drive_file = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
            cursor.execute("INSERT INTO archivo (id_drive, nombre, id_publicacion) VALUES (%s,%s, %s)", (drive_file['id'], file_name, id_publicacion))

        
        # Confirmar transacción
        connect.commit()

    except Exception as e:
        # Manejo de errores y rollback en caso de excepción
        connect.rollback()
        print("Error al insertar la publicación y archivos:", e)

    finally:
        # Desconectar de la base de datos
        disconnect(connect)



def obtenerPublicacionesAsignatura(asignatura:str):
    connect = conectar()
    cursor = connect.cursor()

    try:
        # Consulta para obtener publicaciones filtradas por asignatura
        cursor.execute("""
            SELECT p.id, p.titulo, p.descripcion, p.fecha_publicacion, p.id_usuario, p.id_estado, p.id_tipo, a.nombre AS archivo_nombre, a.id_drive
            FROM publicacion p
            JOIN archivo a 
            ON p.id = a.id_publicacion
            WHERE p.id_asignatura = %s;
        """, (asignatura,))

        # Obtener los resultados
        archivos = cursor.fetchall()

        # Formatear los resultados en una lista de diccionarios
        resultados = []
        publicaciones = {}
        for row in archivos:
            (pub_id, titulo, descripcion, fecha_publicacion, id_usuario,
             id_estado, id_tipo, archivo_nombre, id_drive) = row
            if pub_id not in publicaciones:
                publicaciones[pub_id] = {
                    'id': pub_id,
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'fecha_publicacion': fecha_publicacion.isoformat(),  # Convertir a string ISO
                    'estado': id_estado,
                    'publicador': id_usuario,
                    'tipo_publicacion': id_tipo,
                    'archivos': []
                }

            # Añadir el archivo a la lista de archivos de la publicación
            publicaciones[pub_id]['archivos'].append({
                'id_drive': id_drive,
                'name': archivo_nombre
            })

        # Convertir el diccionario a una lista
        resultados = list(publicaciones.values())

        # Resultados: [{id:1, titulo:a, descripcion:a, fecha_publicacion:x, estado:x, publicador:x, tipo_publicacion:x, archivos: [ {id_drive:1, name:x}, {id_drive:2, name:xy}, ...}], {...}, ...]
        return resultados

    except Exception as e:
        print("Error al obtener publicaciones:", e)
        return []

    finally:
        # Desconectar de la base de datos
        disconnect(connect)


def obtenerAsignaturas(id_carrera: int):
    connect = conectar()
    cursor = connect.cursor()

    try:
        # Consulta para obtener publicaciones filtradas por asignatura
        cursor.execute("""
            SELECT c.id, c.nombre, a.id, a.nombre, a.prefijo, a.codigo, co.color_1
            FROM carrera c
            JOIN asignatura a 
            ON c.id = a.id_carrera
            JOIN colores co
            ON a.id_paleta = co.id
            WHERE c.id = %s;
        """, (id_carrera,))

        # Obtener los resultados
        asignaturas = cursor.fetchall()

        # Formatear los resultados en una lista de diccionarios
        resultados = []
        carreras = {}
        for row in asignaturas:
            (car_id, car_nombre, asig_id, asig_nombre, prefijo, codigo, color_1) = row
            if car_id not in carreras:
                carreras [car_id] = {
                    'id': car_id,
                    'nombre': car_nombre,
                    'asignaturas': []
                }

            # Añadir el archivo a la lista de archivos de la publicación
            carreras[car_id]['asignaturas'].append({
                'id': asig_id,
                'nombre': asig_nombre,
                'prefijo': prefijo,
                'codigo': codigo,
                'color_1': color_1,
            })

        # Convertir el diccionario a una lista
        resultados = list(carreras.values())

        # Resultados: [{id:1, titulo:a, descripcion:a, fecha_publicacion:x, estado:x, publicador:x, tipo_publicacion:x, archivos: [ {id_drive:1, name:x}, {id_drive:2, name:xy}, ...}], {...}, ...]
        return resultados

    except Exception as e:
        print("Error al obtener asignaturas:", e)
        return []

    finally:
        # Desconectar de la base de datos
        disconnect(connect)


def obtenerCarreras():

    connect = conectar()
    cursor = connect.cursor()

    try:

        cursor.execute("""
            WITH numeradas AS (
                SELECT c.id AS carrera_id, c.nombre AS carrera_nombre, a.id AS asignatura_id, a.nombre AS asignatura_nombre, a.prefijo, a.codigo, co.color_1,
                    ROW_NUMBER() OVER (PARTITION BY c.id ORDER BY a.id) AS fila_numero
                FROM carrera c
                JOIN asignatura a 
                ON c.id = a.id_carrera
                JOIN colores co
                ON a.id_paleta = co.id)
            SELECT carrera_id, carrera_nombre, asignatura_id, asignatura_nombre, prefijo, codigo, color_1
            FROM numeradas
            WHERE fila_numero <= 4;
                """)

        # Obtener los resultados
        asignaturas = cursor.fetchall()

        # Formatear los resultados en una lista de diccionarios
        resultados = []
        carreras = {}
        for row in asignaturas:
            (car_id, car_nombre, asig_id, asig_nombre, prefijo, codigo, color_1) = row
            if car_id not in carreras:
                carreras [car_id] = {
                    'id': car_id,
                    'nombre': car_nombre,
                    'asignaturas': []
                }

            # Añadir el archivo a la lista de archivos de la publicación
            carreras[car_id]['asignaturas'].append({
                'id': asig_id,
                'nombre': asig_nombre,
                'prefijo': prefijo,
                'codigo': codigo,
                'color_1': color_1,
            })

        # Convertir el diccionario a una lista
        resultados = list(carreras.values())

        # Resultados: [{id:1, titulo:a, descripcion:a, fecha_publicacion:x, estado:x, publicador:x, tipo_publicacion:x, archivos: [ {id_drive:1, name:x}, {id_drive:2, name:xy}, ...}], {...}, ...]
        return resultados

    except Exception as e:
        print("Error al obtener carreras:", e)
        return []

    finally:
        # Desconectar de la base de datos
        disconnect(connect)


def obtenerTipos() -> None:
    """Obtener los tipos de publicación.
    Returns:
        Lista de tipos de publicación.
    """
    connect = conectar()  # Suponiendo que la función 'conectar()' existe y establece una conexión con la base de datos.
    cursor = connect.cursor()

    try:
        # Obtener todos los registros de la tabla tipoPublicacion
        cursor.execute("SELECT * FROM tipopublicacion")
        
        # Recuperar todos los resultados
        tipos = cursor.fetchall()
        resultados = []
        for tipo in tipos:
            resultados.append({
                "id": tipo[0],
                "nombre": tipo[1]
            })
        return resultados

    except Exception as e:
        # Manejo de errores en caso de que falle la consulta
        print("Error al obtener los datos de tipoPublicacion:", e)

    finally:
        # Desconectar de la base de datos
        cursor.close()
        disconnect(connect)  # Suponiendo que la función 'disconnect()' cierra la conexión.

def handler(modo: str, argumentos: str):
    """Manejar las operaciones de la base de datos.
    Args:
        modo: Modo de operación.
        argumentos: Argumentos de la operación.
    """
    if modo == "insertar":
        argumentos = argumentos.split(";") # -> [titulo, descripcion, fecha, estado, publicador, tipo_publicacion, asignatura;name1,name2,name3]
        drives_names = argumentos[7].split(",")
        timestamp = datetime.fromtimestamp(float(argumentos[2])).strftime("%Y-%m-%d %H:%M:%S")
        insertarPublicacion(argumentos[0], argumentos[1], timestamp, argumentos[3], argumentos[4], argumentos[5], argumentos[6], drives_names)

    elif modo == "getPublicaciones":
        return obtenerPublicacionesAsignatura(argumentos)
    
    elif modo == "getCarreras":
        return obtenerCarreras()
    
    elif modo =="getTipos":
        return obtenerTipos()
    
    elif modo == "getAsignaturas":
        return obtenerAsignaturas(argumentos)
    
    elif modo == "descargar":
        argumentos = argumentos.split(";")
        descargarArchivo(argumentos[0], argumentos[1])
        
    else:
        print("Error: modo incorrecto")
        

# recibir argumentos


# modos: insertar
if len(sys.argv) > 1: # python modo
    modo = sys.argv[1] #
argumentos = ""

if len(sys.argv) > 2: # -> python modo argumentos 
    argumentos = sys.argv[2]

data = handler(modo, argumentos)
if("get" in modo):
    print(json.dumps(data))