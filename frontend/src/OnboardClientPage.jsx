import React, { useState } from 'react';

const OnboardClientPage = () => {
  const [formData, setFormData] = useState({
    clientName: '',
    clientEmail: '',
    sftpUserName: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Update state when input values change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const payload = {
      name: formData.clientName,
      email: formData.clientEmail,
      sftpUserName: formData.sftpUserName,
    };

    try {
      const response = await fetch('http://localhost:5000/customers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.message || 'Failed to onboard client.');
        alert(errorData.message || 'Failed to onboard client.');
      } else {
        const data = await response.json();
        setSuccess(data.message);
        alert(data.message || 'Client added successfully!');
        // Clear the form after success
        setFormData({ clientName: '', clientEmail: '', sftpUserName: '' });
      }
    } catch (err) {
      setError('An error occurred while onboarding the client.');
      alert('An error occurred while onboarding the client.');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '15px' }}>
      <label htmlFor="clientName" style={{ display: 'block', marginBottom: '5px' }}>
        Client Name:
      </label>
      <input
        type="text"
        id="clientName"
        name="clientName"
        value={formData.clientName}
        onChange={handleChange}
        style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
      />

      <label htmlFor="clientEmail" style={{ display: 'block', marginBottom: '5px' }}>
        Client Email:
      </label>
      <input
        type="email"
        id="clientEmail"
        name="clientEmail"
        value={formData.clientEmail}
        onChange={handleChange}
        style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
      />

      <label htmlFor="sftpUserName" style={{ display: 'block', marginBottom: '5px' }}>
        SFTP User Name:
      </label>
      <input
        type="text"
        id="sftpUserName"
        name="sftpUserName"
        value={formData.sftpUserName}
        onChange={handleChange}
        style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
      />

      <button type="submit" style={{ marginTop: '10px' }}>
        Onboard new client
      </button>

      {success && <p style={{ color: 'green' }}>{success}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  );
};

export default OnboardClientPage;
