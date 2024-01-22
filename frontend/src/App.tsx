// src/App.tsx
import React, { useEffect, useState } from 'react';
import './App.css';
import Header from './components/Header/Header';
import Monitor from './components/Monitor/Monitor';
import Data from './components/Data/Data';
import Preferences from './components/Preferences/Preferences';
import Video from './components/Video/Videos';
import Error from './components/Warnings/Warnings';
import Authentication from './components/Authentification/Authentification';
import {TOKEN_KEY} from './const'

const App: React.FC = () => {
  const [activeButton, setActiveButton] = useState(0);
  const [authToken, setAuthToken] = useState<string | null>(null);

  useEffect(()=>{
    if(authToken == undefined){
      setAuthToken(localStorage.getItem(TOKEN_KEY))
    }
  },[authToken])

  const handleLogin = (token: string) => {
    setAuthToken(token);
    // Optionally, store the token in local storage or context for further requests tetete
  };

  const renderMainContent = () => {
    if (!authToken) {
      return <Authentication onLogin={handleLogin} />;
    }

    switch (activeButton) {
      case 0:
        return <Monitor />;
      case 1:
        return <Data />;
      case 2:
        return <Preferences />;
      case 3:
        return <Video />;
      case 4:
        return <Error />;
      default:
        return null;
    }
  };

  return (
    <div className="app">
      {authToken && <Header activeButton={activeButton} onButtonClick={setActiveButton} />}
      <main className="main">{renderMainContent()}</main>
    </div>
  );
};

export default App;
