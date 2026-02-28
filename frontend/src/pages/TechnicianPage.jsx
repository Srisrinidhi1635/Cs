import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import api from '../services/api'

const TechnicianPage = () => {
  const [serviceType, setServiceType] = useState('')
  const [technicians, setTechnicians] = useState([])

  const fetchTechs = async () => {
    const query = serviceType ? `?service_type=${encodeURIComponent(serviceType)}&lat=28.6139&lng=77.2090` : '?lat=28.6139&lng=77.2090'
    const { data } = await api.get(`/technicians${query}`)
    setTechnicians(data)
  }

  useEffect(() => { fetchTechs() }, [])

  return (
    <div className="mx-auto grid max-w-6xl gap-6 px-4 py-8 lg:grid-cols-[260px_1fr]">
      <Sidebar />
      <div className="card p-6">
        <div className="mb-4 flex flex-wrap gap-3">
          <input className="rounded bg-slate-800 p-2" placeholder="Filter service type" value={serviceType} onChange={(e) => setServiceType(e.target.value)} />
          <button className="rounded bg-brand-500 px-4" onClick={fetchTechs}>Search</button>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {technicians.map((tech) => (
            <div key={tech._id} className="rounded-xl border border-slate-800 p-4">
              <p className="font-semibold">{tech.name}</p>
              <p className="text-sm">{tech.service_type}</p>
              <p className="text-sm">Experience: {tech.experience} years</p>
              <p className="text-sm">Distance: {tech.distance_km ?? 'N/A'} km</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default TechnicianPage
