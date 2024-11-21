from flask import Flask, request, jsonify
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from flask_cors import CORS
from datetime import datetime
import subprocess
import os
import json

app = Flask(__name__)
CORS(app)
publicaciones = [
    {"file_name": "Post1", "file_path": "hola.png"}
]

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files['file'].filename
    tituloPost = request.form.get('title', '')
    publicador = request.form.get('user', '')
    tipoPost = request.form.get('type', '')
    asignaturaPost = request.form.get('asignatura', '')
    estadoPost = 1

    

    newPost = {"file_name": "Post2", "file_path": files}
    publicaciones.append(newPost)
    print(files)
    print(publicaciones)
    comando = f"python persistencia_datos.py insertar {tituloPost};desc;{str(datetime.timestamp(datetime.now()))};{estadoPost};{publicador};{tipoPost};{asignaturaPost};{files}"
    os.system(comando)

    return newPost

@app.route('/list', methods=['GET'])
def list_files():
    asignatura = request.args.get('asignatura', default=0)
    result = subprocess.run(
        ['python', 'persistencia_datos.py', 'get', asignatura], 
        stdout=subprocess.PIPE, 
        text=True
    )
    response = jsonify(json.loads(result.stdout))
    return response

@app.route('/tipos', methods=['GET'])
def list_types():
    result = subprocess.run(
        ['python', 'persistencia_datos.py', 'getTipos'], 
        stdout=subprocess.PIPE, 
        text=True
    )
    response = jsonify(json.loads(result.stdout))
    return response

if __name__ == '__main__':
    app.run(debug=True)