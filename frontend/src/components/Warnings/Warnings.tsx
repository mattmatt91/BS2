// WarningsMonitor.tsx
import React, { useEffect, useState } from 'react';
import './Warnings.css';
import * as API from '../../service/api';
import WarningRow from './WarningRow'; // Adjust the path as necessary


interface Warning {
  id: number;
  message: string;
  type: 'system' | 'hardware'| 'sensordata';
  isRead: boolean;
  timestamp: string;
}

const WarningsMonitor: React.FC = () => {
  const [warnings, setWarnings] = useState<Warning[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWarnings = async () => {
      try {
        const response = await API.getWarnings();

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data: Warning[] = await response.json();
        console.log(data)
        setWarnings(data);
        setError(null);
      } catch (error) {
        console.error('Error fetching warnings:', error);
        setError('Error fetching warnings. Please try again.');
      }
    };

    fetchWarnings();
  }, []);

  const handleDelete = async (warningId: number) => {
    try {
      const response = await API.deleteWarning(warningId);
      if (!response.ok) {
        throw new Error('Error deleting warning');
      }
      setWarnings(warnings.filter(warning => warning.id !== warningId));
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const getWarningClass = (type: string) => {
    switch (type) {
      case 'system':
        return 'warning-system';
      case 'hardware':
        return 'warning-hardware';
      case 'sensordata':
        return 'warning-sensordata';
      default:
        return ''; // Default class or you can define a specific class for unknown types
    }
  };

  return (
    <div className="components-container">
      {error && <div className="error-message">Error: {error}</div>}
      {warnings.map((warning) => (
        <WarningRow key={warning.id} warning={warning} handleDelete={handleDelete} />
      ))}
    </div>
  );
};

export default WarningsMonitor;
