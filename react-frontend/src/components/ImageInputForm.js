import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

export default function ImageInputForm({ setInputImage, setOutputImage}) {

    const [inputFile, setInputFile] = useState(null);

    function handleFileSelect(event) {
        // Reset the output image.
        setOutputImage(null);

        // Verify file extension of the uploaded file.
        const selectedFile = event.target.files[0];
        const fileName = selectedFile.name;
        const fileExtension = fileName.substr(fileName.lastIndexOf(".") + 1, fileName.length).toLowerCase();
        if (fileExtension === "jpg" || fileExtension === "jpeg" || fileExtension === "png"){
            // Valid file uploaded - set the image to the uploaded file.
            setInputImage(URL.createObjectURL(selectedFile));
            setInputFile(selectedFile);
        } else {
            alert("Only jpg/jpeg and png files are allowed!");
            document.getElementById("imageInput").value = "";
            setInputImage(null);
            setInputFile(null);
        }  
    };

    function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData();
        formData.append('image', inputFile);
        
        const access_token = Cookies.get('access_token');

        axios.post('http://localhost:5000/predict', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': access_token ? `Bearer ${access_token}` : ''
            }
          })
        .then(response => {
            if ('predictions' in response.data) {
                setOutputImage('data:;base64,' + response.data['predictions'])
            }
            console.log(response);
        })
        .catch(error => {
            console.log(error);
        });
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label htmlFor="imageInput">Select an image: </label>
                <input type="file" id="imageInput" onChange={handleFileSelect} accept="image/png, image/jpeg"/>
                <button type="submit">Upload</button>
            </form>
        </div>
        );
}
