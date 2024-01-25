import React from 'react';
import CustomRange from '../CustomRange/CustomRange';

const Test: React.FC = () => {
  const handleRangeChange = (minValue: number, maxValue: number) => {
    console.log('Range values:', minValue, maxValue);
  };

  return (
    <div>
      <h2>Custom Range Slider</h2>
      <CustomRange min={10} max={200} values={[30, 100]} onChange={handleRangeChange} />
    </div>
  );
};

export default Test;
