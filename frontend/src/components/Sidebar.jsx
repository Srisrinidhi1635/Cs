import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const Sidebar = () => {
  const { user, logout } = useAuth()

  return (
    <aside className="card h-fit p-5">
      <h2 className="text-xl font-bold text-brand-500">Smart Home Assistant</h2>
      <p className="mt-2 text-sm text-slate-400">{user?.name}</p>
      <nav className="mt-5 flex flex-col gap-2 text-sm">
        <Link className="rounded-lg px-3 py-2 hover:bg-slate-800" to="/dashboard">Dashboard</Link>
        <Link className="rounded-lg px-3 py-2 hover:bg-slate-800" to="/technicians">Technicians</Link>
        <Link className="rounded-lg px-3 py-2 hover:bg-slate-800" to="/bookings">Bookings</Link>
        {user?.role === 'admin' && (
          <Link className="rounded-lg px-3 py-2 hover:bg-slate-800" to="/admin">Admin</Link>
        )}
      </nav>
      <button className="mt-6 w-full rounded-lg bg-rose-500 px-4 py-2 text-sm" onClick={logout}>Logout</button>
    </aside>
  )
}

export default Sidebar
