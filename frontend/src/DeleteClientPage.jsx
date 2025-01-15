import React from 'react';
import { useNavigate } from 'react-router-dom';

const DeleteClientPage = () => {
  const navigate = useNavigate(); 


  const mockUserData = [
    { id: 1, clientName: 'Client A', username: 'user_a', sftpUsername: 'sftp_user_a' },
    { id: 2, clientName: 'Client B', username: 'user_b', sftpUsername: 'sftp_user_b' },
    { id: 3, clientName: 'Client C', username: 'user_c', sftpUsername: 'sftp_user_c' },
  ];

    return (
    <div style={{ maxWidth: '600px', margin: 'auto', padding: '20px' }}>
        <h2>User List</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
            <tr>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>Client Name</th>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>Username</th>
            <th style={{ border: '1px solid #ccc', padding: '10px' }}>SFTP Username</th>
            </tr>
        </thead>
        <tbody>
            {mockUserData.map((user) => (
            <tr key={user.id}>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>{user.clientName}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>{user.username}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>{user.sftpUsername}</td>
                <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                    <button style={{ padding: '5px 10px', cursor: 'pointer' }}>Delete</button>
                </td>
            </tr>
            ))}
        </tbody>
        </table>
    </div>
    );
};

export default DeleteClientPage