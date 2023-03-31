import React, { useState } from 'react';
import ImageDisplay from './components/ImageDisplay';
import ImageInputForm from "./components/ImageInputForm";
import axios from 'axios';

// Setup axios interceptors that log the time taken for a request under "responseTime"
// in all the requests sent via axios.
axios.interceptors.request.use( x => {
    x.meta = x.meta || {}
    x.meta.requestStartedAt = new Date().getTime();
    return x;
})

axios.interceptors.response.use( x => {
    x.responseTime = new Date().getTime() - x.config.meta.requestStartedAt;
    return x;
})

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
