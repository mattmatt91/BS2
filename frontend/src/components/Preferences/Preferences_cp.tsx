import React, { useEffect, useState } from 'react';
import { Range } from 'react-range';
import './Preferences.css';
import * as API from '../../service/api';
import { debounce } from 'lodash';

interface Parameter {
  id: number;
  parameter: string;
  datatype: 'Bool' | 'Float' | 'Int' | 'String';
  value: boolean | number | string;
  min_value?: number;
  max_value?: number;
  entrys?: string[];
}

const ParameterComponent: React.FC = () => {
  const [parameters, setParameters] = useState<Parameter[]>([]);
  const [rangeValues, setRangeValues] = useState<{ [key: string]: number[] }>({});

  useEffect(() => {
    const fetchParameters = async () => {
      try {
        const response = await API.getPreferences()
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data)
        setParameters(data);
        const initialRangeValues = data.reduce((acc: any, param: Parameter) => {
          if (param.datatype === 'Float' || param.datatype === 'Int') {
            const minVal = param.min_value || 0;
            const maxVal = param.max_value || 1000; // Set a default high max value or use data from your API
            acc[param.parameter] = [Math.min(minVal, maxVal), Math.max(minVal, maxVal)];
          }
          return acc;
        }, {});
        setRangeValues(initialRangeValues);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchParameters();
  }, []);

  const handleRangeChange = async (paramName: string, newValues: number[]) => {
    setRangeValues({ ...rangeValues, [paramName]: newValues });
    console.log(paramName)
    console.log(newValues)
    // Implement your API call here to send new min and max values
    // newValues[0] is the min value and newValues[1] is the max value
    // Example: debouncedHandleChange(paramName, newValues[0], newValues[1]);
  };

  const debouncedHandleRangeChange = debounce(handleRangeChange, 1000);

  return (
    <div className="preferences-container">
      {parameters.map((param) => (
        <div className="preference-row" key={param.parameter}>
          <label className="preference-label">{param.parameter}:</label>
          <div className="preference-control">
            {renderControl(param, rangeValues[param.parameter] || [0, 100], debouncedHandleRangeChange)}
          </div>
        </div>
      ))}
    </div>
  );
};

const renderControl = (param: Parameter, rangeValues: number[], handleRangeChange: Function) => {
  switch (param.datatype) {
    case 'Bool':
      return (
        <button className='button' onClick={() => handleRangeChange(param.parameter, [Number(!param.value), Number(!param.value)])}>
          {param.value ? 'On' : 'Off'}
        </button>
      );
      case 'Float':
        case 'Int':
          const maxRangeValue = param.max_value || 1000;
          return (
            <div className="range-container">
              <Range
                values={rangeValues}
                step={1}
                min={0}
                max={100}
                onChange={(values: number[]) => handleRangeChange(param.parameter, values)}
                renderTrack={({ props, children }: { props: React.HTMLProps<HTMLDivElement>; children: React.ReactNode; }) => (
                  <div {...props} className="track" style={{...props.style}}>
                    {children}
                  </div>
                )}
                renderThumb={({ props }: { props: React.HTMLProps<HTMLDivElement>; }) => <div {...props} className="thumb" />}
              />
              <div className="range-values">
                <span>{rangeValues[0]}</span>
                <span>{rangeValues[1]}</span>
              </div>
            </div>
          );

    case 'String':
      return (
        <select
          onChange={(e) => handleRangeChange(param.parameter, [0, parseInt(e.target.value, 10)])}
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
