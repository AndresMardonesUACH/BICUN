"use client"
import { useState, useEffect } from 'react';

function FileUploader() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [publicaciones, setPublicaciones] = useState([]);
    const [title, setTitle] = useState('');
    const [user, setUser] = useState('');
    const [type, setType] = useState('');
    const [tipos, setTipos] = useState([]);
    const [asignatura, setAsignatura] = useState('');
    
    
    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    function handleSelect(id) {
        var select = document.getElementById(id);
        var valor = select.options[select.selectedIndex].value;
        if (valor != "") {
            switch (id) {
                case "type":
                    setType(valor)
                    break
            }
        }
    }

    const uploadFile = async () => {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('title', title);
        formData.append('user', user);
        formData.append('type', type);
        formData.append('asignatura', asignatura);

        const response = await fetch('http://localhost:5000/publicacion', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        console.log('File uploaded:', data);
        fetchPublicaciones();  // Update file list after upload
    };

    const fetchPublicaciones = async () => {
        const response = await fetch('http://localhost:5000/publicaciones?asignatura=3');
        const data = await response.json();
        setPublicaciones(data);
    };

    const fetchTipos = async () => {
        const response = await fetch('http://localhost:5000/tiposPublicaciones');
        const data = await response.json();
        setTipos(data);
    };

    useEffect(() => {
        fetchPublicaciones()
        fetchTipos()
        console.log(publicaciones)
    }, [])

    return (
        <div className='div-main'>
            <div className='div-form'>
                <input required type="text" name='title' id='title' placeholder='Título' className="form-input" onChange={(e) => setTitle(e.target.value)} value={title} />
                <input required type="text" name='user' id='user' placeholder='Usuario' className="form-input" onChange={(e) => setUser(e.target.value)} value={user} />
                <select name="type" id="type" required className="form-input" onChange={(e) => handleSelect(e.target.id)} value={type}>
                    {tipos.map((x, index) => (
                        <option key={index} value={x.id}>{x.nombre}</option>
                    ))}
                </select>
                <input required type="text" name='asignatura' id='asignatura' placeholder='Asignatura' className="form-input" onChange={(e) => setAsignatura(e.target.value)} value={asignatura} />

                <input type="file" onChange={handleFileChange} />
                <button onClick={uploadFile}>Upload File</button>

                <h2>Uploaded Files:</h2>
                <ul>
                    {publicaciones.map((post) => (
                        <li key={post.id}>{post.titulo}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default FileUploader;
