import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import api from '../services/api'

const AdminPage = () => {
  const [data, setData] = useState(null)

  const fetchDashboard = () => api.get('/admin/dashboard').then((res) => setData(res.data))

  useEffect(() => { fetchDashboard() }, [])

  const toggleApproval = async (id, approved) => {
    await api.patch(`/technicians/${id}/approve`, { approved })
    fetchDashboard()
  }

  if (!data) return <div className="p-8">Loading...</div>

  return (
    <div className="mx-auto grid max-w-6xl gap-6 px-4 py-8 lg:grid-cols-[260px_1fr]">
      <Sidebar />
      <div className="space-y-6">
        <div className="grid gap-4 sm:grid-cols-3">
          <div className="card p-4">Users: {data.counts.users}</div>
          <div className="card p-4">Technicians: {data.counts.technicians}</div>
          <div className="card p-4">Bookings: {data.counts.bookings}</div>
        </div>
        <div className="card p-6">
          <h3 className="mb-3 text-lg font-semibold">Technician Approval Queue</h3>
          <div className="space-y-2">
            {data.technicians.map((tech) => (
              <div key={tech._id} className="flex items-center justify-between rounded border border-slate-800 p-3">
                <div>
                  <p>{tech.name} ({tech.service_type})</p>
                  <p className="text-sm text-slate-400">{tech.contact}</p>
                </div>
                <div className="space-x-2">
                  <button className="rounded bg-emerald-500 px-3 py-1" onClick={() => toggleApproval(tech._id, true)}>Approve</button>
                  <button className="rounded bg-rose-500 px-3 py-1" onClick={() => toggleApproval(tech._id, false)}>Reject</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminPage
