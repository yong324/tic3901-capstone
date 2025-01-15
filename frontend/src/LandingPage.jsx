import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate(); 

  const onBoardClient = (e) => {
    e.preventDefault();
    navigate('/onboardclient');
  };

  const editClient = (e) => {
    e.preventDefault();
    navigate('/editclient');
  };

  const deleteClient = (e) => {
    e.preventDefault();
    navigate('/deleteclient');
  };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', flexDirection: 'column' }}>
          <p>You have successfully logged in.</p>
          <h1 style={{textAlign:'center'}}>Welcome to AssetProtect onboarding page!</h1>
          <p>Please select what you'd like to do</p>

          <form onSubmit={onBoardClient} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
            <button>Onboarding new client</button>
          </form>

          <form onSubmit={editClient} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
          <button>Edit existing client</button>
          </form>
          
          <form onSubmit={deleteClient} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
          <button>Delete existing client</button>
          </form>
        </div>
      );
};

export default LandingPage
