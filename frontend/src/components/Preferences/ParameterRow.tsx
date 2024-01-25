import React from 'react';
import { renderControl } from './Preferences'; // Adjust the path as necessary
import { Parameter } from './Preferences'; // Import Parameter interface

interface ParameterRowProps {
  param: Parameter;
  handleInputChange: Function;
  currentValue: boolean | number | string | { min: number; max: number };
}

const ParameterRow: React.FC<ParameterRowProps> = ({ param, handleInputChange, currentValue }) => {
  return (
    <>
      <div className="preference-row">
        <label className="preference-label">{param.parameter}:</label>
      </div>
      <div className="preference-row">
        <div className="preference-control">
          {renderControl(param, handleInputChange, currentValue)}
        </div>
      </div>
      <hr className="hr-divider" />
    </>
  );
};


export default ParameterRow;
