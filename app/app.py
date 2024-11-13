from flask import Flask, request, jsonify
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from flask_cors import CORS
from datetime import date
import os

app = Flask(__name__)
CORS(app)
publicaciones = [
    {"file_name": "Post1", "file_path": "hola.png"}
]

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    newPost = {"file_name": "Post2", "file_path": file.filename}
    publicaciones.append(newPost)
    print(file.filename)
    print(publicaciones)
    comando = "python3 persistencia_datos.py insertar Post1;desc;" + date.today() + ";1;martin;1;" + file.filename()
    os.system(comando)

    return newPost

@app.route('/list', methods=['GET'])
def list_files():
    return jsonify(publicaciones)

if __name__ == '__main__':
    app.run(debug=True)