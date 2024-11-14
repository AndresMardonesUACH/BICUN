"use client"
import { useState, useEffect } from 'react';

function FileUploader() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [files, setFiles] = useState([]);
    const [title, setTitle] = useState('');
    const [user, setUser] = useState('');
    const [type, setType] = useState('');
    const [tipos, setTipos] = useState([]);
    const [asignatura, setAsignatura] = useState('');
    
    
    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const uploadFile = async () => {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('title', title);
        formData.append('user', user);
        formData.append('type', type);
        formData.append('asignatura', asignatura);

        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        console.log('File uploaded:', data);
        fetchFiles();  // Update file list after upload
    };

    const fetchFiles = async () => {
        const response = await fetch('http://localhost:5000/list?asignatura=3');
        const data = await response.json();
        setFiles(data);
    };

    const fetchTipos = async () => {
        const response = await fetch('http://localhost:5000/asignaturas');
        const data = await response.json();
        setTipos(data);
    };

    useEffect(() => {
        fetchFiles()
        fetchTipos()
        console.log(files)
    }, [])

    return (
        <div className='div-main'>
            <div className='div-form'>
                <input required type="text" name='title' id='title' placeholder='Título' className="form-input" onChange={(e) => setTitle(e.target.value)} value={title} />
                <input required type="number" name='user' id='user' placeholder='Usuario' className="form-input" onChange={(e) => setUser(e.target.value)} value={user} />
                <select name="type" id="type" required className="form-input" onChange={(e) => handleSelect(e.target.id)} value={type}>
                    {tipos.map((x) => (
                        <option value={x.id}>{x.nombre}</option>
                    ))}
                </select>
                <input required type="text" name='asignatura' id='asignatura' placeholder='Asignatura' className="form-input" onChange={(e) => setAsignatura(e.target.value)} value={asignatura} />

                <input type="file" onChange={handleFileChange} />
                <button onClick={uploadFile}>Upload File</button>

                <h2>Uploaded Files:</h2>
                <ul>
                    {files.map((file) => (
                        <li key={file.id}>{file.id} {file.titulo} {file.asignatura}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default FileUploader;
