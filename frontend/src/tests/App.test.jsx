import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';

// Mock all the page components
vi.mock('./LoginPage', () => ({
  default: () => <div data-testid="login-page">Login Page</div>
}));

vi.mock('./LandingPage', () => ({
  default: () => <div data-testid="landing-page">Landing Page</div>
}));

vi.mock('./OnboardClientPage', () => ({
  default: () => <div data-testid="onboard-client-page">Onboard Client Page</div>
}));

vi.mock('./EditClientPage', () => ({
  default: () => <div data-testid="edit-client-page">Edit Client Page</div>
}));

vi.mock('./DeleteClientPage', () => ({
  default: () => <div data-testid="delete-client-page">Delete Client Page</div>
}));

// helper to set / clear fake JWT auth 
const setAuth = () => {
  localStorage.setItem('username', 'testuser');
  document.cookie = 'access_token_cookie=fake.jwt.token; Path=/'; 
};
const clearAuth = () => {
  localStorage.clear();
  document.cookie = 'access_token_cookie=; Max-Age=0; Path=/';
};

const renderWithRouter = (initialRoute = '/') =>
  render(
    <MemoryRouter initialEntries={[initialRoute]}>
      <App withRouter={false} />
    </MemoryRouter>
  );

beforeEach(() => setAuth());   //add auth before every test
afterEach(() => clearAuth());  //tidy up after each test

it('renders login page at root route /', () => {
  clearAuth();
  renderWithRouter('/');
  expect(screen.getByRole('heading', { name: 'Login' })).toBeInTheDocument();
});

it('renders landing page at /landingpage route', () => {
  renderWithRouter('/landingpage');
  expect(screen.getByText('Welcome to AssetProtect onboarding page!')).toBeInTheDocument();
});

it('renders onboard client page at /onboardclient route', () => {
  renderWithRouter('/onboardclient');
  expect(screen.getByText('Onboard new client')).toBeInTheDocument();
});

it('renders edit client page at /editclient route', () => {
  renderWithRouter('/editclient');
  expect(screen.getByText('Edit or Delete Client Data')).toBeInTheDocument();
});


/*describe('App Component', () => {
  // Helper function to render component with specific route
  const renderWithRouter = (initialRoute = '/') => {
    return render(
      <MemoryRouter initialEntries={[initialRoute]}>
        <App withRouter={false} />
      </MemoryRouter>
    );
  };

  it('renders login page at root route /', () => {
    renderWithRouter('/');
    expect(screen.getByRole('heading', { name: 'Login' })).toBeInTheDocument();
  });

  it('renders landing page at /landingpage route', () => {
    renderWithRouter('/landingpage');
    expect(screen.getByText('Welcome to AssetProtect onboarding page!')).toBeInTheDocument();
  });

  it('renders onboard client page at /onboardclient route', () => {
    renderWithRouter('/onboardclient');
    expect(screen.getByText('Onboard New Client')).toBeInTheDocument();
  });

  it('renders edit client page at /editclient route', () => {
    renderWithRouter('/editclient');
    expect(screen.getByText('Edit or Delete Client Data')).toBeInTheDocument();
  });

  it('renders delete client page at /deleteclient route', () => {
    renderWithRouter('/deleteclient');
    expect(screen.getByText('User List')).toBeInTheDocument();
    expect(screen.getByRole('table')).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: 'Delete' })).toBeTruthy();
  });

});*/