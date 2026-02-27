import { motion } from 'framer-motion'
import { useState } from 'react'
import api from '../services/api'

export default function LandingPage() {
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState(null)

  const submit = async () => {
    try {
      const { data } = await api.post('/chatbot/match', { message, latitude: 28.6139, longitude: 77.209 })
      setResponse(data)
    } catch {
      setResponse({ error: 'Please login first to use the assistant.' })
    }
  }

  return (
    <div className="p-6 md:p-10 space-y-6">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-4xl font-black">
        Smart Home Service Assistant
      </motion.h1>
      <div className="bg-slate-900 rounded-2xl p-6 space-y-4">
        <textarea className="w-full p-3 bg-slate-800 rounded-lg" rows="4" placeholder="Describe your issue..." value={message} onChange={(e) => setMessage(e.target.value)} />
        <button className="px-5 py-2 bg-cyan-500 rounded-lg hover:bg-cyan-400 transition" onClick={submit}>Ask Assistant</button>
        {response && <pre className="bg-slate-950 p-4 rounded-lg overflow-auto text-xs">{JSON.stringify(response, null, 2)}</pre>}
      </div>
    </div>
  )
}
