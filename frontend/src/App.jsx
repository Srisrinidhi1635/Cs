import { Link, Route, Routes } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import AdminPage from './pages/AdminPage'
import AuthPage from './pages/AuthPage'
import BookingPage from './pages/BookingPage'
import LandingPage from './pages/LandingPage'
import TechnicianPage from './pages/TechnicianPage'
import UserDashboard from './pages/UserDashboard'

export default function App() {
  return (
    <div className="min-h-screen p-4 md:p-8">
      <header className="flex justify-between items-center mb-6">
        <Link to="/" className="font-black text-2xl">🏠 Smart Home</Link>
        <Link className="text-cyan-300" to="/auth">Login / Sign Up</Link>
      </header>
      <div className="flex flex-col md:flex-row gap-4">
        <Sidebar />
        <main className="flex-1 bg-slate-900/40 rounded-2xl">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/auth" element={<AuthPage />} />
            <Route path="/dashboard" element={<UserDashboard />} />
            <Route path="/technicians" element={<TechnicianPage />} />
            <Route path="/bookings" element={<BookingPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}
