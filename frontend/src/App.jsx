import { Navigate, Route, Routes } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import AuthPage from './pages/AuthPage'
import UserDashboard from './pages/UserDashboard'
import TechnicianPage from './pages/TechnicianPage'
import BookingPage from './pages/BookingPage'
import AdminPage from './pages/AdminPage'
import TechnicianSignupPage from './pages/TechnicianSignupPage'
import { useAuth } from './contexts/AuthContext'

const Protected = ({ children }) => {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return children
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<AuthPage />} />
      <Route path="/signup" element={<AuthPage />} />
      <Route path="/technician-signup" element={<TechnicianSignupPage />} />
      <Route path="/dashboard" element={<Protected><UserDashboard /></Protected>} />
      <Route path="/technicians" element={<Protected><TechnicianPage /></Protected>} />
      <Route path="/bookings" element={<Protected><BookingPage /></Protected>} />
      <Route path="/admin" element={<Protected><AdminPage /></Protected>} />
    </Routes>
  )
}

export default App
