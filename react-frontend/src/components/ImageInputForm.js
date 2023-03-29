import React, { useState } from 'react';
import axios from 'axios';

export default function ImageInputForm() {

    const [imageFile, setImageFile] = useState(null);
    const [prediction, setPrediction] = useState(null);

    function handleFileSelect(event) {
        setImageFile(event.target.files[0]);
    };

    function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData();
        formData.append('image', imageFile);
        
        axios.post('http://localhost:5000/predict', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
          })
        .then(response => {
            setPrediction('data:;base64,' + response.data['image'])
        })
        .catch(error => {
            console.log(error);
        });
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label htmlFor="image">Select an image:</label>
                <input type="file" id="image" onChange={handleFileSelect} />
                <button type="submit">Upload</button>
            </form>
            {prediction && (
                <img src={prediction} alt="Prediction" />
            )}
        </div>
        );
}
