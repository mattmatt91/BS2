import React, { useEffect, useState } from 'react';
import './Preferences.css';
import * as API from '../../service/api';
import { debounce } from 'lodash';
import CustomRange from '../CustomRange/CustomRange'; // Adjust the path as necessary
import ParameterRow from './ParameterRow';

export interface Parameter {
  parameter: string;
  datatype: 'Bool' | 'Float' | 'Int' | 'String';
  value: boolean | number | string | { min: number; max: number };
  min_value?: number;
  max_value?: number;
  entrys?: string[];
}

const ParameterComponent: React.FC = () => {
  const [parameters, setParameters] = useState<Parameter[]>([]);
  const [currentValues, setCurrentValues] = useState<{ [key: string]: boolean | number | string }>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchParameters = async () => {
      try {
        const response = await API.getPreferences();
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data);
        setParameters(data);
        setError(null);
        setCurrentValues(data.reduce((acc: any, param: Parameter) => {
          if (param.datatype === 'Bool') {
            acc[param.parameter] = param.datatype === 'Bool' ? param.value === '1' : param.value;
          } else {
            acc[param.parameter] = param.value;
          }
          return acc;
        }, {}));
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Error fetching data. Please try again.');
      }
    };

    fetchParameters();
  }, []);

  const handleChange = async (paramName: string, newValue: boolean | number | string, minValue?: number, maxValue?: number) => {
    const apiUrl = process.env.REACT_APP_API_HOSTNAME;
    const endpoint = `${apiUrl}/set_parameter`;
    try {
      const token = localStorage.getItem('token');
      const body = minValue !== undefined && maxValue !== undefined
        ? { parameter: paramName, min: minValue, max: maxValue }
        : { parameter: paramName, value: newValue };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const errorBody = await response.text();
        console.error('Response error:', response.status, errorBody);
        throw new Error('Network response was not ok');
      }

      setParameters(currentParameters =>
        currentParameters.map(param =>
          param.parameter === paramName ? { ...param, value: newValue } : param
        )
      );

    } catch (error) {
      console.error('Error:', error);
    }
  };

  const debouncedHandleChange = debounce(handleChange, 1000);

  const handleInputChange = (paramName: string, newValue: boolean | number | string | number[]) => {
    if (Array.isArray(newValue)) {
      // For 'Float' and 'Int', newValue is an array [minValue, maxValue]
      const [minValue, maxValue] = newValue;
      setCurrentValues({ ...currentValues, [paramName]: `${minValue} - ${maxValue}` });
      debouncedHandleChange(paramName, minValue, maxValue); // Pass min and max as separate arguments
    } else {
      // For other types
      setCurrentValues({ ...currentValues, [paramName]: newValue });
      debouncedHandleChange(paramName, newValue);
    }
  };

  return (
    <div className="components-wrapper">
      {error && <div className="error-message">Error: {error}</div>}
      {parameters.map((param) => (
        <ParameterRow
          key={param.parameter}
          param={param}
          handleInputChange={handleInputChange}
          currentValue={currentValues[param.parameter]}
        />
      ))}
    </div>
  );
};
export const renderControl = (param: Parameter, handleInputChange: Function, currentValue: any) => {
  console.log(param)
  switch (param.datatype) {
    case 'Bool':
      return (
        <button className='button' onClick={() => handleInputChange(param.parameter, !param.value)}>
          {currentValue.toString()}
        </button>
      );
      case 'Float':
        case 'Int':
         // Convert min_value and max_value to numbers
         const minRange = parseFloat(param.min_value !== undefined ? param.min_value.toString() : '0') || 0;
         const maxRange = parseFloat(param.max_value !== undefined ? param.max_value.toString() : '100') || 100;


         const rangeValues = typeof currentValue === 'object' && currentValue !== null
           ? [currentValue.min, currentValue.max]
           : [minRange, maxRange];

         return (
           <CustomRange
             min={minRange}
             max={maxRange}
             values={rangeValues}
             onChange={(minValue, maxValue) => handleInputChange(param.parameter, { min: minValue, max: maxValue })}
           />
         );
    case 'String':
      return (
        <select
          onChange={(e) => handleInputChange(param.parameter, e.target.value)}
          value={currentValue as string}
        >
          {param.entrys?.map((entry) => (
            <option key={entry} value={entry}>{entry}</option>
          ))}
        </select>
      );
    default:
      return null;
  }
};

export default ParameterComponent;
