import React, { useEffect, useState } from 'react';
import './Preferences.css'; // Make sure this path is correct

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

  useEffect(() => {
    const fetchParameters = async () => {
      try {
        const response = await fetch('http://192.168.1.30:8000/parameter');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setParameters(data);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchParameters();
  }, []);

  const handleChange = async (paramName: string, newValue: boolean | number | string) => {
    try {
      const response = await fetch('http://192.168.1.30:8000/set_parameter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ parameter: paramName, value: newValue }),
      });
      console.log(JSON.stringify({ parameter: paramName, value: newValue }))
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

  return (
    <div className="preferences-container">
      <h2>Parameter Controls</h2>
      {parameters.map((param) => (
        <div className="preference-row" key={param.parameter}>
          <label className="preference-label">{param.parameter}:</label>
          <div className="preference-control">
            {renderControl(param, handleChange)}
          </div>
        </div>
      ))}
    </div>
  );
};

const renderControl = (param: Parameter, handleChange: Function) => {
  switch (param.datatype) {
    case 'Bool':
      return (
        <button onClick={() => handleChange(param.parameter, !param.value)}>
          {param.value.toString()}
        </button>
      );
    case 'Float':
    case 'Int':
      return (
        <input
          type="range"
          min={param.min_value}
          max={param.max_value}
          value={param.value as number}
          onChange={(e) => handleChange(param.parameter, parseFloat(e.target.value))}
        />
      );
    case 'String':
      return (
        <select 
          onChange={(e) => handleChange(param.parameter, e.target.value)} 
          value={param.value as string}
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
