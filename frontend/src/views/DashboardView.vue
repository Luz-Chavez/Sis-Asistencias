<template>
  <div class="min-h-screen bg-gray-50">

    <!-- NAV -->
    <nav class="bg-blue-700 shadow-md">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 bg-blue-500 rounded-full flex items-center justify-center
                        text-white font-bold text-sm shrink-0">
              {{ iniciales }}
            </div>
            <div class="hidden sm:block">
              <p class="text-white font-semibold text-sm leading-tight">{{ authStore.user?.nombres }}</p>
              <p class="text-blue-200 text-xs font-mono">{{ authStore.user?.username }}</p>
            </div>
          </div>
          <h1 class="text-white font-bold text-base sm:text-lg">Mi Asistencia</h1>
          <button @click="cerrarSesion"
            class="text-sm bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-800 transition shadow">
            Cerrar sesión
          </button>
        </div>
      </div>
    </nav>

    <main class="max-w-5xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-6">

      <!-- Tarjetas resumen -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white rounded-2xl shadow-sm p-4 text-center border border-gray-100">
          <p class="text-3xl font-black text-blue-600">{{ stats.totalDias }}</p>
          <p class="text-xs text-gray-400 mt-1 uppercase font-semibold tracking-wide">Días registrados</p>
        </div>
        <div class="bg-white rounded-2xl shadow-sm p-4 text-center border border-gray-100">
          <p class="text-3xl font-black text-emerald-500">{{ stats.totalHoras }}h</p>
          <p class="text-xs text-gray-400 mt-1 uppercase font-semibold tracking-wide">Horas acumuladas</p>
        </div>
        <div class="bg-white rounded-2xl shadow-sm p-4 text-center border border-gray-100">
          <p class="text-3xl font-black text-yellow-500">{{ stats.reportesPendientes }}</p>
          <p class="text-xs text-gray-400 mt-1 uppercase font-semibold tracking-wide">Pendientes</p>
        </div>
        <div class="bg-white rounded-2xl shadow-sm p-4 text-center border border-gray-100">
          <p class="text-3xl font-black text-green-600">{{ stats.reportesAprobados }}</p>
          <p class="text-xs text-gray-400 mt-1 uppercase font-semibold tracking-wide">Aprobados</p>
        </div>
      </div>

      <!-- Panel de descarga PDF -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 px-6 py-5">
        <h2 class="font-bold text-gray-800 mb-1 flex items-center gap-2">
          <span class="text-lg">📄</span> Descargar Reporte PDF
        </h2>
        <p class="text-xs text-gray-400 mb-4">
          Elige el período y tipo de reporte. El reporte semanal ocupa media hoja; el mensual, una hoja completa.
        </p>

        <div class="flex flex-wrap items-end gap-3">

          <!-- Tipo -->
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Tipo</label>
            <div class="flex rounded-lg overflow-hidden border border-gray-200">
              <button @click="tipoPdf = 'semanal'"
                :class="tipoPdf === 'semanal' ? 'bg-blue-600 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
                class="px-4 py-2 text-sm font-medium transition">
                Semanal
              </button>
              <button @click="tipoPdf = 'mensual'"
                :class="tipoPdf === 'mensual' ? 'bg-blue-600 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
                class="px-4 py-2 text-sm font-medium transition">
                Mensual
              </button>
            </div>
          </div>

          <!-- Año -->
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Año</label>
            <select v-model="pdfAnio"
              class="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300">
              <option v-for="y in aniosDisponibles" :key="y" :value="y">{{ y }}</option>
            </select>
          </div>

          <!-- Semana (solo si semanal) -->
          <div v-if="tipoPdf === 'semanal'">
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Semana</label>
            <select v-model="pdfSemana"
              class="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300">
              <option v-for="s in semanasDelAnio" :key="s.num" :value="s.num">
                Sem {{ s.num }} — {{ s.rango }}
              </option>
            </select>
          </div>

          <!-- Mes (solo si mensual) -->
          <div v-if="tipoPdf === 'mensual'">
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Mes</label>
            <select v-model="pdfMes"
              class="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300">
              <option v-for="(nombre, idx) in mesesNombres" :key="idx+1" :value="idx+1">{{ nombre }}</option>
            </select>
          </div>

          <!-- Botón descargar -->
          <button @click="descargarPdf" :disabled="descargando"
            class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg
                   text-sm font-bold transition disabled:opacity-50 disabled:cursor-not-allowed shadow">
            <svg v-if="descargando" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
            </svg>
            {{ descargando ? 'Generando...' : 'Descargar PDF' }}
          </button>

        </div>

        <!-- Error descarga -->
        <p v-if="errorDescarga" class="mt-3 text-red-600 text-xs bg-red-50 p-2 rounded-lg">
          {{ errorDescarga }}
        </p>
      </div>

      <!-- Historial -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <div>
            <h2 class="font-bold text-gray-800">Historial de Asistencias</h2>
            <p class="text-xs text-gray-400 mt-0.5">Registro de entradas, salidas y reportes</p>
          </div>
          <button @click="cargarHistorial" title="Actualizar"
            class="text-gray-400 hover:text-blue-500 transition p-1 rounded">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" :class="isLoading ? 'animate-spin' : ''"
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </button>
        </div>

        <div v-if="isLoading" class="py-12 text-center text-gray-400">
          <svg class="animate-spin w-8 h-8 mx-auto mb-3 text-blue-400" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          <p class="text-sm">Cargando historial...</p>
        </div>

        <div v-else-if="historial.length === 0" class="py-12 text-center text-gray-400">
          <div class="text-4xl mb-3">📋</div>
          <p class="font-medium">No tienes asistencias registradas aún.</p>
          <p class="text-xs mt-1">Ficha tu entrada en la pantalla principal.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="min-w-full">
            <thead class="bg-gray-50 border-b border-gray-100">
              <tr>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Fecha</th>
                <th class="px-5 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Entrada</th>
                <th class="px-5 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Salida</th>
                <th class="px-5 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Horas</th>
                <th class="px-5 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Reporte</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="item in historial" :key="item.id" class="hover:bg-gray-50 transition">

                <td class="px-5 py-4">
                  <p class="text-sm font-semibold text-gray-800">{{ formatFecha(item.fecha) }}</p>
                  <p class="text-xs text-gray-400">{{ diaSemana(item.fecha) }}</p>
                </td>

                <td class="px-5 py-4 text-center">
                  <span class="text-sm font-mono text-gray-700">{{ formatHora(item.hora_entrada) }}</span>
                </td>

                <td class="px-5 py-4 text-center">
                  <span v-if="item.hora_salida" class="text-sm font-mono text-gray-700">
                    {{ formatHora(item.hora_salida) }}
                  </span>
                  <span v-else class="text-xs text-yellow-600 bg-yellow-50 px-2 py-0.5 rounded-full font-medium">
                    En curso
                  </span>
                </td>

                <td class="px-5 py-4 text-center">
                  <span v-if="item.horas_trabajadas" class="text-sm font-bold"
                    :class="item.horas_trabajadas >= 4 ? 'text-emerald-600' : 'text-orange-500'">
                    {{ item.horas_trabajadas }}h
                  </span>
                  <span v-else class="text-gray-300 text-sm">—</span>
                </td>

                <td class="px-5 py-4 text-center">
                  <span v-if="!item.hora_salida" class="text-gray-300 text-sm">—</span>

                  <button v-else-if="!item.reporte" @click="abrirModalReporte(item)"
                    class="text-xs bg-blue-50 text-blue-600 px-3 py-1 rounded-full hover:bg-blue-100
                           transition font-medium border border-blue-200">
                    + Agregar reporte
                  </button>

                  <div v-else class="flex flex-col items-center gap-1">
                    <span :class="{
                      'bg-green-100 text-green-700':   item.reporte.estado === 'APROBADO',
                      'bg-red-100 text-red-600':       item.reporte.estado === 'RECHAZADO',
                      'bg-yellow-100 text-yellow-700': item.reporte.estado === 'PENDIENTE',
                    }" class="text-xs font-semibold px-2 py-0.5 rounded-full">
                      {{ item.reporte.estado }}
                    </span>
                    <p v-if="item.reporte.comentarios_director"
                      class="text-xs text-gray-400 max-w-xs truncate"
                      :title="item.reporte.comentarios_director">
                      "{{ item.reporte.comentarios_director }}"
                    </p>
                  </div>
                </td>

              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </main>

    <!-- ══════════════ MODAL: Agregar reporte desde historial ══════════════ -->
    <transition name="modal">
      <div v-if="showModalReporte"
        class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 px-4 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">

          <div class="bg-blue-600 px-6 py-4 flex justify-between items-center">
            <div>
              <h3 class="text-white font-bold text-base">Reporte del día</h3>
              <p class="text-blue-200 text-xs">{{ formatFecha(asistenciaSeleccionada?.fecha) }}</p>
            </div>
            <button @click="showModalReporte = false" class="text-white hover:text-blue-200 text-xl font-bold">&times;</button>
          </div>

          <div class="px-6 py-5">
            <label class="block text-sm font-bold text-gray-700 mb-2">
              ¿Qué actividades realizaste ese día?
            </label>
            <textarea v-model="actividadesModal" rows="5"
              placeholder="Describe las tareas que realizaste..."
              class="w-full border-2 border-gray-200 rounded-xl p-3 text-sm resize-none
                     focus:outline-none focus:border-blue-400 transition"></textarea>
            <p v-if="errorModal" class="mt-2 text-red-600 text-xs bg-red-50 p-2 rounded-lg">{{ errorModal }}</p>
          </div>

          <div class="px-6 pb-5 flex gap-3">
            <button @click="showModalReporte = false"
              class="flex-1 py-2.5 border-2 border-gray-200 text-gray-500 rounded-xl text-sm font-medium hover:bg-gray-50 transition">
              Cancelar
            </button>
            <button @click="guardarReporteModal" :disabled="isSubmittingModal || !actividadesModal.trim()"
              class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm font-bold hover:bg-blue-700
                     transition disabled:opacity-50 shadow">
              {{ isSubmittingModal ? 'Guardando...' : 'Guardar Reporte' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router    = useRouter()
const authStore = useAuthStore()

const historial = ref([])
const isLoading = ref(true)

// ── Modal reporte ──────────────────────────────────────────────────────────────
const showModalReporte       = ref(false)
const asistenciaSeleccionada = ref(null)
const actividadesModal       = ref('')
const isSubmittingModal      = ref(false)
const errorModal             = ref('')

// ── PDF ────────────────────────────────────────────────────────────────────────
const tipoPdf      = ref('semanal')
const pdfAnio      = ref(new Date().getFullYear())
const pdfSemana    = ref(isoSemanaActual())
const pdfMes       = ref(new Date().getMonth() + 1)
const descargando  = ref(false)
const errorDescarga = ref('')

const mesesNombres = [
  'Enero','Febrero','Marzo','Abril','Mayo','Junio',
  'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'
]

const aniosDisponibles = computed(() => {
  const hoy = new Date().getFullYear()
  return [hoy - 1, hoy, hoy + 1].filter(y => y >= 2024)
})

// Genera lista de semanas ISO del año seleccionado
const semanasDelAnio = computed(() => {
  const semanas = []
  let d = new Date(pdfAnio.value, 0, 4) // 4 de enero siempre está en semana 1
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7)) // retroceder al lunes
  let semNum = 1
  while (d.getFullYear() <= pdfAnio.value) {
    const lunes   = new Date(d)
    const domingo = new Date(d)
    domingo.setDate(domingo.getDate() + 6)
    if (lunes.getFullYear() === pdfAnio.value || domingo.getFullYear() === pdfAnio.value) {
      semanas.push({
        num:   semNum,
        rango: `${lunes.getDate().toString().padStart(2,'0')}/${(lunes.getMonth()+1).toString().padStart(2,'0')} – ${domingo.getDate().toString().padStart(2,'0')}/${(domingo.getMonth()+1).toString().padStart(2,'0')}`
      })
    }
    d.setDate(d.getDate() + 7)
    semNum++
    if (semNum > 53) break
  }
  return semanas
})

function isoSemanaActual() {
  const hoy = new Date()
  const inicioAnio = new Date(hoy.getFullYear(), 0, 1)
  const diasDesdeInicio = Math.floor((hoy - inicioAnio) / 86400000)
  return Math.ceil((diasDesdeInicio + inicioAnio.getDay() + 1) / 7)
}

// ── Iniciales avatar ───────────────────────────────────────────────────────────
const iniciales = computed(() => {
  const n = authStore.user?.nombres?.[0] ?? ''
  const a = authStore.user?.apellidos?.[0] ?? ''
  return (n + a).toUpperCase()
})

// ── Estadísticas ───────────────────────────────────────────────────────────────
const stats = computed(() => ({
  totalDias:          historial.value.length,
  totalHoras:         Math.round(historial.value.reduce((a, i) => a + (parseFloat(i.horas_trabajadas) || 0), 0) * 10) / 10,
  reportesPendientes: historial.value.filter(i => i.reporte?.estado === 'PENDIENTE').length,
  reportesAprobados:  historial.value.filter(i => i.reporte?.estado === 'APROBADO').length,
}))

// ── Formatos ───────────────────────────────────────────────────────────────────
const formatFecha = (f) => f ? new Date(f).toLocaleDateString('es-BO', { day:'2-digit', month:'short', year:'numeric' }) : '—'
const diaSemana   = (f) => f ? new Date(f).toLocaleDateString('es-BO', { weekday:'long' }) : ''
const formatHora  = (dt) => dt ? new Date(dt).toLocaleTimeString('es-BO', { hour:'2-digit', minute:'2-digit' }) : '—'

// ── Cargar historial ───────────────────────────────────────────────────────────
const cargarHistorial = async () => {
  isLoading.value = true
  try {
    const { data } = await api.get('/asistencias/mis-asistencias')
    historial.value = data
  } catch (e) {
    if (e.response?.status === 401) cerrarSesion()
  } finally {
    isLoading.value = false
  }
}

// ── Descargar PDF ──────────────────────────────────────────────────────────────
const descargarPdf = async () => {
  descargando.value  = true
  errorDescarga.value = ''
  try {
    let url
    if (tipoPdf.value === 'semanal') {
      url = `/reportes/pdf/semanal?anio=${pdfAnio.value}&semana=${pdfSemana.value}`
    } else {
      url = `/reportes/pdf/mensual?anio=${pdfAnio.value}&mes=${pdfMes.value}`
    }

    // Descarga con blob para que el navegador abra el PDF directamente
    const response = await api.get(url, { responseType: 'blob' })

    const blob = new Blob([response.data], { type: 'application/pdf' })
    const href = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href     = href

    // Extraer nombre de archivo del header si viene
    const cd = response.headers['content-disposition'] || ''
    const match = cd.match(/filename="?([^"]+)"?/)
    a.download = match ? match[1] : `reporte_${tipoPdf.value}.pdf`

    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(href)

  } catch (e) {
    errorDescarga.value = e.response?.data?.detail
      ?? 'No hay registros para el período seleccionado o ocurrió un error.'
  } finally {
    descargando.value = false
  }
}

// ── Modal reporte desde historial ─────────────────────────────────────────────
const abrirModalReporte = (asistencia) => {
  asistenciaSeleccionada.value = asistencia
  actividadesModal.value       = asistencia.reporte?.actividades_realizadas || ''
  errorModal.value             = ''
  showModalReporte.value       = true
}

const guardarReporteModal = async () => {
  if (!actividadesModal.value.trim()) return
  isSubmittingModal.value = true
  errorModal.value = ''
  try {
    await api.post('/reportes/subir', {
      asistencia_id:          asistenciaSeleccionada.value.id,
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

// ── Sesión ─────────────────────────────────────────────────────────────────────
const cerrarSesion = () => {
  authStore.logout()
  router.push('/')
}

onMounted(cargarHistorial)
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.modal-enter-from, .modal-leave-to       { opacity: 0; transform: scale(0.97); }
</style>