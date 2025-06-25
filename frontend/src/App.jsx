import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, } from 'react-router-dom';
import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';
import LandingPage from './LandingPage';
import OnboardClientPage from './OnboardClientPage';
import EditClientPage from './EditClientPage';
import DeleteClientPage from './DeleteClientPage';


const PrivateRoute = ({ children }) => {
  const loggedIn = !!localStorage.getItem('username');
  return loggedIn ? children : <Navigate to="/" replace />;
};

const App = ({ withRouter = true }) => {
  const AppRoutes = (
    <Routes>
      <Route path="/"            element={<LoginPage />} />

      <Route path="/landingpage"
        element={
          <PrivateRoute>
            <LandingPage />
          </PrivateRoute>
        }
      />

      <Route path="/onboardclient"
        element={
          <PrivateRoute>
            <OnboardClientPage />
          </PrivateRoute>
        }
      />

      <Route path="/editclient"
        element={
          <PrivateRoute>
            <EditClientPage />
          </PrivateRoute>
        }
      />

      <Route path="/deleteclient"
        element={
          <PrivateRoute>
            <DeleteClientPage />
          </PrivateRoute>
        }
      />

      <Route path="/register"    element={<RegisterPage />} />
    </Routes>
  );

  // Only wrap in Router if withRouter is true
  return withRouter ? <Router>{AppRoutes}</Router> : AppRoutes;
};

export default App;