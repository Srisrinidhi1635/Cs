import { createContext, useContext, useMemo, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(() => JSON.parse(localStorage.getItem('auth') || 'null'))

  const value = useMemo(() => ({
    auth,
    login: (data) => {
      setAuth(data)
      localStorage.setItem('auth', JSON.stringify(data))
    },
    logout: () => {
      setAuth(null)
      localStorage.removeItem('auth')
    }
  }), [auth])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
