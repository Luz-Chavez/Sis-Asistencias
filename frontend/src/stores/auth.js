import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    // Añadimos un espacio para guardar los datos del usuario, incluyendo su rol
    user: JSON.parse(localStorage.getItem('user')) || null, 
  }),
  actions: {
    async login(email, password) {
      // 1. Autenticación y obtención del Token
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)

      const response = await api.post('/usuarios/login', formData)
      
      this.token = response.data.access_token
      localStorage.setItem('token', this.token)

      // 2. ¡La magia de la redirección! Descargar el perfil del usuario
      try {
        const profileResponse = await api.get('/usuarios/me')
        this.user = profileResponse.data // Aquí viene el { ..., rol: "DIRECTOR" }
        localStorage.setItem('user', JSON.stringify(this.user))
      } catch (error) {
        console.error("Error al obtener el perfil del usuario:", error)
        this.logout() // Por seguridad, si falla el perfil, cerramos la sesión
        throw error
      }
    },
    logout() {
      // Limpiamos todo al salir
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})