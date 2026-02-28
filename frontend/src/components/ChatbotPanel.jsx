import { useState } from 'react'
import { motion } from 'framer-motion'
import api from '../services/api'

const ChatbotPanel = ({ onServiceDetected }) => {
  const [message, setMessage] = useState('')
  const [responses, setResponses] = useState([])

  const sendMessage = async () => {
    if (!message.trim()) return
    try {
      const { data } = await api.post('/chatbot/analyze', { message })
      setResponses((prev) => [...prev, { user: message, bot: data.reply, cls: data.classification }])
      onServiceDetected?.(data.classification.service_type)
      setMessage('')
    } catch (error) {
      setResponses((prev) => [...prev, { user: message, bot: error.response?.data?.error || 'Please login to use AI assistant.' }])
    }
  }

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold">AI Service Chatbot</h3>
      <div className="mt-4 h-72 space-y-3 overflow-y-auto rounded-xl bg-slate-950/60 p-4">
        {responses.map((item, idx) => (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} key={idx} className="space-y-2">
            <p className="rounded-lg bg-slate-800 px-3 py-2 text-sm">🧑 {item.user}</p>
            <p className="rounded-lg bg-brand-600/40 px-3 py-2 text-sm">🤖 {item.bot}</p>
            {item.cls && <p className="text-xs text-brand-500">Detected: {item.cls.service_type} ({item.cls.confidence})</p>}
          </motion.div>
        ))}
      </div>
      <div className="mt-4 flex gap-3">
        <input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Describe your issue..." className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-2" />
        <button onClick={sendMessage} className="rounded-xl bg-brand-500 px-4 py-2 font-medium">Send</button>
      </div>
    </div>
  )
}

export default ChatbotPanel
