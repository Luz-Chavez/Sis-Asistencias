<template>
  <!-- Panel de reportes (antes estaba dentro de EncargadoDashboard.vue) -->
  <div class="space-y-6">
    <!-- Cabecera -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Reportes Diarios</h1>
        <span class="text-sm text-slate-500">{{ reportesFiltrados.length }} / {{ reportes.length }} reportes</span>
      </div>
      <button
        @click="evaluarPendiente"
        class="inline-flex items-center gap-2 bg-blue-900 text-white px-5 py-2.5 rounded-lg hover:bg-blue-800 transition-colors font-medium shadow-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        Evaluar siguiente pendiente
      </button>
    </div>

    <!-- Filtros -->
    <div class="bg-white rounded-lg shadow p-4">
      <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
        <input
          v-model="filterText"
          type="text"
          placeholder="Buscar: pasante, actividades, #ID"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm"
        />

        <select v-model="filterEstado" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="all">Todos los estados</option>
          <option value="PENDIENTE">Pendiente</option>
          <option value="APROBADO">Aprobado</option>
          <option value="RECHAZADO">Rechazado</option>
        </select>

        <select v-model="filterYear" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="all">Todos los años</option>
          <option v-for="y in yearOptions" :key="y" :value="String(y)">{{ y }}</option>
        </select>

        <select v-model="filterMonth" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="all">Todos los meses</option>
          <option v-for="m in monthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
        </select>

        <div class="flex gap-2">
          <select v-model="sortBy" class="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
            <option value="newest">Más recientes</option>
            <option value="oldest">Más antiguos</option>
          </select>
          <button
            type="button"
            @click="limpiarFiltros"
            class="px-4 py-2 text-sm border border-slate-300 rounded-lg hover:bg-slate-50">
            Limpiar
          </button>
        </div>
      </div>
    </div>

    <div v-if="errorReportes" class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{{ errorReportes }}</div>

    <!-- Tabla de reportes -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">#</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Pasante</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Fecha</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Actividades</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-if="isLoadingReportes">
              <td colspan="6" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-8 h-8 border-2 border-slate-300 border-t-blue-600 rounded-full animate-spin"></div>
                  <p class="text-slate-500 text-sm">Cargando reportes...</p>
                </div>
              </td>
            </tr>
            <tr v-else-if="reportesFiltrados.length === 0">
              <td colspan="6" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <p class="text-slate-500">No hay reportes con esos filtros</p>
                </div>
              </td>
            </tr>
            <tr v-else v-for="reporte in reportesFiltrados" :key="reporte.id" class="hover:bg-slate-50/50 transition-colors">
              <td class="px-6 py-4">
                <span class="text-sm font-mono text-slate-500">#{{ reporte.id }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-semibold text-xs">
                    {{ getInicialesFromName(reporte.nombre_pasante) }}
                  </div>
                  <span class="text-sm font-medium text-slate-700">{{ reporte.nombre_pasante || 'Pasante #' + reporte.asistencia_id }}</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-slate-500">{{ formatearFecha(reporte.creado_en) }}</span>
              </td>
              <td class="px-6 py-4">
                <p class="text-sm text-slate-500 max-w-md line-clamp-2">{{ reporte.actividades_realizadas }}</p>
              </td>
              <td class="px-6 py-4 text-center">
                <span :class="getEstadoBadgeClass(reporte.estado)" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium">
                  <span :class="getEstadoDotClass(reporte.estado)" class="w-1.5 h-1.5 rounded-full mr-1.5"></span>
                  {{ reporte.estado || 'PENDIENTE' }}
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <button @click="abrirModalEvaluacion(reporte)"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-blue-600 hover:text-white hover:bg-blue-600 border border-blue-200 hover:border-blue-600 rounded-lg transition-all">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
                  </svg>
                  Evaluar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal de evaluación -->
    <div v-if="showModalEvaluacion" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-5 text-white flex items-start justify-between">
          <div>
            <p class="text-blue-100 text-xs font-medium uppercase tracking-wider">Evaluación de reporte</p>
            <h3 class="text-xl font-bold mt-1">Reporte #{{ reporteSeleccionado?.id }}</h3>
            <p class="text-blue-100 text-xs mt-1">{{ reporteSeleccionado?.nombre_pasante || '—' }} · {{ formatearFecha(reporteSeleccionado?.creado_en) }}</p>
          </div>
          <button type="button" @click="cerrarModalEvaluacion" class="text-blue-100 hover:text-white">✕</button>
        </div>

        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Estado</label>
            <select v-model="evaluacion.estado" class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
              <option value="APROBADO">Aprobado</option>
              <option value="RECHAZADO">Rechazado</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Comentarios</label>
            <textarea v-model="evaluacion.comentarios" rows="4" class="w-full border border-slate-300 rounded-lg p-3 text-sm" placeholder="Escribe una observación (opcional)"></textarea>
          </div>

          <div class="pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button type="button" @click="cerrarModalEvaluacion" class="px-4 py-2 text-sm border rounded-lg">Cancelar</button>
            <button type="button" @click="enviarEvaluacion" :disabled="isSubmittingEval" class="px-5 py-2 text-sm bg-blue-900 text-white rounded-lg disabled:opacity-50">
              {{ isSubmittingEval ? 'Guardando...' : 'Guardar evaluación' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import router from '../router'
import api from '../services/api'

type Reporte = {
  id: number
  asistencia_id: number
  actividades_realizadas: string
  estado: string
  comentarios_director?: string | null
  creado_en?: string | Date
  nombre_pasante?: string | null
}

const authStore = useAuthStore()

const reportes = ref<Reporte[]>([])
const isLoadingReportes = ref(false)
const errorReportes = ref('')
const reporteSeleccionado = ref<Reporte | null>(null)
const showModalEvaluacion = ref(false)
const isSubmittingEval = ref(false)
const evaluacion = ref({ estado: 'APROBADO', comentarios: '' })

// filtros
const filterText = ref('')
const filterEstado = ref<'all' | 'PENDIENTE' | 'APROBADO' | 'RECHAZADO'>('all')
const filterYear = ref<'all' | string>('all')
const filterMonth = ref<'all' | string>('all')
const sortBy = ref<'newest' | 'oldest'>('newest')

const monthOptions = [
  { value: '1', label: 'Enero' },
  { value: '2', label: 'Febrero' },
  { value: '3', label: 'Marzo' },
  { value: '4', label: 'Abril' },
  { value: '5', label: 'Mayo' },
  { value: '6', label: 'Junio' },
  { value: '7', label: 'Julio' },
  { value: '8', label: 'Agosto' },
  { value: '9', label: 'Septiembre' },
  { value: '10', label: 'Octubre' },
  { value: '11', label: 'Noviembre' },
  { value: '12', label: 'Diciembre' },
]

const limpiarFiltros = () => {
  filterText.value = ''
  filterEstado.value = 'all'
  filterYear.value = 'all'
  filterMonth.value = 'all'
  sortBy.value = 'newest'
}

const parseDate = (value: unknown): Date | null => {
  if (!value) return null
  const d = value instanceof Date ? value : new Date(String(value))
  return Number.isNaN(d.getTime()) ? null : d
}

const formatearFecha = (value: unknown) => {
  const d = parseDate(value)
  if (!d) return '—'
  return d.toLocaleDateString('es-BO', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const yearOptions = computed(() => {
  const years = new Set<number>()
  for (const r of reportes.value) {
    const d = parseDate(r.creado_en)
    if (d) years.add(d.getFullYear())
  }
  return Array.from(years).sort((a, b) => b - a)
})

const reportesFiltrados = computed(() => {
  let list = reportes.value.slice()

  // estado
  if (filterEstado.value !== 'all') {
    list = list.filter(r => (r.estado || 'PENDIENTE') === filterEstado.value)
  }

  // año/mes
  if (filterYear.value !== 'all' || filterMonth.value !== 'all') {
    list = list.filter(r => {
      const d = parseDate(r.creado_en)
      if (!d) return false
      if (filterYear.value !== 'all' && String(d.getFullYear()) !== String(filterYear.value)) return false
      if (filterMonth.value !== 'all' && String(d.getMonth() + 1) !== String(filterMonth.value)) return false
      return true
    })
  }

  // texto
  const q = filterText.value.trim().toLowerCase()
  if (q) {
    list = list.filter(r => {
      const nombre = (r.nombre_pasante || '').toLowerCase()
      const actividades = (r.actividades_realizadas || '').toLowerCase()
      const id = String(r.id)
      const asistenciaId = String(r.asistencia_id)
      return (
        nombre.includes(q) ||
        actividades.includes(q) ||
        id.includes(q) ||
        asistenciaId.includes(q)
      )
    })
  }

  // orden
  const factor = sortBy.value === 'newest' ? -1 : 1
  list.sort((a, b) => {
    const da = parseDate(a.creado_en)?.getTime() ?? 0
    const db = parseDate(b.creado_en)?.getTime() ?? 0
    if (da === db) return 0
    return da < db ? -1 * factor : 1 * factor
  })

  return list
})

const cargarReportes = async () => {
  isLoadingReportes.value = true
  errorReportes.value = ''
  try {
    const { data } = await api.get('/reportes/listar')
    reportes.value = data
  } catch (e: any) {
    if (e.response?.status === 401) {
      cerrarSesion()
    } else {
      errorReportes.value = e.response?.data?.detail || 'No se pudo cargar los reportes.'
      reportes.value = []
    }
  } finally {
    isLoadingReportes.value = false
  }
}

const abrirModalEvaluacion = (reporte: Reporte) => {
  reporteSeleccionado.value = reporte
  evaluacion.value.estado = reporte.estado && reporte.estado !== 'PENDIENTE' ? reporte.estado : 'APROBADO'
  evaluacion.value.comentarios = (reporte as any).comentarios_director || ''
  showModalEvaluacion.value = true
}

const cerrarModalEvaluacion = () => {
  showModalEvaluacion.value = false
  reporteSeleccionado.value = null
}

const enviarEvaluacion = async () => {
  if (!reporteSeleccionado.value) return
  isSubmittingEval.value = true
  try {
    await api.put(`/reportes/evaluar/${reporteSeleccionado.value.id}`, {
      estado: evaluacion.value.estado,
      comentarios_director: evaluacion.value.comentarios,
    })
    await cargarReportes()
    cerrarModalEvaluacion()
    alert('✅ Evaluación guardada con éxito')
  } catch {
    alert('Error al guardar la evaluación.')
  } finally {
    isSubmittingEval.value = false
  }
}

const evaluarPendiente = () => {
  const pendiente = reportes.value.find(r => (r.estado || 'PENDIENTE') === 'PENDIENTE')
  if (pendiente) abrirModalEvaluacion(pendiente)
  else alert('No hay reportes pendientes.')
}

// utilidades visuales
const getInicialesFromName = (fullName?: string | null) => {
  if (!fullName) return '?'
  const parts = fullName.split(' ')
  return `${parts[0]?.[0] || ''}${parts[1]?.[0] || ''}`.toUpperCase()
}

const getEstadoBadgeClass = (estado?: string) => {
  if (estado === 'APROBADO') return 'bg-emerald-50 text-emerald-700'
  if (estado === 'RECHAZADO') return 'bg-red-50 text-red-700'
  return 'bg-amber-50 text-amber-700'
}

const getEstadoDotClass = (estado?: string) => {
  if (estado === 'APROBADO') return 'bg-emerald-500'
  if (estado === 'RECHAZADO') return 'bg-red-500'
  return 'bg-amber-500'
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/')
}

onMounted(cargarReportes)
</script>