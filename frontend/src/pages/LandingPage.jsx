import { useState } from 'react'
import { Link } from 'react-router-dom'
import ChatbotPanel from '../components/ChatbotPanel'

const LandingPage = () => {
  const [detectedService, setDetectedService] = useState('')

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <section className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-5">
          <h1 className="text-4xl font-bold">Smart Home Service Assistant</h1>
          <p className="text-slate-300">
            Quickly connect with trusted electricians, plumbers, carpenters, painters, cleaners, masonry experts, and appliance repair technicians.
          </p>
          <div className="flex gap-3">
            <Link to="/signup" className="rounded-xl bg-brand-500 px-5 py-3 font-semibold">Get Started</Link>
            <Link to="/login" className="rounded-xl border border-slate-700 px-5 py-3">Login</Link>
          </div>
          {detectedService && <p className="text-sm text-brand-500">Latest detected service: {detectedService}</p>}
        </div>
        <ChatbotPanel onServiceDetected={setDetectedService} />
      </section>
    </div>
  )
}

export default LandingPage
