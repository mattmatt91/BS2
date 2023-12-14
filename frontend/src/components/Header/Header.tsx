// src/Header.tsx
import React from 'react';
import './Header.css';

interface HeaderProps {
  activeButton: number;
  onButtonClick: (buttonIndex: number) => void;
}

const Header: React.FC<HeaderProps> = ({ activeButton, onButtonClick }) => {
  const buttonLabels = ["Monitor", "Data", "Preferences", "Video"];

  return (
    <div className="header">
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
  );
};

export default Header;
