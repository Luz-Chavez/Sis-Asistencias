<template>
  <div class="min-h-screen bg-[#eef0f7] flex flex-col">

    <!-- Barra superior -->
    <header class="flex items-center justify-between px-8 py-4 relative z-10">
      <span class="text-gray-600 font-semibold text-sm tracking-wide">
        Facultad de Ciencias Sociales · UMSA
      </span>
      <button
        @click="$router.push('/login')"
        class="flex items-center gap-2 text-sm text-gray-600 border border-gray-300 bg-white
               px-4 py-2 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition shadow-sm"
      >
        Iniciar sesión
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
        </svg>
      </button>
    </header>

    <main class="flex-1 flex items-center justify-center px-4 relative z-10">

      <!-- ══════════════════════════════════════════════════
           PANTALLA 1: FICHAJE (entrada / salida)
      ══════════════════════════════════════════════════ -->
      <transition name="slide-fade" mode="out-in">

        <div v-if="pantalla === 'fichaje'" key="fichaje"
          class="bg-white rounded-3xl shadow-xl w-full max-w-md px-8 py-10 text-center">

          <!-- Reloj -->
          <div class="text-6xl font-black text-gray-900 tracking-tight leading-none">
            {{ horaActual }}
          </div>
          <div class="text-sm text-gray-400 mt-2 capitalize">{{ fechaActual }}</div>

          <hr class="my-6 border-gray-100" />

          <!-- Tabs -->
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

          <!-- Mensaje de error/aviso -->
          <transition name="fade">
            <div v-if="mensajeFichaje" :class="[
                esFichajeError
                  ? 'bg-red-50 border-red-200 text-red-700'
                  : 'bg-green-50 border-green-200 text-green-700',
                'mt-4 p-3 rounded-xl border text-sm text-left'
              ]">
              <p class="font-bold">{{ mensajeFichaje.titulo }}</p>
              <p v-if="mensajeFichaje.detalle" class="text-xs opacity-75 mt-0.5">{{ mensajeFichaje.detalle }}</p>
            </div>
          </transition>

          <!-- Botón fichar -->
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

        <!-- ══════════════════════════════════════════════════
             PANTALLA 2: FORMULARIO DE REPORTE (tras salida)
        ══════════════════════════════════════════════════ -->
        <div v-else-if="pantalla === 'reporte'" key="reporte"
          class="w-full max-w-md">
          <div class="bg-white rounded-3xl shadow-xl overflow-hidden">

            <!-- Franja superior con resumen -->
            <div class="bg-gradient-to-r from-slate-700 to-slate-800 px-7 py-6">
              <div class="flex items-center gap-4">
                <div class="w-11 h-11 bg-white/15 rounded-2xl flex items-center justify-center flex-shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div>
                  <p class="text-white font-bold text-base leading-tight">¡Salida registrada!</p>
                  <p class="text-slate-300 text-sm">Hola, <span class="font-semibold text-white">{{ datosJornada.nombre }}</span></p>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-2 mt-5">
                <div class="bg-white/10 rounded-xl p-3 text-center">
                  <p class="text-xs text-slate-300 font-medium uppercase tracking-wide mb-0.5">Entrada</p>
                  <p class="text-sm font-bold text-white">{{ datosJornada.hora_entrada }}</p>
                </div>
                <div class="bg-white/10 rounded-xl p-3 text-center">
                  <p class="text-xs text-slate-300 font-medium uppercase tracking-wide mb-0.5">Salida</p>
                  <p class="text-sm font-bold text-white">{{ datosJornada.hora_salida }}</p>
                </div>
                <div class="bg-emerald-500/30 rounded-xl p-3 text-center border border-emerald-400/30">
                  <p class="text-xs text-emerald-200 font-medium uppercase tracking-wide mb-0.5">Total</p>
                  <p class="text-sm font-bold text-emerald-100">{{ datosJornada.horas_trabajadas }}h</p>
                </div>
              </div>
            </div>

            <!-- Formulario -->
            <div class="px-7 py-6">
              <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">
                Actividades realizadas hoy
              </label>
              <p class="text-xs text-gray-400 mb-3">
                Describe brevemente qué actividades realizaste durante tu jornada.
              </p>
              <textarea
                v-model="actividades"
                rows="5"
                placeholder="Ej: Revisé documentos del archivo central, actualicé la base de datos de estudiantes, apoyé en la recepción..."
                class="w-full border-2 border-gray-200 rounded-xl p-3 text-sm
                       focus:outline-none focus:border-slate-400 transition resize-none"
              ></textarea>

              <transition name="fade">
                <div v-if="mensajeReporte" :class="[
                    esReporteError
                      ? 'bg-red-50 border-red-200 text-red-700'
                      : 'bg-green-50 border-green-200 text-green-700',
                    'mt-3 p-3 rounded-xl border text-sm'
                  ]">
                  {{ mensajeReporte }}
                </div>
              </transition>

              <button
                @click="enviarReporte"
                :disabled="isSubmittingReporte || !actividades.trim()"
                class="w-full mt-4 py-3.5 rounded-xl bg-slate-800 text-white font-bold text-sm
                       hover:bg-slate-700 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
              >
                <span v-if="isSubmittingReporte" class="flex items-center justify-center gap-2">
                  <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                  </svg>
                  Enviando...
                </span>
                <span v-else>Enviar Reporte del Día</span>
              </button>

              <button
                @click="omitirReporte"
                class="w-full mt-2 py-2.5 rounded-xl text-gray-400 text-sm hover:text-gray-600 transition"
              >
                Omitir por ahora
              </button>
            </div>

          </div>
        </div>

        <!-- ══════════════════════════════════════════════════
             PANTALLA 3: CONFIRMACIÓN FINAL
        ══════════════════════════════════════════════════ -->
        <div v-else-if="pantalla === 'confirmacion'" key="confirmacion"
          class="bg-white rounded-3xl shadow-xl w-full max-w-md px-8 py-14 text-center">

          <div class="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-5">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>

          <h2 class="text-2xl font-black text-gray-800">¡Todo listo!</h2>
          <p class="text-gray-500 mt-2 text-sm">
            Tu reporte fue enviado correctamente.<br />¡Hasta mañana, <strong>{{ datosJornada.nombre }}</strong>!
          </p>

          <div class="mt-6 text-xs text-gray-400">
            Esta ventana se cerrará automáticamente en <strong>{{ cuentaRegresiva }}</strong>s
          </div>

          <button @click="volverAlFichaje"
            class="mt-6 px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-sm font-medium
                   hover:bg-indigo-700 transition shadow">
            Volver al inicio
          </button>
        </div>

      </transition>
    </main>

    <!-- Decoración fondo -->
    <div class="fixed top-0 right-0 w-72 h-72 bg-blue-100 rounded-full opacity-40
                -translate-y-1/3 translate-x-1/3 pointer-events-none -z-10"></div>
    <div class="fixed bottom-0 left-0 w-56 h-56 bg-indigo-100 rounded-full opacity-30
                translate-y-1/3 -translate-x-1/3 pointer-events-none -z-10"></div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import api from '../services/api'

// ── Pantallas: 'fichaje' | 'reporte' | 'confirmacion' ────────────────────────
const pantalla = ref('fichaje')

// ── Fichaje ───────────────────────────────────────────────────────────────────
const modo             = ref('entrada')
const username         = ref('')
const isLoading        = ref(false)
const mensajeFichaje   = ref(null)
const esFichajeError   = ref(false)
const inputRef         = ref(null)

// Datos que se guardan tras la salida exitosa
const datosJornada = ref({
  nombre:           '',
  hora_entrada:     '',
  hora_salida:      '',
  horas_trabajadas: 0,
  asistencia_id:    null,
})

// ── Reporte ───────────────────────────────────────────────────────────────────
const actividades         = ref('')
const isSubmittingReporte = ref(false)
const mensajeReporte      = ref('')
const esReporteError      = ref(false)

// ── Confirmación ──────────────────────────────────────────────────────────────
const cuentaRegresiva  = ref(8)
let timerConfirmacion  = null

// ── Reloj ─────────────────────────────────────────────────────────────────────
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

onMounted(() => {
  actualizarReloj()
  intervalo = setInterval(actualizarReloj, 1000)
})

onUnmounted(() => {
  clearInterval(intervalo)
  if (timerConfirmacion) clearInterval(timerConfirmacion)
})

// ── Helpers ───────────────────────────────────────────────────────────────────
const cambiarModo = (nuevoModo) => {
  modo.value          = nuevoModo
  mensajeFichaje.value = null
  username.value      = ''
  nextTick(() => inputRef.value?.focus())
}

let timeoutMensaje = null
const mostrarError = (titulo, detalle) => {
  esFichajeError.value   = true
  mensajeFichaje.value   = { titulo, detalle }
  if (timeoutMensaje) clearTimeout(timeoutMensaje)
  timeoutMensaje = setTimeout(() => { mensajeFichaje.value = null }, 5000)
}

// ── Lógica de fichaje ─────────────────────────────────────────────────────────
const fichar = async () => {
  if (!username.value.trim() || isLoading.value) return

  isLoading.value      = true
  mensajeFichaje.value = null

  try {
    const endpoint = modo.value === 'entrada'
      ? '/asistencias/publico/entrada'
      : '/asistencias/publico/salida'

    const { data } = await api.post(endpoint, { username: username.value.trim() })

    if (modo.value === 'entrada') {
      // Entrada exitosa → mensaje verde y limpiar
      esFichajeError.value = false
      mensajeFichaje.value = {
        detalle: `Entrada registrada a las ${data.hora_entrada}`
      }
      username.value = ''
      if (timeoutMensaje) clearTimeout(timeoutMensaje)
      timeoutMensaje = setTimeout(() => { mensajeFichaje.value = null }, 6000)

    } else {
      // Salida exitosa → guardar datos y pasar a pantalla de reporte
      datosJornada.value = {
        nombre:           data.nombre,
        hora_entrada:     data.hora_entrada,
        hora_salida:      data.hora_salida,
        horas_trabajadas: data.horas_trabajadas,
        asistencia_id:    data.asistencia_id,
      }
      username.value   = ''
      actividades.value = ''
      pantalla.value   = 'reporte'
    }

  } catch (error) {
    const detalle = error.response?.data?.detail || 'Error al conectar con el servidor.'
    const titulos = { 404: '❌ Usuario no encontrado', 403: '🚫 Acceso no permitido', 400: '⚠️ Aviso' }
    mostrarError(titulos[error.response?.status] ?? '❌ Error', detalle)
  } finally {
    isLoading.value = false
  }
}

// ── Enviar reporte ────────────────────────────────────────────────────────────
const enviarReporte = async () => {
  if (!actividades.value.trim() || isSubmittingReporte.value) return

  isSubmittingReporte.value = true
  mensajeReporte.value      = ''

  try {
    await api.post('/reportes/publico/crear', {
      asistencia_id:          datosJornada.value.asistencia_id,
      actividades_realizadas: actividades.value.trim(),
    })

    // Éxito → pantalla de confirmación con cuenta regresiva
    pantalla.value = 'confirmacion'
    iniciarCuentaRegresiva()

  } catch (error) {
    esReporteError.value = true
    mensajeReporte.value = error.response?.data?.detail || 'Error al enviar el reporte. Intenta de nuevo.'
  } finally {
    isSubmittingReporte.value = false
  }
}

// ── Omitir reporte ────────────────────────────────────────────────────────────
const omitirReporte = () => {
  volverAlFichaje()
}

// ── Confirmación con cuenta regresiva ────────────────────────────────────────
const iniciarCuentaRegresiva = () => {
  cuentaRegresiva.value = 8
  timerConfirmacion = setInterval(() => {
    cuentaRegresiva.value--
    if (cuentaRegresiva.value <= 0) {
      clearInterval(timerConfirmacion)
      volverAlFichaje()
    }
  }, 1000)
}

const volverAlFichaje = () => {
  if (timerConfirmacion) clearInterval(timerConfirmacion)
  pantalla.value       = 'fichaje'
  actividades.value    = ''
  mensajeReporte.value = ''
  modo.value           = 'entrada'
  datosJornada.value   = { nombre: '', hora_entrada: '', hora_salida: '', horas_trabajadas: 0, asistencia_id: null }
  nextTick(() => inputRef.value?.focus())
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-fade-enter-active { transition: all 0.35s ease; }
.slide-fade-leave-active { transition: all 0.25s ease; }
.slide-fade-enter-from { opacity: 0; transform: translateY(16px); }
.slide-fade-leave-to   { opacity: 0; transform: translateY(-10px); }
</style>