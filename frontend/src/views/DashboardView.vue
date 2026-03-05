<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-blue-600 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex-shrink-0 flex items-center">
            <h1 class="text-white font-bold text-xl">Sistema de Asistencia</h1>
          </div>
          <div>
            <button 
              @click="cerrarSesion" 
              class="text-sm bg-blue-700 text-white px-4 py-2 rounded-md hover:bg-blue-800 transition-colors"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8 space-y-6">
      
      <div class="bg-white rounded-lg shadow px-5 py-6 sm:px-6">
        <h2 class="text-2xl font-bold text-gray-800">Panel del Pasante</h2>
        <p class="text-gray-600 mt-1">Gestiona tu asistencia y reportes diarios.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <div class="bg-white rounded-lg shadow px-5 py-6 sm:px-6 border-t-4 border-blue-500 flex flex-col justify-between">
          <div>
            <h3 class="text-lg font-bold text-gray-900 mb-4 text-center">1. Registro de Entrada</h3>
            <div class="flex flex-col gap-3">
              <button @click="marcarConGPSReal" :disabled="isLoadingEntrada" class="w-full flex justify-center items-center bg-gray-800 text-white py-2 px-4 rounded shadow hover:bg-gray-900 disabled:opacity-50 transition">
                <span v-if="isLoadingEntrada">Procesando...</span>
                <span v-else>📍 Usar mi GPS Real</span>
              </button>
              <button @click="marcarConGPSSimulado" :disabled="isLoadingEntrada" class="w-full flex justify-center items-center bg-green-600 text-white py-2 px-4 rounded shadow hover:bg-green-700 disabled:opacity-50 transition">
                <span v-if="isLoadingEntrada">Procesando...</span>
                <span v-else>🎓 Simular en UMSA</span>
              </button>
            </div>
          </div>
          <div v-if="mensajeEntrada" :class="[tipoMensajeEntrada, 'mt-4 p-3 rounded text-sm font-medium text-center border']">
            {{ mensajeEntrada }}
          </div>
        </div>

        <div class="bg-white rounded-lg shadow px-5 py-6 sm:px-6 border-t-4 border-red-500 flex flex-col justify-between">
          <div>
            <h3 class="text-lg font-bold text-gray-900 mb-4 text-center">2. Registro de Salida</h3>
            <p class="text-sm text-gray-500 text-center mb-4">Marca tu salida al finalizar tu jornada para calcular tus horas.</p>
            <button @click="marcarSalida" :disabled="isLoadingSalida" class="w-full flex justify-center items-center bg-red-600 text-white py-2 px-4 rounded shadow hover:bg-red-700 disabled:opacity-50 transition">
              <span v-if="isLoadingSalida">Procesando...</span>
              <span v-else>👋 Marcar Salida</span>
            </button>
          </div>
          <div v-if="mensajeSalida" class="mt-4 p-3 rounded text-sm font-medium text-center border bg-blue-50 text-blue-800 border-blue-200">
            {{ mensajeSalida }}
          </div>
        </div>

      </div>

      <div class="bg-white rounded-lg shadow px-5 py-6 sm:px-6 border-t-4 border-purple-500">
        <h3 class="text-lg font-bold text-gray-900 mb-4">3. Reporte de Actividades</h3>
        
        <form @submit.prevent="subirReporte" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">¿Qué actividades realizaste hoy?</label>
            <textarea 
              v-model="actividades" 
              rows="4" 
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
              placeholder="Ej. Hoy realicé el mantenimiento de la base de datos..."
            ></textarea>
          </div>
          
          <button type="submit" :disabled="isLoadingReporte || !actividades" class="w-full md:w-auto px-6 py-2 bg-purple-600 text-white rounded-md shadow hover:bg-purple-700 disabled:opacity-50 transition font-medium">
            <span v-if="isLoadingReporte">Guardando...</span>
            <span v-else>📝 Guardar / Actualizar Reporte</span>
          </button>
          
          <div v-if="mensajeReporte" :class="[tipoMensajeReporte, 'mt-4 p-3 rounded text-sm font-medium border']">
            {{ mensajeReporte }}
          </div>

          <div v-if="tipoMensajeReporte === 'bg-green-100 text-green-800 border-green-400'" class="mt-4 flex justify-center">
            <button 
              @click.prevent="descargarPDF" 
              class="flex items-center gap-2 bg-gray-800 text-white px-6 py-2 rounded-md shadow hover:bg-gray-900 transition font-medium"
            >
              📄 Descargar Comprobante PDF
            </button>
          </div>
        </form>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

const router = useRouter();
const authStore = useAuthStore();

// --- ESTADOS ---
const isLoadingEntrada = ref(false);
const mensajeEntrada = ref('');
const tipoMensajeEntrada = ref('');

const isLoadingSalida = ref(false);
const mensajeSalida = ref('');

const actividades = ref('');
const isLoadingReporte = ref(false);
const mensajeReporte = ref('');
const tipoMensajeReporte = ref('');

const ASISTENCIA_ACTUAL_ID = 1;

// --- FUNCIONES DE ENTRADA ---
const enviarAsistencia = async (lat, lon) => {
  isLoadingEntrada.value = true;
  mensajeEntrada.value = '';

  try {
    const payload = { pasante_id: 1, latitud_entrada: lat, longitud_entrada: lon };
    const response = await api.post('/asistencias/entrada', payload);
    
    tipoMensajeEntrada.value = response.data.esta_en_facultad 
      ? 'bg-green-100 text-green-800 border-green-400' 
      : 'bg-yellow-100 text-yellow-800 border-yellow-400';
    
    mensajeEntrada.value = response.data.mensaje_alerta;

  } catch (error) {
    tipoMensajeEntrada.value = 'bg-red-100 text-red-800 border-red-400';
    if (error.response && error.response.status === 401) {
      alert("Tu sesión ha expirado por seguridad. Por favor, vuelve a iniciar sesión.");
      cerrarSesion();
    } else if (error.response && error.response.status === 400) {
      mensajeEntrada.value = '⚠️ Ya tienes un registro de entrada para el día de hoy.';
    } else {
      mensajeEntrada.value = 'Error al conectar con el servidor.';
    }
  } finally {
    isLoadingEntrada.value = false;
  }
};

const marcarConGPSReal = () => {
  if (!navigator.geolocation) {
    tipoMensajeEntrada.value = 'bg-red-100 text-red-800 border-red-400';
    mensajeEntrada.value = 'Tu navegador no soporta geolocalización.';
    return;
  }
  isLoadingEntrada.value = true;
  mensajeEntrada.value = 'Obteniendo tu ubicación satelital...';
  tipoMensajeEntrada.value = 'bg-blue-100 text-blue-800 border-blue-400';

  navigator.geolocation.getCurrentPosition(
    (position) => enviarAsistencia(position.coords.latitude, position.coords.longitude),
    (error) => {
      isLoadingEntrada.value = false;
      tipoMensajeEntrada.value = 'bg-red-100 text-red-800 border-red-400';
      mensajeEntrada.value = 'No pudimos acceder a tu GPS. Verifica los permisos.';
    }
  );
};

const marcarConGPSSimulado = () => enviarAsistencia(-16.5048, -68.1299);

// --- FUNCIÓN DE SALIDA ---
const marcarSalida = async () => {
  isLoadingSalida.value = true;
  mensajeSalida.value = '';

  try {
    const payload = {
      latitud_salida: -16.5048,
      longitud_salida: -68.1299
    };
    const response = await api.put(`/asistencias/salida/${ASISTENCIA_ACTUAL_ID}`, payload);
    mensajeSalida.value = `¡Salida registrada! Has trabajado ${response.data.horas_trabajadas} horas hoy.`;
    
  } catch (error) {
    if (error.response && error.response.status === 404) {
      mensajeSalida.value = 'Registro no encontrado o la salida ya fue marcada.';
    } else if (error.response && error.response.status === 422) {
      mensajeSalida.value = 'Error de validación con el backend (Revisa la consola F12).';
      console.error("Detalle del Error 422:", error.response.data.detail);
    } else {
      mensajeSalida.value = 'Error al registrar la salida.';
    }
  } finally {
    isLoadingSalida.value = false;
  }
};

// --- FUNCIÓN DE REPORTE (MODO EDICIÓN ACTIVADO) ---
const subirReporte = async () => {
  isLoadingReporte.value = true;
  mensajeReporte.value = '';

  try {
    const payload = {
      asistencia_id: ASISTENCIA_ACTUAL_ID,
      actividades_realizadas: actividades.value,
      archivo_adjunto_url: ""
    };

    await api.post('/reportes/subir', payload);
    
    tipoMensajeReporte.value = 'bg-green-100 text-green-800 border-green-400';
    mensajeReporte.value = '¡Reporte guardado/actualizado exitosamente!';
    
    // Aquí ya NO limpiamos actividades.value para que puedas seguir editando

  } catch (error) {
    tipoMensajeReporte.value = 'bg-red-100 text-red-800 border-red-400';
    mensajeReporte.value = error.response?.data?.detail || 'Error al procesar el reporte.';
  } finally {
    isLoadingReporte.value = false;
  }
};

// --- FUNCIÓN PARA DESCARGAR EL PDF ---
const descargarPDF = async () => {
  try {
    const response = await api.get(`/reportes/descargar/${ASISTENCIA_ACTUAL_ID}`, {
      responseType: 'blob'
    });

    // 1. Extraemos el nombre dinámico que nos manda el backend
    let nombreArchivo = 'ReporteDiario_Asistencia.pdf'; // Nombre de respaldo
    const disposition = response.headers['content-disposition'];
    
    if (disposition && disposition.includes('filename=')) {
      // Limpiamos el texto para sacar exactamente el nombre del archivo
      nombreArchivo = disposition.split('filename=')[1].replace(/["']/g, '');
    }

    // 2. Procesamos la descarga
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    
    // Le asignamos el nombre correcto que extrajimos
    link.setAttribute('download', nombreArchivo); 
    
    document.body.appendChild(link);
    link.click();
    
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(url);

  } catch (error) {
    console.error("Error al descargar:", error);
    alert("Hubo un problema al descargar el comprobante. Revisa la consola.");
  }
};

// --- CERRAR SESIÓN ---
const cerrarSesion = () => {
  authStore.logout();
  router.push('/login');
};
</script>