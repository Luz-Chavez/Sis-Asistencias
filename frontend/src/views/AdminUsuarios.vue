<template>
  <div class="min-h-screen bg-gray-100">

    <!-- NAV -->
    <nav :class="esEncargado ? 'bg-indigo-800' : 'bg-purple-900'" class="shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-6">
            <h1 class="text-white font-bold text-xl hidden md:block">
              {{ esEncargado ? 'Panel del Encargado' : 'Administración' }}
            </h1>
            <div class="flex gap-2">
              <button @click="router.push(esEncargado ? '/encargado' : '/admin')"
                class="text-indigo-200 hover:bg-white/10 px-4 py-2 rounded-md text-sm font-medium transition">
                📝 Ver Reportes
              </button>
              <button class="bg-white/10 text-white px-4 py-2 rounded-md text-sm font-bold cursor-default">
                👥 Gestión de Usuarios
              </button>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-indigo-200 text-sm hidden sm:block">
              {{ authStore.user?.nombres }} ·
              <em class="font-mono text-xs">{{ authStore.user?.username }}</em>
              <span class="ml-1 text-xs opacity-60">({{ authStore.user?.rol }})</span>
            </span>
            <button @click="cerrarSesion"
              class="text-sm bg-white/10 text-white px-4 py-2 rounded-md hover:bg-white/20 transition shadow">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">

      <!-- Cabecera -->
      <div class="flex flex-col md:flex-row justify-between items-center bg-white rounded-lg shadow
                  px-5 py-6 mb-6 border-l-4"
           :class="esEncargado ? 'border-indigo-600' : 'border-purple-600'">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">
            {{ esEncargado ? 'Pasantes de mi Carrera' : 'Directorio General del Sistema' }}
          </h2>
          <p class="text-gray-500 mt-1 text-sm">
            <span v-if="esEncargado">Solo puedes ver y registrar pasantes asignados a tu carrera.</span>
            <span v-else>Vista completa — todos los roles y carreras.</span>
          </p>
        </div>
        <button @click="abrirModalCrear"
          class="mt-4 md:mt-0 text-white px-5 py-2 rounded shadow font-medium flex items-center gap-2 transition"
          :class="esEncargado ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-purple-600 hover:bg-purple-700'">
          + Nuevo {{ esEncargado ? 'Pasante' : 'Usuario' }}
        </button>
      </div>

      <!-- Tabla -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Username</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rol</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Carrera ID</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Estado</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoading">
                <td colspan="6" class="px-6 py-4 text-center text-gray-400">Cargando...</td>
              </tr>
              <tr v-else-if="usuarios.length === 0">
                <td colspan="6" class="px-6 py-4 text-center text-gray-400">No hay usuarios registrados.</td>
              </tr>
              <tr v-else v-for="user in usuarios" :key="user.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 text-sm text-gray-500">#{{ user.id }}</td>
                <td class="px-6 py-4">
                  <div class="text-sm font-medium text-gray-900">{{ user.nombres }} {{ user.apellidos }}</div>
                  <div class="text-xs text-gray-400">{{ user.email }}</div>
                </td>
                <td class="px-6 py-4 text-sm font-mono text-indigo-700">{{ user.username }}</td>
                <td class="px-6 py-4">
                  <span :class="rolClass(user.rol)"
                    class="px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ user.rol || 'Sin rol' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ user.carrera_id || 'N/A' }}</td>
                <td class="px-6 py-4 text-center">
                  <span :class="user.estado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ user.estado ? 'ACTIVO' : 'INACTIVO' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- ── Modal Crear Usuario ─────────────────────────────────────────────── -->
    <div v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/60 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-lg shadow-2xl w-full max-w-2xl my-8">

        <div class="px-6 py-4 flex justify-between items-center rounded-t-lg"
             :class="esEncargado ? 'bg-indigo-600' : 'bg-purple-700'">
          <h3 class="text-lg font-bold text-white">
            Registrar {{ esEncargado ? 'Nuevo Pasante' : 'Nuevo Usuario' }}
          </h3>
          <button @click="cerrarModal" class="text-white hover:text-gray-200 font-bold text-xl">&times;</button>
        </div>

        <!-- Preview del username -->
        <div v-if="usernamePreview" class="mx-6 mt-4 p-3 bg-blue-50 rounded border border-blue-200 text-sm text-blue-800">
          🔑 Username que se generará: <strong class="font-mono">{{ usernamePreview }}</strong>
        </div>

        <!-- Aviso para ENCARGADO -->
        <div v-if="esEncargado" class="mx-6 mt-3 p-3 bg-amber-50 rounded border border-amber-200 text-sm text-amber-800">
          ⚠️ Como Encargado, solo puedes registrar <strong>Pasantes</strong> en tu carrera
          <strong>(ID: {{ authStore.user?.carrera_id }})</strong>.
        </div>

        <form @submit.prevent="registrarUsuario" class="px-6 py-5 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div>
              <label class="block text-sm font-bold text-gray-700">Nombres</label>
              <input v-model="formulario.nombres" type="text" required
                class="mt-1 w-full border border-gray-300 rounded p-2 focus:ring-2 focus:ring-indigo-400 outline-none" />
            </div>

            <div>
              <label class="block text-sm font-bold text-gray-700">Apellidos</label>
              <input v-model="formulario.apellidos" type="text" required
                class="mt-1 w-full border border-gray-300 rounded p-2 focus:ring-2 focus:ring-indigo-400 outline-none" />
            </div>

            <div>
              <label class="block text-sm font-bold text-gray-700">Carnet de Identidad</label>
              <input v-model="formulario.carnet_identidad" type="text" required
                class="mt-1 w-full border border-gray-300 rounded p-2 focus:ring-2 focus:ring-indigo-400 outline-none" />
            </div>

            <div>
              <label class="block text-sm font-bold text-gray-700">Correo Electrónico</label>
              <input v-model="formulario.email" type="email" required
                class="mt-1 w-full border border-gray-300 rounded p-2 focus:ring-2 focus:ring-indigo-400 outline-none" />
            </div>

            <div>
              <label class="block text-sm font-bold text-gray-700">Contraseña (Temporal)</label>
              <input v-model="formulario.password" type="password" required
                class="mt-1 w-full border border-gray-300 rounded p-2 focus:ring-2 focus:ring-indigo-400 outline-none"
                placeholder="Mín. 6 caracteres" />
            </div>

            <!-- Rol: ADMIN elige libremente, ENCARGADO ve solo PASANTE bloqueado -->
            <div>
              <label class="block text-sm font-bold text-gray-700">Rol</label>
              <select v-if="!esEncargado" v-model="formulario.rol_id" required
                class="mt-1 w-full border border-gray-300 rounded p-2 bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
                <option :value="idRol('ADMINISTRADOR')">Administrador</option>
                <option :value="idRol('ENCARGADO')">Encargado</option>
                <option :value="idRol('PASANTE')">Pasante</option>
              </select>
              <input v-else type="text" value="Pasante" disabled
                class="mt-1 w-full border border-gray-200 rounded p-2 bg-gray-100 text-gray-500 cursor-not-allowed" />
            </div>

            <!-- Carrera: ADMIN escribe el ID, ENCARGADO ve la suya bloqueada -->
            <div>
              <label class="block text-sm font-bold text-gray-700">Carrera ID</label>
              <input v-if="!esEncargado" v-model="formulario.carrera_id" type="number"
                class="mt-1 w-full border border-gray-300 rounded p-2 focus:ring-2 focus:ring-indigo-400 outline-none"
                placeholder="Ej. 1" />
              <input v-else type="text" :value="'Tu carrera — ID ' + authStore.user?.carrera_id" disabled
                class="mt-1 w-full border border-gray-200 rounded p-2 bg-gray-100 text-gray-500 cursor-not-allowed" />
            </div>

          </div>

          <div v-if="mensajeError" class="text-red-600 bg-red-50 p-3 text-sm rounded border border-red-200">
            {{ mensajeError }}
          </div>

          <div class="flex justify-end gap-3 border-t pt-4">
            <button type="button" @click="cerrarModal"
              class="px-4 py-2 border rounded text-gray-700 hover:bg-gray-100">Cancelar</button>
            <button type="submit" :disabled="isSubmitting"
              class="px-4 py-2 text-white rounded disabled:opacity-50 transition"
              :class="esEncargado ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-purple-700 hover:bg-purple-800'">
              {{ isSubmitting ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router    = useRouter()
const authStore = useAuthStore()

const usuarios     = ref([])
const isLoading    = ref(true)
const showModal    = ref(false)
const isSubmitting = ref(false)
const mensajeError = ref('')

// IDs de roles cargados desde la BD (via /listar o hardcode según tu seed)
// Si los IDs en tu BD son distintos, ajústalos aquí o carga desde un endpoint
const rolesMap = ref({ ADMINISTRADOR: 1, ENCARGADO: 2, PASANTE: 3 })
const idRol = (nombre) => rolesMap.value[nombre] ?? null

const esEncargado = computed(() => authStore.user?.rol === 'ENCARGADO')

const formulario = ref({
  nombres: '', apellidos: '', carnet_identidad: '',
  email: '', password: '', rol_id: 3, carrera_id: null
})

// Preview del username en tiempo real
const usernamePreview = computed(() => {
  const n  = formulario.value.nombres?.trim()
  const a  = formulario.value.apellidos?.trim()
  const ci = formulario.value.carnet_identidad?.trim()
  if (!n || !a || !ci) return ''
  return `${n[0].toLowerCase()}${a[0].toLowerCase()}${ci}`
})

const rolClass = (rol) => {
  if (rol === 'ADMINISTRADOR') return 'bg-purple-100 text-purple-800'
  if (rol === 'ENCARGADO')     return 'bg-blue-100 text-blue-800'
  if (rol === 'PASANTE')       return 'bg-green-100 text-green-800'
  return 'bg-gray-100 text-gray-800'
}

onMounted(async () => { await cargarUsuarios() })

const cargarUsuarios = async () => {
  isLoading.value = true
  try {
    const res = await api.get('/usuarios/listar')
    usuarios.value = res.data
  } catch (e) {
    console.error('Error al cargar usuarios:', e)
  } finally {
    isLoading.value = false
  }
}

const abrirModalCrear = () => {
  formulario.value = {
    nombres: '', apellidos: '', carnet_identidad: '',
    email: '', password: '',
    // ENCARGADO siempre crea PASANTES en su carrera
    rol_id:     esEncargado.value ? idRol('PASANTE') : idRol('PASANTE'),
    carrera_id: esEncargado.value ? authStore.user?.carrera_id : null
  }
  mensajeError.value = ''
  showModal.value = true
}

const cerrarModal = () => { showModal.value = false }

const registrarUsuario = async () => {
  isSubmitting.value = true
  mensajeError.value = ''
  try {
    const datos = { ...formulario.value }
    // Asegurar que el ENCARGADO siempre envíe su carrera y rol=PASANTE
    if (esEncargado.value) {
      datos.rol_id     = idRol('PASANTE')
      datos.carrera_id = authStore.user?.carrera_id
    }
    if (!datos.carrera_id) datos.carrera_id = null

    await api.post('/usuarios/registro', datos)
    alert('¡Usuario registrado exitosamente!')
    cerrarModal()
    await cargarUsuarios()
  } catch (error) {
    mensajeError.value = error.response?.data?.detail || 'Ocurrió un error al registrar el usuario.'
  } finally {
    isSubmitting.value = false
  }
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/login')
}
</script>