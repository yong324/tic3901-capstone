import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate(); 
  const [customers, setCustomers] = useState([]); // State to store customer data
  const [error, setError] = useState(''); // State to store error messages

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('http://localhost:5000/customers'); // Adjust URL to your API endpoint

        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        setCustomers(data); // Update customers state with the fetched data
      } catch (err) {
        console.error(err);
        setError('Failed to fetch customers. Please try again later.');
      }
    };

    fetchCustomers();
  }, []); // Empty dependency array to run only once on component mount

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
        <button>Edit existing client</button>
      </form>

      <form onSubmit={deleteClient} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
        <button>Delete existing client</button>
      </form>

      <h2 style={{ marginTop: '40px' }}>Customer List</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {customers.length > 0 ? (
        <table border="1" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((customer) => (
              <tr key={customer.id}>
                <td>{customer.id}</td>
                <td>{customer.name}</td>
                <td>{customer.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Loading customers...</p>
      )}
    </div>
  );
};

export default LandingPage;
