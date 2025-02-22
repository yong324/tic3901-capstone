import React, { useState } from 'react';

const OnboardClientPage = () => {
  const [formData, setFormData] = useState({
    clientName: '',
    clientEmail: '',
    sftpUserName: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Helper: Update state when input values change
  const handleChange = ({ target: { name, value } }) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Helper: Show notifications
  const setNotification = (successMsg = '', errorMsg = '') => {
    setSuccess(successMsg);
    setError(errorMsg);
  };

  // Helper: Reusable API call
  const apiCall = async (url, method, body) => {
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Request failed');
    return data;
  };

  // Form submit handler
  const handleSubmit = async (e) => {
    e.preventDefault();
    setNotification();

    const payload = {
      clientName: formData.clientName,
      clientEmail: formData.clientEmail,
      sftpUserName: formData.sftpUserName,
    };

    try {
      const data = await apiCall('http://localhost:5000/client', 'POST', payload);
      setNotification(data.message); // Inline success message
      setFormData({ clientName: '', clientEmail: '', sftpUserName: '' }); // Reset form
    } catch (err) {
      setNotification('', `Failed to onboard client: ${err.message}`);
    }
  };

  // Helper: Render reusable input field
  const renderInput = (label, name, type = 'text') => (
    <>
      <label htmlFor={name} style={{ display: 'block', marginBottom: '5px' }}>
        {label}:
      </label>
      <input
        type={type}
        id={name}
        name={name}
        value={formData[name]}
        onChange={handleChange}
        style={{ width: '100%', padding: '8px', boxSizing: 'border-box', marginBottom: '10px' }}
      />
    </>
  );

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: 'auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2 style={{ textAlign: 'center' }}>Onboard New Client</h2>

      {renderInput('Client Name', 'clientName')}
      {renderInput('Client Email', 'clientEmail', 'email')}
      {renderInput('SFTP User Name', 'sftpUserName')}

      <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#4CAF50', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
        Onboard new client
      </button>

      {success && <p style={{ color: 'green', textAlign: 'center', marginTop: '10px' }}>{success}</p>}
      {error && <p style={{ color: 'red', textAlign: 'center', marginTop: '10px' }}>{error}</p>}
    </form>
  );
};

export default OnboardClientPage;
