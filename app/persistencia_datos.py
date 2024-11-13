# script para gestionar las operaciones de la base de datos
# PostgreSQL

import sys
import psycopg2
from psycopg2 import Error



# conectarse a la base de datos
def connect():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="localhost",
                                        database="arqui")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None
    

# desconectar de la base de datos
def disconnect(connection):
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")



# recibir argumentos
if len(sys.argv) > 1:
    modo = sys.argv[1] # modos: insertar
    argumentos = sys.argv[2]
else:
    print("Error: faltan argumentos")


print("Modo:", modo)
"""
modo: insertar
argumentos: "prueba 2020;descripcion de prueba;2020-10-10;1;rosendo;1;path1,path2,path3"
"""
def formato(modo: str, argumentos: str) -> None:
    if modo == "insertar":
        argumentos = argumentos.split(";") # -> [titulo, descripcion, fecha, estado, publicador, tipo_publicacion, asignatura, paths]
        insertarPublicacion(argumentos[0], argumentos[1], argumentos[2], argumentos[3], argumentos[4], argumentos[5], argumentos[6], argumentos[7])
    else:
        print("Error: modo incorrecto")


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
    connect = connect()
    cursor = connect.cursor()

    try:
        # Insertar la publicación y obtener el id_publicacion
        cursor.execute("""
            INSERT INTO publicaciones (titulo, descripcion, fecha, estado, publicador, tipo_publicacion, asignatura)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (titulo, descripcion, fecha, estado, publicador, tipo_publicacion, asignatura))
        
        # Obtener el id de la publicación insertada
        id_publicacion = cursor.fetchone()[0]
        
        # Insertar archivos en una sola consulta
        paths = paths.split(",")
        archivos_data = [(path.strip(), id_publicacion) for path in paths]
        cursor.executemany("INSERT INTO archivos (path, publicacion) VALUES (%s, %s)", archivos_data)
        
        # Confirmar transacción
        connect.commit()

    except Exception as e:
        # Manejo de errores y rollback en caso de excepción
        connect.rollback()
        print("Error al insertar la publicación y archivos:", e)

    finally:
        # Desconectar de la base de datos
        disconnect(connect)



