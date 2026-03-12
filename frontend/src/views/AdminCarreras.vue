<template>
  <div class="min-h-screen bg-slate-50 font-sans">

    <!-- Navbar -->
    <nav class="bg-slate-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <!-- Logo UMSA -->
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-900 to-slate-800 rounded-xl flex items-center justify-center shadow-md border border-slate-700">
                <span class="text-amber-400 font-extrabold text-xs tracking-wider">UMSA</span>
              </div>
              <div class="hidden md:block border-l-2 border-white/10 pl-4 py-1">
                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Facultad de Cs. Sociales</p>
                <p class="text-sm font-extrabold text-white tracking-tight">Sistema de PasantÃ­as</p>
              </div>
            </div>

            <!-- NavegaciÃ³n -->
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
                GestiÃ³n de Usuarios
              </button>
              <button
                class="bg-white/10 text-white px-4 py-2 rounded-lg text-sm font-bold cursor-default shadow-sm border border-white/10 flex items-center gap-1.5">
                <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
                </svg>
                Carreras y Logos
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

      <!-- Mobile nav -->
      <div class="md:hidden border-t border-white/10 bg-slate-900 px-4 py-2 flex gap-2">
        <button @click="router.push('/admin')" class="flex-1 bg-transparent text-slate-400 hover:bg-white/10 px-3 py-2 rounded-lg text-xs font-semibold transition-all">
          Reportes
        </button>
        <button @click="router.push('/usuarios')" class="flex-1 bg-transparent text-slate-400 hover:bg-white/10 px-3 py-2 rounded-lg text-xs font-semibold transition-all">
          Usuarios
        </button>
        <button class="flex-1 bg-white/10 text-white border border-white/10 px-3 py-2 rounded-lg text-xs font-bold">
          Carreras
        </button>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-6">

      <!-- Hero Banner -->
      <div class="bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 rounded-2xl p-8 lg:p-10 text-white shadow-lg relative overflow-hidden flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
        <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500 opacity-20 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
        <div class="absolute bottom-0 left-10 w-32 h-32 bg-amber-500 opacity-20 rounded-full blur-2xl pointer-events-none"></div>

        <div class="relative z-10 max-w-xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/20 mb-4 backdrop-blur-md">
            <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
            <p class="text-xs font-bold text-amber-300 uppercase tracking-widest">GestiÃ³n Institucional</p>
          </div>
          <h2 class="text-3xl lg:text-4xl font-extrabold mb-3 tracking-tight leading-tight">
            Carreras y <span class="text-amber-400">Logos</span>
          </h2>
          <p class="text-blue-100/80 text-sm lg:text-base font-medium leading-relaxed">
            Personaliza cada carrera con su logo institucional. Los cambios se reflejan en todos los paneles del sistema.
          </p>
        </div>

        <div class="relative z-10 flex gap-4 w-full md:w-auto flex-wrap">
          <div class="flex-1 md:flex-none bg-white/10 backdrop-blur-md border border-white/20 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-white drop-shadow-md mb-1">{{ carreras.length }}</p>
            <p class="text-[10px] text-blue-200 uppercase tracking-widest font-bold">Total Carreras</p>
          </div>
          <div class="flex-1 md:flex-none bg-gradient-to-b from-emerald-500/20 to-emerald-600/20 backdrop-blur-md border border-emerald-400/30 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-emerald-400 drop-shadow-md mb-1">{{ totalActivas }}</p>
            <p class="text-[10px] text-emerald-200 uppercase tracking-widest font-bold">Activas</p>
          </div>
          <div class="flex-1 md:flex-none bg-gradient-to-b from-amber-500/20 to-amber-600/20 backdrop-blur-md border border-amber-400/30 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-amber-400 drop-shadow-md mb-1">{{ totalConLogo }}</p>
            <p class="text-[10px] text-amber-200 uppercase tracking-widest font-bold">Con Logo</p>
          </div>
        </div>
      </div>

      <!-- Formulario nueva carrera -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="px-8 py-5 bg-slate-900 flex items-center gap-3 border-b border-slate-800">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <h3 class="text-base font-black text-white tracking-tight">Registrar Nueva Carrera</h3>
        </div>

        <div class="p-6">
          <div class="flex flex-col md:flex-row md:items-end gap-4">
            <div class="flex-1">
              <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Nombre de la carrera</label>
              <input v-model="nueva.nombre" type="text" placeholder="Ej: SociologÃ­a"
                class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm font-medium placeholder:font-normal" />
            </div>
            <div class="flex-1">
              <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">DescripciÃ³n</label>
              <input v-model="nueva.descripcion" type="text" placeholder="Opcional"
                class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm font-medium placeholder:font-normal" />
            </div>
            <button @click="crear" :disabled="creando"
              class="px-6 py-3 rounded-xl bg-emerald-600 text-white text-sm font-bold hover:bg-emerald-700 disabled:opacity-50 transition-all shadow-md flex items-center gap-2 whitespace-nowrap">
              <span v-if="creando" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
              </svg>
              {{ creando ? 'Creando...' : 'Crear Carrera' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Error global -->
      <div v-if="error" class="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-rose-700 text-sm font-bold flex items-center gap-3">
        <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        {{ error }}
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="bg-white rounded-2xl border border-slate-200 p-16 text-center">
        <div class="flex flex-col items-center gap-4 text-slate-400">
          <svg class="animate-spin h-10 w-10 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="font-bold text-slate-500">Cargando carreras...</p>
        </div>
      </div>

      <!-- Grid de carreras -->
      <div v-else>

        <!-- Encabezado de secciÃ³n + botÃ³n actualizar -->
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-extrabold text-slate-800">Carreras registradas</h3>
            <p class="text-xs text-slate-400 font-medium mt-0.5">Edita los datos y sube el logo de cada carrera.</p>
          </div>
          <button @click="cargar" :disabled="isLoading"
            class="flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-600 text-sm font-bold hover:bg-slate-50 disabled:opacity-50 transition-all shadow-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Actualizar lista
          </button>
        </div>

        <!-- Empty state -->
        <div v-if="carreras.length === 0" class="bg-white rounded-2xl border border-slate-200 p-16 text-center">
          <div class="flex flex-col items-center gap-4 text-slate-400">
            <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center border border-slate-100">
              <svg class="w-10 h-10 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h7"/>
              </svg>
            </div>
            <p class="font-extrabold text-slate-600 text-lg">No hay carreras registradas</p>
            <p class="text-sm text-slate-400 font-medium">Usa el formulario de arriba para crear la primera.</p>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div v-for="c in carreras" :key="c.id"
            class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow">

            <!-- Cabecera de la tarjeta -->
            <div class="px-6 py-4 flex items-center justify-between bg-slate-50 border-b border-slate-200">
              <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-2xl bg-white border border-slate-200 overflow-hidden shadow-sm flex items-center justify-center flex-shrink-0">
                  <img v-if="c.logo_url" :src="resolveStaticUrl(c.logo_url)" alt="Logo" class="w-full h-full object-contain p-1.5" />
                  <span v-else class="text-slate-400 text-[10px] font-extrabold uppercase tracking-wider text-center leading-tight px-1">Sin Logo</span>
                </div>
                <div>
                  <p class="text-[10px] text-slate-400 font-mono font-bold tracking-wider">ID: {{ c.id }}</p>
                  <p class="text-base font-black text-slate-800 leading-tight">{{ c.nombre }}</p>
                  <span :class="c.estado ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-100 text-slate-500 border-slate-200'"
                    class="inline-flex items-center gap-1.5 text-[10px] px-2 py-0.5 rounded-full border font-bold uppercase tracking-wider mt-1">
                    <span class="w-1.5 h-1.5 rounded-full" :class="c.estado ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                    {{ c.estado ? 'ACTIVA' : 'INACTIVA' }}
                  </span>
                </div>
              </div>
              <button @click="eliminar(c)"
                class="p-2 rounded-xl border border-rose-200 text-rose-600 bg-rose-50 hover:bg-rose-100 transition-colors shadow-sm"
                title="Eliminar carrera">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>

            <!-- Cuerpo editable -->
            <div class="p-6 space-y-5">

              <div>
                <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Nombre</label>
                <input v-model="c._edit.nombre" type="text"
                  class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm font-medium" />
              </div>

              <div>
                <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">DescripciÃ³n</label>
                <textarea v-model="c._edit.descripcion" rows="2"
                  class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none text-sm font-medium"></textarea>
              </div>

              <div>
                <label class="block text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-2">Logo URL</label>
                <input v-model="c._edit.logo_url" type="text" placeholder="/static/logos/archivo.png"
                  class="w-full border border-slate-200 rounded-xl p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm font-medium placeholder:font-normal" />
                <p class="text-xs text-slate-400 mt-1.5 font-medium">Si subes una imagen abajo, se llenarÃ¡ automÃ¡ticamente.</p>
              </div>

              <!-- Subir imagen + controles -->
              <div class="bg-slate-50 rounded-xl border border-slate-200 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-extrabold text-slate-500 uppercase tracking-widest">Subir logo</label>
                  <input type="file" accept="image/*" @change="(e) => onFileChange(c, e)"
                    class="text-xs text-slate-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-slate-200 file:text-slate-700 hover:file:bg-slate-300 transition-all cursor-pointer" />
                </div>
                <div class="flex items-center gap-3">
                  <label class="flex items-center gap-2 text-sm text-slate-600 font-semibold cursor-pointer select-none">
                    <input type="checkbox" v-model="c._edit.estado" class="w-4 h-4 rounded accent-blue-700" />
                    Activa
                  </label>
                  <button @click="guardar(c)" :disabled="savingId === c.id"
                    class="px-5 py-2.5 rounded-xl bg-blue-900 text-white text-sm font-bold hover:bg-blue-800 disabled:opacity-50 transition-all shadow-md flex items-center gap-2">
                    <span v-if="savingId === c.id" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                    <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                    </svg>
                    {{ savingId === c.id ? 'Guardando...' : 'Guardar' }}
                  </button>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'

const router    = useRouter()
const authStore = useAuthStore()

const carreras  = ref([])
const nueva     = ref({ nombre: '', descripcion: '' })
const creando   = ref(false)
const isLoading = ref(true)
const error     = ref('')
const savingId  = ref(null)

// KPIs
const totalActivas  = computed(() => carreras.value.filter(c => c.estado).length)
const totalConLogo  = computed(() => carreras.value.filter(c => c.logo_url).length)

// Utilidad para iniciales del avatar
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
    const res = await api.get('/carreras/')
    carreras.value = (res.data || []).map(c => ({
      ...c,
      _edit: {
        nombre:      c.nombre,
        descripcion: c.descripcion || '',
        logo_url:    c.logo_url || '',
        estado:      !!c.estado,
      },
    }))
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al cargar carreras.'
  } finally {
    isLoading.value = false
  }
}

const crear = async () => {
  const nombre = (nueva.value.nombre || '').trim()
  if (!nombre) {
    error.value = 'El nombre de la carrera es obligatorio.'
    return
  }
  creando.value = true
  error.value = ''
  try {
    await api.post('/carreras/', {
      nombre,
      descripcion: (nueva.value.descripcion || '').trim() || null,
      estado: true,
    })
    nueva.value = { nombre: '', descripcion: '' }
    await cargar()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear la carrera.'
  } finally {
    creando.value = false
  }
}

const eliminar = async (c) => {
  if (!confirm(`Â¿Eliminar la carrera "${c.nombre}"? (Se desactivarÃ¡)`)) return
  error.value = ''
  savingId.value = c.id
  try {
    await api.delete(`/carreras/${c.id}`)
    await cargar()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al eliminar.'
  } finally {
    savingId.value = null
  }
}

const onFileChange = async (c, event) => {
  const file = event?.target?.files?.[0]
  if (!file) return
  error.value = ''
  savingId.value = c.id
  try {
    const fd = new FormData()
    fd.append('file', file)
    const res = await api.post(`/carreras/${c.id}/logo`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    c.logo_url         = res.data.logo_url
    c._edit.logo_url   = res.data.logo_url || ''
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al subir el logo.'
  } finally {
    savingId.value = null
    if (event?.target) event.target.value = ''
  }
}

const guardar = async (c) => {
  savingId.value = c.id
  error.value = ''
  try {
    const payload = {
      nombre:      c._edit.nombre,
      descripcion: c._edit.descripcion,
      logo_url:    c._edit.logo_url || null,
      estado:      !!c._edit.estado,
    }
    const res    = await api.put(`/carreras/${c.id}`, payload)
    c.nombre     = res.data.nombre
    c.descripcion = res.data.descripcion
    c.logo_url   = res.data.logo_url
    c.estado     = res.data.estado
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al guardar.'
  } finally {
    savingId.value = null
  }
}

onMounted(cargar)
</script>

