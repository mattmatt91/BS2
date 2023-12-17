// src/components/Authentication/Authentication.tsx

import React, { useState, FormEvent } from 'react';

interface AuthenticationProps {
  onLogin: (token: string) => void;
}

const Authentication: React.FC<AuthenticationProps> = ({ onLogin }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Ensure this environment variable is set
    const endpoint = `${apiUrl}/token`;

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${username}&password=${password}`,
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem('token', data.access_token); // Store the token
        onLogin(data.access_token); // Invoke the onLogin callback
      } else {
        console.error('Login failed:', data.detail);
      }
    } catch (error) {
      console.error('Login request failed:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username" 
        />
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password" 
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Authentication;
