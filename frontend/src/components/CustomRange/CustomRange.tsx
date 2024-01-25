import React, { useState, useEffect, useCallback } from 'react';
import { Range } from 'react-range';
import './CustomRange.css'; // Import the CSS file
import { debounce } from 'lodash';


interface CustomRangeProps {
  min: number;
  max: number;
  values: number[];
  onChange: (minValue: number, maxValue: number) => void;
}


const CustomRange: React.FC<CustomRangeProps> = ({ min, max, values, onChange }) => {
  const [rangeValues, setRangeValues] = useState<number[]>(values);

  const debouncedOnChange = useCallback(
    debounce((minValue: number, maxValue: number) => {
      onChange(minValue, maxValue);
    }, 1000), // 500ms delay
    [] // Dependencies array
  );

  useEffect(() => {
    setRangeValues(values);
  }, [values]);

  const handleRangeChange = (newValues: number[]) => {
    setRangeValues(newValues);
    debouncedOnChange(newValues[0], newValues[1]);
  };

  return (
    <div className="range-slider">
      <Range
        step={1}
        min={min}
        max={max}
        values={rangeValues}
        onChange={handleRangeChange}
        renderTrack={({ props, children }) => (
          <div {...props} className="range-slider-track" style={props.style}>
            {children}
          </div>
        )}
        renderThumb={({ props }) => (
          <div {...props} className="range-slider-thumb" style={props.style} />
        )}
      />
    </div>
  );
};

export default CustomRange;
