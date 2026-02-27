import { useState } from 'react'
import api, { setAuthToken } from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function AuthPage() {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ name: '', email: '', phone: '', country: '', state: '', password: '' })
  const { login } = useAuth()

  const submit = async (e) => {
    e.preventDefault()
    const url = mode === 'login' ? '/auth/login' : '/auth/register'
    const { data } = await api.post(url, form)
    login(data)
    setAuthToken(data.token)
  }

  return (
    <form onSubmit={submit} className="max-w-md mx-auto my-10 p-6 bg-slate-900 rounded-2xl space-y-3">
      <h2 className="text-2xl font-bold">{mode === 'login' ? 'Login' : 'Sign Up'}</h2>
      {mode === 'register' && <input className="w-full p-2 bg-slate-800 rounded" placeholder="Name" onChange={(e) => setForm({ ...form, name: e.target.value })} />}
      <input className="w-full p-2 bg-slate-800 rounded" placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
      {mode === 'register' && <input className="w-full p-2 bg-slate-800 rounded" placeholder="Phone" onChange={(e) => setForm({ ...form, phone: e.target.value })} />}
      {mode === 'register' && <input className="w-full p-2 bg-slate-800 rounded" placeholder="Country" onChange={(e) => setForm({ ...form, country: e.target.value })} />}
      {mode === 'register' && <input className="w-full p-2 bg-slate-800 rounded" placeholder="State" onChange={(e) => setForm({ ...form, state: e.target.value })} />}
      <input type="password" className="w-full p-2 bg-slate-800 rounded" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <button className="w-full bg-cyan-500 p-2 rounded">Continue</button>
      <button type="button" className="text-sm text-cyan-300" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>Switch to {mode === 'login' ? 'sign up' : 'login'}</button>
    </form>
  )
}
