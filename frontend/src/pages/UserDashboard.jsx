import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import ChatbotPanel from '../components/ChatbotPanel'
import api from '../services/api'

const UserDashboard = () => {
  const [service, setService] = useState('')
  const [technicians, setTechnicians] = useState([])

  useEffect(() => {
    if (!service) return
    api.get(`/technicians?service_type=${encodeURIComponent(service)}&lat=28.6139&lng=77.2090`).then(({ data }) => {
      setTechnicians(data)
    })
  }, [service])

  return (
    <div className="mx-auto grid max-w-6xl gap-6 px-4 py-8 lg:grid-cols-[260px_1fr]">
      <Sidebar />
      <div className="space-y-6">
        <ChatbotPanel onServiceDetected={setService} />
        <div className="card p-6">
          <h3 className="text-lg font-semibold">Recommended Technicians</h3>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            {technicians.map((tech) => (
              <div key={tech._id} className="rounded-xl border border-slate-800 p-4">
                <img src={tech.photo} className="h-32 w-full rounded-lg object-cover" />
                <p className="mt-3 font-semibold">{tech.name}</p>
                <p className="text-sm text-slate-400">{tech.service_type} • {tech.experience} yrs</p>
                <p className="text-sm text-slate-400">Distance: {tech.distance_km ?? 'N/A'} km</p>
                <p className="text-sm text-amber-400">⭐ {tech.rating}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default UserDashboard
