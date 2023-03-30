import React from 'react'

export default function ImageDisplay({ inputImage, outputImage}) {
  return (
    <div>
        {inputImage && (
            <img src={inputImage} alt="Input" />
        )}
        {outputImage && (
            <img src={outputImage} alt="Prediction" />
        )}
    </div>
  )
}
