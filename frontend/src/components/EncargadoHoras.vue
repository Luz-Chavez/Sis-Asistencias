<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Horas de Pasantes</h1>
        <p class="text-sm text-slate-500">
          {{ itemsFiltrados.length }} / {{ items.length }} pasantes
          <span v-if="periodoLabel" class="ml-2">· {{ periodoLabel }}</span>
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="descargarCSV"
          class="inline-flex items-center gap-2 border border-slate-300 bg-white px-4 py-2.5 rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium">
          CSV
        </button>
        <button
          type="button"
          @click="cargarResumen"
          class="inline-flex items-center gap-2 bg-blue-900 text-white px-5 py-2.5 rounded-lg hover:bg-blue-800 transition-colors font-medium shadow-sm">
          Actualizar
        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
        <input
          v-model="filterText"
          type="text"
          placeholder="Buscar: pasante, @username"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm"
        />

        <select v-model="tipo" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="dia">Día</option>
          <option value="semana">Semana</option>
          <option value="mes">Mes</option>
          <option value="total">Total</option>
        </select>

        <input
          v-model="fecha"
          :disabled="tipo === 'total'"
          type="date"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white disabled:bg-slate-100 disabled:text-slate-400"
        />

        <select v-model="sortBy" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="horas_desc">Más horas</option>
          <option value="horas_asc">Menos horas</option>
          <option value="nombre_asc">Nombre (A-Z)</option>
        </select>
      </div>

      <div v-if="error" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
        {{ error }}
      </div>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Pasante</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Usuario</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Registros</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Sin salida</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">Horas</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">Progreso</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-if="isLoading">
              <td colspan="6" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-8 h-8 border-2 border-slate-300 border-t-blue-600 rounded-full animate-spin"></div>
                  <p class="text-slate-500 text-sm">Cargando resumen...</p>
                </div>
              </td>
            </tr>

            <tr v-else-if="itemsFiltradosOrdenados.length === 0">
              <td colspan="6" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <p class="text-slate-500">No hay datos con esos filtros</p>
                </div>
              </td>
            </tr>

            <tr v-else v-for="row in itemsFiltradosOrdenados" :key="row.pasante_id" class="hover:bg-slate-50/50 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-700 font-semibold text-xs">
                    {{ getIniciales(row.nombres, row.apellidos) }}
                  </div>
                  <div>
                    <p class="text-sm font-medium text-slate-800">{{ row.nombres }} {{ row.apellidos }}</p>
                    <p class="text-xs text-slate-400">ID: {{ row.pasante_id }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-slate-600 font-mono">@{{ row.username }}</span>
              </td>
              <td class="px-6 py-4 text-center">
                <span class="text-sm text-slate-600">{{ row.registros }}</span>
              </td>
              <td class="px-6 py-4 text-center">
                <span
                  :class="row.sin_salida > 0 ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-slate-50 text-slate-600 border-slate-200'"
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border">
                  {{ row.sin_salida }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <span class="text-sm font-semibold text-slate-800">{{ formatHoras(row.horas) }}</span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <div class="w-28 h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-emerald-500 rounded-full" :style="{ width: progresoPct(row.horas) + '%' }"></div>
                  </div>
                  <span class="text-xs text-slate-500 w-12 text-right">{{ progresoPct(row.horas) }}%</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const tipo = ref('semana')
const fecha = ref(new Date().toISOString().slice(0, 10))
const sortBy = ref('horas_desc')
const filterText = ref('')

const items = ref([])
const periodo = ref(null)

const isLoading = ref(false)
const error = ref('')

const periodoLabel = computed(() => {
  if (!periodo.value) return ''
  if (periodo.value.tipo === 'total') return 'Total'
  if (periodo.value.inicio && periodo.value.fin) {
    return `${periodo.value.tipo} · ${periodo.value.inicio} → ${periodo.value.fin}`
  }
  return periodo.value.tipo
})

const itemsFiltrados = computed(() => {
  const q = (filterText.value || '').trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter(r => {
    const nombre = `${r.nombres || ''} ${r.apellidos || ''}`.toLowerCase()
    const user = (r.username || '').toLowerCase()
    return nombre.includes(q) || user.includes(q) || String(r.pasante_id).includes(q)
  })
})

const itemsFiltradosOrdenados = computed(() => {
  const arr = [...itemsFiltrados.value]
  if (sortBy.value === 'horas_asc') {
    arr.sort((a, b) => (a.horas || 0) - (b.horas || 0))
  } else if (sortBy.value === 'nombre_asc') {
    arr.sort((a, b) => (`${a.nombres} ${a.apellidos}`).localeCompare(`${b.nombres} ${b.apellidos}`))
  } else {
    arr.sort((a, b) => (b.horas || 0) - (a.horas || 0))
  }
  return arr
})

const formatHoras = (h) => {
  const v = Number(h || 0)
  return `${v.toFixed(2)}h`
}

const progresoPct = (h) => {
  const total = 240
  const v = Number(h || 0)
  const pct = Math.max(0, Math.min(100, Math.round((v / total) * 100)))
  return pct
}

const getIniciales = (nombres, apellidos) => {
  const n = (nombres || '').trim().split(/\s+/).filter(Boolean)
  const a = (apellidos || '').trim().split(/\s+/).filter(Boolean)
  const i1 = n[0]?.[0] || ''
  const i2 = a[0]?.[0] || n[1]?.[0] || ''
  return (i1 + i2).toUpperCase()
}

const cargarResumen = async () => {
  error.value = ''
  isLoading.value = true
  try {
    const params = { tipo: tipo.value }
    if (tipo.value !== 'total') params.fecha = fecha.value

    // Admin podría enviar carrera_id; Encargado/Pasante se ignora del lado backend
    if (authStore.user?.rol_id === 1 && authStore.user?.carrera_id) {
      params.carrera_id = authStore.user.carrera_id
    }

    const { data } = await api.get('/asistencias/resumen-horas', { params })
    items.value = data?.items || []
    periodo.value = data?.periodo || null
  } catch (e) {
    console.error('Error resumen horas:', e)
    error.value = e?.response?.data?.detail || 'No se pudo cargar el resumen de horas.'
    items.value = []
    periodo.value = null
  } finally {
    isLoading.value = false
  }
}

const descargarCSV = () => {
  const rows = itemsFiltradosOrdenados.value
  const header = ['pasante_id', 'nombres', 'apellidos', 'username', 'registros', 'sin_salida', 'horas']
  const lines = [header.join(',')]
  for (const r of rows) {
    const line = [
      r.pasante_id,
      JSON.stringify(r.nombres || ''),
      JSON.stringify(r.apellidos || ''),
      JSON.stringify(r.username || ''),
      r.registros,
      r.sin_salida,
      Number(r.horas || 0).toFixed(2),
    ].join(',')
    lines.push(line)
  }

  const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  const safeTipo = (tipo.value || 'periodo')
  a.href = url
  a.download = `resumen_horas_${safeTipo}.csv`
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

onMounted(() => {
  cargarResumen()
})
</script>
