export function getData(){

    const token = localStorage.getItem('token'); // Retrieve the stored token
    const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Read the environment variable
    const endpoint = `${apiUrl}/data`; // Use a template string to create the endpoint

    return fetch(endpoint, {
        headers: {
          'Authorization': `Bearer ${token}` // Include the token in the request
        }
      });
}

export function getMonitor(){

  const token = localStorage.getItem('token'); // Retrieve the stored token
  const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Read the environment variable
  const endpoint = `${apiUrl}/sensor-data`; // Use a template string to create the endpoint

  return fetch(endpoint, {
    headers: {
      'Authorization': `Bearer ${token}` // Include the token in the request
    }
  });
}


export function getPreferences(){
  const token = localStorage.getItem('token'); // Retrieve the stored token
  const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Read the environment variable
  const endpoint = `${apiUrl}/parameter`; // Use a template string to create the endpoint
  return fetch(endpoint, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

export function getWarnings(){
  const token = localStorage.getItem('token'); // Retrieve the stored token
  const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Read the environment variable
  const endpoint = `${apiUrl}/warnings`; // Use a template string to create the endpoint
  return fetch(endpoint, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

export function deleteWarning(warningId: number) {
  const token = localStorage.getItem('token');
  const apiUrl = process.env.REACT_APP_API_HOSTNAME;
  const endpoint = `${apiUrl}/warnings/${warningId}`;
  return fetch(endpoint, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

export function getImage(){
  const token = localStorage.getItem('token');
  const apiUrl = process.env.REACT_APP_API_HOSTNAME; // Read the environment variable
  const endpoint = `${apiUrl}/video`; // Use a template string to create the endpoint
  return fetch(endpoint, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}
