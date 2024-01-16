import { Data as PlotData } from 'plotly.js';
import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import * as API from '../../service/api'
import './Data.css';

interface SensorDataItem {
  sensor: string;
  Value: any; // Adjust the type according to your actual data structure
}

const Data: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorDataItem[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.getData()

        if (!response.ok) {
          localStorage.clear()
          window.location.reload()
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setSensorData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const organizeData = (): PlotData[] => {
    const timestamps = sensorData.filter(item => item.sensor === 'timestamp').map(item => item.Value);
    const sensorTypes = ['humidity', 'temperature', 'pressure',  'lamp_bloom', 'lamp_grow', 'fan'];

    return sensorTypes.map(sensorType => {
      const sensorValues = sensorData.filter(item => item.sensor === sensorType).map(item => item.Value);
      return {
        x: timestamps,
        y: sensorValues,
        type: 'scatter',
        mode: 'lines',
        name: sensorType,
      };
    });
  };

  const handleDownloadCsv = () => {
    const token = localStorage.getItem('token'); // Retrieve the stored token
    const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Read the environment variable
    const endpoint = `${apiUrl}/data_download`; // Use a template string to create the endpoint

    fetch(endpoint, {
      headers: {
        'Authorization': `Bearer ${token}` // Include the token in the request
      }
    }).then(response => {
      response.blob().then(blob => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = 'sensor_data.csv';
        a.click();
      });
    }).catch(error => console.error('Error downloading CSV:', error));
  };

  const plotData = organizeData(); // Use the organized data for plotting
  const layout = { title: 'Sensor Data Plot' };

  return (
    <div className="data-container">
      <div className="plot-container">
        <Plot data={plotData} layout={layout} />
      </div>
      <p>
        <button onClick={handleDownloadCsv}>Download CSV</button>
      </p>
    </div>
  );

};

export default Data;
