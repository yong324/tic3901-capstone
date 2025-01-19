import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('')
    const navigate = useNavigate(); 

    const handleLogin = async (e) => {
      e.preventDefault();

      try {
          const response = await fetch('http://localhost:5173/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ username, password }),
          });

          const data = await response.json();

          if (response.ok) {
              setMessage(`Login successful! Role: ${data.role}, Customer ID: ${data.customers_id}`);
              // Optionally redirect or handle post-login logic
              window.location.href = "/dashboard";
          } else {
              setMessage(data.message);
          }
      } catch (error) {
          console.error('Error:', error);
          setMessage('An error occurred. Please try again later.');
      }
  };


    /*const handleLogin = (e) => {
        e.preventDefault();

        if (username == 'username' && password == 'password') {
            navigate('/landingpage')
        } else {
            setError('Invalid Username or Password');
        }
    };*/

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '50px' }}>
          <h1>Login</h1>
          <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ marginBottom: '10px', padding: '10px', fontSize: '16px' }}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ marginBottom: '10px', padding: '10px', fontSize: '16px' }}
            />
            <button type="submit" style={{ padding: '10px', fontSize: '16px' }}>Login</button>
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
          </form>
        </div>
      ); 
}
export default LoginPage;