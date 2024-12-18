import psycopg2
from psycopg2 import sql

# Datos de conexión
user = 'postgres'  # Cambia por tu usuario
password = '123456'  # Cambia por tu contraseña
host = 'localhost'
port = '5432'

# Nombre de la base de datos a la que te conectarás
new_db_name = 'BICUN'  # Cambia este nombre por la base de datos ya creada

# Ruta al archivo SQL
sql_file_path = './initDB.sql'  # Cambia esta ruta al archivo de tu SQL

try:
    # Conectar a la base de datos predeterminada 'postgres'
    conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
    conn.autocommit = True  # Necesario para ejecutar CREATE DATABASE
    cursor = conn.cursor()

    # Crear la base de datos
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))

    print(f"Base de datos '{new_db_name}' creada con éxito.")

    # Cerrar la conexión a la base de datos predeterminada
    cursor.close()
    conn.close()

    # Ahora conectarse a la nueva base de datos BICUN
    conn = psycopg2.connect(dbname=new_db_name, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    # Ejecuta las instrucciones para crear tablas y demás datos aquí
    # Por ejemplo, ejecuta el archivo SQL:
    with open('initDB.sql', 'r') as sql_file:
        sql = sql_file.read()
        cursor.execute(sql)

    print(f"Tablas y datos insertados en la base de datos '{new_db_name}'.")

    # Confirmar los cambios
    conn.commit()

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Ocurrió un error: {e}")
