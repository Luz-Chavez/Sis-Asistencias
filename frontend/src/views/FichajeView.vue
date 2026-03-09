<template>
  <div class="min-h-screen bg-[#eef0f7] flex flex-col">

    <!-- Barra superior -->
    <header class="flex items-center justify-between px-8 py-4 relative z-10">
      <span class="text-gray-600 font-semibold text-sm tracking-wide">
        Facultad de Ciencias Sociales · UMSA
      </span>
      <button
        type="button"
        @click="goLogin"
        class="flex items-center gap-2 text-sm text-gray-600 border border-gray-300 bg-white
               px-4 py-2 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition shadow-sm"
      >
        Iniciar sesion
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
        </svg>
      </button>
    </header>

    <!-- Tarjeta central -->
    <main class="flex-1 flex items-center justify-center px-4 relative z-10">
      <div class="bg-white rounded-3xl shadow-xl w-full max-w-md px-8 py-10 text-center">

        <!-- Reloj -->
        <div class="text-6xl font-black text-gray-900 tracking-tight leading-none">
          {{ horaActual }}
        </div>
        <div class="text-sm text-gray-400 mt-2 capitalize">{{ fechaActual }}</div>

        <hr class="my-6 border-gray-100" />

        <!-- Tabs Entrada / Salida -->
        <div class="flex rounded-xl overflow-hidden border border-gray-200 mb-6">
          <button
            @click="cambiarModo('entrada')"
            :class="modo === 'entrada' ? 'bg-blue-600 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
            class="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-semibold transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h7a2 2 0 012 2v1"/>
            </svg>
            Entrada
          </button>
          <button
            @click="cambiarModo('salida')"
            :class="modo === 'salida' ? 'bg-gray-700 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
            class="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-semibold transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h5a2 2 0 012 2v1"/>
            </svg>
            Salida
          </button>
        </div>

        <!-- Input username -->
        <label class="block text-left text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">
          Ingresa tu username
        </label>
        <div class="relative">
          <svg xmlns="http://www.w3.org/2000/svg"
            class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
            fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          <input
            v-model="username"
            ref="inputRef"
            type="text"
            placeholder="Ej. jp1234567"
            @keyup.enter="fichar"
            class="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl text-sm
                   focus:outline-none focus:border-blue-400 transition"
          />
        </div>

        <!-- Resultado -->
        <transition name="fade">
          <div v-if="mensaje" :class="[
              esError ? 'bg-red-50 border-red-200 text-red-700' : 'bg-green-50 border-green-200 text-green-700',
              'mt-4 p-4 rounded-xl border text-sm text-left'
            ]">
            <p class="font-bold">{{ mensaje.titulo }}</p>
            <p v-if="mensaje.detalle" class="text-xs opacity-75 mt-0.5">{{ mensaje.detalle }}</p>
          </div>
        </transition>

        <!-- BotÃ³n fichar -->
        <button
          @click="fichar"
          :disabled="isLoading || !username.trim()"
          :class="modo === 'entrada'
            ? 'bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300'
            : 'bg-gray-700 hover:bg-gray-800 disabled:bg-gray-400'"
          class="w-full mt-5 py-3.5 rounded-xl text-white font-bold text-sm
                 transition disabled:cursor-not-allowed shadow-md"
        >
          <span v-if="isLoading" class="flex items-center justify-center gap-2">
            <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            Procesando...
          </span>
          <span v-else>
            {{ modo === 'entrada' ? 'Registrar Entrada' : 'Registrar Salida' }}
          </span>
        </button>

      </div>
    </main>

    <!-- DecoraciÃ³n fondo -->
    <div class="fixed top-0 right-0 w-72 h-72 bg-blue-100 rounded-full opacity-40
                -translate-y-1/3 translate-x-1/3 pointer-events-none"></div>
    <div class="fixed bottom-0 left-0 w-56 h-56 bg-indigo-100 rounded-full opacity-30
                translate-y-1/3 -translate-x-1/3 pointer-events-none"></div>

    <!-- MODAL: Reporte de actividades (aparece tras registrar salida) -->
    <transition name="modal">
      <div v-if="showModalReporte"
        class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-70
               px-4 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">

          <!-- Cabecera verde Ã©xito -->
          <div class="bg-gradient-to-r from-emerald-500 to-teal-600 px-6 py-5 text-white">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center text-xl">A
                
              </div>
              <div>
                <h3 class="font-bold text-lg leading-tight">¡Salida registrada!</h3>
                <p class="text-emerald-100 text-sm">
                  {{ datosUltimaSalida?.nombre }} 
                  {{ datosUltimaSalida?.hora_entrada }} ’ {{ datosUltimaSalida?.hora_salida }} 
                  {{ datosUltimaSalida?.horas_trabajadas }}h trabajadas
                </p>
              </div>
            </div>
          </div>

          <!-- Cuerpo formulario -->
          <div class="px-6 py-5">
            <p class="text-gray-700 font-semibold mb-1">Reporte de actividades del dia</p>
            <p class="text-gray-400 text-xs mb-4">
              Describe brevemente que hiciste hoy. Esto quedara registrado para tu encargado.
            </p>

            <textarea
              v-model="actividades"
              rows="5"
              placeholder="Ej: Apoya en la organizacion del archivo, redacté 3 oficios, asistí a reunión de coordinación..."
              class="w-full border-2 border-gray-200 rounded-xl p-3 text-sm resize-none
                     focus:outline-none focus:border-emerald-400 transition"
            ></textarea>

            <p v-if="errorReporte" class="mt-2 text-red-600 text-xs bg-red-50 p-2 rounded-lg">
              {{ errorReporte }}
            </p>
          </div>

          <!-- Botones -->
          <div class="px-6 pb-6 flex gap-3">
            <button
              @click="omitirReporte"
              class="flex-1 py-2.5 border-2 border-gray-200 text-gray-500 rounded-xl text-sm font-medium
                     hover:bg-gray-50 transition"
            >
              Omitir por ahora
            </button>
            <button
              @click="enviarReporte"
              :disabled="isSubmittingReporte || !actividades.trim()"
              class="flex-1 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl text-sm
                     font-bold transition disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
            >
              <span v-if="isSubmittingReporte" class="flex items-center justify-center gap-2">
                <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                </svg>
                Enviando...
              </span>
              <span v-else>Enviar Reporte</span>
            </button>
          </div>

        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const goLogin = () => router.push({ name: 'login' })

const modo      = ref('entrada')
const username  = ref('')
const isLoading = ref(false)
const mensaje   = ref(null)
const esError   = ref(false)
const inputRef  = ref(null)

// â”€â”€ Modal reporte â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const showModalReporte    = ref(false)
const actividades         = ref('')
const isSubmittingReporte = ref(false)
const errorReporte        = ref('')
const datosUltimaSalida   = ref(null)   // { nombre, hora_entrada, hora_salida, horas_trabajadas, asistencia_id }

// â”€â”€ Reloj â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const horaActual  = ref('')
const fechaActual = ref('')
let intervalo = null

const actualizarReloj = () => {
  const ahora = new Date()
  horaActual.value = ahora.toLocaleTimeString('es-BO', {
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  })
  fechaActual.value = ahora.toLocaleDateString('es-BO', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
  })
}

onMounted(() => { actualizarReloj(); intervalo = setInterval(actualizarReloj, 1000) })
onUnmounted(() => clearInterval(intervalo))

// â”€â”€ Cambiar modo â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const cambiarModo = (nuevoModo) => {
  modo.value     = nuevoModo
  mensaje.value  = null
  username.value = ''
  nextTick(() => inputRef.value?.focus())
}

// â”€â”€ Fichaje â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
let timeoutMensaje = null

const fichar = async () => {
  if (!username.value.trim() || isLoading.value) return

  isLoading.value = true
  mensaje.value   = null
  if (timeoutMensaje) clearTimeout(timeoutMensaje)

  try {
    const endpoint = modo.value === 'entrada'
      ? '/asistencias/publico/entrada'
      : '/asistencias/publico/salida'

    const { data } = await api.post(endpoint, { username: username.value.trim() })

    esError.value = false

    if (modo.value === 'entrada') {
      // Entrada â†’ solo mostrar mensaje en pantalla
      mensaje.value = {
        titulo:  `BIENVENDIA ${data.nombre}!`,
        detalle: `Entrada registrada a las ${data.hora_entrada}`
      }
      username.value = ''
      timeoutMensaje = setTimeout(() => { mensaje.value = null }, 6000)

    } else {
      // Salida â†’ guardar datos y abrir modal de reporte
      datosUltimaSalida.value = {
        nombre:          data.nombre,
        hora_entrada:    data.hora_entrada,
        hora_salida:     data.hora_salida,
        horas_trabajadas: data.horas_trabajadas,
        asistencia_id:   data.asistencia_id,
      }
      actividades.value  = ''
      errorReporte.value = ''
      username.value     = ''
      showModalReporte.value = true
    }

  } catch (error) {
    esError.value = true
    const detalle = error.response?.data?.detail || 'Error al conectar con el servidor.'
    const titulos = { 404: ' Usuario no encontrado', 403: 'ðŸš« Acceso no permitido', 400: '¸Aviso' }
    mensaje.value = { titulo: titulos[error.response?.status] ?? 'âŒ Error', detalle }
  } finally {
    isLoading.value = false
  }
}

// â”€â”€ Enviar reporte â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const enviarReporte = async () => {
  if (!actividades.value.trim()) return

  isSubmittingReporte.value = true
  errorReporte.value = ''

  try {
    await api.post('/reportes/publico/crear', {
      asistencia_id:          datosUltimaSalida.value.asistencia_id,
      actividades_realizadas: actividades.value.trim(),
    })

    showModalReporte.value = false
    esError.value = false
    mensaje.value = {
      titulo:  ' Reporte enviado correctamente',
      detalle: `Gracias, ${datosUltimaSalida.value.nombre}. Tu encargado lo revisarÃ¡ pronto.`
    }
    timeoutMensaje = setTimeout(() => { mensaje.value = null }, 7000)

  } catch (error) {
    errorReporte.value = error.response?.data?.detail || 'Error al enviar el reporte. Intenta de nuevo.'
  } finally {
    isSubmittingReporte.value = false
  }
}

// â”€â”€ Omitir reporte â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const omitirReporte = () => {
  showModalReporte.value = false
  esError.value = false
  mensaje.value = {
    titulo:  `ðŸ‘‹ Â¡Hasta luego, ${datosUltimaSalida.value?.nombre}!`,
    detalle: 'Recuerda que puedes enviar tu reporte desde el panel de pasante.'
  }
  timeoutMensaje = setTimeout(() => { mensaje.value = null }, 6000)
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active   { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to         { opacity: 0; }
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.modal-enter-from, .modal-leave-to       { opacity: 0; transform: scale(0.96); }
</style>