import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const AuthPage = () => {
  const { pathname } = useLocation()
  const isSignup = pathname.includes('signup')
  const navigate = useNavigate()
  const { login, register } = useAuth()
  const [form, setForm] = useState({
    name: '', email: '', phone: '', country: '', state: '', password: '', role: 'user'
  })
  const [error, setError] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    try {
      if (isSignup) {
        await register(form)
      } else {
        await login(form.email, form.password)
      }
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.error || 'Request failed')
    }
  }

  return (
    <div className="mx-auto mt-16 max-w-lg px-4">
      <form onSubmit={submit} className="card space-y-4 p-6">
        <h2 className="text-2xl font-bold">{isSignup ? 'Create Account' : 'Login'}</h2>
        {error && <p className="rounded bg-rose-500/20 p-2 text-sm text-rose-300">{error}</p>}
        {isSignup && <input className="w-full rounded bg-slate-800 p-2" placeholder="Name" onChange={(e) => setForm({ ...form, name: e.target.value })} />}
        <input className="w-full rounded bg-slate-800 p-2" placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
        {isSignup && <input className="w-full rounded bg-slate-800 p-2" placeholder="Phone" onChange={(e) => setForm({ ...form, phone: e.target.value })} />}
        {isSignup && <input className="w-full rounded bg-slate-800 p-2" placeholder="Country" onChange={(e) => setForm({ ...form, country: e.target.value })} />}
        {isSignup && <input className="w-full rounded bg-slate-800 p-2" placeholder="State" onChange={(e) => setForm({ ...form, state: e.target.value })} />}
        <input className="w-full rounded bg-slate-800 p-2" type="password" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
        {isSignup && (
          <select className="w-full rounded bg-slate-800 p-2" onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        )}
        <button className="w-full rounded bg-brand-500 py-2 font-medium">{isSignup ? 'Sign Up' : 'Login'}</button>
      </form>
    </div>
  )
}

export default AuthPage
