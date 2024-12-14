from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import subprocess
import os
import json
import mimetypes
import time


app = Flask(__name__)
CORS(app)

#python gestionPublicaciones.py -m flask


# --------------------------------------------------------------------------------------------

# NUEVO --------------------------------------------------------------------------------------------
@app.route('/archivo/<file_id>/<file_name>', methods=['GET'])
def handle_download(file_id, file_name):
    if not file_id:
        return jsonify({'error': 'Se requiere el parámetro file_id'}), 400

    try:
        comando = f"python ../persistenciaDatos/persistencia_datos.py downloadArchivo {file_id}"
        os.system(comando)
        ruta = f'../interfaz/public/downloads/{file_name}'
        @after_this_request
        def borrar_archivo(response):
            try:    
                os.remove(ruta)
                print(f"Archivo {ruta} eliminado después de la descarga.")
            except Exception as e:
                print(f"Error al eliminar el archivo: {e}")
            return response
        

        return send_file(ruta, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# --------------------------------------------------------------------------------------------

@app.route('/publicacion', methods=['POST'])
def upload_files():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    files = request.files.getlist('file')  # Obtener todos los archivos
    if not files or all(file.filename == '' for file in files):
        return jsonify({'message': 'No files selected'}), 400

    tituloPost = request.form.get('title')
    publicador = request.form.get('user')
    tipoPost = request.form.get('type')
    asignaturaPost = request.form.get('asignatura')
    estadoPost = 1

    # Servicio de Google Drive
    try:
        comando = f"python ../persistenciaDatos/persistencia_datos.py insertar {tituloPost};desc;{str(datetime.timestamp(datetime.now()))};{estadoPost};{publicador};{tipoPost};{asignaturaPost};"
        for file in files:
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)  # Guardar archivo temporalmente


            # Ejecutar persistencia de datos
            comando += filename 
            if (file!=files[len(files) - 1]):
                comando += ","

        os.system(comando)

        return jsonify({'message': 'Archivos subidos exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# --------------------------------------------------------------------------------------------

@app.route('/publicaciones/<asignatura>', methods=['GET'])
def list_files(asignatura):
    try:
        result = subprocess.run(
            ['python', '../persistenciaDatos/persistencia_datos.py', 'getPublicaciones', asignatura], 
            stdout=subprocess.PIPE, 
            text=True
        )
        response = jsonify(json.loads(result.stdout))
        return response
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
# --------------------------------------------------------------------------------------------

@app.route('/tiposPublicaciones', methods=['GET'])
def list_types():
    result = subprocess.run(
        ['python', '../persistenciaDatos/persistencia_datos.py', 'getTipos'], 
        stdout=subprocess.PIPE, 
        text=True
    )
    response = jsonify(json.loads(result.stdout))
    return response

# --------------------------------------------------------------------------------------------

@app.route('/carreras', methods=['GET'])
def list_carreras():
    try:
        result = subprocess.run(
            ['python', '../persistenciaDatos/persistencia_datos.py', 'getCarreras'], 
            stdout=subprocess.PIPE, 
            text=True
        )
        response = jsonify(json.loads(result.stdout))
        return response
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# --------------------------------------------------------------------------------------------
# NUEVO ENDPOINT

@app.route('/asignaturas/<id_carrera>', methods=['GET'])
def list_asignaturas(id_carrera):
    try:
        result = subprocess.run(
            ['python', '../persistenciaDatos/persistencia_datos.py', 'getAsignaturas', id_carrera], 
            stdout=subprocess.PIPE, 
            text=True
        )
        print(result)
        response = jsonify(json.loads(result.stdout))
        return response
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# --------------------------------------------------------------------------------------------

# MAIN

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, host='0.0.0.0', port=5000)
