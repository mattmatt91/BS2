import React, { useEffect, useState } from 'react';
import './Video.css'; // Import the CSS file


const ImageComponent = () => {
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await fetch('http://192.168.1.30:8000/video'); // Make sure the URL is correct
        if (response.ok) {
          const blob = await response.blob();
          setImageSrc(URL.createObjectURL(blob));
        } else {
          console.error('Error fetching image:', response.status);
        }
      } catch (error) {
        console.error('Error fetching image:', error);
      }
    };

    fetchImage();
  }, []);

  return (
    <div className="image-container">
      <h2>Image Component</h2>
      {imageSrc ? <img src={imageSrc} alt="Loaded Image" /> : <p>Loading image...</p>}
    </div>
  );
};

export default ImageComponent;
