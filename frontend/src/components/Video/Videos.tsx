import React, { useEffect, useState } from 'react';
import './Video.css';
import * as API from '../../service/api'

const ImageComponent = () => {
  const [imageSrc, setImageSrc] = useState('');
  const [isDownloading, setIsDownloading] = useState(false);


  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await API.getImage()

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


  const handleDownloadVid = () => {
    setIsDownloading(true); // Start loading
    const token = localStorage.getItem('token'); // Retrieve the stored token
    const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Read the environment variable
    const endpoint = `${apiUrl}/video_download`; // Use a template string to create the endpoint

    fetch(endpoint, {
      headers: {
        'Authorization': `Bearer ${token}` // Include the token in the request
      }
    }).then(response => {
      response.blob().then(blob => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = 'timelapse.mp4';
        a.click();
        setIsDownloading(false); // Stop loading after download
      });
    }).catch(error => {
      console.error('Error downloading CSV:', error);
      setIsDownloading(false); // Stop loading on error
    });
  };

  return (
    <div className="image-container">
      <h2>Image Component</h2>
      {imageSrc ? <img src={imageSrc} alt="Loaded Image" /> : <p>Loading image...</p>}
      <p>
        {isDownloading ? (
          <p>Loading...</p> // Replace with your loading animation or label
        ) : (
          <button onClick={handleDownloadVid}>Download Timelapse</button>
        )}
      </p>
    </div>
  );
};

export default ImageComponent;
