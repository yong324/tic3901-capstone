import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const EditClientPage = () => {
  const navigate = useNavigate();
  const [clients, setClients] = useState([]);
  const [editingClientId, setEditingClientId] = useState(null);
  const [editedClient, setEditedClient] = useState({});
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const clientNameInputRef = useRef(null);

  // Focus on the client name input when edit mode is enabled
  useEffect(() => {
    if (editingClientId !== null && clientNameInputRef.current) {
      clientNameInputRef.current.focus();
    }
  }, [editingClientId]);

  // Fetch all client metadata from backend
  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await fetch('http://localhost:5000/client_metadata'); // Update URL if needed
        if (!response.ok) {
          throw new Error('Failed to fetch client data');
        }
        const data = await response.json();
        setClients(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchClients();
  }, []);

  // Handler when clicking the Edit button
  const handleEditClick = (client) => {
    setEditingClientId(client.client_id);
    setEditedClient({ ...client });
    setError('');
    setSuccessMessage('');
  };

  // Handler for input changes in the editing row
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditedClient((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Handler to save the edited client data with a confirmation alert
  const handleSaveClick = async (client_id) => {
    // Check for duplicate client name in the local state
    if (editedClient.client_name) {
      const duplicate = clients.find(
        (client) =>
          client.client_name === editedClient.client_name &&
          client.client_id !== client_id
      );
      if (duplicate) {
        setError("Failed to edit: Client name must be unique. This client name already exists.");
        return; // Do not send the PUT request if duplicate exists
      }
    }

    // Confirmation alert before saving changes
    if (!window.confirm("Are you sure you want to save the changes?")) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/client/${client_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editedClient),
      });
      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch {
          errorData = { error: await response.text() };
        }
        throw new Error(
          errorData.error || errorData.message || 'Failed to update client data'
        );
      }
      // Update local state with new data
      setClients((prevClients) =>
        prevClients.map((client) =>
          client.client_id === client_id ? editedClient : client
        )
      );
      setEditingClientId(null);
      setSuccessMessage("Client updated successfully!");
      setError('');
    } catch (err) {
      setError("Failed to edit: " + err.message);
    }
  };

  // Handler to cancel editing
  const handleCancelClick = () => {
    setEditingClientId(null);
    setEditedClient({});
    setError('');
    setSuccessMessage('');
  };

  // Handler to delete a client record with a confirmation alert
  const handleDeleteClick = async (client_id) => {
    // Confirmation alert before deleting
    if (!window.confirm("Are you sure you want to delete this client?")) {
      return;
    }

    setError('');
    setSuccessMessage('');
    try {
      const response = await fetch(`http://localhost:5000/client/${client_id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch {
          errorData = { error: await response.text() };
        }
        throw new Error(
          errorData.error || errorData.message || 'Failed to delete client data'
        );
      }
      // Remove deleted client from local state
      setClients((prevClients) =>
        prevClients.filter((client) => client.client_id !== client_id)
      );
      setSuccessMessage("Client deleted successfully!");
    } catch (err) {
      setError("Failed to delete: " + err.message);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: 'auto', padding: '20px' }}>
      <h2>Edit or Delete Client Data</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>Client ID</th>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>Client Name</th>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>Email</th>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>Permissions</th>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>Added Datetime</th>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {[...clients]
            .sort((a, b) => a.client_id - b.client_id)
            .map((client) => (
              <tr key={client.client_id}>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                  {client.client_id}
                </td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                  {editingClientId === client.client_id ? (
                    <input
                      type="text"
                      name="client_name"
                      ref={clientNameInputRef}
                      value={editedClient.client_name || ''}
                      onChange={handleInputChange}
                    />
                  ) : (
                    client.client_name
                  )}
                </td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                  {editingClientId === client.client_id ? (
                    <input
                      type="email"
                      name="email"
                      value={editedClient.email || ''}
                      onChange={handleInputChange}
                    />
                  ) : (
                    client.email
                  )}
                </td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                  {editingClientId === client.client_id ? (
                    <input
                      type="text"
                      name="permissions"
                      value={editedClient.permissions || ''}
                      onChange={handleInputChange}
                    />
                  ) : (
                    client.permissions
                  )}
                </td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                  {new Date(client.added_datetime).toLocaleString()}
                </td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                  {editingClientId === client.client_id ? (
                    <div style={{ display: 'flex', gap: '10px' }}>
                      <button type="button" onClick={() => handleSaveClick(client.client_id)}>
                        Save
                      </button>
                      <button type="button" onClick={handleCancelClick}>
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div style={{ display: 'flex', gap: '10px' }}>
                      <button type="button" onClick={() => handleEditClick(client)}>
                        Edit
                      </button>
                      <button type="button" onClick={() => handleDeleteClick(client.client_id)}>
                        Delete
                      </button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default EditClientPage;
