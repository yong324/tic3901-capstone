// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';
import LandingPage from './LandingPage';
import OnboardClientPage from './OnboardClientPage';
import EditClientPage from './EditClientPage';
import DeleteClientPage from './DeleteClientPage';

const App = ({ withRouter = true }) => {
  const AppRoutes = (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/landingpage" element={<LandingPage />} />
      <Route path="/onboardclient" element={<OnboardClientPage />} />
      <Route path="/editclient" element={<EditClientPage />} />
      <Route path="/deleteclient" element={<DeleteClientPage />} />
      <Route path="/register" element={<RegisterPage />} />
    </Routes>
  );

  // Only wrap in Router if withRouter is true
  return withRouter ? <Router>{AppRoutes}</Router> : AppRoutes;
};

export default App;