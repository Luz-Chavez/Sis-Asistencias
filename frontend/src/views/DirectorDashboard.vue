<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-indigo-800 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-6">
            <h1 class="text-white font-bold text-xl hidden md:block">Panel de Dirección</h1>
            
            <div class="flex gap-2">
              <button class="bg-indigo-900 text-white px-4 py-2 rounded-md text-sm font-bold shadow-inner cursor-default">
                📝 Ver Reportes
              </button>
              <button @click="router.push('/usuarios')" class="text-indigo-200 hover:bg-indigo-700 hover:text-white px-4 py-2 rounded-md text-sm font-medium transition">
                👥 Gestión de Usuarios
              </button>
            </div>
            
          </div>
          <div class="flex items-center gap-4">
             <span class="text-indigo-200 text-sm hidden sm:block font-medium">
              Hola, {{ authStore.user?.nombres }}
            </span>
            <button @click="cerrarSesion" class="text-sm bg-indigo-700 text-white px-4 py-2 rounded-md hover:bg-indigo-900 transition-colors shadow">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
      
      <div class="bg-white rounded-lg shadow px-5 py-6 sm:px-6 mb-6 border-l-4 border-indigo-600">
        <h2 class="text-2xl font-bold text-gray-800">Reportes Diarios Recibidos</h2>
        <p class="text-gray-600 mt-1">Revisa y evalúa las actividades reportadas por los pasantes de la Facultad.</p>
      </div>

      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID Reporte</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pasante</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actividades Resumidas</th>
                <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoading" class="text-center">
                <td colspan="5" class="px-6 py-4 text-gray-500">Cargando reportes...</td>
              </tr>
              <tr v-else-if="reportes.length === 0" class="text-center">
                <td colspan="5" class="px-6 py-4 text-gray-500">No hay reportes para revisar en este momento.</td>
              </tr>
              <tr v-else v-for="reporte in reportes" :key="reporte.id" class="hover:bg-gray-50 transition">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ reporte.id }}</td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-semibold">
                  {{ reporte.nombre_pasante || 'Pasante (Asistencia #' + reporte.asistencia_id + ')' }}
                </td>

                <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                  {{ reporte.actividades_realizadas }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center">
                  <span 
                    :class="[
                      reporte.estado === 'APROBADO' ? 'bg-green-100 text-green-800' : '',
                      reporte.estado === 'RECHAZADO' ? 'bg-red-100 text-red-800' : '',
                      reporte.estado === 'PENDIENTE' || !reporte.estado ? 'bg-yellow-100 text-yellow-800' : '',
                      'px-2 inline-flex text-xs leading-5 font-semibold rounded-full'
                    ]"
                  >
                    {{ reporte.estado || 'PENDIENTE' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                  <button 
                    @click="abrirModal(reporte)"
                    class="text-indigo-600 hover:text-indigo-900 bg-indigo-50 px-3 py-1 rounded shadow-sm hover:shadow transition"
                  >
                    Revisar y Evaluar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </main>

    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 px-4 backdrop-blur-sm">
      
      <div class="relative bg-white rounded-lg shadow-2xl w-full max-w-lg overflow-hidden">
        
        <div class="bg-indigo-600 px-6 py-4 flex justify-between items-center">
          <h3 class="text-lg font-bold text-white">
            Evaluación del Reporte #{{ reporteSeleccionado?.id }}
          </h3>
          <button @click="cerrarModal" class="text-white hover:text-gray-200 font-bold text-xl">&times;</button>
        </div>

        <div class="px-6 py-5">
          <p class="text-sm text-gray-700 font-bold mb-2">Actividades Reportadas:</p>
          <div class="bg-indigo-50 p-3 rounded border border-indigo-100 text-sm text-gray-800 mb-5 whitespace-pre-wrap shadow-inner">
            {{ reporteSeleccionado?.actividades_realizadas }}
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-1">Decisión</label>
              <select v-model="evaluacion.estado" class="w-full border border-gray-300 rounded-md shadow-sm py-2.5 px-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-white cursor-pointer">
                <option value="APROBADO">✅ Aprobar Reporte</option>
                <option value="RECHAZADO">❌ Rechazar Reporte</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-1">Comentarios (Opcional)</label>
              <textarea 
                v-model="evaluacion.comentarios" 
                rows="3" 
                class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Escribe una retroalimentación para el pasante..."
              ></textarea>
            </div>
          </div>
        </div>

        <div class="bg-gray-50 px-6 py-4 flex justify-end gap-3 border-t">
          <button @click="cerrarModal" type="button" class="px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-100 transition">
            Cancelar
          </button>
          <button @click="enviarEvaluacion" type="button" :disabled="isSubmitting" class="px-4 py-2 bg-indigo-600 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 transition disabled:opacity-50">
            {{ isSubmitting ? 'Guardando...' : 'Guardar Evaluación' }}
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

const router = useRouter();
const authStore = useAuthStore();

// Estados reactivos
const reportes = ref([]);
const isLoading = ref(true);
const showModal = ref(false);
const reporteSeleccionado = ref(null);
const isSubmitting = ref(false);

// Datos del formulario de evaluación
const evaluacion = ref({
  estado: 'APROBADO',
  comentarios: ''
});

// Cargar reportes al montar el componente
onMounted(async () => {
  await cargarReportes();
});

const cargarReportes = async () => {
  isLoading.value = true;
  try {
    const response = await api.get('/reportes/listar');
    reportes.value = response.data;
  } catch (error) {
    console.error("Error al cargar reportes:", error);
    if (error.response && error.response.status === 401) {
      alert("Sesión expirada o no autorizada.");
      cerrarSesion();
    }
  } finally {
    isLoading.value = false;
  }
};

// Control del Modal
const abrirModal = (reporte) => {
  reporteSeleccionado.value = reporte;
  // Si ya tenía evaluación, la cargamos
  evaluacion.value.estado = reporte.estado && reporte.estado !== 'PENDIENTE' ? reporte.estado : 'APROBADO';
  evaluacion.value.comentarios = reporte.comentarios_director || '';
  showModal.value = true;
};

const cerrarModal = () => {
  showModal.value = false;
  reporteSeleccionado.value = null;
};

// Enviar la evaluación al backend
const enviarEvaluacion = async () => {
  isSubmitting.value = true;
  try {
    await api.put(`/reportes/evaluar/${reporteSeleccionado.value.id}`, {
      estado: evaluacion.value.estado,
      comentarios_director: evaluacion.value.comentarios
    });
    
    // Recargamos la tabla para ver los cambios
    await cargarReportes();
    cerrarModal();
    alert("¡Evaluación guardada con éxito!");
    
  } catch (error) {
    console.error("Error al evaluar:", error);
    alert("Ocurrió un error al guardar la evaluación.");
  } finally {
    isSubmitting.value = false;
  }
};

const cerrarSesion = () => {
  authStore.logout();
  router.push('/login');
};
</script>