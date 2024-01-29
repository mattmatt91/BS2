import React, { useEffect, useState } from 'react';
import './Monitor.css';
import * as API from '../../service/api'
import ValueDisplayRow from "./DisplayValue"

interface SensorData {
  sensor: string;
  Value: any; // Adjust this type according to the actual shape of your sensor data
}

const Monitor: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.getMonitor()

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data)
        setSensorData(data);
        setError(null);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Error fetching data. Please try again.');
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 1000);
    return () => clearInterval(intervalId);
  }, []);





  return (
    <div className="display-container">
      {error && <div>Error: {error}</div>}
      <table>
    {sensorData.map((entry, index) => (
            <tr key={index}>
              <ValueDisplayRow name={entry.sensor} value={entry.Value} />
            </tr>
          ))}

  </table>
    </div>
  );
};

export default Monitor;
