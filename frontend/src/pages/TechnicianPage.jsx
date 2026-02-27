import { useEffect, useState } from 'react'
import api from '../services/api'

export default function TechnicianPage() {
  const [technicians, setTechnicians] = useState([])

  useEffect(() => {
    api.get('/technicians').then(({ data }) => setTechnicians(data)).catch(() => setTechnicians([]))
  }, [])

  return (
    <div className="p-6 grid md:grid-cols-2 gap-4">
      {technicians.map((tech) => (
        <article key={tech.id} className="bg-slate-900 p-4 rounded-xl">
          <p className="font-bold">{tech.name}</p>
          <p>{tech.service_type}</p>
          <p>{tech.experience} years</p>
          <p>Rating: {tech.rating || 'N/A'}</p>
        </article>
      ))}
    </div>
  )
}
