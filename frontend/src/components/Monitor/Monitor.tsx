import React, { useEffect, useState } from 'react';
import './Monitor.css';
import * as API from '../../service/api'

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

  const isTrueValue = (value: any) => {
    return value === true || value === 1 || value === '1';
  };

  const isFalseValue = (value: any) => {
    return value === false || value === 0 || value === '0';
  };

  const displayValue = (value: any) => {
    if (isTrueValue(value)) {
      return <span className="value-true">On</span>;
    } else if (isFalseValue(value)) {
      return <span className="value-false">Off</span>;
    }
    return value;
  };

  return (
    <div className="monitor">
      {error && <div>Error: {error}</div>}
      <table>
    <thead>
      <tr>
        <th>Sensor</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
    {sensorData.map((entry, index) => (
            <tr key={index}>
              <td>{entry.sensor}</td>
              <td>{displayValue(entry.Value)}</td>
            </tr>
          ))}
    </tbody>
  </table>
    </div>
  );
};

export default Monitor;
