"use client"
import { useState } from 'react';

function FileUploader() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [files, setFiles] = useState([]);

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const uploadFile = async () => {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        console.log('File uploaded:', data);
        fetchFiles();  // Update file list after upload
    };

    const fetchFiles = async () => {
        const response = await fetch('http://localhost:5000/list');
        const data = await response.json();
        setFiles(data);
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={uploadFile}>Upload File</button>

            <h2>Uploaded Files:</h2>
            <ul>
                {files.map((file) => (
                    <li key={file.id}>{file.name}</li>
                ))}
            </ul>
        </div>
    );
}

export default FileUploader;
