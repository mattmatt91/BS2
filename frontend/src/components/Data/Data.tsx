import React, { useEffect, useState, useLayoutEffect, useRef } from 'react';
import Plot from 'react-plotly.js';
import * as API from '../../service/api';
import './Data.css';
import { Data as PlotlyData, Layout as PlotlyLayout } from 'plotly.js';

interface SensorDataItem {
  sensor: string;
  Value: any; // Adjust the type according to your actual data structure
}

const Data: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorDataItem[]>([]);
  const [plotWidth, setPlotWidth] = useState<number>(0);
  const plotContainerRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const updatePlotSize = () => {
      if (plotContainerRef.current) {
        setPlotWidth(plotContainerRef.current.offsetWidth);
      }
    };

    window.addEventListener('resize', updatePlotSize);
    updatePlotSize();

    return () => window.removeEventListener('resize', updatePlotSize);
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.getData();

        if (!response.ok) {
          localStorage.clear();
          window.location.reload();
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

  const organizeData = (): PlotlyData[] => {
    const timestamps = sensorData.filter(item => item.sensor === 'timestamp').map(item => item.Value);
    const sensorTypes = ['humidity', 'temperature', 'pressure', 'lamp_bloom', 'lamp_grow', 'fan'];

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

  const plotData = organizeData();
  const layout: Partial<PlotlyLayout> = {
    autosize: false,
    width: plotWidth,
    height: 400,
    legend: {
      orientation: 'h',
      x: 0,
      y: 10, // Adjust the vertical position of the legend
      xanchor: 'left',
      yanchor: 'bottom'
    },
    // ... [any other layout properties you need]
  };

  return (
    <div className="data-container">
      <div className="plot-container" ref={plotContainerRef}>
        <Plot data={plotData} layout={layout} />
      </div>
      <p>
        <button onClick={handleDownloadCsv}>Download CSV</button>
      </p>
    </div>
  );
};

export default Data;
