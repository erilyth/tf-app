import React, { useState } from 'react';
import ImageDisplay from './components/ImageDisplay';
import ImageInputForm from "./components/ImageInputForm";

function App() {

  const [inputImage, setInputImage] = useState(null);
  const [outputImage, setOutputImage] = useState(null);

  return (
    <div>
      <ImageInputForm setInputImage={setInputImage} setOutputImage={setOutputImage} />  
      <ImageDisplay inputImage={inputImage} outputImage={outputImage} />
    </div>
  );
}

export default App;
