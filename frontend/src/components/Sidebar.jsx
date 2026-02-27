import { Link } from 'react-router-dom'

export default function Sidebar() {
  return (
    <aside className="w-full md:w-64 bg-slate-900 p-4 rounded-2xl">
      <h2 className="text-xl font-bold mb-4">Dashboard</h2>
      <nav className="space-y-2 text-sm">
        <Link className="block hover:text-cyan-300" to="/dashboard">User Dashboard</Link>
        <Link className="block hover:text-cyan-300" to="/technicians">Technicians</Link>
        <Link className="block hover:text-cyan-300" to="/bookings">Bookings</Link>
        <Link className="block hover:text-cyan-300" to="/admin">Admin</Link>
      </nav>
    </aside>
  )
}
