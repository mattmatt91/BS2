import React, { useEffect, useState } from 'react';
import './Monitor.css';

const Monitor: React.FC = () => {
  const [sensorData, setSensorData] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/sensor-data'); // Change to the actual API endpoint
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setSensorData(data);
        setError(null); // Clear any previous errors
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Error fetching data. Please try again.'); // Set an error message
      }
    };

    // Fetch data initially
    fetchData();

    // Set up a timer to fetch data every second
    const intervalId = setInterval(fetchData, 1000);

    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  // Function to convert boolean to "on" or "off"
  const displayValue = (value: any) => {
    if (typeof value === 'boolean') {
      return value ? 'on' : 'off';
    }
    return value;
  };

  return (
    <div className="monitor">
      <h2>Sensor Data</h2>
      {error && <div>Error: {error}</div>}
      <table>
        <thead>
          <tr>
            <th>Sensor</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {sensorData &&
            sensorData.map((entry, index) => (
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
