import React from 'react';
import './DisplayValue.css';

interface ValueDisplayRowProps {
  name: string;
  value: boolean | number;
}

const ValueDisplayRow: React.FC<ValueDisplayRowProps> = ({ name, value }) => {
  const isTrueValue = (value: any) => {
    return value === true || value === 1 || value === '1';
  };

  const isFalseValue = (value: any) => {
    return value === false || value === 0 || value === '0';
  };

  const displayValue = (value: boolean | number) => {
    if (isTrueValue(value)) {
      return <span className="value-true">On</span>;
    } else if (isFalseValue(value)) {
      return <span className="value-false">Off</span>;
    } else if (typeof value === 'number') {
      return value.toFixed(2); // Assuming float values need to be displayed with two decimal places
    }
    return value; // Fallback for any other cases
  };

  return (


    <div className="value-display-wrapper">
      <div className="value-display-row">
        <h2>
          <label className="value-display-label">{name}:</label>
        </h2>
      </div>
      <div className="value-display-row">
        <div className="value-display-content">
          {displayValue(value)}
        </div>
      </div>
      <hr className="hr-divider" />
    </div>
  );
};

export default ValueDisplayRow;
