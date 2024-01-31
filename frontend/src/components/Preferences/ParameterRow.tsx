import React from 'react';
import { renderControl } from './Preferences'; // Adjust the path as necessary
import { Parameter } from './Preferences'; // Import Parameter interface
import './ParameterRow.css';

interface ParameterRowProps {
  param: Parameter;
  handleInputChange: Function;
  currentValue: boolean | number | string | { min: number; max: number };
}

const ParameterRow: React.FC<ParameterRowProps> = ({ param, handleInputChange, currentValue }) => {
  return (

    <div className="component-wrapper">
      <div className="component-row">
        <label className="component-label">{param.parameter}:</label>
        <div className="component-control">
          {renderControl(param, handleInputChange, currentValue)}
        </div>
      </div>
      <hr className="hr-divider" />
    </div>
  );

};


export default ParameterRow;
