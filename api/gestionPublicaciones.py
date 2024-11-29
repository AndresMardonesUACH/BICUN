from flask import Flask, request, jsonify
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import subprocess
import os
import json
import time

app = Flask(__name__)
CORS(app)

# Configuración de Google Drive API
CREDENTIALS_FILE = 'credentials.json'  # Tu archivo de credenciales JSON
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Función para autenticar y obtener servicio de Google Drive
def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

# Función para crear o buscar una carpeta en Google Drive por asignatura
def get_or_create_folder(service, asignatura):
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

publicaciones = [
    {"file_name": "Post1", "file_path": "hola.png"}
]

@app.route('/publicacion', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    tituloPost = request.form.get('title')
    publicador = request.form.get('user')
    tipoPost = request.form.get('type')
    asignaturaPost = request.form.get('asignatura')
    estadoPost = 1

    # Guardar el archivo temporalmente
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    # Subir el archivo a Google Drive con metadatos
    try:
        service = get_drive_service()

        # Obtener o crear la carpeta de la asignatura
        folder_id = get_or_create_folder(service, asignaturaPost)

        # Subir el archivo a la carpeta de la asignatura en Google Drive
        file_metadata = {
            'name': filename,
            'parents': [folder_id],  # Colocar el archivo en la carpeta de la asignatura
            'description': f'Uploaded by {publicador}, Type: {tipoPost}, Asignatura: {asignaturaPost}',
            'properties': {
                'user': publicador,
                'type': tipoPost,
                'asignatura': asignaturaPost
            }
        }
        media = MediaFileUpload(filepath, mimetype='application/octet-stream')
        drive_file = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()

        newPost = {"file_name": "Post2", "file_path": file}
        publicaciones.append(newPost)
        comando = f"python ../persistenciaDatos/persistencia_datos.py insertar {tituloPost};desc;{str(datetime.timestamp(datetime.now()))};{estadoPost};{publicador};{tipoPost};{asignaturaPost};{file.filename}"
        os.system(comando)
        os.remove(filepath)

        return jsonify({'file_id': drive_file['id'], 'file_name': drive_file['name'], 'message': 'Archivo subido exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/publicaciones', methods=['GET'])
def list_files():
    asignatura = request.args.get('asignatura', default=0)

    try:
        service = get_drive_service()

        # Obtener el ID de la carpeta de la asignatura
        folder_id = get_or_create_folder(service, asignatura) if asignatura else None

        # Configurar la consulta para listar archivos en la carpeta de asignatura
        query = f"'{folder_id}' in parents" if folder_id else "mimeType != 'application/vnd.google-apps.folder'"
        
        results = service.files().list(q=query, pageSize=10, fields="files(id, name, properties)").execute()
        items = results.get('files', [])
        files = [{'id': item['id'], 'titulo': item['name'], 'asignatura': item['properties'].get('asignatura', '')} for item in items]

        result = subprocess.run(
            ['python', '../persistenciaDatos/persistencia_datos.py', 'get', asignatura], 
            stdout=subprocess.PIPE, 
            text=True
        )
        response = jsonify(json.loads(result.stdout))
        return response
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
@app.route('/tiposPublicaciones', methods=['GET'])
def list_types():
    result = subprocess.run(
        ['python', '../persistenciaDatos/persistencia_datos.py', 'getTipos'], 
        stdout=subprocess.PIPE, 
        text=True
    )
    response = jsonify(json.loads(result.stdout))
    return response

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, host='0.0.0.0', port=5000)