import React from 'react';
import './Header.css';

interface HeaderProps {
  activeButton: number;  // Renamed from activeOption
  onButtonClick: (buttonIndex: number) => void;  // Renamed from onOptionChange
}

const Header: React.FC<HeaderProps> = ({ activeButton, onButtonClick }) => {
  const options = ["Monitor", "Data", "Preferences", "Video", "Warnings", "Test"];

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    onButtonClick(parseInt(event.target.value, 10));  // Renamed from onOptionChange
  };

  return (
    <div className="header">
      <img src="/logo.png" alt="Logo" className="logo" />
      <select className="dropdown" value={activeButton} onChange={handleChange}>
        {options.map((label, index) => (
          <option key={index} value={index}>
            {label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default Header;
