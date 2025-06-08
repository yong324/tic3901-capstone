import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isSuccess, setIsSuccess] = useState(false);
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();

        if (password.length <= 6) {
            setIsSuccess(false);
            setMessage('Password must be more than 6 characters.');
            return;
        }

        if (password !== confirmPassword) {
            setIsSuccess(false);
            setMessage('Passwords do not match.');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                setIsSuccess(true);
                setMessage('Registration successful. Redirecting to login...');
                setTimeout(() => navigate('/'), 2000);
            } else {
                setIsSuccess(false);
                setMessage(data.message || 'Registration failed.');
            }
        } catch (err) {
            console.error('Error:', err);
            setIsSuccess(false);
            setMessage('An error occurred. Please try again later.');
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '50px' }}>
            <h1>Register</h1>
            <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    autoFocus
                    style={{ marginBottom: '10px', padding: '10px', fontSize: '16px' }}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    style={{ marginBottom: '10px', padding: '10px', fontSize: '16px' }}
                />
                <input
                    type="password"
                    placeholder="Confirm Password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    style={{ marginBottom: '10px', padding: '10px', fontSize: '16px' }}
                />
                <button type="submit" style={{ padding: '10px', fontSize: '16px' }}>Register</button>
                {message && (
                    <p style={{ marginTop: '10px', color: isSuccess ? 'green' : 'red' }}>
                        {message}
                    </p>
                )}
            </form>
        </div>
    );
};

export default RegisterPage;
