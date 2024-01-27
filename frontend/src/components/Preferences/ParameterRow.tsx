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
    <>
      <div className="preference-row">
        <h2>

        <label className="preference-label">{param.parameter}:</label>
        </h2>
      </div>
      <div className="preference-row">
        <div className="preference-control">
          {renderControl(param, handleInputChange, currentValue)}
        </div>
      </div>
      <hr className="hr-divider" />
    </>
    </div>
  );

};


export default ParameterRow;
