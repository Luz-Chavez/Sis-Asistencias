<template>
  <div class="min-h-screen bg-gray-100">
    <!-- NAV -->
    <nav class="bg-purple-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-6">
            <h1 class="text-white font-bold text-xl hidden md:block">Panel Administrador</h1>
            <div class="flex gap-2">
              <button class="bg-purple-950 text-white px-4 py-2 rounded-md text-sm font-bold shadow-inner cursor-default">
                📝 Todos los Reportes
              </button>
              <button @click="router.push('/usuarios')"
                class="text-purple-200 hover:bg-purple-800 hover:text-white px-4 py-2 rounded-md text-sm font-medium transition">
                👥 Gestión de Usuarios
              </button>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-purple-200 text-sm hidden sm:block">
              {{ authStore.user?.nombres }} · <em class="font-mono text-xs">{{ authStore.user?.username }}</em>
            </span>
            <button @click="cerrarSesion"
              class="text-sm bg-purple-700 text-white px-4 py-2 rounded-md hover:bg-purple-600 transition shadow">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">

      <div class="bg-white rounded-lg shadow px-5 py-6 sm:px-6 mb-6 border-l-4 border-purple-600">
        <h2 class="text-2xl font-bold text-gray-800">Todos los Reportes de la Facultad</h2>
        <p class="text-gray-600 mt-1">Vista global — todos los pasantes y todas las carreras.</p>
      </div>

      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">#</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pasante</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actividades</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Estado</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Fecha</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoading"><td colspan="5" class="px-6 py-4 text-center text-gray-500">Cargando...</td></tr>
              <tr v-else-if="reportes.length === 0">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">No hay reportes registrados.</td>
              </tr>
              <tr v-else v-for="reporte in reportes" :key="reporte.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 text-sm font-medium text-gray-900">#{{ reporte.id }}</td>
                <td class="px-6 py-4 text-sm text-gray-900 font-semibold">
                  {{ reporte.nombre_pasante || 'Pasante #' + reporte.asistencia_id }}
                </td>
                <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">{{ reporte.actividades_realizadas }}</td>
                <td class="px-6 py-4 text-center">
                  <span :class="estadoClass(reporte.estado)"
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ reporte.estado || 'PENDIENTE' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-500 text-center">
                  {{ reporte.creado_en ? new Date(reporte.creado_en).toLocaleDateString('es-BO') : '—' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router    = useRouter()
const authStore = useAuthStore()

const reportes  = ref([])
const isLoading = ref(true)

const estadoClass = (estado) => {
  if (estado === 'APROBADO')  return 'bg-green-100 text-green-800'
  if (estado === 'RECHAZADO') return 'bg-red-100 text-red-800'
  return 'bg-yellow-100 text-yellow-800'
}

onMounted(async () => {
  isLoading.value = true
  try {
    const response = await api.get('/reportes/listar')
    reportes.value = response.data
  } catch (error) {
    console.error('Error al cargar reportes:', error)
  } finally {
    isLoading.value = false
  }
})

const cerrarSesion = () => {
  authStore.logout()
  router.push('/')
}
</script>