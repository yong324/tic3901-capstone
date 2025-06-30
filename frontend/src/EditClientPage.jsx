import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCsrfToken } from './csrf';   

const EditClientPage = () => {
  const navigate = useNavigate();
  const [clients, setClients] = useState([]);
  const [editingClientId, setEditingClientId] = useState(null);
  const [editedClient, setEditedClient] = useState({});
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const clientNameInputRef = useRef(null);
  const backendIp = import.meta.env.VITE_BACKEND_IP;

  useEffect(() => {
    if (editingClientId !== null && clientNameInputRef.current) {
      clientNameInputRef.current.focus();
    }
  }, [editingClientId]);

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const res = await fetch(`http://${backendIp}:5000/client_metadata`, {
          credentials: 'include'              //send JWT cookies
        });

        if (res.status === 401) {             //unauthenticated, redirect to login
          navigate('/', { replace: true });
          return;
        }
        if (!res.ok) throw new Error('Failed to fetch client data');
        setClients(await res.json());
      } catch (err) {
        setError(err.message);
      }
    };

    fetchClients();
  }, [navigate], [backendIp]);
  
  const setNotification = (success = '', err = '') => {
    setSuccessMessage(success);
    setError(err);
  };

  const handleEditClick = (client) => {
    setEditingClientId(client.client_id);
    setEditedClient({ ...client });
    setNotification();
  };

  const handleInputChange = ({ target: { name, value } }) => {
    setEditedClient((prev) => ({ ...prev, [name]: value }));
  };

  const isDuplicateClientName = (client_id) => {
    const duplicate = clients.find(
      (c) => c.client_name === editedClient.client_name && c.client_id !== client_id
    );
    if (duplicate) {
      setError('Failed to edit: Client name must be unique. This client name already exists.');
      return true;
    }
    return false;
  };

  const apiCall = async (url, method, body = null) => {
    const options = {
      method,
      credentials: 'include',               // include JWT cookies
      headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': getCsrfToken() },
      ...(body && { body: JSON.stringify(body) }),
    };

    const res = await fetch(url, options);

    if (res.status === 401) {               // token expired, redirect to login
      navigate('/', { replace: true });
      throw new Error('Unauthenticated');
    }
    if (!res.ok) {
      const errData = await res.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(errData.error || errData.message || 'Operation failed');
    }
    return res.json();
  };

  const handleSaveClick = async (client_id) => {
    if (isDuplicateClientName(client_id)) return;
    if (!window.confirm('Are you sure you want to save the changes?')) return;

    try {
      await apiCall(`http://${backendIp}:5000/client/${client_id}`, 'PUT', editedClient);
      setClients((prev) =>
        prev.map((c) => (c.client_id === client_id ? editedClient : c))
      );
      setEditingClientId(null);
      setNotification('Client updated successfully!');
    } catch (err) {
      setError(`Failed to edit: ${err.message}`);
    }
  };

  const handleCancelClick = () => {
    setEditingClientId(null);
    setEditedClient({});
    setNotification();
  };

  const handleDeleteClick = async (client_id) => {
    if (!window.confirm('Are you sure you want to delete this client?')) return;

    try {
      await apiCall(`http://${backendIp}:5000/client/${client_id}`, 'DELETE');
      setClients((prev) => prev.filter((c) => c.client_id !== client_id));

      setNotification('Client deleted successfully!');
    } catch (err) {
      setError(`Failed to delete: ${err.message}`);
    }
  };

  const renderInputOrText = (client, fieldName, type = 'text') => (
    editingClientId === client.client_id ? (
      <input
        type={type}
        name={fieldName}
        ref={fieldName === 'client_name' ? clientNameInputRef : null}
        value={editedClient[fieldName] || ''}
        onChange={handleInputChange}
        style={{ width: '100%', padding: '5px', boxSizing: 'border-box', whiteSpace: 'nowrap', overflow: 'hidden' }}
      />
    ) : (
      <div style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
        {client[fieldName]}
      </div>
    )
  );

  const columnWidths = ['8%', '10%', '18%', '10%', '15%', '13%', '15%', '11%'];

  return (
    <div style={{ maxWidth: '1600px', margin: 'auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2 style={{ textAlign: 'center' }}>Edit or Delete Client Data</h2>
      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
      {successMessage && <p style={{ color: 'green', textAlign: 'center' }}>{successMessage}</p>}
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px', tableLayout: 'fixed' }}>
      <thead>
        <tr>
          {['Client ID', 'Client Name', 'Email', 'Permissions', 'SFTP Username', 'SFTP Directory', 'Added Datetime', 'Actions'].map((header, index) => (
            <th
              key={header}
              style={{
                width: columnWidths[index],
                border: '1px solid #ccc',
                padding: '10px',
                backgroundColor: '#e0e0e0',
                color: '#333',
                textAlign: 'left',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
              }}
            >
              {header}
            </th>
          ))}
        </tr>
      </thead>
        <tbody>
          {[...clients]
            .sort((a, b) => a.client_id - b.client_id)
            .map((client) => (
              <tr key={client.client_id}>
                <td style={{ border: '1px solid #ccc', padding: '10px', whiteSpace: 'nowrap' }}>{client.client_id}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>{renderInputOrText(client, 'client_name')}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>{renderInputOrText(client, 'email', 'email')}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>{renderInputOrText(client, 'permissions')}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>{renderInputOrText(client, 'sftp_username')}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>{renderInputOrText(client, 'sftp_directory')}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px', whiteSpace: 'nowrap' }}>{new Date(client.added_datetime).toLocaleString()}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                  <div style={{ display: 'flex', gap: '5px', whiteSpace: 'nowrap' }}>
                    {editingClientId === client.client_id ? (
                      <>
                        <button
                          type="button"
                          onClick={() => handleSaveClick(client.client_id)}
                          style={{ backgroundColor: '#4CAF50', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '5px', cursor: 'pointer' }}
                        >
                          Save
                        </button>
                        <button
                          type="button"
                          onClick={handleCancelClick}
                          style={{ backgroundColor: '#808080', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '5px', cursor: 'pointer' }}
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          type="button"
                          onClick={() => handleEditClick(client)}
                          style={{ backgroundColor: '#008CBA', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '5px', cursor: 'pointer' }}
                        >
                          Edit
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDeleteClick(client.client_id)}
                          style={{ backgroundColor: '#FF0000', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '5px', cursor: 'pointer' }}
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default EditClientPage;
