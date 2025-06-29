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
    fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([])
    });
  });


  it('renders welcome message and buttons', async () => {
    renderWithRouter(<LandingPage />);
    
    await waitFor(() => {
      // Check for welcome messages
      expect(screen.getByText('You have successfully logged in.')).toBeInTheDocument();
      expect(screen.getByText('Welcome to AssetProtect onboarding page!')).toBeInTheDocument();
      expect(screen.getByText("Please select what you'd like to do")).toBeInTheDocument();
      
      // Check for buttons
      expect(screen.getByText('Onboarding new client')).toBeInTheDocument();
      expect(screen.getByText('Edit Or Delete existing client')).toBeInTheDocument();
    });
  });

  it('fetches client data on mount', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockClients)
    });

    renderWithRouter(<LandingPage />);

    // Verify fetch was called with correct URL
    expect(fetch).toHaveBeenCalledWith('http://undefined:5000/client_metadata');
    
    // Wait for fetch to complete
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(1);
    });
  });

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