<template>
  <div class="min-h-screen bg-slate-50 font-sans pb-12">

    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div class="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-blue-900 to-red-700"></div>
      <div class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-blue-900 rounded-lg flex items-center justify-center text-white font-black text-[11px] tracking-wider shadow-sm">UMSA</div>
            <div class="border-l border-slate-300 pl-4 py-1 hidden sm:block">
              <p class="text-[10px] text-red-700 font-bold uppercase tracking-widest leading-none mb-1">Facultad de Cs. Sociales</p>
              <p class="text-sm font-extrabold text-slate-800 leading-none">Sistema de Pasantías <span class="text-slate-400 font-medium ml-1">| Admin</span></p>
            </div>
          </div>
          <nav class="hidden lg:flex items-center gap-2">
            <button @click="router.push('/admin')" class="text-slate-500 hover:bg-slate-50 hover:text-blue-900 px-4 py-2 rounded-lg text-sm font-semibold transition-all">Monitor Global</button>
            <button @click="router.push('/usuarios')" class="text-slate-500 hover:bg-slate-50 hover:text-blue-900 px-4 py-2 rounded-lg text-sm font-semibold transition-all">Usuarios</button>
            <button @click="router.push('/programas')" class="text-slate-500 hover:bg-slate-50 hover:text-blue-900 px-4 py-2 rounded-lg text-sm font-semibold transition-all">Programas</button>
            <button class="bg-blue-50 text-blue-900 px-4 py-2 rounded-lg text-sm font-bold transition-all">Carreras</button>
          </nav>
          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-slate-800 text-sm font-bold leading-tight">{{ authStore.user?.nombres }}</span>
              <span class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Administrador</span>
            </div>
            <button @click="router.push('/perfil')" class="w-9 h-9 bg-slate-100 rounded-full flex items-center justify-center text-blue-900 font-bold text-sm border border-slate-200 hover:bg-slate-200">{{ obtenerIniciales(authStore.user?.nombres, authStore.user?.apellidos) }}</button>
            <div class="h-5 w-px bg-slate-300 hidden sm:block"></div>
            <button @click="cerrarSesion" class="text-slate-500 hover:text-red-600 transition-colors"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg></button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">

      <div>
        <h1 class="text-3xl font-black text-slate-800 tracking-tight">Catálogo de Carreras</h1>
        <p class="text-slate-500 text-sm mt-1">Configura las carreras de la Facultad y sus logos institucionales.</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
        <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">Registrar Nueva Carrera</h2>
        <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-end">
          <div class="flex-1 w-full">
            <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Nombre Oficial</label>
            <input v-model="nueva.nombre" type="text" placeholder="Ej. Trabajo Social" class="w-full border border-slate-300 rounded-lg p-2.5 outline-none focus:border-blue-500 text-sm font-medium" />
          </div>
          <div class="flex-1 w-full">
            <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Descripción</label>
            <input v-model="nueva.descripcion" type="text" placeholder="Opcional" class="w-full border border-slate-300 rounded-lg p-2.5 outline-none focus:border-blue-500 text-sm font-medium" />
          </div>
          <button @click="crear" :disabled="creando" class="w-full sm:w-auto px-5 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-bold hover:bg-blue-700 disabled:opacity-50">
            {{ creando ? 'Procesando...' : 'Añadir' }}
          </button>
        </div>
        <div v-if="error" class="mt-3 text-red-600 text-sm font-medium">{{ error }}</div>
      </div>

      <div v-if="isLoading" class="text-center py-10 text-slate-400 font-medium">Cargando catálogo...</div>
      <div v-else-if="carreras.length === 0" class="text-center py-10 text-slate-400 font-medium">No hay carreras en el sistema.</div>
      
      <div class="grid grid-cols-1 gap-4">
        <div v-for="c in carreras" :key="c.id" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col md:flex-row">
          
          <div class="md:w-32 bg-slate-50 border-r border-slate-100 flex flex-col items-center justify-center p-4 shrink-0">
            <div class="w-16 h-16 bg-white border border-slate-200 rounded-lg flex items-center justify-center overflow-hidden mb-2 shadow-sm">
              <img v-if="c.logo_url" :src="resolveStaticUrl(c.logo_url)" class="w-full h-full object-contain p-1" />
              <span v-else class="text-[9px] text-slate-400 font-bold">SIN LOGO</span>
            </div>
            <span class="text-[10px] font-mono text-slate-400">ID: {{ c.id }}</span>
          </div>

          <div class="p-5 flex-1 flex flex-col justify-between">
            <div>
              <div class="flex justify-between items-start mb-2">
                <input v-model="c._edit.nombre" class="font-bold text-slate-800 bg-transparent border-b border-slate-300 outline-none focus:border-blue-500 w-full max-w-[250px]" />
                <button @click="eliminar(c)" class="text-slate-300 hover:text-red-500" title="Eliminar"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg></button>
              </div>
              <input v-model="c._edit.descripcion" placeholder="Descripción de la carrera" class="text-xs text-slate-500 bg-transparent border-b border-slate-200 outline-none focus:border-blue-500 w-full mb-4" />
            </div>

            <div class="flex flex-wrap items-center justify-between gap-3 mt-auto">
              <div class="flex items-center gap-2 bg-slate-50 p-1.5 rounded-lg border border-slate-100">
                <input type="file" accept="image/*" @change="(e) => onFileChange(c, e)" class="text-[10px] w-48 text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:bg-slate-200 file:text-slate-700 cursor-pointer" />
              </div>
              <div class="flex items-center gap-4">
                <label class="flex items-center gap-1.5 text-xs font-bold text-slate-600 cursor-pointer">
                  <input type="checkbox" v-model="c._edit.estado" class="w-3.5 h-3.5 rounded text-blue-600" />
                  Activa
                </label>
                <button @click="guardar(c)" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-md transition-colors">Guardar</button>
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

const carreras = ref([]); const nueva = ref({ nombre: '', descripcion: '' })
const creando = ref(false); const isLoading = ref(true); const error = ref('')

const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.trim().charAt(0) : ''; const a = apellidos ? apellidos.trim().charAt(0) : ''
  if (!a && nombres) return nombres.substring(0, 2).toUpperCase()
  return (n + a).toUpperCase() || 'A'
}

const resolveStaticUrl = (url) => {
  if (!url) return null; const s = String(url);
  if (s.startsWith('http://') || s.startsWith('https://')) return s;
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`; return s
}

const cerrarSesion = () => { authStore.logout(); router.push('/login') }

const cargar = async () => {
  isLoading.value = true; error.value = ''
  try {
    const res = await api.get('/carreras/')
    carreras.value = (res.data || []).map(c => ({ ...c, _edit: { nombre: c.nombre, descripcion: c.descripcion || '', logo_url: c.logo_url || '', estado: !!c.estado } }))
  } catch (e) { error.value = 'Error al cargar.'; carreras.value = [] } finally { isLoading.value = false }
}

const crear = async () => {
  if (!nueva.value.nombre?.trim()) { error.value = 'Nombre obligatorio.'; return }
  creando.value = true; error.value = ''
  try { await api.post('/carreras/', { nombre: nueva.value.nombre, descripcion: nueva.value.descripcion || null, estado: true }); nueva.value = { nombre: '', descripcion: '' }; await cargar() } catch (e) { error.value = 'Error al crear.' } finally { creando.value = false }
}

const guardar = async (c) => {
  try { await api.put(`/carreras/${c.id}`, { nombre: c._edit.nombre, descripcion: c._edit.descripcion, logo_url: c._edit.logo_url || null, estado: c._edit.estado }); await cargar() } catch (e) { alert('Error al guardar') }
}

const eliminar = async (c) => {
  if (confirm(`¿Desactivar ${c.nombre}?`)) { try { await api.delete(`/carreras/${c.id}`); await cargar() } catch (e) { alert('Error') } }
}

const onFileChange = async (c, event) => {
  const file = event?.target?.files?.[0]; if (!file) return
  try { const fd = new FormData(); fd.append('file', file); const res = await api.post(`/carreras/${c.id}/logo`, fd); c._edit.logo_url = res.data.logo_url || ''; await guardar(c) } catch (e) { alert('Error al subir logo') }
}

onMounted(cargar)
</script>