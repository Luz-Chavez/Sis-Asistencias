import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
})

// Interceptor: Antes de cada petición, revisa si hay un token y lo añade
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api