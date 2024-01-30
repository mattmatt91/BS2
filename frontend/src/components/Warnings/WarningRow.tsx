import React from 'react';
import './WarningRow.css'; // Adjust the path as necessary


interface Warning {
  id: number;
  message: string;
  type: 'system' | 'hardware' | 'sensordata';
  isRead: boolean;
  timestamp: string;
}
interface WarningRowProps {
  warning: Warning;
  handleDelete: (warningId: number) => void;
}

const WarningRow: React.FC<WarningRowProps> = ({ warning, handleDelete }) => {
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
    <div className={`component-wrapper ${getWarningClass(warning.type)}`}>
      <div className="component-row">

        <div className="warning-message">
          {warning.message}
        </div>
        <div className="warning-timestamp">
          {warning.timestamp}
        </div>
        <div className="warning-action">
          <button className='button' onClick={() => handleDelete(warning.id)}>Delete</button>
        </div>
        <hr className="hr-divider" />
      </div>
    </div>
  );
};

export default WarningRow;
