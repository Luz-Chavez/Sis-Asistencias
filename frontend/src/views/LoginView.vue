<template>
  <div class="min-h-screen flex items-center justify-center umsa-page px-4">
    <div class="max-w-md w-full umsa-card rounded-lg p-8">

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
          <div class="mt-2 text-right">
            <button type="button" @click="abrirModalReset"
              class="text-xs font-medium text-blue-700 hover:text-blue-800 hover:underline">
              Olvidaste tu contrasena
            </button>
          </div>
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

      <!-- Modal recuperar contrasena -->
      <div v-if="showResetModal" class="fixed inset-0 z-50 flex items-start sm:items-center justify-center bg-slate-900/60 px-4 py-8 backdrop-blur-sm overflow-y-auto">
        <div class="bg-white w-full max-w-md rounded-xl shadow-2xl border border-gray-200 overflow-hidden max-h-[calc(100vh-4rem)] flex flex-col">
          <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-800">Recuperar contrasena</h3>
            <button @click="cerrarModalReset" class="text-gray-500 hover:text-gray-800">X</button>
          </div>
          <div class="p-6 overflow-y-auto">
            <p class="text-sm text-gray-600 mb-4">
              Ingresa tu correo. Si existe una cuenta, se enviara un enlace de recuperacion.
            </p>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Correo</label>
                <input v-model="resetEmail" type="email" required placeholder="tu@correo.com"
                  class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                         placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>

              <div v-if="resetMensajeOk" class="text-emerald-700 text-sm text-center bg-emerald-50 p-2 rounded border border-emerald-200">
                {{ resetMensajeOk }}
              </div>
              <div v-if="resetErrorMessage" class="text-red-600 text-sm text-center bg-red-50 p-2 rounded border border-red-200">
                {{ resetErrorMessage }}
              </div>

              <button type="button" @click="enviarReset" :disabled="isResetLoading"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm
                       text-sm font-medium text-white bg-blue-600 hover:bg-blue-700
                       focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                       disabled:opacity-50 transition-colors">
                <span v-if="isResetLoading">Enviando...</span>
                <span v-else>Enviar enlace</span>
              </button>

              <button type="button" @click="cerrarModalReset"
                class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm
                       text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors">
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const email      = ref('')
const password   = ref('')
const isLoading  = ref(false)
const errorMessage = ref('')
const showResetModal = ref(false)
const resetEmail = ref('')
const isResetLoading = ref(false)
const resetErrorMessage = ref('')
const resetMensajeOk = ref('')

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

const abrirModalReset = () => {
  resetEmail.value = email.value || ''
  resetErrorMessage.value = ''
  resetMensajeOk.value = ''
  showResetModal.value = true
}

const cerrarModalReset = () => {
  showResetModal.value = false
}

const enviarReset = async () => {
  resetErrorMessage.value = ''
  resetMensajeOk.value = ''
  const correo = (resetEmail.value || '').trim()
  if (!correo) {
    resetErrorMessage.value = 'El correo es obligatorio.'
    return
  }

  isResetLoading.value = true
  try {
    await api.post('/usuarios/password-reset/solicitar', { email: correo })
    resetMensajeOk.value = 'Listo. Revisa tu correo para continuar.'
  } catch (e) {
    resetErrorMessage.value = e.response?.data?.detail || 'No se pudo enviar el enlace.'
  } finally {
    isResetLoading.value = false
  }
}
</script>
