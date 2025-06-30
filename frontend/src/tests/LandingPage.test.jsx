import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LandingPage from '../LandingPage';
import {act} from 'react'

// Mock client data
const mockClients = [
  { client_id: 1, client_name: 'Test Client 1' },
  { client_id: 2, client_name: 'Test Client 2' }
];

// Mock navigation
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

// Mock fetch
global.fetch = vi.fn();

// Helper function to render with Router
const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

// Renders a component within Router and wraps it in React's act() for safe async updates
const renderWithAct = async (component) => {
  await act(async () => {
    renderWithRouter(component);
  });
};

describe('LandingPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();     // Reset fetch mock default response
    fetch.mockReset();
    localStorage.setItem('username', 'testuser');   // give a username for JWT
    fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([])
    });
  });


  it('renders welcome message and buttons', async () => {
    renderWithRouter(<LandingPage />);
    
    await waitFor(() => {
      // Check for welcome messages
      expect(
        screen.getByText((content, element) =>
          element.tagName.toLowerCase() === 'p' &&
          content.includes('You have successfully logged in as') &&
          element.textContent.includes('testuser')
        )
      ).toBeInTheDocument();
      expect(screen.getByText('Welcome to AssetProtect onboarding page!')).toBeInTheDocument();
      expect(screen.getByText("Please select what you'd like to do")).toBeInTheDocument();
      
      // Check for buttons
      expect(screen.getByText('Onboarding new client')).toBeInTheDocument();
      expect(screen.getByText('Edit Or Delete existing client')).toBeInTheDocument();
    });
  });

  it('logs out the user and navigates to login page', async () => {
    localStorage.setItem('username', 'testuser');

    // Spy on localStorage.removeItem
    const removeItemSpy = vi.spyOn(Storage.prototype, 'removeItem');

    // Mock fetch logout response
    fetch.mockResolvedValueOnce({ ok: true });

    await renderWithAct(<LandingPage />);

    const logoutButton = screen.getByText('Logout');
    fireEvent.submit(logoutButton.closest('form'));  // Simulate form submission

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/logout', {
        method: 'POST',
        credentials: 'include',
      });
      expect(removeItemSpy).toHaveBeenCalledWith('username');
      expect(mockNavigate).toHaveBeenCalledWith('/', { replace: true });
    });

    removeItemSpy.mockRestore();
  });



  //Removed as there is no more client table at Landing Page
  /*it('fetches client data on mount', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockClients)
    });

    renderWithRouter(<LandingPage />);

    // Verify fetch was called with correct URL
    expect(fetch).toHaveBeenCalledWith('http://localhost:5000/client_metadata', expect.objectContaining({
      credentials: 'include'
    }));

    
    // Wait for fetch to complete
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(1);
    });
  });*/

  /* re-look into this error
  it('handles fetch error gracefully', async () => {
    fetch.mockRejectedValueOnce(new Error('Failed to fetch'));

    renderWithRouter(<LandingPage />);

    await waitFor(() => {
      expect(screen.getByText('Failed to fetch clients. Please try again later.')).toBeInTheDocument();
    });
  });
    */

  it('navigates to onboard client page when clicking onboard button', async () => {
    await renderWithAct(<LandingPage />);
    
    const onboardButton = screen.getByText('Onboarding new client');
    fireEvent.click(onboardButton);
  
    expect(mockNavigate).toHaveBeenCalledWith('/onboardclient');
  });
  

  it('navigates to edit client page when clicking edit button', async () => {
    await renderWithAct(<LandingPage />);
    
    const editButton = screen.getByText('Edit Or Delete existing client');
    act(() => {fireEvent.click(editButton)});

    expect(mockNavigate).toHaveBeenCalledWith('/editclient');
  });

  /* re-look at how to configure unhappy paths
  it('handles unsuccessful API response', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      statusText: 'Not Found'
    });

    renderWithRouter(<LandingPage />);

    await waitFor(() => {
      expect(screen.getByText('Failed to fetch clients. Please try again later.')).toBeInTheDocument();
    });
  });
  */

  /*
  it('prevents default form submission behavior', () => {
    renderWithRouter(<LandingPage />);
    
    const onboardForm = screen.getByText('Onboarding new client').closest('form');
    const editForm = screen.getByText('Edit Or Delete existing client').closest('form');
    
    const preventDefault = vi.fn();
    
    fireEvent.submit(onboardForm, { preventDefault });
    expect(preventDefault).toHaveBeenCalled();
    
    fireEvent.submit(editForm, { preventDefault });
    expect(preventDefault).toHaveBeenCalled();
  });
  */
});