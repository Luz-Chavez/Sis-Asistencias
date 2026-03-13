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
            <button class="bg-blue-50 text-blue-900 px-4 py-2 rounded-lg text-sm font-bold transition-all">Programas</button>
            <button @click="router.push('/carreras')" class="text-slate-500 hover:bg-slate-50 hover:text-blue-900 px-4 py-2 rounded-lg text-sm font-semibold transition-all">Carreras</button>
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
        <h1 class="text-3xl font-black text-slate-800 tracking-tight">Programas y Convenios</h1>
        <p class="text-slate-500 text-sm mt-1">Crea programas institucionales para asignarlos a los pasantes.</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
        <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">Registrar Programa</h2>
        <div class="flex flex-col sm:flex-row gap-4">
          <div class="flex-1">
            <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Nombre Oficial</label>
            <input v-model="nuevo.nombre" type="text" placeholder="Ej. Pasantía Informática 2026" class="w-full border border-slate-300 rounded-lg p-2.5 outline-none focus:border-blue-500 text-sm font-medium" />
          </div>
          <div class="w-full sm:w-32">
            <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Gestión</label>
            <input v-model="nuevo.gestion" type="text" placeholder="2026" class="w-full border border-slate-300 rounded-lg p-2.5 outline-none focus:border-blue-500 text-sm font-medium" />
          </div>
        </div>
        <div class="mt-4">
          <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Descripción</label>
          <textarea v-model="nuevo.descripcion" rows="2" class="w-full border border-slate-300 rounded-lg p-2.5 outline-none focus:border-blue-500 text-sm resize-none"></textarea>
        </div>
        <div v-if="error" class="mt-3 text-red-600 text-sm font-medium">{{ error }}</div>
        <div class="mt-4 flex justify-end">
          <button @click="crear" :disabled="creando" class="px-5 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-bold hover:bg-blue-700 disabled:opacity-50">
            {{ creando ? 'Guardando...' : 'Crear Programa' }}
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="text-center py-10 text-slate-400 font-medium">Cargando...</div>
      <div v-else-if="!programas.length" class="text-center py-10 text-slate-400 font-medium">No hay programas.</div>
      
      <div class="space-y-4">
        <div v-for="p in programas" :key="p.id" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-5 py-3 bg-slate-50 border-b border-slate-100 flex justify-between items-center">
            <div>
              <span class="text-xs font-mono font-bold text-slate-400 mr-2">#{{ p.id }}</span>
              <span class="font-bold text-slate-800">{{ p.nombre }}</span>
              <span :class="p.estado ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-200 text-slate-600'" class="ml-3 text-[10px] px-2 py-0.5 rounded uppercase font-bold">{{ p.estado ? 'Activo' : 'Inactivo' }}</span>
            </div>
            <button @click="desactivar(p)" class="text-slate-400 hover:text-red-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg></button>
          </div>
          
          <div class="p-5">
            <div class="flex flex-col sm:flex-row gap-4 mb-4">
              <div class="flex-1">
                <input v-model="p._edit.nombre" type="text" class="w-full border-b border-slate-300 py-1 outline-none focus:border-blue-500 text-sm font-medium text-slate-800 bg-transparent" />
              </div>
              <div class="w-24">
                <input v-model="p._edit.gestion" type="text" class="w-full border-b border-slate-300 py-1 outline-none focus:border-blue-500 text-sm text-slate-600 text-center bg-transparent" />
              </div>
            </div>
            <textarea v-model="p._edit.descripcion" rows="1" class="w-full border border-slate-200 rounded bg-slate-50 p-2 text-sm text-slate-600 resize-none outline-none focus:border-blue-500"></textarea>
            
            <div class="mt-4 flex items-center justify-between border-t border-slate-100 pt-4">
              <div class="flex items-center gap-2">
                <a v-if="p.documento_url" :href="resolveStaticUrl(p.documento_url)" target="_blank" class="text-xs text-blue-600 hover:underline font-medium">Ver PDF/Doc</a>
                <span v-else class="text-xs text-slate-400">Sin archivo</span>
                <input type="file" accept="application/pdf,image/*" @change="(e) => onFileChange(p, e)" class="text-[10px] w-48 text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:bg-slate-100 file:text-slate-600 ml-4 cursor-pointer" />
                <button v-if="p._file" @click="subirDocumento(p)" class="text-[10px] bg-slate-800 text-white px-2 py-1 rounded">Subir</button>
              </div>
              <button @click="guardar(p)" class="px-4 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition-colors">Guardar</button>
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

const programas = ref([]); const nuevo = ref({ nombre: '', descripcion: '', gestion: '' })
const creando = ref(false); const isLoading = ref(true); const error = ref(''); const subiendoId = ref(null)

const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.trim().charAt(0) : ''; const a = apellidos ? apellidos.trim().charAt(0) : ''
  if (!a && nombres) return nombres.substring(0, 2).toUpperCase()
  return (n + a).toUpperCase() || 'A'
}

const resolveStaticUrl = (url) => {
  if (!url) return null; const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`; return s
}

const cerrarSesion = () => { authStore.logout(); router.push('/login') }

const cargar = async () => {
  isLoading.value = true; error.value = ''
  try {
    const res = await api.get('/programas/listar', { params: { incluir_inactivos: true } })
    programas.value = (res.data || []).map(p => ({ ...p, _edit: { nombre: p.nombre, descripcion: p.descripcion || '', gestion: p.gestion || '', estado: !!p.estado }, _file: null }))
  } catch (e) { error.value = 'Error al cargar.'; programas.value = [] } finally { isLoading.value = false }
}

const crear = async () => {
  if (!nuevo.value.nombre?.trim()) { error.value = 'Nombre obligatorio.'; return }
  creando.value = true; error.value = ''
  try {
    await api.post('/programas/crear', { nombre: nuevo.value.nombre, descripcion: nuevo.value.descripcion || null, gestion: nuevo.value.gestion || null, estado: true })
    nuevo.value = { nombre: '', descripcion: '', gestion: '' }; await cargar()
  } catch (e) { error.value = 'Error al crear.' } finally { creando.value = false }
}

const guardar = async (p) => {
  try { await api.put(`/programas/editar/${p.id}`, { nombre: p._edit.nombre, descripcion: p._edit.descripcion || null, gestion: p._edit.gestion || null, estado: p._edit.estado }); await cargar() } catch (e) { alert('Error al guardar') }
}

const desactivar = async (p) => {
  if (confirm(`¿Desactivar ${p.nombre}?`)) { try { await api.delete(`/programas/desactivar/${p.id}`); await cargar() } catch (e) { alert('Error') } }
}

const onFileChange = (p, event) => { p._file = event?.target?.files?.[0] || null }

const subirDocumento = async (p) => {
  if (!p._file) return; subiendoId.value = p.id
  try { const fd = new FormData(); fd.append('archivo', p._file); await api.post(`/programas/documento/${p.id}`, fd); p._file = null; await cargar() } catch (e) { alert('Error al subir') } finally { subiendoId.value = null }
}

onMounted(cargar)
</script>