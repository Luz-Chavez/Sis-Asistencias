<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-indigo-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-6">
            <h1 class="text-white font-bold text-xl hidden md:block">Directorio</h1>
            
            <div class="flex gap-2">
              <button @click="router.push('/director')" class="text-indigo-200 hover:bg-indigo-800 hover:text-white px-4 py-2 rounded-md text-sm font-medium transition">
                📝 Ver Reportes
              </button>
              <button class="bg-indigo-800 text-white px-4 py-2 rounded-md text-sm font-bold shadow-inner cursor-default">
                👥 Gestión de Usuarios
              </button>
            </div>
            
          </div>
          <div class="flex items-center gap-4">
            <span class="text-indigo-200 text-sm hidden sm:block font-medium">
              {{ authStore.user?.nombres }} ({{ authStore.user?.rol }})
            </span>
            <button @click="cerrarSesion" class="text-sm bg-indigo-700 text-white px-4 py-2 rounded-md hover:bg-indigo-600 transition shadow">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
      
      <div class="flex flex-col md:flex-row justify-between items-center bg-white rounded-lg shadow px-5 py-6 sm:px-6 mb-6 border-l-4 border-indigo-600">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Directorio del Sistema</h2>
          <p class="text-gray-600 mt-1" v-if="esDirector">Administrando pasantes de tu carrera.</p>
          <p class="text-gray-600 mt-1" v-else>Administración general de la Facultad.</p>
        </div>
        <div class="mt-4 md:mt-0">
          <button @click="abrirModalCrear" class="bg-indigo-600 text-white px-5 py-2 rounded shadow hover:bg-indigo-700 transition font-medium flex items-center gap-2">
            <span>+</span> Nuevo Usuario
          </button>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Usuario</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rol</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Carrera ID</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Estado</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoading" class="text-center"><td colspan="5" class="px-6 py-4">Cargando...</td></tr>
              <tr v-else-if="usuarios.length === 0" class="text-center"><td colspan="5" class="px-6 py-4">No hay usuarios.</td></tr>
              <tr v-else v-for="user in usuarios" :key="user.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{{ user.id }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ user.nombres }} {{ user.apellidos }}</div>
                  <div class="text-sm text-gray-500">{{ user.email }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">{{ user.rol || 'Rol #' + user.rol_id }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.carrera_id || 'N/A' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center">
                  <span :class="[user.estado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'px-2 inline-flex text-xs leading-5 font-semibold rounded-full']">
                    {{ user.estado ? 'ACTIVO' : 'INACTIVO' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </main>

    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-lg shadow-2xl w-full max-w-2xl my-8">
        <div class="bg-indigo-600 px-6 py-4 flex justify-between items-center rounded-t-lg">
          <h3 class="text-lg font-bold text-white">Registrar Nuevo {{ esDirector ? 'Pasante' : 'Usuario' }}</h3>
          <button @click="cerrarModal" class="text-white hover:text-gray-200 font-bold text-xl">&times;</button>
        </div>

        <form @submit.prevent="registrarUsuario" class="px-6 py-5 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-bold text-gray-700">Nombres</label>
              <input v-model="formulario.nombres" type="text" required class="mt-1 w-full border border-gray-300 rounded p-2">
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Apellidos</label>
              <input v-model="formulario.apellidos" type="text" required class="mt-1 w-full border border-gray-300 rounded p-2">
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Carnet de Identidad</label>
              <input v-model="formulario.carnet_identidad" type="text" required class="mt-1 w-full border border-gray-300 rounded p-2">
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Correo Electrónico</label>
              <input v-model="formulario.email" type="email" required class="mt-1 w-full border border-gray-300 rounded p-2">
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Contraseña (Temporal)</label>
              <input v-model="formulario.password" type="password" required class="mt-1 w-full border border-gray-300 rounded p-2" placeholder="Ej. 123456">
            </div>
            
            <div v-if="!esDirector">
              <label class="block text-sm font-bold text-gray-700">Rol del Usuario</label>
              <select v-model="formulario.rol_id" required class="mt-1 w-full border border-gray-300 rounded p-2 bg-white">
                <option value="1">Decano</option>
                <option value="2">Coordinador</option>
                <option value="3">Director de Carrera</option>
                <option value="4">Pasante</option>
              </select>
            </div>
            <div v-else>
              <label class="block text-sm font-bold text-gray-700">Rol del Usuario</label>
              <input type="text" value="Pasante" disabled class="mt-1 w-full border border-gray-300 rounded p-2 bg-gray-100 text-gray-500">
            </div>

            <div v-if="!esDirector">
              <label class="block text-sm font-bold text-gray-700">ID de la Carrera (Opcional)</label>
              <input v-model="formulario.carrera_id" type="number" class="mt-1 w-full border border-gray-300 rounded p-2" placeholder="Ej. 1 para Social, 2 para Com...">
            </div>
            <div v-else>
              <label class="block text-sm font-bold text-gray-700">Carrera Asignada</label>
              <input type="text" :value="'Tu Carrera (ID: ' + authStore.user?.carrera_id + ')'" disabled class="mt-1 w-full border border-gray-300 rounded p-2 bg-gray-100 text-gray-500">
            </div>
          </div>

          <div v-if="mensajeError" class="text-red-600 bg-red-50 p-2 text-sm rounded border border-red-200">
            {{ mensajeError }}
          </div>

          <div class="flex justify-end gap-3 mt-6 border-t pt-4">
            <button type="button" @click="cerrarModal" class="px-4 py-2 border rounded text-gray-700 hover:bg-gray-100">Cancelar</button>
            <button type="submit" :disabled="isSubmitting" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:opacity-50">
              {{ isSubmitting ? 'Guardando...' : 'Guardar Usuario' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

const router = useRouter();
const authStore = useAuthStore();

// Estados de la tabla
const usuarios = ref([]);
const isLoading = ref(true);

// Estados del Modal
const showModal = ref(false);
const isSubmitting = ref(false);
const mensajeError = ref('');

// Determinamos si el usuario actual es solo Director
const esDirector = computed(() => authStore.user?.rol === 'DIRECTOR');

// Formulario reactivo
const formulario = ref({
  nombres: '',
  apellidos: '',
  carnet_identidad: '',
  email: '',
  password: '',
  rol_id: 4, // Por defecto Pasante
  carrera_id: null
});

onMounted(async () => {
  await cargarUsuarios();
});

const cargarUsuarios = async () => {
  isLoading.value = true;
  try {
    const response = await api.get('/usuarios/listar');
    usuarios.value = response.data;
  } catch (error) {
    console.error("Error al cargar usuarios:", error);
  } finally {
    isLoading.value = false;
  }
};

const abrirModalCrear = () => {
  // Limpiamos el formulario
  formulario.value = { nombres: '', apellidos: '', carnet_identidad: '', email: '', password: '', rol_id: 4, carrera_id: null };
  mensajeError.value = '';
  
  // Si es director, forzamos la seguridad desde el inicio
  if (esDirector.value) {
    formulario.value.rol_id = 4; // Solo puede crear Pasantes
    formulario.value.carrera_id = authStore.user?.carrera_id; // Solo en su carrera
  }
  
  showModal.value = true;
};

const cerrarModal = () => {
  showModal.value = false;
};

const registrarUsuario = async () => {
  isSubmitting.value = true;
  mensajeError.value = '';
  try {
    // Si el usuario deja la carrera en blanco siendo Decano, la enviamos como null
    const datosEnviar = { ...formulario.value };
    if (!datosEnviar.carrera_id) datosEnviar.carrera_id = null;

    await api.post('/usuarios/registro', datosEnviar);
    
    alert("¡Usuario creado exitosamente!");
    cerrarModal();
    await cargarUsuarios(); // Recargamos la tabla
  } catch (error) {
    mensajeError.value = error.response?.data?.detail || "Ocurrió un error al registrar el usuario.";
  } finally {
    isSubmitting.value = false;
  }
};

const cerrarSesion = () => {
  authStore.logout();
  router.push('/login');
};
</script>