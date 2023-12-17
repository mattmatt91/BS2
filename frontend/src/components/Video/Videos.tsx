import React, { useEffect, useState } from 'react';
import './Video.css';

const ImageComponent = () => {
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    const fetchImage = async () => {
      const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Read the environment variable
      const endpoint = `${apiUrl}/video`; // Use a template string to create the endpoint
      const token = localStorage.getItem('token'); // Retrieve the stored token

      try {
        const response = await fetch(endpoint, {
          headers: {
            'Authorization': `Bearer ${token}` // Include the token in the request
          }
        });

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
