<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
    <!-- NAVBAR -->
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
            <button
              @click="router.push('/dashboard')"
              class="px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-all"
              title="Volver"
            >
              Volver
            </button>
            <button
              @click="cerrarSesion"
              class="flex items-center gap-2 text-sm text-slate-600 hover:text-red-600 transition-colors"
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

    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-6 py-5 border-b border-slate-100 bg-slate-50/50">
          <h1 class="text-xl font-bold text-slate-800">Reporte PDF</h1>
          <p class="text-sm text-slate-500">Descarga tu reporte semanal o mensual.</p>
        </div>

        <div class="p-6">
          <div class="flex flex-wrap items-end gap-3">
            <div class="flex-1 min-w-[200px]">
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1.5">Tipo</label>
              <div class="flex rounded-lg overflow-hidden border border-slate-200">
                <button
                  @click="tipoPdf = 'semanal'"
                  :class="tipoPdf === 'semanal' ? 'bg-emerald-900 text-white' : 'bg-white text-slate-500 hover:bg-slate-50'"
                  class="px-4 py-2 text-sm font-medium transition-all duration-200 w-full"
                >
                  Semanal
                </button>
                <button
                  @click="tipoPdf = 'mensual'"
                  :class="tipoPdf === 'mensual' ? 'bg-emerald-900 text-white' : 'bg-white text-slate-500 hover:bg-slate-50'"
                  class="px-4 py-2 text-sm font-medium transition-all duration-200 w-full"
                >
                  Mensual
                </button>
              </div>
            </div>

            <div v-if="tipoPdf === 'semanal'" class="flex-1 min-w-[200px]">
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1.5">Cualquier dia de la semana</label>
              <input
                type="date"
                v-model="pdfFechaSemana"
                :min="`${anioMin}-01-01`"
                :max="`${anioMax}-12-31`"
                class="border border-slate-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none
                       focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
              />
              <p v-if="infoSemana" class="mt-1.5 text-xs text-emerald-700 font-medium">{{ infoSemana }}</p>
            </div>

            <div v-if="tipoPdf === 'mensual'" class="flex gap-2 items-end flex-1 min-w-[200px]">
              <div class="flex-1">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1.5">Mes</label>
                <select
                  v-model="pdfMes"
                  class="border border-slate-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none
                         focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
                >
                  <option v-for="(nombre, idx) in mesesNombres" :key="idx + 1" :value="idx + 1">{{ nombre }}</option>
                </select>
              </div>
              <div class="flex-1">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1.5">Ano</label>
                <select
                  v-model="pdfAnio"
                  class="border border-slate-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none
                         focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
                >
                  <option v-for="y in aniosDisponibles" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
            </div>

            <button
              @click="descargarPdf"
              :disabled="descargando"
              class="inline-flex items-center justify-center gap-2 bg-emerald-900 hover:bg-emerald-800 text-white px-5 py-2 rounded-lg
                     text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm flex-1"
            >
              <svg v-if="descargando" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
              </svg>
              {{ descargando ? 'Generando...' : 'Descargar PDF' }}
            </button>
          </div>

          <p v-if="errorDescarga" class="mt-4 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-lg">
            {{ errorDescarga }}
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const resolveStaticUrl = (url) => {
  if (!url) return null
  const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`
  return s
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/')
}

const tipoPdf = ref('semanal')
const pdfAnio = ref(new Date().getFullYear())
const pdfMes = ref(new Date().getMonth() + 1)
const descargando = ref(false)
const errorDescarga = ref('')

const pdfFechaSemana = ref(new Date().toISOString().split('T')[0])
const anioMin = new Date().getFullYear()
const anioMax = 2028

const mesesNombres = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

const aniosDisponibles = computed(() => {
  const inicio = new Date().getFullYear()
  const anos = []
  for (let y = inicio; y <= 2028; y++) anos.push(y)
  return anos
})

function isoSemana(d) {
  const tmp = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()))
  tmp.setUTCDate(tmp.getUTCDate() + 4 - (tmp.getUTCDay() || 7))
  const inicio = new Date(Date.UTC(tmp.getUTCFullYear(), 0, 1))
  return Math.ceil((((tmp - inicio) / 86400000) + 1) / 7)
}

const infoSemana = computed(() => {
  if (!pdfFechaSemana.value) return ''
  const d = new Date(pdfFechaSemana.value + 'T12:00:00')
  const diaSem = (d.getDay() + 6) % 7
  const lunes = new Date(d); lunes.setDate(d.getDate() - diaSem)
  const domingo = new Date(lunes); domingo.setDate(lunes.getDate() + 6)
  const fmt = (dt) => dt.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })
  const sem = isoSemana(d)
  return `Semana ${sem}  ·  ${fmt(lunes)} – ${fmt(domingo)}`
})

const descargarPdf = async () => {
  descargando.value = true
  errorDescarga.value = ''
  try {
    let url
    if (tipoPdf.value === 'semanal') {
      const d = new Date(pdfFechaSemana.value + 'T12:00:00')
      const sem = isoSemana(d)
      const anio = d.getFullYear()
      url = `/reportes/pdf/semanal?anio=${anio}&semana=${sem}`
    } else {
      url = `/reportes/pdf/mensual?anio=${pdfAnio.value}&mes=${pdfMes.value}`
    }

    const response = await api.get(url, { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const href = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = href
    const cd = response.headers['content-disposition'] || ''
    const match = cd.match(/filename="?([^"]+)"?/)
    a.download = match ? match[1] : `reporte_${tipoPdf.value}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(href)
  } catch (e) {
    errorDescarga.value = e.response?.data?.detail ?? 'No hay registros para el periodo seleccionado.'
  } finally {
    descargando.value = false
  }
}
</script>

