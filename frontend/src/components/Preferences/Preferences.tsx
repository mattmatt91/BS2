import React, { useEffect, useState } from 'react';
import './Preferences.css';
import * as API from '../../service/api';
import { debounce } from 'lodash';

interface Parameter {
  parameter: string;
  datatype: 'Bool' | 'Float' | 'Int' | 'String';
  value: boolean | number | string;
  min_value?: number;
  max_value?: number;
  entrys?: string[];
}

const ParameterComponent: React.FC = () => {
  const [parameters, setParameters] = useState<Parameter[]>([]);
  const [currentValues, setCurrentValues] = useState<{ [key: string]: boolean | number | string }>({});

  useEffect(() => {
    const fetchParameters = async () => {
      try {
        const response = await API.getPreferences()
        console.log(response)
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setParameters(data);
        setCurrentValues(data.reduce((acc: any, param: Parameter) => {
          if (param.datatype === 'Bool') {
            acc[param.parameter] = param.datatype === 'Bool' ? param.value === '1' : param.value;
          } else {
            acc[param.parameter] = param.value;
          }
          return acc;
        }, {}));
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchParameters();
  }, []);

  const handleChange = async (paramName: string, newValue: boolean | number | string) => {
    const apiUrl = process.env.REACT_APP_API_HOSTNAME;
    const endpoint = `${apiUrl}/set_parameter`;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ parameter: paramName, value: newValue }),
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

  const debouncedHandleChange = debounce(handleChange, 500);

  const handleInputChange = (paramName: string, newValue: boolean | number | string) => {
    setCurrentValues({ ...currentValues, [paramName]: newValue });
    debouncedHandleChange(paramName, newValue);
  };

  return (
    <div className="preferences-container">
      {parameters.map((param) => (
        <div className="preference-row" key={param.parameter}>
          <label className="preference-label">{param.parameter}:</label>
          <div className="preference-control">
            {renderControl(param, handleInputChange, currentValues[param.parameter])}
          </div>
        </div>
      ))}
    </div>
  );
};

const renderControl = (param: Parameter, handleInputChange: Function, currentValue: boolean | number | string) => {
  switch (param.datatype) {
    case 'Bool':
      return (
        <button className='button' onClick={() => handleInputChange(param.parameter, !param.value)}>
          {currentValue.toString()}
        </button>
      );
    case 'Float':
    case 'Int':
      return (
        <>
          <input
            type="range"
            min={param.min_value}
            max={param.max_value}
            value={currentValue as number}
            onChange={(e) => handleInputChange(param.parameter, parseFloat(e.target.value))}
          />
          <span>{currentValue}</span>
        </>
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
