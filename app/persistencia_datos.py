# script para gestionar las operaciones de la base de datos
# PostgreSQL

import sys
import psycopg2
from psycopg2 import Error
from datetime import datetime
import json



# conectarse a la base de datos
def conectar():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="contra",
                                      host="db", # nombre del servicio en docker-compose.yml
                                      database="arqui",
                                      port = "5433"
                                      )
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None
    

# desconectar de la base de datos
def disconnect(connection):
    if connection:
        connection.close()
        # print("PostgreSQL connection is closed")



# recibir argumentos
if len(sys.argv) > 1:
    modo = sys.argv[1] # modos: insertar
if len(sys.argv) == 3:
    argumentos = sys.argv[2]
else:
    argumentos= ""



# print("Modo:", modo)
"""
modo: insertar
argumentos: "prueba 2020;descripcion de prueba;2020-10-10;1;rosendo;1;path1,path2,path3"
"""

"""
titulo: prueba 2020"
descripcion: "descripcion de prueba"
fecha: "2020-10-10"
estado: "1"
publicador: "rosendo"
tipo_publicacion: "1"
asignatura: "Ingeniería de Software"
paths: "path1, path2, path3"
"""
def insertarPublicacion(titulo: str, descripcion: str, fecha: str, estado: str, publicador: str, tipo_publicacion: str, asignatura: str, paths: str) -> None:
    connect = conectar()
    cursor = connect.cursor()

    try:
        # Insertar la publicación y obtener el id_publicacion
        cursor.execute("""
            INSERT INTO publicacion (titulo, descripcion, fecha_publicacion, id_estado, id_usuario, id_tipo, id_asignatura)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (titulo, descripcion, fecha, estado, publicador, tipo_publicacion, asignatura))
        # Obtener el id de la publicación insertada
        id_publicacion = cursor.fetchone()[0]
        
        # Insertar archivos en una sola consulta
        paths = paths.split(",")
        archivos_data = [(path.strip(), id_publicacion) for path in paths]
        cursor.executemany("INSERT INTO archivo (ruta, id_publicacion) VALUES (%s, %s)", archivos_data)
        
        # Confirmar transacción
        connect.commit()

    except Exception as e:
        # Manejo de errores y rollback en caso de excepción
        connect.rollback()
        print("Error al insertar la publicación y archivos:", e)

    finally:
        # Desconectar de la base de datos
        disconnect(connect)

def obtenerPublicacionesAsignatura(asignatura: str):
    connect = conectar()
    cursor = connect.cursor()

    try:
        # Consulta para obtener publicaciones filtradas por asignatura
        cursor.execute("""
            SELECT p.id, p.titulo, p.descripcion, TO_CHAR(p.fecha_publicacion, 'YYYY-MM-DD HH24:MI:SS') AS formatted_date, e.nombre AS estado, 
                   u.nombre AS publicador, t.nombre AS tipo_publicacion, a.nombre AS asignatura
            FROM publicacion p
            JOIN estadopublicacion e ON p.id_estado = e.id
            JOIN usuario u ON p.id_usuario = u.id
            JOIN tipopublicacion t ON p.id_tipo = t.id
            JOIN asignatura a ON p.id_asignatura = a.id
            WHERE a.id = %s
            ORDER BY p.fecha_publicacion DESC
        """, (asignatura,))

        # Obtener los resultados
        publicaciones = cursor.fetchall()

        # Formatear los resultados en una lista de diccionarios
        resultados = []
        for publicacion in publicaciones:
            resultados.append({
                "id": publicacion[0],
                "titulo": publicacion[1],
                "descripcion": publicacion[2],
                "fecha_publicacion": publicacion[3],
                "estado": publicacion[4],
                "publicador": publicacion[5],
                "tipo_publicacion": publicacion[6],
                "asignatura": publicacion[7]
            })
        return resultados

    except Exception as e:
        print("Error al obtener publicaciones:", e)
        return []

    finally:
        # Desconectar de la base de datos
        disconnect(connect)

def obtenerTipos() -> None:
    connect = conectar()  # Suponiendo que la función 'conectar()' existe y establece una conexión con la base de datos.
    cursor = connect.cursor()

    try:
        # Obtener todos los registros de la tabla tipoPublicacion
        cursor.execute("SELECT * FROM tipoPublicacion")
        
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
    if modo == "insertar":
        argumentos = argumentos.split(";") # -> [titulo, descripcion, fecha, estado, publicador, tipo_publicacion, asignatura, paths]
        timestamp = datetime.fromtimestamp(float(argumentos[2])).strftime("%Y-%m-%d %H:%M:%S")
        insertarPublicacion(argumentos[0], argumentos[1], timestamp, argumentos[3], argumentos[4], argumentos[5], argumentos[6], argumentos[7])
        return
    elif modo == "get":
        return obtenerPublicacionesAsignatura(argumentos)
    elif modo =="getTipos":
        return obtenerTipos()
    else:
        print("Error: modo incorrecto")

data = handler(modo, argumentos)
print(json.dumps(data))