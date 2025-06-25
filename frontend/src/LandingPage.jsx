import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');  // retrieve username

  const onBoardClient = (e) => {
    e.preventDefault();
    navigate('/onboardclient');
  };

  const editClient = (e) => {
    e.preventDefault();
    navigate('/editclient');
  };

  const handleLogout = async () => {
    try {
      await fetch('http://localhost:5000/logout', {
        method: 'POST',
        credentials: 'include'
      });
    } catch (err) {
      console.warn('Logout request failed, clearing client state anyway');
    }
    localStorage.removeItem('username');
    navigate('/', { replace: true });
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', padding: '20px' }}>
      <p>You have successfully logged in as <strong>{username}</strong>.</p>
      <h1 style={{ textAlign: 'center' }}>Welcome to AssetProtect onboarding page!</h1>
      <p>Please select what you'd like to do</p>

      <form onSubmit={onBoardClient} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
        <button>Onboarding new client</button>
      </form>

      <form onSubmit={editClient} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
        <button>Edit Or Delete existing client</button>
      </form>
      
      <form onSubmit={handleLogout} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
        <button style={{ backgroundColor: '#b30000', color: 'white' }}>Logout</button>
      </form>
    </div>
  );
};

export default LandingPage;
