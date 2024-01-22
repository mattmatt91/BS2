// WarningsMonitor.tsx
import React, { useEffect, useState } from 'react';
import './Warnings.css';
import * as API from '../../service/api';

interface Warning {
  id: number;
  message: string;
  type: 'system' | 'hardware';
  isRead: boolean;
  timestamp: string;
}

const WarningsMonitor: React.FC = () => {
  const [warnings, setWarnings] = useState<Warning[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.getWarnings();

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data: Warning[] = await response.json();
        setWarnings(data);
        setError(null);
      } catch (error) {
        console.error('Error fetching warnings:', error);
        setError('Error fetching warnings. Please try again.');
      }
    };

    fetchData();
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
    return type === 'system' ? 'warning-system' : 'warning-hardware';
  };

  return (
    <div className="warnings-monitor">
      {error && <div className="error-message">Error: {error}</div>}
      <table>
        <thead>
          <tr>
            <th>Message</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {warnings.map((warning) => (
            <tr key={warning.id} className={getWarningClass(warning.type)}>
              <td>{warning.message}</td>
              <td>
                <button className='button' onClick={() => handleDelete(warning.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default WarningsMonitor;
