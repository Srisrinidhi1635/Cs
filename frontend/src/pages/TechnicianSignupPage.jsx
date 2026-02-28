import { useState } from 'react'
import api from '../services/api'

const TechnicianSignupPage = () => {
  const [form, setForm] = useState({ name: '', service_type: '', experience: '', city: '', lat: '', lng: '', contact: '', photo: '' })
  const [message, setMessage] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    const { data } = await api.post('/technicians', form)
    setMessage(data.message)
    setForm({ name: '', service_type: '', experience: '', city: '', lat: '', lng: '', contact: '', photo: '' })
  }

  return (
    <div className="mx-auto mt-10 max-w-xl px-4">
      <form onSubmit={submit} className="card space-y-3 p-6">
        <h2 className="text-2xl font-bold">Technician Registration</h2>
        {message && <p className="rounded bg-emerald-500/20 p-2 text-sm text-emerald-300">{message}</p>}
        {Object.keys(form).map((key) => (
          <input
            key={key}
            className="w-full rounded bg-slate-800 p-2"
            placeholder={key.replace('_', ' ')}
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          />
        ))}
        <button className="w-full rounded bg-brand-500 py-2">Submit</button>
      </form>
    </div>
  )
}

export default TechnicianSignupPage
