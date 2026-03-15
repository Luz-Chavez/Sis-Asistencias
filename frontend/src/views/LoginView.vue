<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
      
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800">Iniciar Sesión</h2>
        <p class="text-gray-600 mt-2">Sistema de Control de Asistencia</p>
        <p class="text-sm text-gray-500">Facultad de Ciencias Sociales - UMSA</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
          <div class="mt-1">
            <input 
              v-model="email"
              id="email" 
              name="email" 
              type="email" 
              required 
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="tu@correo.com"
            >
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <div class="mt-1">
            <input 
              v-model="password"
              id="password" 
              name="password" 
              type="password" 
              required 
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="••••••••"
            >
          </div>
        </div>

        <div v-if="errorMessage" class="text-red-600 text-sm text-center bg-red-50 p-2 rounded">
          {{ errorMessage }}
        </div>

        <div>
          <button 
            type="submit" 
            :disabled="isLoading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
          >
            <span v-if="isLoading">Iniciando...</span>
            <span v-else>Entrar</span>
          </button>
        </div>
      </form>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const email = ref('');
const password = ref('');
const isLoading = ref(false);
const errorMessage = ref('');

const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    await authStore.login(email.value, password.value);
    
    // --- LÍNEAS NUEVAS PARA DEPURAR (RAYOS X) ---
    console.log("Token recibido:", authStore.token);
    console.log("Datos del usuario en Pinia:", authStore.user);
    
    const rol = authStore.user?.rol;
    console.log("El rol detectado es:", rol);
    // --------------------------------------------
    
    if (rol === 'DIRECTOR' || rol === 'DECANO' || rol === 'COORDINADOR') {
      router.push('/director'); 
    } else {
      router.push('/dashboard'); 
    }
    
  } catch (error) {
    // ... resto de tus errores ...
    if (error.response && error.response.status === 401) {
      errorMessage.value = 'Correo o contraseña incorrectos.';
    } else {
      errorMessage.value = 'Error al conectar con el servidor.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>