import { useEffect, useState } from 'react'
import api from '../services/api'

export default function BookingPage() {
  const [bookings, setBookings] = useState([])

  const load = () => api.get('/bookings/me').then(({ data }) => setBookings(data)).catch(() => setBookings([]))
  useEffect(() => { load() }, [])

  return (
    <div className="p-6 space-y-3">
      {bookings.map((booking) => (
        <div className="bg-slate-900 p-4 rounded-xl" key={booking.id}>
          <p>{booking.service_type}</p>
          <p className="text-sm text-slate-400">{booking.status}</p>
        </div>
      ))}
    </div>
  )
}
