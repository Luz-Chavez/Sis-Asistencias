<template>
  <div class="min-h-screen bg-slate-50 font-sans">
    
    <nav class="bg-slate-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-6">
            <h1 class="text-white font-bold text-xl hidden md:block tracking-wide">
              Panel de AdministraciÃ³n
            </h1>
            <div class="flex gap-2">
              <button class="bg-white/10 text-white px-4 py-2 rounded-lg text-sm font-bold cursor-default shadow-sm border border-white/5">
                <svg class="w-4 h-4 inline-block mr-1.5 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Todos los Reportes
              </button>
              <button @click="router.push('/usuarios')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all">
                <svg class="w-4 h-4 inline-block mr-1.5 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                GestiÃ³n de Usuarios
              </button>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-white text-sm font-medium">{{ authStore.user?.nombres }}</span>
              <span class="text-slate-400 text-xs">{{ authStore.user?.rol }}</span>
            </div>
            <button @click="cerrarSesion"
              class="text-sm bg-rose-600 hover:bg-rose-500 text-white px-4 py-2 rounded-lg transition-colors shadow-sm font-medium">
              Cerrar SesiÃ³n
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">

      <div class="mb-8">
        <h2 class="text-2xl font-bold text-slate-800 mb-2">Resumen de Reportes Diarios</h2>
        <p class="text-slate-500 text-sm mb-6">Revisa las actividades de los pasantes y aprueba sus horas de trabajo.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div class="p-3 bg-slate-100 text-slate-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </div>
            <div>
              <p class="text-sm text-slate-500 font-medium">Total Reportes</p>
              <p class="text-2xl font-bold text-slate-800">{{ reportes.length }}</p>
            </div>
          </div>
          
          <div class="bg-white p-5 rounded-xl shadow-sm border border-amber-200 flex items-center gap-4 relative overflow-hidden">
            <div class="absolute right-0 top-0 bottom-0 w-2 bg-amber-400"></div>
            <div class="p-3 bg-amber-100 text-amber-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
            <div>
              <p class="text-sm text-slate-500 font-medium">Por Evaluar</p>
              <p class="text-2xl font-bold text-amber-600">{{ totalPendientes }}</p>
            </div>
          </div>

          <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div class="p-3 bg-emerald-100 text-emerald-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
            <div>
              <p class="text-sm text-slate-500 font-medium">Aprobados</p>
              <p class="text-2xl font-bold text-slate-800">{{ totalAprobados }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-6 flex flex-col md:flex-row justify-between items-center gap-4">
        
        <div class="flex flex-wrap gap-2 w-full md:w-auto">
          <button @click="filtroActual = 'TODOS'" :class="filtroActual === 'TODOS' ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'" class="px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Todos
          </button>
          <button @click="filtroActual = 'PENDIENTE'" :class="filtroActual === 'PENDIENTE' ? 'bg-amber-100 text-amber-800 border-amber-200' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'" class="px-4 py-2 rounded-lg text-sm font-medium border border-transparent transition-colors">
            Pendientes
          </button>
          <button @click="filtroActual = 'APROBADO'" :class="filtroActual === 'APROBADO' ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'" class="px-4 py-2 rounded-lg text-sm font-medium border border-transparent transition-colors">
            Aprobados
          </button>
          <button @click="filtroActual = 'RECHAZADO'" :class="filtroActual === 'RECHAZADO' ? 'bg-rose-100 text-rose-800 border-rose-200' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'" class="px-4 py-2 rounded-lg text-sm font-medium border border-transparent transition-colors">
            Rechazados
          </button>
        </div>

        <div class="relative w-full md:w-80">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input v-model="searchQuery" type="text" placeholder="Buscar por nombre o actividad..."
            class="block w-full pl-10 pr-3 py-2 border border-slate-300 rounded-lg bg-slate-50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white sm:text-sm transition-colors" />
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Pasante & Fecha</th>
                <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider w-1/3">Actividades</th>
                <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">Horas Totales</th>
                <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-100">
              
              <tr v-if="isLoading">
                <td colspan="5" class="px-6 py-16 text-center">
                  <div class="flex flex-col items-center justify-center text-slate-400">
                    <svg class="animate-spin h-8 w-8 mb-4 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    <p class="font-medium text-slate-500">Cargando reportes...</p>
                  </div>
                </td>
              </tr>
              
              <tr v-else-if="filteredReportes.length === 0">
                <td colspan="5" class="px-6 py-16 text-center">
                  <div class="flex flex-col items-center justify-center text-slate-400">
                    <svg class="w-16 h-16 mb-4 text-slate-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    <p class="font-medium text-slate-500 text-lg">No hay reportes para mostrar</p>
                    <p class="text-sm mt-1">Intenta cambiar los filtros o la bÃºsqueda.</p>
                  </div>
                </td>
              </tr>

              <tr v-else v-for="reporte in filteredReportes" :key="reporte.id" class="hover:bg-slate-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex flex-col">
                    <span class="text-sm font-bold text-slate-800">{{ reporte.nombre_pasante || 'Pasante Desconocido' }}</span>
                    <span class="text-xs text-slate-500 mt-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                      {{ reporte.creado_en ? new Date(reporte.creado_en).toLocaleDateString('es-BO') : 'â€”' }}
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <p class="text-sm text-slate-600 line-clamp-2" :title="reporte.actividades_realizadas">
                    {{ reporte.actividades_realizadas }}
                  </p>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center">
                  <span class="text-sm font-bold text-slate-700 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
                    {{ reporte.horas_totales ?? reporte.horas_trabajadas ?? '0' }} hrs
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center">
                  <span :class="estadoBadgeClass(reporte.estado)" class="px-3 py-1.5 inline-flex items-center gap-1.5 text-xs font-bold rounded-full border">
                    <span class="w-1.5 h-1.5 rounded-full" :class="estadoDotClass(reporte.estado)"></span>
                    {{ reporte.estado || 'PENDIENTE' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center">
                  <div class="flex justify-center gap-2">
                    <button @click="abrirModalEvaluar(reporte)" 
                            :class="reporte.estado === 'PENDIENTE' ? 'bg-amber-100 text-amber-700 hover:bg-amber-200 border-amber-200' : 'bg-white text-slate-500 hover:bg-slate-100 hover:text-indigo-600 border-slate-200'"
                            class="px-3 py-1.5 rounded-lg border text-sm font-medium transition-colors flex items-center gap-1.5 shadow-sm"
                            :title="reporte.estado === 'PENDIENTE' ? 'Revisar y Evaluar' : 'Ver Detalles'">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                      {{ reporte.estado === 'PENDIENTE' ? 'Evaluar' : 'Ver' }}
                    </button>
                    <button @click="descargarPDF(reporte)" 
                            class="p-1.5 bg-white text-slate-500 border border-slate-200 hover:text-rose-600 hover:border-rose-200 hover:bg-rose-50 rounded-lg transition-colors shadow-sm" 
                            title="Descargar Comprobante PDF">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg my-8 border border-slate-200 overflow-hidden transform transition-all">
        
        <div class="px-6 py-4 bg-slate-800 flex justify-between items-center">
          <h3 class="text-lg font-bold text-white tracking-wide flex items-center gap-2">
            <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            EvaluaciÃ³n de Actividades
          </h3>
          <button @click="showModal = false" class="text-white/60 hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <div class="p-6">
          <div class="mb-6 bg-slate-50 p-5 rounded-xl border border-slate-200">
            <div class="flex justify-between items-start mb-4 pb-4 border-b border-slate-200">
              <div>
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Pasante</p>
                <p class="text-base font-bold text-slate-800">{{ reporteAEvaluar?.nombre_pasante }}</p>
              </div>
              <div class="text-right">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Horas Totales Acumuladas</p>
                <p class="text-base font-bold text-indigo-600">{{ reporteAEvaluar?.horas_totales ?? reporteAEvaluar?.horas_trabajadas ?? '0' }} hrs</p>
              </div>
            </div>
            <div>
              <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Actividades Realizadas</p>
              <p class="text-sm text-slate-700 leading-relaxed bg-white p-3 rounded-lg border border-slate-100">
                {{ reporteAEvaluar?.actividades_realizadas }}
              </p>
            </div>
          </div>

          <form @submit.prevent="guardarEvaluacion" class="space-y-5">
            <div>
              <label class="block text-sm font-bold text-slate-800 mb-3">Â¿Aprobar estas actividades?</label>
              <div class="flex gap-4">
                <label class="flex-1 cursor-pointer">
                  <input type="radio" v-model="formEvaluacion.estado" value="APROBADO" class="peer sr-only">
                  <div class="text-center p-3 rounded-xl border-2 peer-checked:border-emerald-500 peer-checked:bg-emerald-50 text-slate-500 peer-checked:text-emerald-700 hover:bg-slate-50 transition-all">
                    <div class="text-2xl mb-1">✅…</div>
                    <div class="font-bold text-sm">Aprobar Horas</div>
                  </div>
                </label>
                <label class="flex-1 cursor-pointer">
                  <input type="radio" v-model="formEvaluacion.estado" value="RECHAZADO" class="peer sr-only">
                  <div class="text-center p-3 rounded-xl border-2 peer-checked:border-rose-500 peer-checked:bg-rose-50 text-slate-500 peer-checked:text-rose-700 hover:bg-slate-50 transition-all">
                    <div class="text-2xl mb-1">❌</div>
                    <div class="font-bold text-sm">Rechazar</div>
                  </div>
                </label>
              </div>
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-800 mb-2">Comentarios (Opcional)</label>
              <p class="text-xs text-slate-500 mb-2">Si rechazas el reporte, explica al pasante quÃ© debe corregir.</p>
              <textarea v-model="formEvaluacion.comentarios_director" rows="3"
                class="w-full border border-slate-300 rounded-xl p-3 focus:ring-2 focus:ring-slate-800 outline-none transition-shadow text-sm"
                placeholder="Escribe tu mensaje aquÃ­..."></textarea>
            </div>

            <div v-if="mensajeError" class="text-rose-700 bg-rose-50 p-3 text-sm rounded-xl border border-rose-200 flex items-center gap-2">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              {{ mensajeError }}
            </div>

            <div class="flex justify-end gap-3 pt-5 border-t border-slate-100">
              <button type="button" @click="showModal = false" class="px-6 py-2.5 border border-slate-300 rounded-xl text-slate-600 font-medium hover:bg-slate-50 transition-colors">Cancelar</button>
              <button type="submit" :disabled="isSubmitting" class="px-6 py-2.5 bg-slate-800 text-white rounded-xl font-medium hover:bg-slate-900 disabled:opacity-50 transition-all shadow-md">
                {{ isSubmitting ? 'Procesando...' : 'Confirmar DecisiÃ³n' }}
              </button>
            </div>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router    = useRouter()
const authStore = useAuthStore()

const reportes     = ref([])
const searchQuery  = ref('')
const filtroActual = ref('TODOS') // PENDIENTE, APROBADO, RECHAZADO, TODOS
const isLoading    = ref(true)
const showModal    = ref(false)
const isSubmitting = ref(false)
const mensajeError = ref('')

const reporteAEvaluar = ref(null)
const formEvaluacion  = ref({ estado: 'APROBADO', comentarios_director: '' })

// KPIs
const totalPendientes = computed(() => reportes.value.filter(r => r.estado === 'PENDIENTE').length)
const totalAprobados  = computed(() => reportes.value.filter(r => r.estado === 'APROBADO').length)

// Buscador Inteligente y Filtros
const filteredReportes = computed(() => {
  let resultado = reportes.value

  // 1. Aplicar filtro de botones (PestaÃ±as)
  if (filtroActual.value !== 'TODOS') {
    resultado = resultado.filter(r => r.estado === filtroActual.value)
  }

  // 2. Aplicar buscador de texto
  if (searchQuery.value) {
    const lower = searchQuery.value.toLowerCase()
    resultado = resultado.filter(r => 
      (r.nombre_pasante || '').toLowerCase().includes(lower) ||
      r.actividades_realizadas.toLowerCase().includes(lower) ||
      r.estado.toLowerCase().includes(lower)
    )
  }

  return resultado
})

const estadoBadgeClass = (estado) => {
  if (estado === 'APROBADO')  return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  if (estado === 'RECHAZADO') return 'bg-rose-50 text-rose-700 border-rose-200'
  return 'bg-amber-50 text-amber-700 border-amber-200'
}

const estadoDotClass = (estado) => {
  if (estado === 'APROBADO')  return 'bg-emerald-500'
  if (estado === 'RECHAZADO') return 'bg-rose-500'
  return 'bg-amber-500'
}

onMounted(async () => {
  await cargarReportes()
})

const cargarReportes = async () => {
  isLoading.value = true
  try {
    const response = await api.get('/reportes/listar')
    reportes.value = response.data
  } catch (error) {
    console.error('Error al cargar reportes:', error)
  } finally {
    isLoading.value = false
  }
}

// â”€â”€ LÃ³gica para Evaluar Reporte â”€â”€
const abrirModalEvaluar = (reporte) => {
  reporteAEvaluar.value = reporte
  formEvaluacion.value = {
    estado: reporte.estado === 'PENDIENTE' ? 'APROBADO' : reporte.estado,
    comentarios_director: reporte.comentarios_director || ''
  }
  mensajeError.value = ''
  showModal.value = true
}

const guardarEvaluacion = async () => {
  isSubmitting.value = true
  mensajeError.value = ''
  try {
    await api.put(`/reportes/evaluar/${reporteAEvaluar.value.id}`, formEvaluacion.value)
    showModal.value = false
    await cargarReportes() // Recargar para ver los cambios
  } catch (error) {
    console.error(error)
    mensajeError.value = error.response?.data?.detail || "Error al evaluar el reporte. Revisa tus permisos."
  } finally {
    isSubmitting.value = false
  }
}

// â”€â”€ LÃ³gica para Descargar PDF â”€â”€
const descargarPDF = async (reporte) => {
  try {
    const response = await api.get(`/reportes/descargar/${reporte.id}`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    const nombre = reporte.nombre_pasante ? reporte.nombre_pasante.replace(/\s+/g, '') : 'Pasante'
    link.setAttribute('download', `Reporte_${nombre}_${reporte.id}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error al descargar el PDF:', error)
    alert('OcurriÃ³ un error al intentar descargar el documento.')
  }
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/login')
}
</script>
