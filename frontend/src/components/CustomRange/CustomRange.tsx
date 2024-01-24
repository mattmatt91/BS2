import React, { useState } from 'react';
import { Range } from 'react-range';
import './CustomRange.css'; // Import the CSS file

interface CustomRangeProps {
  min: number;
  max: number;
  onChange: (minValue: number, maxValue: number) => void;
}

const CustomRange: React.FC<CustomRangeProps> = ({ min, max, onChange }) => {
  const [values, setValues] = useState([min, max]);

  return (
    <div className="range-slider">
      <Range
        step={1}
        min={min}
        max={max}
        values={values}
        onChange={(newValues) => {
          setValues(newValues);
          onChange(newValues[0], newValues[1]);
        }}
        renderTrack={({ props, children }) => (
          <div
            {...props}
            className="range-slider-track"
            style={props.style}
          >
            {children}
          </div>
        )}
        renderThumb={({ props }) => (
          <div
            {...props}
            className="range-slider-thumb"
            style={props.style}
          />
        )}
      />
    </div>
  );
};

export default CustomRange;
