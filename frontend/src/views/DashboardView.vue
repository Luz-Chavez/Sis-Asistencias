<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">

    <!-- NAVBAR INSTITUCIONAL -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">

          <!-- Logo Institucional -->
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-gradient-to-br from-emerald-900 to-emerald-800 rounded-lg flex items-center justify-center shadow-md">
              <span class="text-white font-bold text-xs">UMSA</span>
            </div>
            <div class="hidden md:block border-l border-slate-300 pl-4">
              <p class="text-xs text-slate-500 font-medium uppercase tracking-wider">Facultad de Ciencias Sociales</p>
              <p class="text-sm font-bold text-slate-800">Sistema de Pasantías</p>
            </div>
          </div>

          <!-- Usuario y Acciones -->
          <div class="flex items-center gap-4">
            <div class="hidden sm:flex items-center gap-3 px-3 py-1.5 bg-slate-50 rounded-lg">
              <div class="w-8 h-8 bg-emerald-900 rounded-full flex items-center justify-center text-white font-semibold text-xs">
                {{ iniciales }}
              </div>
              <div class="text-right">
                <p class="text-xs font-semibold text-slate-700">{{ authStore.user?.nombres }} {{ authStore.user?.apellidos }}</p>
                <p class="text-xs text-slate-400 font-mono">{{ authStore.user?.username }}</p>
              </div>
            </div>
            <button @click="cerrarSesion"
              class="flex items-center gap-2 text-sm text-slate-600 hover:text-red-600 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
              <span class="hidden sm:inline">Salir</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

      <!-- Banner de bienvenida -->
      <div class="bg-gradient-to-r from-emerald-900 via-emerald-800 to-emerald-900 rounded-2xl p-8 text-white shadow-lg">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div>
            <p class="text-emerald-200 text-sm font-medium uppercase tracking-wider mb-1">Bienvenido(a)</p>
            <h1 class="text-3xl font-bold mb-2">{{ authStore.user?.nombres }} {{ authStore.user?.apellidos }}</h1>
            <p class="text-emerald-100 text-sm">Panel de Control — Pasante</p>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm">
              <p class="text-3xl font-bold">{{ stats.totalDias }}</p>
              <p class="text-xs text-emerald-200 uppercase tracking-wider">Días</p>
            </div>
            <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm">
              <p class="text-3xl font-bold">{{ stats.totalHoras }}h</p>
              <p class="text-xs text-emerald-200 uppercase tracking-wider">Horas</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Métricas -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">

        <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
          <div class="flex items-start justify-between">
            <div class="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
            </div>
            <span class="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">DÍAS</span>
          </div>
          <div class="mt-4">
            <p class="text-3xl font-bold text-slate-800">{{ stats.totalDias }}</p>
            <p class="text-sm text-slate-500 mt-1">Días registrados</p>
          </div>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-300">
          <div class="flex items-start justify-between">
            <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span class="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-full">TOTAL</span>
          </div>
          <div class="mt-4">
            <p class="text-3xl font-bold text-slate-800">{{ stats.totalHoras }}h</p>
            <p class="text-sm text-slate-500 mt-1">Horas acumuladas</p>
          </div>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-amber-200 transition-all duration-300">
          <div class="flex items-start justify-between">
            <div class="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <span class="text-xs font-medium text-amber-600 bg-amber-50 px-2 py-1 rounded-full">PENDIENTE</span>
          </div>
          <div class="mt-4">
            <p class="text-3xl font-bold text-slate-800">{{ stats.reportesPendientes }}</p>
            <p class="text-sm text-slate-500 mt-1">Reportes pendientes</p>
          </div>
        </div>

        <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
          <div class="flex items-start justify-between">
            <div class="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span class="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">{{ stats.pctAprobados }}%</span>
          </div>
          <div class="mt-4">
            <p class="text-3xl font-bold text-slate-800">{{ stats.reportesAprobados }}</p>
            <p class="text-sm text-slate-500 mt-1">Reportes aprobados</p>
          </div>
          <div class="mt-3 h-1.5 bg-slate-100 rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 rounded-full transition-all duration-500"
              :style="{ width: stats.pctAprobados + '%' }"></div>
          </div>
        </div>

      </div>

<!-- Panel de descarga PDF -->
<div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden w-full h-full">
  <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
    <h2 class="text-lg font-semibold text-slate-800">Descargar Reporte PDF</h2>
    <p class="text-sm text-slate-500"></p>
  </div>
  <div class="p-6 flex flex-col h-full">
    <div class="flex flex-wrap items-end gap-3 flex-1">

      <!-- Tipo -->
      <div class="flex-1 min-w-[200px]">
        <label class="block text-xs font-bold text-slate-500 uppercase mb-1.5">Tipo</label>
        <div class="flex rounded-lg overflow-hidden border border-slate-200">
          <button @click="tipoPdf = 'semanal'"
            :class="tipoPdf === 'semanal' ? 'bg-emerald-900 text-white' : 'bg-white text-slate-500 hover:bg-slate-50'"
            class="px-4 py-2 text-sm font-medium transition-all duration-200 w-full">
            Semanal
          </button>
          <button @click="tipoPdf = 'mensual'"
            :class="tipoPdf === 'mensual' ? 'bg-emerald-900 text-white' : 'bg-white text-slate-500 hover:bg-slate-50'"
            class="px-4 py-2 text-sm font-medium transition-all duration-200 w-full">
            Mensual
          </button>
        </div>
      </div>

      <!-- Semanal -->
      <div v-if="tipoPdf === 'semanal'" class="flex-1 min-w-[200px]">
        <label class="block text-xs font-bold text-slate-500 uppercase mb-1.5">
          Cualquier día de la semana
        </label>
        <input
          type="date"
          v-model="pdfFechaSemana"
          :min="`${anioMin}-01-01`"
          :max="`${anioMax}-12-31`"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none
                 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
        />
        <p v-if="infoSemana" class="mt-1.5 text-xs text-emerald-700 font-medium">
          {{ infoSemana }}
        </p>
      </div>

      <!-- Mensual -->
      <div v-if="tipoPdf === 'mensual'" class="flex gap-2 items-end flex-1 min-w-[200px]">
        <div class="flex-1">
          <label class="block text-xs font-bold text-slate-500 uppercase mb-1.5">Mes</label>
          <select v-model="pdfMes"
            class="border border-slate-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none
                   focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all">
            <option v-for="(nombre, idx) in mesesNombres" :key="idx+1" :value="idx+1">
              {{ nombre }}
            </option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-xs font-bold text-slate-500 uppercase mb-1.5">Año</label>
          <select v-model="pdfAnio"
            class="border border-slate-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none
                   focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all">
            <option v-for="y in aniosDisponibles" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>
      </div>

      <!-- Botón descargar -->
      <button @click="descargarPdf" :disabled="descargando"
        class="inline-flex items-center justify-center gap-2 bg-emerald-900 hover:bg-emerald-800 text-white px-5 py-2 rounded-lg
               text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm flex-1">
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

    <p v-if="errorDescarga" class="mt-3 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-lg">
      {{ errorDescarga }}
    </p>
  </div>
</div>


      <!-- Historial de Asistencias -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-semibold text-slate-800">Historial de Asistencias</h2>
            <p class="text-sm text-slate-500">Registro de entradas, salidas y reportes</p>
          </div>
          <button @click="cargarHistorial" title="Actualizar"
            class="p-2 text-slate-400 hover:text-emerald-700 hover:bg-emerald-50 rounded-lg transition-all">
            <svg class="w-5 h-5" :class="isLoading ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </button>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="py-16 text-center text-slate-400">
          <svg class="animate-spin w-8 h-8 mx-auto mb-3 text-emerald-400" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          <p class="text-sm">Cargando historial...</p>
        </div>

        <!-- Vacío -->
        <div v-else-if="historial.length === 0" class="py-16 text-center">
          <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-slate-700 mb-1">No tienes asistencias registradas</h3>
          <p class="text-slate-500 text-sm">Ficha tu entrada en la pantalla principal.</p>
        </div>

        <!-- Tabla -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full">
            <thead class="bg-slate-50 border-b border-slate-200">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Fecha</th>
                <th class="px-6 py-3 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Entrada</th>
                <th class="px-6 py-3 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Salida</th>
                <th class="px-6 py-3 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Horas</th>
                <th class="px-6 py-3 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Reporte</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="item in historial" :key="item.id"
                class="hover:bg-slate-50 transition-colors duration-150">

                <td class="px-6 py-4">
                  <p class="text-sm font-semibold text-slate-800">{{ formatFecha(item.fecha) }}</p>
                  <p class="text-xs text-slate-400 capitalize">{{ diaSemana(item.fecha) }}</p>
                </td>

                <td class="px-6 py-4 text-center">
                  <span class="text-sm font-mono text-slate-700">{{ formatHora(item.hora_entrada) }}</span>
                </td>

                <td class="px-6 py-4 text-center">
                  <span v-if="item.hora_salida" class="text-sm font-mono text-slate-700">
                    {{ formatHora(item.hora_salida) }}
                  </span>
                  <span v-else class="inline-flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full font-medium border border-amber-200">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
                    En curso
                  </span>
                </td>

                <td class="px-6 py-4 text-center">
                  <span v-if="item.horas_trabajadas" class="text-sm font-bold"
                    :class="item.horas_trabajadas >= 4 ? 'text-emerald-600' : 'text-orange-500'">
                    {{ item.horas_trabajadas }}h
                  </span>
                  <span v-else class="text-slate-300 text-sm">—</span>
                </td>

                <td class="px-6 py-4 text-center">
                  <span v-if="!item.hora_salida" class="text-slate-300 text-sm">—</span>

                  <button v-else-if="!item.reporte" @click="abrirModalReporte(item)"
                    class="inline-flex items-center gap-1 text-xs bg-emerald-50 text-emerald-700 px-3 py-1.5
                           rounded-full hover:bg-emerald-100 transition-colors font-medium border border-emerald-200">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                    </svg>
                    Agregar reporte
                  </button>

                  <div v-else class="flex flex-col items-center gap-1.5">
                    <span :class="{
                      'bg-emerald-50 text-emerald-700 border-emerald-200': item.reporte.estado === 'APROBADO',
                      'bg-red-50 text-red-600 border-red-200':             item.reporte.estado === 'RECHAZADO',
                      'bg-amber-50 text-amber-700 border-amber-200':       item.reporte.estado === 'PENDIENTE',
                    }" class="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full border">
                      <span :class="{
                        'bg-emerald-500': item.reporte.estado === 'APROBADO',
                        'bg-red-500':     item.reporte.estado === 'RECHAZADO',
                        'bg-amber-500':   item.reporte.estado === 'PENDIENTE',
                      }" class="w-1.5 h-1.5 rounded-full"></span>
                      {{ item.reporte.estado }}
                    </span>
                    <p v-if="item.reporte.comentarios_director"
                      class="text-xs text-slate-400 max-w-xs truncate italic"
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

    <!-- MODAL: Agregar reporte -->
    <transition name="modal">
      <div v-if="showModalReporte"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">

          <div class="bg-gradient-to-r from-emerald-900 to-emerald-800 px-6 py-5 flex justify-between items-start">
            <div>
              <p class="text-emerald-200 text-xs font-medium uppercase tracking-wider">Reporte del día</p>
              <h3 class="text-xl font-bold text-white mt-1">{{ formatFecha(asistenciaSeleccionada?.fecha) }}</h3>
            </div>
            <button @click="showModalReporte = false" class="text-emerald-200 hover:text-white transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <div class="p-6">
            <label class="block text-sm font-medium text-slate-700 mb-2">
              ¿Qué actividades realizaste ese día?
            </label>
            <textarea v-model="actividadesModal" rows="5"
              placeholder="Describe las tareas que realizaste..."
              class="w-full border border-slate-300 rounded-lg p-3 text-sm resize-none
                     focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"></textarea>
            <p v-if="errorModal" class="mt-2 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-lg">
              {{ errorModal }}
            </p>
          </div>

          <div class="px-6 pb-6 flex gap-3">
            <button @click="showModalReporte = false"
              class="flex-1 py-2.5 border border-slate-300 text-slate-600 rounded-lg text-sm font-medium
                     hover:bg-slate-50 transition-colors">
              Cancelar
            </button>
            <button @click="guardarReporteModal" :disabled="isSubmittingModal || !actividadesModal.trim()"
              class="flex-1 py-2.5 bg-emerald-900 text-white rounded-lg text-sm font-medium hover:bg-emerald-800
                     transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm">
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
const tipoPdf        = ref('semanal')
const pdfAnio        = ref(new Date().getFullYear())
const pdfMes         = ref(new Date().getMonth() + 1)
const descargando    = ref(false)
const errorDescarga  = ref('')

// Semanal: el pasante elige cualquier día de esa semana
const pdfFechaSemana = ref(new Date().toISOString().split('T')[0])
const anioMin        = new Date().getFullYear()
const anioMax        = 2028

const mesesNombres = [
  'Enero','Febrero','Marzo','Abril','Mayo','Junio',
  'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'
]

const aniosDisponibles = computed(() => {
  const inicio = new Date().getFullYear()
  const anos = []
  for (let y = inicio; y <= 2028; y++) anos.push(y)
  return anos
})

// Muestra el rango lunes-domingo de la fecha elegida
const infoSemana = computed(() => {
  if (!pdfFechaSemana.value) return ''
  const d = new Date(pdfFechaSemana.value + 'T12:00:00')
  const diaSem = (d.getDay() + 6) % 7
  const lunes  = new Date(d); lunes.setDate(d.getDate() - diaSem)
  const domingo = new Date(lunes); domingo.setDate(lunes.getDate() + 6)
  const fmt = (dt) => dt.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })
  const sem = isoSemana(d)
  return `Semana ${sem}  ·  ${fmt(lunes)} – ${fmt(domingo)}`
})

function isoSemana(d) {
  const tmp = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()))
  tmp.setUTCDate(tmp.getUTCDate() + 4 - (tmp.getUTCDay() || 7))
  const inicio = new Date(Date.UTC(tmp.getUTCFullYear(), 0, 1))
  return Math.ceil((((tmp - inicio) / 86400000) + 1) / 7)
}

// ── Iniciales ──────────────────────────────────────────────────────────────────
const iniciales = computed(() => {
  const n = authStore.user?.nombres?.[0] ?? ''
  const a = authStore.user?.apellidos?.[0] ?? ''
  return (n + a).toUpperCase()
})

// ── Estadísticas ───────────────────────────────────────────────────────────────
const stats = computed(() => {
  const aprobados = historial.value.filter(i => i.reporte?.estado === 'APROBADO').length
  const total     = historial.value.filter(i => i.reporte).length
  return {
    totalDias:          historial.value.length,
    totalHoras:         Math.round(historial.value.reduce((a, i) => a + (parseFloat(i.horas_trabajadas) || 0), 0) * 10) / 10,
    reportesPendientes: historial.value.filter(i => i.reporte?.estado === 'PENDIENTE').length,
    reportesAprobados:  aprobados,
    pctAprobados:       total > 0 ? Math.round((aprobados / total) * 100) : 0,
  }
})

// ── Formatos ───────────────────────────────────────────────────────────────────
const formatFecha = (f) => {
  if (!f) return '—'
  return new Date(f).toLocaleDateString('es-BO', { day: '2-digit', month: 'short', year: 'numeric' })
}
const diaSemana = (f) => {
  if (!f) return ''
  return new Date(f).toLocaleDateString('es-BO', { weekday: 'long' })
}
const formatHora = (dt) => {
  if (!dt) return '—'
  return new Date(dt).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' })
}

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
  descargando.value   = true
  errorDescarga.value = ''
  try {
    // Para semanal: calcular semana ISO desde la fecha elegida
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
    const a    = document.createElement('a')
    a.href     = href
    const cd    = response.headers['content-disposition'] || ''
    const match = cd.match(/filename="?([^"]+)"?/)
    a.download  = match ? match[1] : `reporte_${tipoPdf.value}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(href)
  } catch (e) {
    errorDescarga.value = e.response?.data?.detail
      ?? 'No hay registros para el período seleccionado.'
  } finally {
    descargando.value = false
  }
}

// ── Modal reporte ──────────────────────────────────────────────────────────────
const abrirModalReporte = (asistencia) => {
  asistenciaSeleccionada.value = asistencia
  actividadesModal.value       = asistencia.reporte?.actividades_realizadas || ''
  errorModal.value             = ''
  showModalReporte.value       = true
}

const guardarReporteModal = async () => {
  if (!actividadesModal.value.trim()) return
  isSubmittingModal.value = true
  errorModal.value        = ''
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