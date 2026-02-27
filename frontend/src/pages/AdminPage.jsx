import { useEffect, useState } from 'react'
import api from '../services/api'

export default function AdminPage() {
  const [data, setData] = useState(null)
  useEffect(() => {
    api.get('/admin/dashboard').then((response) => setData(response.data)).catch(() => setData(null))
  }, [])
  return <div className="p-6"><pre className="text-xs">{JSON.stringify(data, null, 2)}</pre></div>
}
