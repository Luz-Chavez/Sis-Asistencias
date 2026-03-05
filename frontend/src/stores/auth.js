import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),
  actions: {
    async login(email, password) {
      // OAuth2 en FastAPI exige que los datos se envíen como formulario, no como JSON
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)

      // Llamamos a tu ruta real de login
      const response = await api.post('/usuarios/login', formData)
      
      // Guardamos el token en Pinia y en el navegador
      this.token = response.data.access_token
      localStorage.setItem('token', this.token)
    },
    logout() {
      this.token = null
      localStorage.removeItem('token')
    }
  }
})