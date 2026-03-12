import axios from 'axios'

export const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
export const API_ORIGIN = new URL(API_BASE_URL).origin

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
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