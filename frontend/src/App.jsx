// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import LandingPage from './LandingPage';
import OnboardClientPage from './OnboardClientPage';
import EditClientPage from './EditClientPage';
import DeleteClientPage from './DeleteClientPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/landingpage" element={<LandingPage />} />
        <Route path="/onboardclient" element={<OnboardClientPage />} />
        <Route path="/editclient" element={<EditClientPage />} />
        <Route path="/deleteclient" element={<DeleteClientPage />} />
      </Routes>
    </Router>
  );
};

export default App;