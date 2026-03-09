<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">

      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800">Iniciar Sesión</h2>
        <p class="text-gray-600 mt-2">Sistema de Control de Asistencia</p>
        <p class="text-sm text-gray-500">Facultad de Ciencias Sociales - UMSA</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
          <input
            v-model="email"
            id="email"
            type="email"
            required
            class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                   placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="tu@correo.com"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input
            v-model="password"
            id="password"
            type="password"
            required
            class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                   placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="••••••••"
          />
        </div>

        <div v-if="errorMessage" class="text-red-600 text-sm text-center bg-red-50 p-2 rounded">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm
                 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700
                 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                 disabled:opacity-50 transition-colors"
        >
          <span v-if="isLoading">Iniciando...</span>
          <span v-else>Entrar</span>
        </button>

      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email      = ref('')
const password   = ref('')
const isLoading  = ref(false)
const errorMessage = ref('')

const authStore = useAuthStore()
const router    = useRouter()

const handleLogin = async () => {
  isLoading.value    = true
  errorMessage.value = ''

  try {
    await authStore.login(email.value, password.value)

    const rol = authStore.user?.rol
    console.log('Rol detectado:', rol)

    // ✅ Redirección según los 3 roles del sistema
    if (rol === 'ADMINISTRADOR') {
      router.push('/admin')
    } else if (rol === 'ENCARGADO') {
      router.push('/encargado')
    } else {
      router.push('/dashboard')   // PASANTE
    }

  } catch (error) {
    if (error.response?.status === 401) {
      errorMessage.value = 'Correo o contraseña incorrectos.'
    } else if (error.response?.status === 403) {
      errorMessage.value = 'Tu cuenta está desactivada. Contacta al administrador.'
    } else {
      errorMessage.value = 'Error al conectar con el servidor.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>