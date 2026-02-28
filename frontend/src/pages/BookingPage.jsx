import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import api from '../services/api'

const BookingPage = () => {
  const [bookings, setBookings] = useState([])
  const [form, setForm] = useState({ technician_id: '', service_type: '', issue_description: '', scheduled_at: '' })

  const fetchBookings = () => api.get('/bookings').then(({ data }) => setBookings(data))

  useEffect(() => { fetchBookings() }, [])

  const createBooking = async (e) => {
    e.preventDefault()
    await api.post('/bookings', form)
    setForm({ technician_id: '', service_type: '', issue_description: '', scheduled_at: '' })
    fetchBookings()
  }

  const cancelBooking = async (id) => {
    await api.delete(`/bookings/${id}`)
    fetchBookings()
  }

  return (
    <div className="mx-auto grid max-w-6xl gap-6 px-4 py-8 lg:grid-cols-[260px_1fr]">
      <Sidebar />
      <div className="space-y-6">
        <form onSubmit={createBooking} className="card space-y-3 p-6">
          <h3 className="text-lg font-semibold">Book Technician</h3>
          <input className="w-full rounded bg-slate-800 p-2" placeholder="Technician ID" value={form.technician_id} onChange={(e) => setForm({ ...form, technician_id: e.target.value })} />
          <input className="w-full rounded bg-slate-800 p-2" placeholder="Service type" value={form.service_type} onChange={(e) => setForm({ ...form, service_type: e.target.value })} />
          <textarea className="w-full rounded bg-slate-800 p-2" placeholder="Issue description" value={form.issue_description} onChange={(e) => setForm({ ...form, issue_description: e.target.value })} />
          <input className="w-full rounded bg-slate-800 p-2" placeholder="Scheduled at (optional)" value={form.scheduled_at} onChange={(e) => setForm({ ...form, scheduled_at: e.target.value })} />
          <button className="rounded bg-brand-500 px-4 py-2">Request Booking</button>
        </form>

        <div className="card p-6">
          <h3 className="text-lg font-semibold">My Bookings</h3>
          <div className="mt-3 space-y-3">
            {bookings.map((booking) => (
              <div key={booking._id} className="flex items-center justify-between rounded-lg border border-slate-800 p-3">
                <div>
                  <p className="font-medium">{booking.service_type}</p>
                  <p className="text-sm text-slate-400">{booking.issue_description}</p>
                  <p className="text-xs text-slate-500">Status: {booking.status}</p>
                </div>
                {booking.status !== 'cancelled' && <button onClick={() => cancelBooking(booking._id)} className="rounded bg-rose-500 px-3 py-1 text-sm">Cancel</button>}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default BookingPage
