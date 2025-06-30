import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import LoginPage from '../LoginPage'

// Mock window.location
const mockLocation = {
  href: '',
}

Object.defineProperty(window, 'location', {
  value: mockLocation,
  writable: true,
})

// Mock fetch globally
global.fetch = vi.fn()

// Helper function to render with Router
const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  )
}

describe('LoginPage', () => {
  beforeEach(() => {
    // Clear mocks before each test
    vi.clearAllMocks()
    mockLocation.href = ''
  })

  it('renders login form correctly', () => {
    renderWithRouter(<LoginPage />)
    
    // Check if all form elements are present
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument()
  })

  it('updates input values when typing', () => {
    renderWithRouter(<LoginPage />)
    
    const usernameInput = screen.getByPlaceholderText('Username')
    const passwordInput = screen.getByPlaceholderText('Password')

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'testpass' } })

    expect(usernameInput.value).toBe('testuser')
    expect(passwordInput.value).toBe('testpass')
  })

  it('handles successful login', async () => {
    // Mock successful fetch response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ role: 'admin', username: 'testuser' })
    })

    renderWithRouter(<LoginPage />)
    
    // Fill in the form
    fireEvent.change(screen.getByPlaceholderText('Username'), { 
      target: { value: 'testuser' } 
    })
    fireEvent.change(screen.getByPlaceholderText('Password'), { 
      target: { value: 'testpass' } 
    })

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /login/i }))

    // Wait for async operations
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/login', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username: 'testuser', 
          password: 'testpass' 
        }),
      })
      expect(window.location.href).toBe('/landingpage')
    })
  })

  it('handles failed login', async () => {
    // Mock failed fetch response
    fetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({ message: 'Invalid credentials' })
    })

    renderWithRouter(<LoginPage />)
    
    // Fill in the form
    fireEvent.change(screen.getByPlaceholderText('Username'), { 
      target: { value: 'wronguser' } 
    })
    fireEvent.change(screen.getByPlaceholderText('Password'), { 
      target: { value: 'wrongpass' } 
    })

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /login/i }))

    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument()
    })
  })

})