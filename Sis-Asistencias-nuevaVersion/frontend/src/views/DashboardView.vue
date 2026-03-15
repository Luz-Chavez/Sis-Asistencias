<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <div class="w-11 h-11 rounded-xl flex items-center justify-center shadow-md bg-white/95 border border-white/50 ring-1 ring-slate-200 overflow-hidden">
              <img
                v-if="authStore.user?.carrera_logo_url"
                :src="resolveStaticUrl(authStore.user.carrera_logo_url)"
                alt="Logo carrera"
                class="w-full h-full object-contain p-1"
              />
              <span v-else class="text-emerald-900 font-bold text-xs">UMSA</span>
            </div>
            <div class="hidden md:block border-l border-slate-300 pl-4">
              <p class="text-xs text-slate-500 font-medium uppercase tracking-wider">Facultad de Ciencias Sociales</p>
              <p class="text-sm font-bold text-slate-800">Sistema de Pasantias</p>
            </div>
          </div>

          <div class="flex items-center gap-2">
            <div class="hidden sm:flex items-center gap-3 px-3 py-1.5 bg-slate-50 rounded-lg">
              <button @click="router.push('/perfil')" title="Perfil"
                class="w-8 h-8 bg-emerald-900 rounded-full flex items-center justify-center text-white font-semibold text-xs hover:bg-emerald-800 transition-colors">
                {{ iniciales }}
              </button>
              <div class="text-right">
                <p class="text-xs font-semibold text-slate-700">{{ authStore.user?.nombres }} {{ authStore.user?.apellidos }}</p>
                <p class="text-xs text-slate-400 font-mono">{{ authStore.user?.username }}</p>
              </div>
            </div>

            <button
              @click="router.push('/reporte-pdf')"
              class="hidden sm:inline-flex items-center gap-2 text-sm text-slate-600 hover:text-emerald-700 hover:bg-emerald-50 px-3 py-2 rounded-lg transition-colors"
              title="Reporte PDF"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <span>Reporte PDF</span>
            </button>

            <button
              @click="cerrarSesion"
              class="flex items-center gap-2 text-sm text-slate-600 hover:text-red-600 transition-colors px-3 py-2 rounded-lg"
              title="Salir"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
              <span class="hidden sm:inline">Salir</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

      <div v-if="alerta20h" class="bg-gradient-to-r from-amber-500 to-orange-500 rounded-2xl p-6 text-white flex items-center justify-between gap-4 shadow-lg animate-pulse shadow-amber-500/20">
        <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            </div>
            <div>
                <p class="text-xs font-black uppercase tracking-widest text-amber-100">¡Atención, ya casi terminas!</p>
                <h3 class="mt-1 text-xl font-black">Faltan menos de {{ progreso.horas_restantes }} horas para terminar tu pasantía.</h3>
                <p class="text-sm text-amber-50 mt-1 font-medium">Asegúrate de que todos tus reportes estén validados por tu Encargado y Aprobados por el Administrador.</p>
            </div>
        </div>
      </div>


      <div class="bg-gradient-to-r from-emerald-900 via-emerald-800 to-emerald-900 rounded-2xl p-8 text-white shadow-lg">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div>
            <p class="text-emerald-200 text-sm font-medium uppercase tracking-wider mb-1">Bienvenido</p>
            <h1 class="text-3xl font-bold mb-2">{{ authStore.user?.nombres }} {{ authStore.user?.apellidos }}</h1>
            <p class="text-emerald-100 text-sm">Panel de control - Pasante</p>
            <p v-if="authStore.user?.proyecto_nombre" class="mt-2 inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-800/50 border border-emerald-700/50">
                <svg class="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                Proyecto: {{ authStore.user?.proyecto_nombre }}
            </p>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm">
              <p class="text-3xl font-bold">{{ stats.totalDias }}</p>
              <p class="text-xs text-emerald-200 uppercase tracking-wider">Dias</p>
            </div>
            <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm">
              <p class="text-3xl font-bold">{{ formatHorasLegibles(stats.totalHoras) }}</p>
              <p class="text-xs text-emerald-200 uppercase tracking-wider">Horas</p>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
          <p class="text-xs font-bold text-slate-500 uppercase">Reportes pendientes</p>
          <p class="mt-2 text-3xl font-bold text-slate-800">{{ stats.reportesPendientes }}</p>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
          <p class="text-xs font-bold text-slate-500 uppercase">Reportes aprobados</p>
          <p class="mt-2 text-3xl font-bold text-emerald-600">{{ stats.reportesAprobados }}</p>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
          <p class="text-xs font-bold text-slate-500 uppercase">Porcentaje aprobado</p>
          <p class="mt-2 text-3xl font-bold text-slate-800">{{ stats.pctAprobados }}%</p>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
          <p class="text-xs font-bold text-slate-500 uppercase">Total con reporte</p>
          <p class="mt-2 text-3xl font-bold text-slate-800">{{ stats.totalConReporte }}</p>
        </div>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <h2 class="text-lg font-semibold text-slate-800">Horas</h2>
          <p class="text-sm text-slate-500">Separacion de horas registradas y validadas</p>
        </div>
        <div class="p-6 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="p-4 rounded-xl border border-slate-200 bg-slate-50">
            <p class="text-xs font-bold text-slate-500 uppercase">Meta</p>
            <p class="mt-1 text-2xl font-black text-slate-800">{{ formatHorasLegibles(progreso.meta_horas) }}</p>
          </div>
          <div class="p-4 rounded-xl border border-slate-200 bg-slate-50">
            <p class="text-xs font-bold text-slate-500 uppercase">Total Registrado</p>
            <p class="mt-1 text-2xl font-black text-slate-800">{{ formatHorasLegibles(progreso.total_horas) }}</p>
          </div>
          <div class="p-4 rounded-xl border border-blue-200 bg-blue-50 relative overflow-hidden">
             <div class="absolute top-0 right-0 bg-blue-200 text-blue-800 text-[9px] font-black px-2 py-0.5 rounded-bl-lg">POR ENCARGADO</div>
            <p class="text-xs font-bold text-blue-700 uppercase">Horas Verificadas</p>
            <p class="mt-1 text-2xl font-black text-blue-900">{{ formatHorasLegibles(progreso.horas_verificadas) }}</p>
          </div>
          <div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50 relative overflow-hidden">
             <div class="absolute top-0 right-0 bg-emerald-200 text-emerald-800 text-[9px] font-black px-2 py-0.5 rounded-bl-lg">POR ADMIN</div>
            <p class="text-xs font-bold text-emerald-700 uppercase">Horas Validadas</p>
            <p class="mt-1 text-2xl font-black text-emerald-900">{{ formatHorasLegibles(progreso.horas_validadas) }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-semibold text-slate-800">Historial</h2>
            <p class="text-sm text-slate-500">Entradas, salidas y reportes</p>
          </div>
          <button
            @click="cargarHistorial"
            class="p-2 text-slate-400 hover:text-emerald-700 hover:bg-emerald-50 rounded-lg transition-all"
            title="Actualizar"
          >
            <svg class="w-5 h-5" :class="isLoading ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </button>
        </div>

        <div v-if="isLoading" class="py-16 text-center text-slate-400">
          <svg class="animate-spin w-8 h-8 mx-auto mb-3 text-emerald-400" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          <p class="text-sm">Cargando historial...</p>
        </div>

        <div v-else-if="historial.length === 0" class="py-16 text-center text-slate-400">
          <p class="text-sm">No hay registros aun.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-100">
            <thead class="bg-slate-50 border-b border-slate-200">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Fecha</th>
                <th class="px-6 py-3 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Entrada</th>
                <th class="px-6 py-3 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Salida</th>
                <th class="px-6 py-3 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Horas</th>
                <th class="px-6 py-3 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-3 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Comentario</th>
                <th class="px-6 py-3 text-right text-xs font-extrabold text-slate-500 uppercase tracking-wider">Accion</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-100/80">
              <tr v-for="item in historial" :key="item.id" class="hover:bg-slate-50/50">
                <td class="px-6 py-4 text-sm text-slate-700">{{ formatFecha(item.fecha) }}</td>
                <td class="px-6 py-4 text-sm text-slate-700 font-mono">{{ formatHora(item.hora_entrada) }}</td>
                <td class="px-6 py-4 text-sm text-slate-700 font-mono">{{ formatHora(item.hora_salida) }}</td>
                <td class="px-6 py-4 text-sm font-bold text-slate-700">{{ item.horas_trabajadas ?? '—' }}</td>
                <td class="px-6 py-4">
                  <span
                    class="inline-flex items-center px-2.5 py-1.5 border rounded-full text-[10px] font-black uppercase tracking-widest"
                    :class="badgeClass(item.reporte?.estado || 'PENDIENTE')"
                  >
                    {{ item.reporte?.estado || 'PENDIENTE' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-slate-600 max-w-sm truncate" :title="item.reporte?.comentarios_director || ''">
                  {{ item.reporte?.comentarios_director || '—' }}
                </td>
                <td class="px-6 py-4 text-right">
                  <button
                    @click="abrirModalReporte(item)"
                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold bg-emerald-900 text-white hover:bg-emerald-800 transition-colors"
                  >
                    Reporte
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <transition name="modal">
        <div v-if="showModalReporte" class="fixed inset-0 z-[999] flex items-center justify-center px-4">
          <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showModalReporte = false"></div>
          <div class="relative bg-white w-full max-w-xl rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/70">
              <h3 class="text-lg font-bold text-slate-800">Reporte del dia</h3>
              <p class="text-sm text-slate-500">
                {{ asistenciaSeleccionada ? formatFecha(asistenciaSeleccionada.fecha) : '' }}
              </p>
            </div>
            <div class="p-6 space-y-3">
              <label class="block text-sm font-semibold text-slate-700">Actividades</label>
              <textarea
                v-model="actividadesModal"
                rows="6"
                placeholder="Describe las tareas que realizaste..."
                class="w-full border border-slate-300 rounded-xl p-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
              />
              <p v-if="errorModal" class="text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-lg font-medium">
                {{ errorModal }}
              </p>
            </div>
            <div class="px-6 pb-6 flex gap-3">
              <button
                @click="showModalReporte = false"
                class="flex-1 py-2.5 border border-slate-300 text-slate-600 rounded-xl text-sm font-bold hover:bg-slate-50 transition-colors"
              >
                Cancelar
              </button>
              <button
                @click="guardarReporteModal"
                :disabled="isSubmittingModal || !actividadesModal.trim()"
                class="flex-1 py-2.5 bg-emerald-900 text-white rounded-xl text-sm font-bold hover:bg-emerald-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
              >
                {{ isSubmittingModal ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </div>
        </div>
      </transition>

      <transition name="modal">
        <div v-if="showModalProyecto" class="fixed inset-0 z-[999] flex items-center justify-center px-4">
          <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showModalProyecto = false"></div>
          <div class="relative bg-white w-full max-w-md rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/70">
              <h3 class="text-lg font-bold text-slate-800">Registrar Proyecto</h3>
              <p class="text-sm text-slate-500">Asigna el programa/proyecto al que perteneces.</p>
            </div>
            <div class="p-6 space-y-4">
              <div>
                  <label class="block text-sm font-semibold text-slate-700 mb-1.5">Nombre del Proyecto/Programa <span class="text-red-500">*</span></label>
                  <input v-model="formProyecto.proyecto_nombre" type="text" class="w-full border border-slate-300 rounded-xl p-3 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" placeholder="Ej: Proyecto de Grado 2026">
              </div>
              <div>
                  <label class="block text-sm font-semibold text-slate-700 mb-1.5">URL de Documento de Respaldo</label>
                  <input v-model="formProyecto.proyecto_documento_url" type="url" class="w-full border border-slate-300 rounded-xl p-3 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" placeholder="Enlace a Google Drive o archivo PDF">
                  <p class="text-xs text-slate-500 mt-1">Opcional: Sube el documento de tu pasantía a la nube y pega aquí el enlace.</p>
              </div>
            </div>
            <div class="px-6 pb-6 flex gap-3">
              <button @click="showModalProyecto = false" class="flex-1 py-2.5 border border-slate-300 text-slate-600 rounded-xl text-sm font-bold hover:bg-slate-50 transition-colors">Cancelar</button>
              <button @click="guardarProyecto" :disabled="isSubmittingProyecto || !formProyecto.proyecto_nombre.trim()" class="flex-1 py-2.5 bg-emerald-600 text-white rounded-xl text-sm font-bold hover:bg-emerald-700 transition-colors disabled:opacity-50">
                Guardar
              </button>
            </div>
          </div>
        </div>
      </transition>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'
import { formatFecha, formatHora, formatHorasLegibles } from '../utils/formatters'

const router    = useRouter()
const authStore = useAuthStore()

const resolveStaticUrl = (url) => {
  if (!url) return null
  const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`
  return s
}

const historial  = ref([])
const isLoading  = ref(true)
const progreso   = ref({
  meta_horas:       240,
  total_horas:      0,
  horas_verificadas: 0,
  horas_validadas:  0,
  horas_restantes:  240,
})

const showModalReporte       = ref(false)
const asistenciaSeleccionada = ref(null)
const actividadesModal       = ref('')
const isSubmittingModal      = ref(false)
const errorModal             = ref('')

const showModalProyecto      = ref(false)
const formProyecto           = ref({ proyecto_nombre: '', proyecto_documento_url: '' })
const isSubmittingProyecto   = ref(false)

const iniciales = computed(() => {
  const n = authStore.user?.nombres?.[0]  ?? ''
  const a = authStore.user?.apellidos?.[0] ?? ''
  return (n + a).toUpperCase()
})

const stats = computed(() => {
  const conReporte  = historial.value.filter(i => i.reporte).length
  const aprobados   = historial.value.filter(i => (i.reporte?.estado || '').toUpperCase() === 'APROBADO').length
  const pendientes  = historial.value.filter(i => (i.reporte?.estado || '').toUpperCase() === 'PENDIENTE').length
  const totalHoras  = Math.round(
    historial.value.reduce((a, i) => a + (parseFloat(i.horas_trabajadas) || 0), 0) * 10
  ) / 10

  return {
    totalDias:         historial.value.length,
    totalHoras,
    totalConReporte:   conReporte,
    reportesPendientes: pendientes,
    reportesAprobados: aprobados,
    pctAprobados:      conReporte > 0 ? Math.round((aprobados / conReporte) * 100) : 0,
  }
})

const alerta20h = computed(() => {
  const restante = Number(progreso.value?.horas_restantes ?? 0)
  return restante > 0 && restante <= 20
})

const badgeClass = (estado) => {
  const e = String(estado || 'PENDIENTE').toUpperCase()
  if (e === 'APROBADO')   return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  if (e === 'VERIFICADO') return 'bg-blue-50 text-blue-700 border-blue-200'
  if (e === 'RECHAZADO')  return 'bg-rose-50 text-rose-700 border-rose-200'
  return 'bg-amber-50 text-amber-700 border-amber-200'
}

const cargarHistorial = async () => {
  isLoading.value = true
  try {
    const { data } = await api.get('/asistencias/mis-asistencias')
    historial.value = data
    const pr = await api.get('/asistencias/mi-progreso')
    progreso.value  = pr.data
  } catch (e) {
    if (e.response?.status === 401) cerrarSesion()
  } finally {
    isLoading.value = false
  }
}

const abrirModalReporte = (asistencia) => {
  asistenciaSeleccionada.value = asistencia
  actividadesModal.value       = asistencia.reporte?.actividades_realizadas || ''
  errorModal.value             = ''
  showModalReporte.value       = true
}

const guardarReporteModal = async () => {
  if (!asistenciaSeleccionada.value || !actividadesModal.value.trim()) return

  isSubmittingModal.value = true
  errorModal.value        = ''
  try {
    await api.post('/reportes/subir', {
      asistencia_id:         asistenciaSeleccionada.value.id,
      actividades_realizadas: actividadesModal.value.trim(),
    })
    showModalReporte.value = false
    await cargarHistorial()
  } catch (e) {
    errorModal.value = e.response?.data?.detail || 'Error al guardar el reporte.'
  } finally {
    isSubmittingModal.value = false
  }
}

const guardarProyecto = async () => {
  if (!formProyecto.value.proyecto_nombre.trim()) return
  isSubmittingProyecto.value = true
  try {
    await api.put('/usuarios/mi-perfil', {
      proyecto_nombre:       formProyecto.value.proyecto_nombre.trim(),
      proyecto_documento_url: formProyecto.value.proyecto_documento_url.trim() || null,
    })
    authStore.user.proyecto_nombre = formProyecto.value.proyecto_nombre.trim()
    showModalProyecto.value        = false
    alert('✅ Proyecto registrado correctamente')
  } catch (e) {
    alert(e.response?.data?.detail || 'Hubo un error al guardar el proyecto')
  } finally {
    isSubmittingProyecto.value = false
  }
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/')
}

onMounted(() => {
  cargarHistorial()
  if (authStore.user?.proyecto_nombre) {
    formProyecto.value.proyecto_nombre = authStore.user.proyecto_nombre
  }
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.modal-enter-from,
.modal-leave-to     { opacity: 0; transform: scale(0.97); }
</style>