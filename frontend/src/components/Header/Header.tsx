import React from 'react';
import './Header.css';

interface HeaderProps {
  activeButton: number;
  onButtonClick: (buttonIndex: number) => void;
}

const Header: React.FC<HeaderProps> = ({ activeButton, onButtonClick }) => {
  const buttonLabels = ["Monitor", "Data", "Preferences", "Video", "Errors"];

  return (
    <div className="header">
      <img src="/logo.png" alt="Logo" className="logo" />
      <div className="buttons-container">
        {buttonLabels.map((label, index) => (
          <button
            key={index}
            className={`button ${activeButton === index ? 'active' : ''}`}
            onClick={() => onButtonClick(index)}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Header;
