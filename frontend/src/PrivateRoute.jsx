import { Navigate } from 'react-router-dom';

export default function PrivateRoute({ children }) {
  const loggedIn = !!localStorage.getItem('username');
  return loggedIn ? children : <Navigate to="/" replace />;
}
