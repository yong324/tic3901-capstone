import React from 'react';
import { useNavigate } from 'react-router-dom';

const OnboardClientPage = () => {
  const navigate = useNavigate(); 

    return (
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="clientName" style={{ display: 'block', marginBottom: '5px' }}>Client Name:</label>
        <input
          type="text"
          id="clientName"
          name="clientName"
          style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
        />

      <label htmlFor="clientName" style={{ display: 'block', marginBottom: '5px' }}>Client Email:</label>
        <input
          type="text"
          id="clientName"
          name="clientName"
          style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
        />

      <label htmlFor="clientName" style={{ display: 'block', marginBottom: '5px' }}>SFTP User Name:</label>
        <input
          type="text"
          id="clientName"
          name="clientName"
          style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
        />

      <button>Onboard new client</button>
      </div>
      );
};

export default OnboardClientPage
