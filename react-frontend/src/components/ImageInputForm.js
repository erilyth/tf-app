import React, { useState } from 'react';
import axios from 'axios';

export default function ImageInputForm() {

    const [imageFile, setImageFile] = useState(null);

    function handleFileSelect(event) {
        setImageFile(event.target.files[0]);
    };

    function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData();
        formData.append('image', imageFile);
    }

    axios.get('http://flask-server-service:8080')
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.log(error);
    });

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="image">Select an image:</label>
            <input type="file" id="image" onChange={handleFileSelect} />
            <button type="submit">Upload</button>
        </form>
        );
}
