<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Pasantes</h1>
        <p class="text-slate-500 mt-1">Carrera ID: {{ authStore.user?.carrera_id ?? '—' }}</p>
      </div>

      <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
        <input v-model="filterText" type="text" placeholder="Buscar: nombre, username, CI, email"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
        <select v-model="filterState" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="all">Todos</option>
          <option value="active">Activos</option>
          <option value="inactive">Inactivos</option>
        </select>
        <button type="button" @click="abrirModalCrear"
          class="inline-flex items-center justify-center gap-2 bg-blue-900 text-white px-5 py-2.5 rounded-lg hover:bg-blue-800 transition-colors font-medium shadow-sm">
          Nuevo Pasante
        </button>
      </div>
    </div>

    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Pasante</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Email</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">CI</th>
              <th class="px-6 py-3 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-if="isLoadingUsuarios">
              <td colspan="5" class="px-6 py-10 text-center text-slate-500">Cargando...</td>
            </tr>
            <tr v-else-if="usuariosFiltrados.length === 0">
              <td colspan="5" class="px-6 py-10 text-center text-slate-500">Sin pasantes.</td>
            </tr>
            <tr v-else v-for="u in usuariosFiltrados" :key="u.id" class="hover:bg-slate-50/50">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 bg-blue-900 rounded-full flex items-center justify-center text-white text-xs font-bold">
                    {{ getIniciales(u.nombres, u.apellidos) }}
                  </div>
                  <div class="min-w-0">
                    <p class="text-sm font-semibold text-slate-800 truncate">{{ u.nombres }} {{ u.apellidos }}</p>
                    <p class="text-xs text-slate-400 font-mono">@{{ u.username }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-slate-600">{{ u.email }}</td>
              <td class="px-6 py-4 text-sm text-slate-600">{{ u.carnet_identidad }}</td>
              <td class="px-6 py-4 text-center">
                <span :class="u.estado ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-100 text-slate-600 border-slate-200'"
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border">
                  {{ u.estado ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button class="text-sm text-blue-700 hover:underline" @click="abrirModalVer(u)">Ver</button>
                <span class="mx-2 text-slate-300">|</span>
                <button class="text-sm text-slate-700 hover:underline" @click="abrirModalEditar(u)">Editar</button>
                <span class="mx-2 text-slate-300">|</span>
                <button class="text-sm" :class="u.estado ? 'text-red-600' : 'text-emerald-700'" @click="confirmarCambioEstado(u)">
                  {{ u.estado ? 'Baja' : 'Reactivar' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Ver -->
    <div v-if="showModalVer" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-5 text-white flex items-start justify-between">
          <div>
            <p class="text-blue-100 text-xs font-medium uppercase tracking-wider">Pasante</p>
            <h3 class="text-xl font-bold mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</h3>
          </div>
          <button type="button" @click="showModalVer = false" class="text-blue-100 hover:text-white">✕</button>
        </div>

        <div class="p-6" v-if="pasanteSeleccionado">
          <div class="flex gap-2 mb-4">
            <button type="button" @click="tabVer = 'detalles'"
              :class="tabVer === 'detalles' ? 'bg-slate-100 text-slate-800' : 'bg-transparent text-slate-600'"
              class="px-3 py-1.5 rounded-lg text-xs font-semibold border border-slate-200">Detalles</button>
            <button type="button" @click="tabVer = 'historial'"
              :class="tabVer === 'historial' ? 'bg-slate-100 text-slate-800' : 'bg-transparent text-slate-600'"
              class="px-3 py-1.5 rounded-lg text-xs font-semibold border border-slate-200">Historial</button>
          </div>

          <div v-if="tabVer === 'detalles'" class="space-y-4">
            <div :class="cumplioPasantia ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-slate-50 border-slate-200 text-slate-700'"
              class="p-3 rounded-lg border">
              <p class="text-sm font-semibold" v-if="cumplioPasantia">Pasantía completada</p>
              <p class="text-sm font-semibold" v-else>Progreso de pasantía</p>
              <p class="text-xs mt-0.5" v-if="errorHistorial">{{ errorHistorial }}</p>
              <p class="text-xs mt-0.5" v-else>Horas: {{ isLoadingHistorial ? '...' : totalHorasPasante }} / 240</p>
            </div>

            <div class="grid sm:grid-cols-2 gap-3">
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">Username</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.username }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">Email</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.email }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">CI</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.carnet_identidad }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">RU</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.ru ?? '—' }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg sm:col-span-2">
                <p class="text-xs text-slate-400">Unidad asignada</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.unidad_asignada ?? '—' }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">Carrera ID</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.carrera_id ?? '—' }}</p>
              </div>
            </div>
          </div>

          <div v-else class="space-y-3">
            <div class="flex flex-col sm:flex-row gap-2">
              <select v-model="filterHistorialYear" class="border border-slate-300 rounded-lg px-3 py-2 text-xs bg-white">
                <option value="all">Todos los años</option>
                <option v-for="y in historialYears" :key="y" :value="String(y)">{{ y }}</option>
              </select>
              <select v-model="filterHistorialMonth" class="border border-slate-300 rounded-lg px-3 py-2 text-xs bg-white">
                <option value="all">Todos los meses</option>
                <option v-for="m in monthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
              </select>
              <select v-model="historialVista" class="border border-slate-300 rounded-lg px-3 py-2 text-xs bg-white">
                <option value="detalle">Detalle</option>
                <option value="dia">Por día</option>
                <option value="semana">Por semana</option>
                <option value="mes">Por mes</option>
              </select>
              <button type="button" @click="refrescarHistorial" class="px-3 py-2 text-xs border border-slate-300 rounded-lg hover:bg-slate-50">Actualizar</button>
              <button type="button" @click="descargarCSVHistorial" class="px-3 py-2 text-xs border border-slate-300 rounded-lg hover:bg-slate-50">CSV</button>
              <span v-if="isLoadingHistorial" class="self-center text-xs text-slate-500">Cargando...</span>
            </div>

            <p v-if="errorHistorial" class="text-xs text-red-600 bg-red-50 border border-red-200 p-2 rounded">{{ errorHistorial }}</p>
            <p class="text-xs text-slate-500">Registros: {{ historialFiltrado.length }} · Horas: {{ totalHorasHistorial }}h</p>

            <p class="text-xs text-slate-500">Esta semana: {{ horasSemanaActual }}h · Este mes: {{ horasMesActual }}h</p>

            <div v-if="historialVista === 'detalle'">
              <div v-if="historialFiltrado.length" class="border border-slate-200 rounded-xl overflow-hidden">
                <div class="max-h-72 overflow-y-auto">
                  <div v-for="a in historialFiltrado" :key="a.id" class="p-3 border-b border-slate-100 last:border-b-0">
                    <div class="flex items-start justify-between gap-3">
                      <div class="min-w-0">
                        <p class="text-sm font-semibold text-slate-800">
                          {{ formatFecha(a.fecha) }} · {{ formatHora(a.hora_entrada) }} → {{ a.hora_salida ? formatHora(a.hora_salida) : '—' }}
                        </p>
                        <p class="text-xs text-slate-500 mt-0.5">
                          Horas: {{ a.horas_trabajadas ?? '—' }}h ·
                          <span v-if="a.reporte">Reporte: {{ a.reporte.estado }}</span>
                          <span v-else>Sin reporte</span>
                        </p>
                        <p v-if="a.reporte?.actividades_realizadas" class="text-xs text-slate-600 mt-2 line-clamp-2">{{ a.reporte.actividades_realizadas }}</p>
                      </div>
                      <div class="shrink-0 flex flex-col items-end gap-2">
                        <span v-if="a.reporte" :class="reporteBadge(a.reporte.estado)" class="text-[11px] font-semibold px-2 py-0.5 rounded-full border">
                          {{ a.reporte.estado }}
                        </span>
                        <button type="button" @click="descargarPDFDia(a)" class="px-3 py-1.5 text-xs border border-slate-300 rounded-lg hover:bg-slate-50">PDF</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <p v-else class="text-xs text-slate-500">Sin asistencias registradas.</p>
            </div>

            <div v-else>
              <div v-if="resumenHistorial.length" class="border border-slate-200 rounded-xl overflow-hidden">
                <div class="max-h-72 overflow-y-auto">
                  <div v-for="r in resumenHistorial" :key="r.key" class="p-3 border-b border-slate-100 last:border-b-0">
                    <div class="flex items-center justify-between gap-3">
                      <div class="min-w-0">
                        <p class="text-sm font-semibold text-slate-800">{{ r.label }}</p>
                        <p class="text-xs text-slate-500 mt-0.5">Registros: {{ r.registros }} · Horas: {{ r.horas }}h</p>
                      </div>
                      <div class="shrink-0 flex items-center gap-2">
                        <button type="button" @click="descargarPDFPeriodo(r)" class="px-3 py-1.5 text-xs border border-slate-300 rounded-lg hover:bg-slate-50">PDF</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <p v-else class="text-xs text-slate-500">Sin asistencias registradas.</p>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-end gap-3">
          <button type="button" @click="showModalVer = false" class="px-4 py-2 text-sm border rounded-lg hover:bg-slate-100">Cerrar</button>
        </div>
      </div>
    </div>

    <!-- Modal Crear -->
    <div v-if="showModalCrear" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-5 text-white flex items-start justify-between">
          <div>
            <p class="text-blue-100 text-xs font-medium uppercase tracking-wider">Registro</p>
            <h3 class="text-xl font-bold mt-1">Nuevo Pasante</h3>
          </div>
          <button type="button" @click="showModalCrear = false" class="text-blue-100 hover:text-white">✕</button>
        </div>

        <form @submit.prevent="registrarPasante" class="p-6 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Nombres</label>
              <input v-model="formulario.nombres" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Apellidos</label>
              <input v-model="formulario.apellidos" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">CI</label>
              <input v-model="formulario.carnet_identidad" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">RU</label>
              <input v-model="formulario.ru" class="w-full border border-slate-300 rounded-lg p-3 text-sm" placeholder="Registro Universitario (opcional)" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input v-model="formulario.email" type="email" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>

          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1">Celular</label>
            <input v-model="formulario.celular" type="tel" required
              class="w-full border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm"
              placeholder="Ej. 70123456" />
          </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1">Unidad asignada</label>
              <input v-model="formulario.unidad_asignada" class="w-full border border-slate-300 rounded-lg p-3 text-sm" placeholder="Ej. Biblioteca / Secretaría / Unidad X" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
              <input v-model="formulario.password" type="password" minlength="6" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
          </div>

          <div v-if="mensajeError" class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{{ mensajeError }}</div>

          <div class="pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button type="button" @click="showModalCrear = false" class="px-4 py-2 text-sm border rounded-lg">Cancelar</button>
            <button type="submit" :disabled="isSubmittingCrear" class="px-5 py-2 text-sm bg-blue-900 text-white rounded-lg disabled:opacity-50">
              {{ isSubmittingCrear ? 'Registrando...' : 'Registrar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar -->
    <div v-if="showModalEditar" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-5 text-white flex items-start justify-between">
          <div>
            <p class="text-blue-100 text-xs font-medium uppercase tracking-wider">Edición</p>
            <h3 class="text-xl font-bold mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</h3>
          </div>
          <button type="button" @click="showModalEditar = false" class="text-blue-100 hover:text-white">✕</button>
        </div>

        <form @submit.prevent="guardarEdicion" class="p-6 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Nombres</label>
              <input v-model="formEditar.nombres" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Apellidos</label>
              <input v-model="formEditar.apellidos" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">CI</label>
              <input v-model="formEditar.carnet_identidad" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">RU</label>
              <input v-model="formEditar.ru" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input v-model="formEditar.email" type="email" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Celular</label>
              <input v-model="formEditar.celular" type="tel" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1">Unidad asignada</label>
              <input v-model="formEditar.unidad_asignada" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
          </div>

          <div v-if="mensajeErrorEditar" class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{{ mensajeErrorEditar }}</div>

          <div class="pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button type="button" @click="showModalEditar = false" class="px-4 py-2 text-sm border rounded-lg">Cancelar</button>
            <button type="submit" :disabled="isSubmittingEditar" class="px-5 py-2 text-sm bg-blue-900 text-white rounded-lg disabled:opacity-50">
              {{ isSubmittingEditar ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirmar baja -->
    <div v-if="showModalBaja" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-lg p-6 max-w-sm w-full text-center">
        <h4 class="text-lg font-semibold mb-2">{{ pasanteSeleccionado?.estado ? 'Dar de baja?' : 'Reactivar?' }}</h4>
        <p class="mb-4">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</p>
        <button type="button" @click="showModalBaja = false" class="px-4 py-2 mr-2 border rounded">Cancelar</button>
        <button type="button" @click="ejecutarCambioEstado" class="px-4 py-2 bg-red-600 text-white rounded">Confirmar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'


type Usuario = {
  id: number
  nombres: string
  apellidos: string
  carnet_identidad: string
  ru?: string | null
  unidad_asignada?: string | null
  username: string
  email: string
  celular?: string | null
  rol_id: number
  carrera_id: number | null
  estado: boolean
  rol?: string | null
}

type Reporte = {
  id: number
  actividades_realizadas?: string | null
  estado: 'PENDIENTE' | 'APROBADO' | 'RECHAZADO' | string
  comentarios_director?: string | null
  creado_en?: string | null
}

type Asistencia = {
  id: number
  pasante_id: number
  fecha: string
  hora_entrada: string
  hora_salida?: string | null
  horas_trabajadas?: number | null
  reporte?: Reporte | null
}

const router = useRouter()
const authStore = useAuthStore()

const filterText = ref('')
const filterState = ref<'all' | 'active' | 'inactive'>('all')

const isLoadingUsuarios = ref(false)
const usuarios = ref<Usuario[]>([])

const showModalVer = ref(false)
const showModalCrear = ref(false)
const showModalEditar = ref(false)
const showModalBaja = ref(false)

const tabVer = ref<'detalles' | 'historial'>('detalles')
const pasanteSeleccionado = ref<Usuario | null>(null)

const isLoadingHistorial = ref(false)
const historial = ref<Asistencia[]>([])
const errorHistorial = ref<string>('')

const filterHistorialYear = ref<'all' | string>('all')
const filterHistorialMonth = ref<'all' | string>('all')
const historialVista = ref<'detalle' | 'dia' | 'semana' | 'mes'>('detalle')

const isSubmittingCrear = ref(false)
const mensajeError = ref('')

const isSubmittingEditar = ref(false)
const mensajeErrorEditar = ref('')

const formulario = ref({
  nombres: '',
  apellidos: '',
  carnet_identidad: '',
  ru: '',
  unidad_asignada: '',
  email: '',
  celular: '',
  password: '',
})

const formEditar = ref({
  nombres: '',
  apellidos: '',
  carnet_identidad: '',
  ru: '',
  unidad_asignada: '',
  email: '',
  celular: '',
})

const monthOptions = [
  { value: '01', label: 'Enero' },
  { value: '02', label: 'Febrero' },
  { value: '03', label: 'Marzo' },
  { value: '04', label: 'Abril' },
  { value: '05', label: 'Mayo' },
  { value: '06', label: 'Junio' },
  { value: '07', label: 'Julio' },
  { value: '08', label: 'Agosto' },
  { value: '09', label: 'Septiembre' },
  { value: '10', label: 'Octubre' },
  { value: '11', label: 'Noviembre' },
  { value: '12', label: 'Diciembre' },
] as const

function httpStatus(error: any): number | null {
  return error?.response?.status ?? null
}

function httpDetail(error: any): string {
  return error?.response?.data?.detail ?? error?.message ?? 'Error'
}

function requireLoginIf401(error: any) {
  if (httpStatus(error) === 401) {
    authStore.logout()
    router.push('/login')
    return true
  }
  return false
}

function getIniciales(nombres?: string, apellidos?: string) {
  const n = (nombres || '').trim()
  const a = (apellidos || '').trim()
  const ni = n ? n[0].toUpperCase() : 'X'
  const ai = a ? a[0].toUpperCase() : 'X'
  return `${ni}${ai}`
}

function toDate(value?: string | null): Date | null {
  if (!value) return null
  const d = new Date(value)
  return Number.isNaN(d.getTime()) ? null : d
}

function formatFecha(value: string) {
  const d = toDate(value)
  if (!d) return String(value)
  return d.toLocaleDateString('es-BO', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

function formatHora(value?: string | null) {
  const d = toDate(value ?? undefined)
  if (!d) return value ? String(value) : '—'
  return d.toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' })
}

function reporteBadge(estado?: string) {
  const e = (estado || '').toUpperCase()
  if (e === 'APROBADO') return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  if (e === 'RECHAZADO') return 'bg-red-50 text-red-700 border-red-200'
  return 'bg-amber-50 text-amber-700 border-amber-200'
}

const usuariosFiltrados = computed(() => {
  const text = filterText.value.trim().toLowerCase()
  return usuarios.value
    .filter(u => (u.rol === 'PASANTE' || u.rol_id === 3))
    .filter(u => {
      if (filterState.value === 'active') return !!u.estado
      if (filterState.value === 'inactive') return !u.estado
      return true
    })
    .filter(u => {
      if (!text) return true
      const haystack = `${u.nombres} ${u.apellidos} ${u.username} ${u.carnet_identidad} ${u.email}`.toLowerCase()
      return haystack.includes(text)
    })
})

const historialYears = computed(() => {
  const years = new Set<number>()
  for (const a of historial.value) {
    const d = toDate(a.fecha)
    if (d) years.add(d.getFullYear())
  }
  return Array.from(years).sort((a, b) => b - a)
})

const historialFiltrado = computed(() => {
  return historial.value.filter(a => {
    const d = toDate(a.fecha)
    if (!d) return true

    if (filterHistorialYear.value !== 'all') {
      const y = Number(filterHistorialYear.value)
      if (!Number.isNaN(y) && d.getFullYear() !== y) return false
    }

    if (filterHistorialMonth.value !== 'all') {
      const mm = String(d.getMonth() + 1).padStart(2, '0')
      if (mm !== filterHistorialMonth.value) return false
    }

    return true
  })
})

const totalHorasPasante = computed(() => {
  const total = historial.value.reduce((acc, a) => acc + (Number(a.horas_trabajadas) || 0), 0)
  return Math.round(total * 100) / 100
})

const totalHorasHistorial = computed(() => {
  const total = historialFiltrado.value.reduce((acc, a) => acc + (Number(a.horas_trabajadas) || 0), 0)
  return Math.round(total * 100) / 100
})


type ResumenHistorialRow = {
  key: string
  label: string
  fechaParam: string
  horas: number
  registros: number
}

function round2(value: number) {
  return Math.round(value * 100) / 100
}

function startOfWeekMonday(date: Date) {
  const d = new Date(date)
  d.setHours(0, 0, 0, 0)
  const day = (d.getDay() + 6) % 7 // lunes=0
  d.setDate(d.getDate() - day)
  return d
}

function formatShortDate(date: Date) {
  return date.toLocaleDateString('es-BO', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const horasSemanaActual = computed(() => {
  const now = new Date()
  const start = startOfWeekMonday(now)
  const end = new Date(start)
  end.setDate(end.getDate() + 7)

  const total = historial.value.reduce((acc, a) => {
    const d = toDate(a.fecha)
    if (!d) return acc
    if (d >= start && d < end) return acc + (Number(a.horas_trabajadas) || 0)
    return acc
  }, 0)

  return round2(total)
})

const horasMesActual = computed(() => {
  const now = new Date()
  const y = now.getFullYear()
  const m = now.getMonth()

  const total = historial.value.reduce((acc, a) => {
    const d = toDate(a.fecha)
    if (!d) return acc
    if (d.getFullYear() === y && d.getMonth() === m) return acc + (Number(a.horas_trabajadas) || 0)
    return acc
  }, 0)

  return round2(total)
})

const resumenHistorial = computed<ResumenHistorialRow[]>(() => {
  if (historialVista.value === 'detalle') return []

  const map = new Map<string, ResumenHistorialRow>()

  for (const a of historialFiltrado.value) {
    const d = toDate(a.fecha)
    if (!d) continue

    let key = ''
    let label = ''

    if (historialVista.value === 'dia') {
      const yyyy = String(d.getFullYear())
      const mm = String(d.getMonth() + 1).padStart(2, '0')
      const dd = String(d.getDate()).padStart(2, '0')
      key = `${yyyy}-${mm}-${dd}`
      label = formatShortDate(d)
    } else if (historialVista.value === 'mes') {
      const yyyy = String(d.getFullYear())
      const mm = String(d.getMonth() + 1).padStart(2, '0')
      key = `${yyyy}-${mm}`
      label = d.toLocaleDateString('es-BO', { year: 'numeric', month: 'long' })
    } else {
      const start = startOfWeekMonday(d)
      const end = new Date(start)
      end.setDate(end.getDate() + 6)
      const yyyy = String(start.getFullYear())
      const mm = String(start.getMonth() + 1).padStart(2, '0')
      const dd = String(start.getDate()).padStart(2, '0')
      key = `${yyyy}-${mm}-${dd}`
      label = `Semana del ${formatShortDate(start)} al ${formatShortDate(end)}`
    }

    const row = map.get(key) || { key, label, fechaParam: '', horas: 0, registros: 0 }
    row.horas += Number(a.horas_trabajadas) || 0
    row.registros += 1
    if (!row.fechaParam) {
      if (historialVista.value === 'mes') row.fechaParam = key + '-01'
      else row.fechaParam = key
    }
    map.set(key, row)
  }

  const rows = Array.from(map.values())
  rows.sort((a, b) => b.key.localeCompare(a.key))
  for (const r of rows) r.horas = round2(r.horas)
  return rows
})

function csvCell(value: any) {
  const s = value === null || value === undefined ? '' : String(value)
  const escaped = s.replace(/"/g, '""')
  return `"${escaped}"`
}

function descargarCSVHistorial() {
  const u = pasanteSeleccionado.value
  const base = u?.username || 'pasante'
  const fecha = new Date().toISOString().slice(0, 10)

  let csv = ''

  if (historialVista.value === 'detalle') {
    const header = ['fecha', 'hora_entrada', 'hora_salida', 'horas', 'reporte_estado', 'actividades']
    const rows = historialFiltrado.value.map(a => [
      formatFecha(a.fecha),
      formatHora(a.hora_entrada),
      a.hora_salida ? formatHora(a.hora_salida) : '',
      a.horas_trabajadas ?? '',
      a.reporte?.estado ?? '',
      a.reporte?.actividades_realizadas ?? '',
    ])
    csv = [header, ...rows].map(r => r.map(csvCell).join(',')).join('\n')
  } else {
    const header = ['periodo', 'registros', 'horas']
    const rows = resumenHistorial.value.map(r => [r.label, r.registros, r.horas])
    csv = [header, ...rows].map(r => r.map(csvCell).join(',')).join('\n')
  }

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `historial_${base}_${fecha}.csv`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

async function descargarPDF(tipo: 'dia' | 'semana' | 'mes', fechaParam: string) {
  if (!pasanteSeleccionado.value) return

  try {
    const res = await api.get('/asistencias/reporte-pdf', {
      params: {
        tipo,
        fecha: fechaParam,
        pasante_id: pasanteSeleccionado.value.id,
      },
      responseType: 'blob',
    })

    const blob = new Blob([res.data], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `reporte_${tipo}_${pasanteSeleccionado.value.username}_${fechaParam}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    const status = e.response?.status
    const data = e.response?.data
    let detail: string | null = null

    try {
      if (data instanceof Blob) {
        const text = await data.text()
        try {
          const parsed = JSON.parse(text)
          detail = parsed?.detail ? String(parsed.detail) : text
        } catch {
          detail = text
        }
      } else if (data?.detail) {
        detail = String(data.detail)
      }
    } catch {
      // ignore
    }

    alert(detail ? `${status ? status + ': ' : ''}${detail}` : `No se pudo descargar el PDF.${status ? ' (' + status + ')' : ''}`)
  }
}

function fechaISOFrom(value: any): string | null {
  if (value === null || value === undefined) return null
  const s = String(value)
  const m = s.match(/^(\d{4}-\d{2}-\d{2})/)
  return m ? m[1] : null
}

async function descargarPDFDia(a: Asistencia) {
  const iso = fechaISOFrom(a.fecha) || (toDate(a.fecha)?.toISOString().slice(0, 10) ?? null)
  if (!iso) {
    alert('No se pudo determinar la fecha del registro.')
    return
  }
  await descargarPDF('dia', iso)
}

async function descargarPDFPeriodo(row: ResumenHistorialRow) {
  const tipo = historialVista.value
  if (tipo === 'detalle') return
  await descargarPDF(tipo, row.fechaParam)
}

const cumplioPasantia = computed(() => totalHorasPasante.value >= 240)

async function cargarUsuarios() {
  isLoadingUsuarios.value = true
  try {
    const res = await api.get('/usuarios/listar')
    usuarios.value = Array.isArray(res.data) ? (res.data as Usuario[]) : []
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    console.error('Error cargando usuarios:', e)
  } finally {
    isLoadingUsuarios.value = false
  }
}

async function cargarHistorial(pasanteId: number) {
  isLoadingHistorial.value = true
  errorHistorial.value = ''
  try {
    const res = await api.get('/asistencias/mis-asistencias', { params: { pasante_id: pasanteId } })
    historial.value = Array.isArray(res.data) ? (res.data as Asistencia[]) : []
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    errorHistorial.value = httpDetail(e)
    historial.value = []
  } finally {
    isLoadingHistorial.value = false
  }
}

function refrescarHistorial() {
  if (!pasanteSeleccionado.value) return
  return cargarHistorial(pasanteSeleccionado.value.id)
}

function abrirModalVer(u: Usuario) {
  pasanteSeleccionado.value = u
  tabVer.value = 'detalles'
  filterHistorialYear.value = 'all'
  filterHistorialMonth.value = 'all'
  historialVista.value = 'detalle'
  historial.value = []
  errorHistorial.value = ''
  showModalVer.value = true
  cargarHistorial(u.id)
}

function abrirModalCrear() {
  mensajeError.value = ''
  formulario.value = { nombres: '', apellidos: '', carnet_identidad: '', ru: '', unidad_asignada: '', email: '', celular: '', password: '' }
  showModalCrear.value = true
}

function abrirModalEditar(u: Usuario) {
  mensajeErrorEditar.value = ''
  pasanteSeleccionado.value = u
  formEditar.value = {
    nombres: u.nombres ?? '',
    apellidos: u.apellidos ?? '',
    carnet_identidad: u.carnet_identidad ?? '',
    ru: u.ru ?? '',
    unidad_asignada: u.unidad_asignada ?? '',
    email: u.email ?? '',
    celular: (u.celular as any) ?? '',
  }
  showModalEditar.value = true
}

async function registrarPasante() {
  mensajeError.value = ''
  const carreraId = authStore.user?.carrera_id ?? null
  if (!carreraId) {
    mensajeError.value = 'Tu cuenta de encargado no tiene carrera asignada.'
    return
  }

  isSubmittingCrear.value = true
  try {
    await api.post('/usuarios/registro', {
      nombres: formulario.value.nombres,
      apellidos: formulario.value.apellidos,
      carnet_identidad: formulario.value.carnet_identidad,
      ru: (formulario.value.ru || '').trim() || null,
      unidad_asignada: (formulario.value.unidad_asignada || '').trim() || null,
      email: formulario.value.email,
      celular: formulario.value.celular,
      password: formulario.value.password,
      rol_id: 3,
      carrera_id: carreraId,
    })
    showModalCrear.value = false
    await cargarUsuarios()
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    mensajeError.value = httpDetail(e)
  } finally {
    isSubmittingCrear.value = false
  }
}

async function guardarEdicion() {
  mensajeErrorEditar.value = ''
  if (!pasanteSeleccionado.value) return

  isSubmittingEditar.value = true
  try {
    const res = await api.put(`/usuarios/editar/${pasanteSeleccionado.value.id}`, {
      nombres: formEditar.value.nombres,
      apellidos: formEditar.value.apellidos,
      carnet_identidad: formEditar.value.carnet_identidad,
      ru: (formEditar.value.ru || '').trim() || null,
      unidad_asignada: (formEditar.value.unidad_asignada || '').trim() || null,
      email: formEditar.value.email,
      celular: (formEditar.value.celular || '').trim() || null,
    })
    showModalEditar.value = false
    const actualizado = res.data as Usuario
    pasanteSeleccionado.value = actualizado
    await cargarUsuarios()
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    mensajeErrorEditar.value = httpDetail(e)
  } finally {
    isSubmittingEditar.value = false
  }
}

function confirmarCambioEstado(u: Usuario) {
  pasanteSeleccionado.value = u
  showModalBaja.value = true
}

async function ejecutarCambioEstado() {
  if (!pasanteSeleccionado.value) return
  const objetivo = pasanteSeleccionado.value

  try {
    if (objetivo.estado) {
      await api.delete(`/usuarios/desactivar/${objetivo.id}`)
    } else {
      await api.put(`/usuarios/editar/${objetivo.id}`, { estado: true })
    }
    showModalBaja.value = false
    await cargarUsuarios()
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    console.error('Error cambiando estado:', e)
  }
}

watch(tabVer, (tab) => {
  if (tab === 'historial' && pasanteSeleccionado.value && historial.value.length === 0 && !isLoadingHistorial.value) {
    cargarHistorial(pasanteSeleccionado.value.id)
  }
})

onMounted(() => {
  cargarUsuarios()
})

</script>
