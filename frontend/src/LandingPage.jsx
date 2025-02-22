import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate();
  const [clients, setClients] = useState([]); // Renamed state variable to clients
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await fetch('http://localhost:5000/client_metadata'); // Updated endpoint

        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        setClients(data); // Update state with the fetched client metadata
      } catch (err) {
        console.error(err);
        setError('Failed to fetch clients. Please try again later.');
      }
    };

    fetchClients();
  }, []);

  const onBoardClient = (e) => {
    e.preventDefault();
    navigate('/onboardclient');
  };

  const editClient = (e) => {
    e.preventDefault();
    navigate('/editclient');
  };

  const deleteClient = (e) => {
    e.preventDefault();
    navigate('/deleteclient');
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', padding: '20px' }}>
      <p>You have successfully logged in.</p>
      <h1 style={{ textAlign: 'center' }}>Welcome to AssetProtect onboarding page!</h1>
      <p>Please select what you'd like to do</p>

      <form onSubmit={onBoardClient} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
        <button>Onboarding new client</button>
      </form>

      <form onSubmit={editClient} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
        <button>Edit Or Delete existing client</button>
      </form>

      <h2 style={{ marginTop: '40px' }}>Client List</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {clients.length > 0 ? (
        <table border="1" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
          <thead>
            <tr>
              <th>Client ID</th>
              <th>Client Name</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {clients.map((client) => (
              <tr key={client.client_id}>
                <td>{client.client_id}</td>
                <td>{client.client_name}</td>
                <td>{client.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Loading clients...</p>
      )}
    </div>
  );
};

export default LandingPage;
