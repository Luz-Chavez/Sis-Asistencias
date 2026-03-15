<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-blue-50">
    <!-- Header -->
    <header class="bg-emerald-900 text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center gap-4">
            <button
              @click="$router.go(-1)"
              class="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg text-white transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              Volver
            </button>
            <div>
              <h1 class="text-xl font-bold">Reporte PDF</h1>
              <p class="text-emerald-100 text-sm">Descarga tu reporte semanal o mensual.</p>
            </div>
          </div>
          <button
            @click="cerrarSesion"
            class="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg text-white transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            Cerrar sesión
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-6 py-5 border-b border-slate-100 bg-slate-50/50">
          <h1 class="text-xl font-bold text-slate-800">Reporte PDF</h1>
        </div>

        <div class="p-6">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-4">
            <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
              </svg>
              Configurar Reporte PDF
            </h3>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <!-- Tipo de Reporte -->
              <div>
                <label class="block text-sm font-semibold text-slate-700 mb-2">Tipo de Reporte</label>
                <div class="flex rounded-lg overflow-hidden border border-slate-300">
                  <button
                    @click="tipoPdf = 'semanal'"
                    :class="tipoPdf === 'semanal' ? 'bg-emerald-600 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'"
                    class="px-4 py-3 text-sm font-medium transition-all duration-200 flex-1"
                  >Semanal</button>
                  <button
                    @click="tipoPdf = 'mensual'"
                    :class="tipoPdf === 'mensual' ? 'bg-emerald-600 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'"
                    class="px-4 py-3 text-sm font-medium transition-all duration-200 flex-1"
                  >Mensual</button>
                </div>
              </div>

              <!-- Filtro Semanal -->
              <div v-if="tipoPdf === 'semanal'">
                <label class="block text-sm font-semibold text-slate-700 mb-2">Seleccionar Semana</label>
                <div class="space-y-3">
                  <div>
                    <label class="block text-xs text-slate-600 mb-1">Cualquier día de la semana</label>
                    <input
                      type="date"
                      v-model="pdfFechaSemana"
                      class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none
                             focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
                    />
                  </div>
                  <div v-if="infoSemana" class="bg-emerald-50 border border-emerald-200 rounded-lg p-3">
                    <p class="text-sm text-emerald-800 font-medium">{{ infoSemana }}</p>
                  </div>
                </div>
              </div>

              <!-- Filtro Mensual -->
              <div v-if="tipoPdf === 'mensual'">
                <label class="block text-sm font-semibold text-slate-700 mb-2">Seleccionar Mes y Año</label>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs text-slate-600 mb-1">Mes</label>
                    <select
                      v-model="pdfMes"
                      class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none
                             focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
                    >
                      <option v-for="(nombre, idx) in mesesNombres" :key="idx + 1" :value="idx + 1">{{ nombre }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-xs text-slate-600 mb-1">Año</label>
                    <select
                      v-model="pdfAnio"
                      class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none
                             focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
                    >
                      <option v-for="y in aniosDisponibles" :key="y" :value="y">{{ y }}</option>
                    </select>
                  </div>
                </div>
                <div v-if="pdfMes && pdfAnio" class="bg-blue-50 border border-blue-200 rounded-lg p-3 mt-3">
                  <p class="text-sm text-blue-800 font-medium">
                    Reporte: {{ mesesNombres[pdfMes - 1] }} {{ pdfAnio }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <p v-if="errorDescarga" class="mt-4 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-lg">
            {{ errorDescarga }}
          </p>

          <p v-if="avisoPasante" class="mt-4 text-amber-700 text-sm bg-amber-50 border border-amber-200 p-3 rounded-lg">
            {{ avisoPasante }}
          </p>

          <p v-if="errorVistaPrevia" class="mt-4 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-lg">
            {{ errorVistaPrevia }}
          </p>
        </div>
      </div>

      <!-- TABLA DE ASISTENCIAS -->
      <div v-if="datosVistaPrevia.length > 0" class="bg-white border border-slate-200 rounded-xl shadow-lg overflow-hidden mt-6">
        <div class="bg-slate-800 text-white px-6 py-4">
          <h3 class="text-lg font-semibold flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
            Reporte {{ tipoPdf === 'semanal' ? 'Semanal' : 'Mensual' }}
          </h3>
          <p v-if="usuarioReporte && requierePasante" class="text-slate-300 text-xs mt-1">
            Pasante: {{ usuarioReporte?.nombres }} {{ usuarioReporte?.apellidos }} (ID: {{ usuarioReporte?.id }})
          </p>
          <p class="text-slate-300 text-sm mt-1">
            <span v-if="tipoPdf === 'semanal'">
              {{ obtenerRangoFechasSemana() }}
            </span>
            <span v-else>
              {{ mesesNombres[pdfMes - 1] }} {{ pdfAnio }}
            </span>
          </p>
        </div>

        <div class="p-6">
          <!-- Tabla -->
          <div class="overflow-x-auto">
            <table class="w-full text-sm border-collapse">
              <thead>
                <tr class="bg-slate-100 border-b-2 border-slate-300">
                  <th class="px-4 py-3 text-left font-bold text-slate-700 whitespace-nowrap">Fecha</th>
                  <th class="px-4 py-3 text-left font-bold text-slate-700 whitespace-nowrap">Entrada</th>
                  <th class="px-4 py-3 text-left font-bold text-slate-700 whitespace-nowrap">Salida</th>
                  <th class="px-4 py-3 text-left font-bold text-slate-700 whitespace-nowrap">Horas</th>
                  <th class="px-4 py-3 text-left font-bold text-blue-700 whitespace-nowrap">Est. Encargado</th>
                  <th class="px-4 py-3 text-left font-bold text-emerald-700 whitespace-nowrap">Est. Admin</th>
                  <th class="px-4 py-3 text-left font-bold text-slate-700">Actividades</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, index) in datosVistaPrevia"
                  :key="index"
                  :class="index % 2 === 0 ? 'bg-white' : 'bg-slate-50'"
                  class="border-b border-slate-200 hover:bg-blue-50/30 transition-colors"
                >
                  <td class="px-4 py-3 text-slate-800 font-medium whitespace-nowrap">{{ row.fecha }}</td>
                  <td class="px-4 py-3 text-slate-700 font-mono whitespace-nowrap">{{ row.entrada }}</td>
                  <td class="px-4 py-3 text-slate-700 font-mono whitespace-nowrap">{{ row.salida }}</td>
                  <td class="px-4 py-3 text-slate-800 font-bold whitespace-nowrap">{{ row.horas }}</td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span :class="badgeEstado(row.estado_encargado)"
                          class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                      {{ row.estado_encargado }}
                    </span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span :class="badgeEstado(row.estado_admin)"
                          class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                      {{ row.estado_admin }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-slate-600 max-w-xs truncate" :title="row.comentario">
                    {{ row.comentario || '—' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Resumen -->
          <div class="mt-6 bg-emerald-50 border border-emerald-200 rounded-xl p-5">
            <h4 class="font-bold text-emerald-900 mb-3">Resumen del Período</h4>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
              <div class="bg-white rounded-lg p-3 border border-emerald-100 text-center">
                <p class="text-xs font-bold text-emerald-700 uppercase mb-1">Total Días</p>
                <p class="text-2xl font-black text-emerald-900">{{ datosVistaPrevia.length }}</p>
              </div>
              <div class="bg-white rounded-lg p-3 border border-emerald-100 text-center">
                <p class="text-xs font-bold text-emerald-700 uppercase mb-1">Total Horas</p>
                <p class="text-2xl font-black text-emerald-900">{{ totalHorasVistaPrevia }}h</p>
              </div>
              <div class="bg-white rounded-lg p-3 border border-emerald-100 text-center">
                <p class="text-xs font-bold text-emerald-700 uppercase mb-1">Aprobados</p>
                <p class="text-2xl font-black text-emerald-900">{{ contadorEstados['APROBADO'] || 0 }}</p>
              </div>
              <div class="bg-white rounded-lg p-3 border border-amber-100 text-center">
                <p class="text-xs font-bold text-amber-700 uppercase mb-1">Pendientes</p>
                <p class="text-2xl font-black text-amber-900">{{ contadorEstados['PENDIENTE'] || 0 }}</p>
              </div>
            </div>
            
            <!-- Botón para generar PDF -->
            <div class="flex justify-center">
              <button
                @click="generarPdfDesdeVistaPrevia"
                :disabled="descargando || !puedeGenerarPdf"
                class="inline-flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl
                       text-base font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
              >
                <svg v-if="descargando" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
                </svg>
                {{ descargando ? 'Generando PDF...' : 'Generar PDF desde Datos' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Mensaje cuando no hay datos -->
      <div v-else-if="(tipoPdf === 'semanal' && pdfFechaSemana) || (tipoPdf === 'mensual' && pdfMes && pdfAnio)" class="bg-white border border-slate-200 rounded-xl shadow-lg overflow-hidden mt-6">
        <div class="p-12 text-center">
          <svg class="w-12 h-12 text-slate-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
          </svg>
          <p class="text-slate-600 font-medium">No hay asistencias para este período</p>
          <p class="text-slate-400 text-sm mt-1">Selecciona otro período o registra tus asistencias primero</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const route     = useRoute()
const router    = useRouter()
const authStore = useAuthStore()

const rol = computed(() => authStore.user?.rol)
const requierePasante = computed(() => rol.value === 'ADMINISTRADOR' || rol.value === 'ENCARGADO')

const pasanteId = computed(() => {
  if (!requierePasante.value) return authStore.user?.id ?? null
  const q = route.query?.pasante_id ?? route.query?.pasanteId ?? route.query?.id
  const n = q != null && q !== '' ? Number(q) : null
  return Number.isFinite(n) ? n : null
})

// Estados
const tipoPdf              = ref('semanal')
const pdfFechaSemana       = ref('')
const pdfMes               = ref(new Date().getMonth() + 1)
const pdfAnio              = ref(new Date().getFullYear())
const datosVistaPrevia     = ref([])
const totalHorasVistaPrevia = ref(0)
const contadorEstados      = ref({})
const descargando          = ref(false)
const errorDescarga        = ref('')
const errorVistaPrevia     = ref('')
const usuarioReporte       = ref(null)

// Watchers para cargar datos automáticamente
watch([pdfFechaSemana, pdfMes, pdfAnio, tipoPdf, pasanteId], () => {
  if (requierePasante.value && !pasanteId.value) return
  if ((tipoPdf.value === 'semanal' && pdfFechaSemana.value) || 
      (tipoPdf.value === 'mensual' && pdfMes.value && pdfAnio.value)) {
    cargarVistaPrevia()
  }
}, { immediate: false })

watch([pasanteId, requierePasante], async () => {
  errorVistaPrevia.value = ''
  usuarioReporte.value = null

  if (!requierePasante.value) {
    usuarioReporte.value = authStore.user ?? null
    return
  }

  if (!pasanteId.value) return

  try {
    const { data } = await api.get('/usuarios/listar', { timeout: 30000 })
    const found = (data || []).find((u) => String(u.id) === String(pasanteId.value))
    if (!found) {
      errorVistaPrevia.value = 'No se encontro el pasante con ese id.'
      return
    }
    usuarioReporte.value = found
  } catch (e) {
    errorVistaPrevia.value = e.response?.data?.detail || 'No se pudo cargar los datos del pasante.'
  }
}, { immediate: true })

const avisoPasante = computed(() => {
  if (!requierePasante.value) return ''
  if (pasanteId.value) return ''
  return 'Para ver el reporte como encargado o admin, abre esta vista con ?pasante_id=ID (ej: /reporte-pdf?pasante_id=12).'
})

const puedeGenerarPdf = computed(() => {
  if (descargando.value) return false
  if (requierePasante.value) return !!usuarioReporte.value
  return true
})

// Computed
const infoSemana = computed(() => {
  if (!pdfFechaSemana.value) return ''
  const d      = new Date(pdfFechaSemana.value + 'T12:00:00')
  const diaSem = (d.getDay() + 6) % 7
  const lunes = new Date(d); lunes.setDate(d.getDate() - diaSem)
  const viernes = new Date(lunes); viernes.setDate(lunes.getDate() + 4)
  return `Semana del ${lunes.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })} al ${viernes.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })}`
})

const mesesNombres = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

const aniosDisponibles = computed(() => {
  const actual = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => actual - 2 + i)
})

// Función para badge de estado
const badgeEstado = (estado) => {
  const base = 'px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wide'
  switch (estado?.toUpperCase()) {
    case 'VERIFICADO':
    case 'APROBADO':
      return `${base} bg-green-100 text-green-800`
    case 'RECHAZADO':
      return `${base} bg-red-100 text-red-800`
    case 'PENDIENTE':
      return `${base} bg-yellow-100 text-yellow-800`
    default:
      return `${base} bg-gray-100 text-gray-800`
  }
}

// Función para obtener rango de fechas de lunes a viernes
const obtenerRangoFechasSemana = () => {
  if (!pdfFechaSemana.value) return ''
  
  const d = new Date(pdfFechaSemana.value + 'T12:00:00')
  const diaSem = (d.getDay() + 6) % 7
  const lunes = new Date(d); lunes.setDate(d.getDate() - diaSem)
  const martes = new Date(lunes); martes.setDate(lunes.getDate() + 1)
  const miercoles = new Date(lunes); miercoles.setDate(lunes.getDate() + 2)
  const jueves = new Date(lunes); jueves.setDate(lunes.getDate() + 3)
  const viernes = new Date(lunes); viernes.setDate(lunes.getDate() + 4)
  
  const formatFecha = (fecha) => {
    return fecha.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit' })
  }
  
  const diasSemana = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES']
  const fechas = [
    formatFecha(lunes),
    formatFecha(martes), 
    formatFecha(miercoles),
    formatFecha(jueves),
    formatFecha(viernes)
  ]
  
  let rangoTexto = ''
  diasSemana.forEach((dia, index) => {
    rangoTexto += `${dia} ${fechas[index]}`
    if (index < diasSemana.length - 1) {
      rangoTexto += ' | '
    }
  })
  
  return rangoTexto
}

// ── Cargar vista previa ──────────────────────────────────────────────────────
const cargarVistaPrevia = async () => {
  datosVistaPrevia.value      = []
  totalHorasVistaPrevia.value = 0
  contadorEstados.value       = {}
  errorVistaPrevia.value      = ''

  try {
    if (requierePasante.value && !pasanteId.value) return

    const params = {}
    if (tipoPdf.value === 'semanal') {
      const d      = new Date(pdfFechaSemana.value + 'T12:00:00')
      const diaSem = (d.getDay() + 6) % 7
      const lunes  = new Date(d); lunes.setDate(d.getDate() - diaSem)
      params.semana = isoSemana(lunes)
      params.anio = lunes.getFullYear()
    } else {
      params.mes = pdfMes.value
      params.anio = pdfAnio.value
    }

    if (requierePasante.value && pasanteId.value) {
      params.pasante_id = pasanteId.value
    }

    const { data: asistencias } = await api.get('/asistencias/mis-asistencias', { params })

    datosVistaPrevia.value = asistencias.map((asist) => ({
      fecha:            new Date(asist.fecha).toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' }),
      entrada:          asist.hora_entrada ? new Date(asist.hora_entrada).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' }) : '—',
      salida:           asist.hora_salida  ? new Date(asist.hora_salida).toLocaleTimeString('es-BO',  { hour: '2-digit', minute: '2-digit' }) : '—',
      horas:            asist.horas_trabajadas ? `${asist.horas_trabajadas}h` : '—',
      estado_encargado: asist.reporte?.estado_encargado ?? (asist.reporte ? 'PENDIENTE' : 'SIN REGISTRO'),
      estado_admin:     asist.reporte?.estado_admin     ?? (asist.reporte ? 'PENDIENTE' : 'SIN REGISTRO'),
      comentario:       asist.reporte?.actividades_realizadas || '',
    }))

    totalHorasVistaPrevia.value = Math.round(
      asistencias.reduce((acc, a) => acc + (parseFloat(a.horas_trabajadas) || 0), 0) * 10
    ) / 10

    contadorEstados.value = asistencias.reduce((cnt, a) => {
      const e = a.reporte?.estado_admin ?? (a.reporte ? 'PENDIENTE' : 'SIN REGISTRO')
      cnt[e]  = (cnt[e] || 0) + 1
      return cnt
    }, {})

  } catch (err) {
    console.error('Error cargando datos:', err)
    errorVistaPrevia.value = err.response?.data?.detail || 'Error al cargar asistencias.'
  }
}

// ── Generar PDF ─────────────────────────────────────────────────────────────
const generarPdfDesdeVistaPrevia = async () => {
  descargando.value = true
  errorDescarga.value = ''

  try {
    const u = usuarioReporte.value || authStore.user || {}

    // Cargar jsPDF desde el CDN
    const script = document.createElement('script')
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'
    document.head.appendChild(script)
    
    // Esperar a que el script cargue
    await new Promise((resolve) => {
      script.onload = resolve
    })

    // Usar window.jspdf.jsPDF
    const { jsPDF } = window.jspdf
    const doc = new jsPDF()

    // Configuración de página
    const pageWidth = doc.internal.pageSize.getWidth()
    const pageHeight = doc.internal.pageSize.getHeight()
    const margin = 15

    // === ENCABEZADO PROFESIONAL UMSA ===
    let yPosition = 25

    // Rectángulo de encabezado más pequeño
    doc.setFillColor(30, 58, 138) // Azul profesional oscuro
    doc.rect(margin, yPosition - 8, pageWidth - 2 * margin, 30, 'F')

    // Título principal más pequeño
    doc.setTextColor(255, 255, 255)
    doc.setFontSize(16)
    doc.setFont(undefined, 'bold')
    doc.text(`REPORTE ${tipoPdf.value === 'semanal' ? 'SEMANAL' : 'MENSUAL'}`, pageWidth / 2, yPosition + 2, { align: 'center' })

    // Subtítulo con período
    doc.setFontSize(10)
    doc.setFont(undefined, 'normal')
    const periodo = tipoPdf.value === 'semanal' ? obtenerRangoFechasSemana() : `${mesesNombres[pdfMes.value - 1]} ${pdfAnio.value}`
    doc.text(`Período: ${periodo}`, pageWidth / 2, yPosition + 10, { align: 'center' })

    // Fecha de generación más pequeña
    doc.setFontSize(7)
    doc.setFont(undefined, 'italic')
    doc.text(`Generado: ${new Date().toLocaleDateString('es-BO')} ${new Date().toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' })}`, pageWidth / 2, yPosition + 17, { align: 'center' })

    // Reset color para resto del documento
    doc.setTextColor(0, 0, 0)

    // === INFORMACIÓN DEL USUARIO - DISEÑO UMSA ===
    yPosition += 35

    // Caja de información más grande y profesional
    doc.setFillColor(240, 248, 255) // Azul muy claro
    doc.rect(margin, yPosition - 6, pageWidth - 2 * margin, 35, 'F')
    doc.setDrawColor(30, 58, 138) // Borde azul profesional UMSA
    doc.rect(margin, yPosition - 6, pageWidth - 2 * margin, 35)

    // Título con diseño UMSA
    doc.setTextColor(30, 58, 138) // Azul profesional UMSA
    doc.setFontSize(12)
    doc.setFont(undefined, 'bold')
    doc.text('DATOS DEL USUARIO - FACULTAD DE CIENCIAS SOCIALES - UMSA', margin + 8, yPosition + 3)

    // Línea separadora
    doc.setDrawColor(30, 58, 138)
    doc.setLineWidth(0.5)
    doc.line(margin + 8, yPosition + 8, pageWidth - margin - 8, yPosition + 8)

    // Datos del usuario más grandes y profesionales
    doc.setTextColor(55, 65, 81) // Gris oscuro
    doc.setFontSize(9)
    doc.setFont(undefined, 'normal')

    const pasanteData = [
      `Nombre Completo: ${authStore.user?.nombres || ''} ${authStore.user?.apellidos || ''}`,
      `C.I.: ${authStore.user?.carnet_identidad || '—'}`,
      `R.U.: ${authStore.user?.ru || '—'}`,
      `Unidad Asignada: ${authStore.user?.unidad_asignada || '—'}`,
      `Carrera: ${authStore.user?.carrera_nombre || authStore.user?.carrera?.nombre || '—'}`,
      `Usuario Sistema: ${authStore.user?.username || '—'}`
    ]

    // Usar datos del pasante cuando el rol es admin/encargado
    pasanteData[0] = `Nombre Completo: ${u?.nombres || ''} ${u?.apellidos || ''}`
    pasanteData[1] = `C.I.: ${u?.carnet_identidad || 'â€”'}`
    pasanteData[2] = `R.U.: ${u?.ru || 'â€”'}`
    pasanteData[3] = `Unidad Asignada: ${u?.unidad_asignada || 'â€”'}`
    pasanteData[4] = `Carrera: ${u?.carrera_nombre || u?.carrera?.nombre || 'â€”'}`
    pasanteData[5] = `Usuario Sistema: ${u?.username || 'â€”'}`

    // Distribución más espaciada y profesional
    doc.text(pasanteData[0], margin + 10, yPosition + 15)
    doc.text(pasanteData[1], margin + 95, yPosition + 15)
    doc.text(pasanteData[2], margin + 10, yPosition + 21)
    doc.text(pasanteData[3], margin + 95, yPosition + 21)
    doc.text(pasanteData[4], margin + 10, yPosition + 27)
    doc.text(pasanteData[5], margin + 95, yPosition + 27)

    // === TABLA DE ASISTENCIAS COMPACTA ===
    yPosition += 40

    // Título de la tabla más pequeño
    doc.setTextColor(30, 58, 138) // Azul profesional
    doc.setFontSize(12)
    doc.setFont(undefined, 'bold')
    doc.text('REGISTRO DE ASISTENCIAS', margin, yPosition)

    yPosition += 8

    // Encabezados de tabla compactos
    const headers = ['Fecha', 'Entrada', 'Salida', 'Horas', 'Est. Encargado', 'Est. Admin', 'Actividades']
    const colWidths = [22, 20, 20, 15, 28, 25, 55]
    const tableStartX = margin

    // Encabezado de tabla
    doc.setFillColor(30, 58, 138) // Azul profesional
    doc.rect(tableStartX, yPosition - 3, pageWidth - 2 * margin, 6, 'F')

    doc.setTextColor(255, 255, 255)
    doc.setFontSize(7)
    doc.setFont(undefined, 'bold')
    headers.forEach((header, index) => {
      const xPos = tableStartX + colWidths.slice(0, index).reduce((a, b) => a + b, 0)
      doc.text(header, xPos + 2, yPosition + 1)
    })

    yPosition += 5

    // Filas de datos (máximo 10 para que quepa en una página)
    const maxRows = 10
    const rowsToShow = datosVistaPrevia.value.slice(0, maxRows)

    rowsToShow.forEach((row, index) => {
      // Fondo alternativo
      if (index % 2 === 0) {
        doc.setFillColor(248, 250, 252) // Azul muy claro
        doc.rect(tableStartX, yPosition - 2, pageWidth - 2 * margin, 5, 'F')
      }

      // Datos de la fila
      const rowData = [
        row.fecha,
        row.entrada,
        row.salida,
        row.horas,
        row.estado_encargado || '—',
        row.estado_admin || '—',
        (row.comentario || '').substring(0, 30) + ((row.comentario || '').length > 30 ? '...' : '')
      ]

      // Colorear estados
      let xPos = tableStartX
      rowData.forEach((data, colIndex) => {
        if (colIndex === 4) { // Estado Encargado
          const estado = String(data || '').toUpperCase()
          if (estado === 'VERIFICADO') {
            doc.setTextColor(34, 197, 94) // Verde
          } else if (estado === 'RECHAZADO') {
            doc.setTextColor(239, 68, 68) // Rojo
          } else if (estado === 'PENDIENTE') {
            doc.setTextColor(245, 158, 11) // Amarillo
          } else {
            doc.setTextColor(107, 114, 128) // Gris
          }
        } else if (colIndex === 5) { // Estado Admin
          const estado = String(data || '').toUpperCase()
          if (estado === 'APROBADO') {
            doc.setTextColor(34, 197, 94) // Verde
          } else if (estado === 'RECHAZADO') {
            doc.setTextColor(239, 68, 68) // Rojo
          } else if (estado === 'PENDIENTE') {
            doc.setTextColor(245, 158, 11) // Amarillo
          } else {
            doc.setTextColor(107, 114, 128) // Gris
          }
        } else {
          doc.setTextColor(55, 65, 81) // Color normal
        }
        
        doc.text(data || '—', xPos, yPosition + 3)
        xPos += colWidths[colIndex]
      })

      yPosition += 5
    })

    // === RESUMEN MUY COMPACTO ===
    yPosition += 8

    // Caja de resumen muy compacta
    doc.setFillColor(30, 58, 138) // Azul profesional
    doc.rect(margin, yPosition - 3, pageWidth - 2 * margin, 6, 'F')

    doc.setTextColor(255, 255, 255)
    doc.setFontSize(10)
    doc.setFont(undefined, 'bold')
    doc.text('RESUMEN DEL PERÍODO', pageWidth / 2, yPosition + 1, { align: 'center' })

    yPosition += 10

    // Tarjetas de resumen ultra compactas
    const resumenData = [
      { label: 'Total Días', value: datosVistaPrevia.value.length, color: [30, 58, 138] },
      { label: 'Total Horas', value: `${totalHorasVistaPrevia.value}h`, color: [30, 58, 138] },
      { label: 'Aprobados', value: contadorEstados.value['APROBADO'] || 0, color: [34, 197, 94] },
      { label: 'Pendientes', value: contadorEstados.value['PENDIENTE'] || 0, color: [245, 158, 11] }
    ]

    const cardWidth = (pageWidth - 2 * margin - 8) / 4
    resumenData.forEach((item, index) => {
      const cardX = margin + (cardWidth + 8) * index

      // Fondo de tarjeta
      doc.setFillColor(...item.color)
      doc.rect(cardX, yPosition - 6, cardWidth, 14, 'F')

      // Borde de tarjeta
      doc.setDrawColor(30, 58, 138) // Azul profesional
      doc.rect(cardX, yPosition - 6, cardWidth, 14)

      // Texto de tarjeta
      doc.setTextColor(255, 255, 255)
      doc.setFontSize(6)
      doc.setFont(undefined, 'normal')
      doc.text(item.label, cardX + cardWidth / 2, yPosition - 2, { align: 'center' })

      doc.setFontSize(9)
      doc.setFont(undefined, 'bold')
      doc.text(String(item.value), cardX + cardWidth / 2, yPosition + 4, { align: 'center' })
    })

    // === FIRMAS COMPACTAS ===
    yPosition += 25

    // Título de firmas compacto
    doc.setFillColor(30, 58, 138) // Azul profesional
    doc.rect(margin, yPosition - 3, pageWidth - 2 * margin, 6, 'F')

    doc.setTextColor(255, 255, 255)
    doc.setFontSize(10)
    doc.setFont(undefined, 'bold')
    doc.text('FIRMAS DE VALIDACIÓN', pageWidth / 2, yPosition + 1, { align: 'center' })

    yPosition += 10

    // Línea horizontal
    doc.setDrawColor(30, 58, 138)
    doc.setLineWidth(0.8)
    doc.line(margin + 5, yPosition, pageWidth - margin - 5, yPosition)
    yPosition += 10

    // Configuración de firmas compactas (2x2)
    const firmaWidth = (pageWidth - 2 * margin - 20) / 2
    const firmaPositions = [
      { x: margin + 5, label: 'Firma del Usuario', name: `${authStore.user?.nombres || ''} ${authStore.user?.apellidos || ''}` },
      { x: margin + 5 + firmaWidth + 10, label: 'Firma del Encargado', name: '________________________' },
      { x: margin + 5, label: 'Firma del Administrador', name: '________________________' },
      { x: margin + 5 + firmaWidth + 10, label: 'Sello Institucional', name: '________________________' }
    ]

    firmaPositions[0].name = `${u?.nombres || ''} ${u?.apellidos || ''}`

    firmaPositions.forEach((firma, index) => {
      const yPos = yPosition + (index < 2 ? 0 : 25)

      // Línea de firma más corta
      doc.setDrawColor(107, 114, 128)
      doc.setLineWidth(0.5)
      doc.line(firma.x, yPos, firma.x + firmaWidth - 10, yPos)

      // Etiqueta
      doc.setTextColor(55, 65, 81)
      doc.setFontSize(7)
      doc.setFont(undefined, 'normal')
      doc.text(firma.label, firma.x, yPos - 3)

      // Nombre
      doc.setFontSize(8)
      doc.text(firma.name, firma.x, yPos + 5)
    })

    // === PIE DE PÁGINA COMPACTO ===
    yPosition = pageHeight - 15
    doc.setDrawColor(203, 213, 225)
    doc.line(margin, yPosition, pageWidth - margin, yPosition)

    doc.setTextColor(107, 114, 128)
    doc.setFontSize(6)
    doc.setFont(undefined, 'italic')
    doc.text('Sistema de Asistencias - Reporte generado automáticamente', pageWidth / 2, yPosition + 8, { align: 'center' })

    // Descargar el PDF
    const nombrePasante = `${u?.nombres || ''}_${u?.apellidos || ''}`.trim().replace(/\s+/g, '_') || `pasante_${u?.id || ''}`
    const filename = `reporte_${tipoPdf.value}_${nombrePasante}_${new Date().toISOString().split('T')[0]}.pdf`
    doc.save(filename)

  } catch (error) {
    console.error('Error generando PDF:', error)
    errorDescarga.value = 'Error al generar el PDF. Intenta nuevamente.'
  } finally {
    descargando.value = false
  }
}

// ── Utilidades ───────────────────────────────────────────────────────────────
const isoSemana = (date) => {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
  const dayNum = d.getUTCDay() || 7
  d.setUTCDate(d.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1))
  return Math.ceil((((d - yearStart) / 86400000) + 1)/7)
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/login')
}
</script>
