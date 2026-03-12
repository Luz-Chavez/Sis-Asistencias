<template>
  <div class="min-h-screen bg-slate-50 font-sans">

    <nav class="bg-slate-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-900 to-slate-800 rounded-xl flex items-center justify-center shadow-md border border-slate-700">
                <span class="text-amber-400 font-extrabold text-xs tracking-wider">UMSA</span>
              </div>
              <div class="hidden md:block border-l-2 border-white/10 pl-4 py-1">
                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Facultad de Cs. Sociales</p>
                <p class="text-sm font-extrabold text-white tracking-tight">Sistema de Pasantias</p>
              </div>
            </div>

            <div class="hidden md:flex gap-2 ml-4">
              <button @click="router.push('/admin')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                </svg>
                Volver a Reportes
              </button>
              <button @click="router.push('/usuarios')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                </svg>
                Gestion de Usuarios
              </button>
              <button @click="router.push('/carreras')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
                </svg>
                Carreras y Logos
              </button>
              <button
                class="bg-white/10 text-white px-4 py-2 rounded-lg text-sm font-bold cursor-default shadow-sm border border-white/10 flex items-center gap-1.5">
                <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Programas
              </button>
            </div>
          </div>

          <div class="flex items-center gap-4">
            <div class="hidden sm:flex items-center gap-3">
              <div class="flex flex-col items-end">
                <span class="text-white text-sm font-bold leading-tight">{{ authStore.user?.nombres }}</span>
                <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider">{{ authStore.user?.rol }}</span>
              </div>
              <button @click="router.push('/perfil')" title="Perfil"
                class="w-9 h-9 bg-white/10 rounded-full flex items-center justify-center text-white font-bold text-sm border border-white/20 hover:bg-white/20 transition-colors">
                {{ obtenerIniciales(authStore.user?.nombres, authStore.user?.apellidos) }}
              </button>
            </div>
            <div class="h-6 w-px bg-white/10 hidden sm:block"></div>
            <button @click="cerrarSesion"
              class="flex items-center gap-2 text-sm font-semibold text-slate-300 hover:text-rose-400 transition-colors group">
              <span class="hidden sm:inline">Salir</span>
              <svg class="w-5 h-5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div class="md:hidden border-t border-white/10 bg-slate-900 px-4 py-2 flex gap-2">
        <button @click="router.push('/admin')" class="flex-1 bg-transparent text-slate-400 hover:bg-white/10 px-3 py-2 rounded-lg text-xs font-semibold transition-all">
          Reportes
        </button>
        <button @click="router.push('/usuarios')" class="flex-1 bg-transparent text-slate-400 hover:bg-white/10 px-3 py-2 rounded-lg text-xs font-semibold transition-all">
          Usuarios
        </button>
        <button class="flex-1 bg-white/10 text-white border border-white/10 px-3 py-2 rounded-lg text-xs font-bold">
          Programas
        </button>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-6">

      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <div class="flex flex-col lg:flex-row lg:items-end gap-4">
          <div class="flex-1">
            <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Nombre</label>
            <input v-model="nuevo.nombre" type="text" placeholder="Ej. Programa de Pasantia Informatica 2026"
              class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm font-medium" />
          </div>
          <div class="w-full lg:w-56">
            <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Gestion/Anio</label>
            <input v-model="nuevo.gestion" type="text" placeholder="2026"
              class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm font-medium" />
          </div>
        </div>
        <div class="mt-4">
          <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Descripcion</label>
          <textarea v-model="nuevo.descripcion" rows="2" placeholder="Descripcion corta del programa"
            class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none text-sm font-medium"></textarea>
        </div>

        <div v-if="error" class="mt-4 text-rose-700 bg-rose-50 p-4 text-sm rounded-xl border border-rose-200 font-bold">
          {{ error }}
        </div>

        <div class="mt-5 flex justify-end">
          <button @click="crear" :disabled="creando"
            class="px-6 py-3 rounded-xl bg-blue-900 text-white font-bold hover:bg-blue-800 disabled:opacity-50 transition-colors shadow-sm flex items-center gap-2">
            <span v-if="creando" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            Crear programa
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div v-if="isLoading" class="bg-white rounded-2xl border border-slate-200 shadow-sm p-10 text-center text-slate-500 font-bold">
          Cargando programas...
        </div>

        <div v-else-if="!programas.length" class="bg-white rounded-2xl border border-slate-200 shadow-sm p-10 text-center text-slate-500">
          <p class="font-extrabold text-slate-600 text-lg">No hay programas registrados</p>
          <p class="text-sm mt-1 text-slate-400 font-medium">Usa el formulario para crear el primero.</p>
        </div>

        <div v-else v-for="p in programas" :key="p.id"
          class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow">

          <div class="px-6 py-4 flex items-center justify-between bg-slate-50 border-b border-slate-200">
            <div>
              <p class="text-[10px] text-slate-400 font-mono font-bold tracking-wider">ID: {{ p.id }}</p>
              <p class="text-base font-black text-slate-800 leading-tight">{{ p.nombre }}</p>
              <span :class="p.estado ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-100 text-slate-500 border-slate-200'"
                class="inline-flex items-center gap-1.5 text-[10px] px-2 py-0.5 rounded-full border font-bold uppercase tracking-wider mt-1">
                <span class="w-1.5 h-1.5 rounded-full" :class="p.estado ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                {{ p.estado ? 'ACTIVO' : 'INACTIVO' }}
              </span>
            </div>
            <button @click="desactivar(p)" :disabled="!p.estado"
              class="p-2 rounded-xl border border-slate-200 text-slate-600 bg-white hover:bg-slate-50 transition-colors shadow-sm disabled:opacity-50"
              title="Desactivar programa">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
              </svg>
            </button>
          </div>

          <div class="p-6 space-y-5">
            <div>
              <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Nombre</label>
              <input v-model="p._edit.nombre" type="text"
                class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm font-medium" />
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Gestion/Anio</label>
                <input v-model="p._edit.gestion" type="text"
                  class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm font-medium" />
              </div>
              <div class="flex items-end">
                <label class="inline-flex items-center gap-2 text-sm font-bold text-slate-700 select-none">
                  <input type="checkbox" v-model="p._edit.estado" class="w-4 h-4 rounded border-slate-300 text-blue-700 focus:ring-blue-500" />
                  Activo
                </label>
              </div>
            </div>

            <div>
              <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Descripcion</label>
              <textarea v-model="p._edit.descripcion" rows="2"
                class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none text-sm font-medium"></textarea>
            </div>

            <div class="bg-slate-50 rounded-xl border border-slate-200 p-4 space-y-3">
              <div class="flex items-center justify-between gap-3">
                <div class="flex flex-col">
                  <span class="text-xs font-extrabold text-slate-500 uppercase tracking-widest">Documento</span>
                  <a v-if="p.documento_url" :href="resolveStaticUrl(p.documento_url)" target="_blank"
                    class="text-xs text-blue-700 font-bold hover:underline mt-1">
                    Ver documento
                  </a>
                  <span v-else class="text-xs text-slate-400 font-medium mt-1">Sin documento</span>
                </div>
                <button @click="guardar(p)" :disabled="savingId === p.id"
                  class="px-4 py-2 rounded-xl border border-blue-700 bg-blue-700 text-white font-bold hover:bg-blue-800 disabled:opacity-50 transition-colors shadow-sm flex items-center gap-2">
                  <span v-if="savingId === p.id" class="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
                  Guardar
                </button>
              </div>

              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <input type="file" accept="application/pdf,image/*" @change="(e) => onFileChange(p, e)"
                  class="text-xs text-slate-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-slate-200 file:text-slate-700 hover:file:bg-slate-300 transition-all cursor-pointer" />
                <button @click="subirDocumento(p)" :disabled="!p._file || subiendoId === p.id"
                  class="px-4 py-2 rounded-xl border font-bold text-sm transition-colors shadow-sm flex items-center gap-2"
                  :class="!p._file ? 'border-slate-200 text-slate-400 bg-slate-50 cursor-not-allowed' : 'border-emerald-700 bg-emerald-700 text-white hover:bg-emerald-800'">
                  <span v-if="subiendoId === p.id" class="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
                  Subir
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const programas = ref([])
const nuevo = ref({ nombre: '', descripcion: '', gestion: '' })
const creando = ref(false)
const isLoading = ref(true)
const error = ref('')
const savingId = ref(null)
const subiendoId = ref(null)

const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.trim().charAt(0) : ''
  const a = apellidos ? apellidos.trim().charAt(0) : ''
  if (!a && nombres) {
    const parts = nombres.trim().split(' ')
    if (parts.length > 1) return (parts[0][0] + parts[1][0]).toUpperCase()
    return nombres.substring(0, 2).toUpperCase()
  }
  return (n + a).toUpperCase() || 'U'
}

const resolveStaticUrl = (url) => {
  if (!url) return null
  const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`
  return s
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/login')
}

const cargar = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const res = await api.get('/programas/listar', { params: { incluir_inactivos: true } })
    programas.value = (res.data || []).map(p => ({
      ...p,
      _edit: {
        nombre: p.nombre,
        descripcion: p.descripcion || '',
        gestion: p.gestion || '',
        estado: !!p.estado,
      },
      _file: null,
    }))
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al cargar programas.'
    programas.value = []
  } finally {
    isLoading.value = false
  }
}

const crear = async () => {
  const nombre = (nuevo.value.nombre || '').trim()
  if (!nombre) {
    error.value = 'El nombre del programa es obligatorio.'
    return
  }
  creando.value = true
  error.value = ''
  try {
    await api.post('/programas/crear', {
      nombre,
      descripcion: (nuevo.value.descripcion || '').trim() || null,
      gestion: (nuevo.value.gestion || '').trim() || null,
      estado: true,
    })
    nuevo.value = { nombre: '', descripcion: '', gestion: '' }
    await cargar()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear el programa.'
  } finally {
    creando.value = false
  }
}

const guardar = async (p) => {
  savingId.value = p.id
  error.value = ''
  try {
    await api.put(`/programas/editar/${p.id}`, {
      nombre: (p._edit.nombre || '').trim(),
      descripcion: (p._edit.descripcion || '').trim() || null,
      gestion: (p._edit.gestion || '').trim() || null,
      estado: !!p._edit.estado,
    })
    await cargar()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al guardar el programa.'
  } finally {
    savingId.value = null
  }
}

const desactivar = async (p) => {
  if (!confirm(`Deseas desactivar el programa "${p.nombre}"?`)) return
  error.value = ''
  try {
    await api.delete(`/programas/desactivar/${p.id}`)
    await cargar()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al desactivar el programa.'
  }
}

const onFileChange = (p, event) => {
  const files = event?.target?.files || []
  p._file = files.length ? files[0] : null
}

const subirDocumento = async (p) => {
  if (!p._file) return
  subiendoId.value = p.id
  error.value = ''
  try {
    const formData = new FormData()
    formData.append('archivo', p._file)
    await api.post(`/programas/documento/${p.id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    p._file = null
    await cargar()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al subir el documento.'
  } finally {
    subiendoId.value = null
  }
}

onMounted(async () => {
  await cargar()
})
</script>
