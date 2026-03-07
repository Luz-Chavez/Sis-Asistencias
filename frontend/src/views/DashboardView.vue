<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-blue-600 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex-shrink-0 flex items-center">
            <h1 class="text-white font-bold text-xl">Sistema de Asistencia</h1>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-blue-100 text-sm hidden md:block">
              Hola, {{ authStore.user?.nombres }}
            </span>
            <button 
              @click="cerrarSesion" 
              class="text-sm bg-blue-700 text-white px-4 py-2 rounded-md hover:bg-blue-800 transition-colors shadow"
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
            <p class="text-sm text-gray-500 text-center mb-4">Activa tu ubicación para registrar tu llegada a la institución.</p>
            <div class="flex flex-col gap-3">
              <button @click="marcarConGPSReal" :disabled="isLoadingEntrada || asistenciaActualId" class="w-full flex justify-center items-center bg-gray-800 text-white py-3 px-4 rounded shadow hover:bg-gray-900 disabled:opacity-50 transition font-medium">
                <span v-if="isLoadingEntrada">Procesando...</span>
                <span v-else-if="asistenciaActualId">✅ Entrada Registrada</span>
                <span v-else>📍 Usar mi GPS Real para Entrar</span>
              </button>
            </div>
          </div>
          <div v-if="mensajeEntrada" :class="[tipoMensajeEntrada, 'mt-4 p-3 rounded text-sm font-medium text-center border']">
            {{ mensajeEntrada }}
          </div>
        </div>

        <div :class="['bg-white rounded-lg shadow px-5 py-6 sm:px-6 border-t-4 border-red-500 flex flex-col justify-between transition-opacity', !asistenciaActualId ? 'opacity-50 grayscale' : '']">
          <div>
            <h3 class="text-lg font-bold text-gray-900 mb-4 text-center">2. Registro de Salida</h3>
            <p class="text-sm text-gray-500 text-center mb-4">Marca tu salida al finalizar tu jornada para calcular tus horas.</p>
            <button @click="marcarSalida" :disabled="isLoadingSalida || !asistenciaActualId" class="w-full flex justify-center items-center bg-red-600 text-white py-3 px-4 rounded shadow hover:bg-red-700 disabled:opacity-50 transition font-medium">
              <span v-if="isLoadingSalida">Procesando...</span>
              <span v-else>👋 Marcar Salida con GPS</span>
            </button>
          </div>
          <div v-if="mensajeSalida" class="mt-4 p-3 rounded text-sm font-medium text-center border bg-blue-50 text-blue-800 border-blue-200">
            {{ mensajeSalida }}
          </div>
        </div>

      </div>

      <div :class="['bg-white rounded-lg shadow px-5 py-6 sm:px-6 border-t-4 border-purple-500 transition-opacity', !asistenciaActualId ? 'opacity-50 grayscale pointer-events-none' : '']">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-gray-900">3. Reporte de Actividades</h3>
          
          <span v-if="estadoReporte" :class="[
            estadoReporte === 'APROBADO' ? 'bg-green-100 text-green-800 border-green-200' : '',
            estadoReporte === 'RECHAZADO' ? 'bg-red-100 text-red-800 border-red-200' : '',
            estadoReporte === 'PENDIENTE' ? 'bg-yellow-100 text-yellow-800 border-yellow-200' : '',
            'px-3 py-1 rounded-full text-xs font-bold border uppercase tracking-wide'
          ]">
            {{ estadoReporte }}
          </span>
        </div>

        <div v-if="!asistenciaActualId" class="mb-4 text-sm text-purple-600 font-medium bg-purple-50 p-3 rounded border border-purple-100">
          ⚠️ Debes registrar tu entrada primero para habilitar el reporte de hoy.
        </div>

        <div v-if="comentariosDirector" class="mb-4 p-4 rounded-md border-l-4" :class="estadoReporte === 'APROBADO' ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'">
          <p class="text-sm font-bold text-gray-800 mb-1">👨‍💼 Comentario del Director:</p>
          <p class="text-sm text-gray-700 italic">"{{ comentariosDirector }}"</p>
        </div>
        
        <form @submit.prevent="subirReporte" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">¿Qué actividades realizaste hoy?</label>
            <textarea 
              v-model="actividades" 
              rows="4" 
              required
              :disabled="estadoReporte === 'APROBADO' || !asistenciaActualId"
              :class="estadoReporte === 'APROBADO' ? 'bg-gray-100 cursor-not-allowed text-gray-600' : 'bg-white text-gray-900'"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 transition-colors"
              placeholder="Ej. Hoy realicé el mantenimiento de la base de datos..."
            ></textarea>
          </div>
          
          <button v-if="estadoReporte !== 'APROBADO'" type="submit" :disabled="isLoadingReporte || !actividades || !asistenciaActualId" class="w-full md:w-auto px-6 py-2 bg-purple-600 text-white rounded-md shadow hover:bg-purple-700 disabled:opacity-50 transition font-medium">
            <span v-if="isLoadingReporte">Guardando...</span>
            <span v-else>📝 Guardar / Actualizar Reporte</span>
          </button>
          
          <div v-if="mensajeReporte && estadoReporte !== 'APROBADO'" :class="[tipoMensajeReporte, 'mt-4 p-3 rounded text-sm font-medium border']">
            {{ mensajeReporte }}
          </div>

          <div v-if="estadoReporte" class="mt-4 flex justify-center md:justify-start">
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
import { ref, onMounted } from 'vue';
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

const estadoReporte = ref('');
const comentariosDirector = ref('');

// ID DINÁMICO: Lo recuperamos de LocalStorage si el usuario recarga la página
const asistenciaActualId = ref(localStorage.getItem('asistencia_actual') || null);

// --- CARGAR DATOS AL ENTRAR A LA PANTALLA ---
onMounted(async () => {
  // Si tenemos un ID de asistencia guardado de hoy, buscamos si ya tiene reporte
  if (asistenciaActualId.value) {
    try {
      const response = await api.get(`/reportes/ver/${asistenciaActualId.value}`);
      actividades.value = response.data.actividades_realizadas;
      estadoReporte.value = response.data.estado || 'PENDIENTE';
      comentariosDirector.value = response.data.comentarios_director || '';
    } catch (error) {
      console.log("No hay reporte para hoy todavía.");
    }
  }
});

// --- FUNCIONES DE ENTRADA ---
const enviarAsistencia = async (lat, lon) => {
  isLoadingEntrada.value = true;
  mensajeEntrada.value = '';
  try {
    // USAMOS EL ID REAL DEL USUARIO LOGUEADO
    const payload = { pasante_id: authStore.user?.id, latitud_entrada: lat, longitud_entrada: lon };
    const response = await api.post('/asistencias/entrada', payload);
    
    // CAPTURAMOS EL ID QUE NOS DEVUELVE EL BACKEND PARA ESTA ASISTENCIA
    // Dependiendo de cómo lo devuelva tu backend (response.data.id o response.data.asistencia.id)
    const nuevoId = response.data.id || response.data.asistencia?.id;
    
    if (nuevoId) {
      asistenciaActualId.value = nuevoId;
      localStorage.setItem('asistencia_actual', nuevoId); // Lo guardamos por si refresca la página
    }

    tipoMensajeEntrada.value = response.data.esta_en_facultad ? 'bg-green-100 text-green-800 border-green-400' : 'bg-yellow-100 text-yellow-800 border-yellow-400';
    mensajeEntrada.value = response.data.mensaje_alerta || 'Entrada registrada exitosamente.';

  } catch (error) {
    tipoMensajeEntrada.value = 'bg-red-100 text-red-800 border-red-400';
    if (error.response && error.response.status === 401) {
      alert("Tu sesión ha expirado por seguridad.");
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
      mensajeEntrada.value = 'No pudimos acceder a tu GPS. Verifica los permisos de tu navegador.';
    }
  );
};

// --- FUNCIÓN DE SALIDA ---
const marcarSalida = async () => {
  if (!asistenciaActualId.value) return;
  
  // Obtenemos el GPS para la salida
  navigator.geolocation.getCurrentPosition(async (position) => {
    isLoadingSalida.value = true;
    mensajeSalida.value = '';
    try {
      const payload = { latitud_salida: position.coords.latitude, longitud_salida: position.coords.longitude };
      const response = await api.put(`/asistencias/salida/${asistenciaActualId.value}`, payload);
      mensajeSalida.value = `¡Salida registrada! Has trabajado ${response.data.horas_trabajadas} horas hoy.`;
      
      // Opcional: Limpiamos el localStorage si la jornada terminó totalmente
      // localStorage.removeItem('asistencia_actual');
      
    } catch (error) {
      mensajeSalida.value = 'Error al registrar la salida o ya fue marcada.';
    } finally {
      isLoadingSalida.value = false;
    }
  });
};

// --- FUNCIÓN DE REPORTE ---
const subirReporte = async () => {
  if (!asistenciaActualId.value) return;
  
  isLoadingReporte.value = true;
  mensajeReporte.value = '';
  try {
    const payload = { asistencia_id: asistenciaActualId.value, actividades_realizadas: actividades.value, archivo_adjunto_url: "" };
    await api.post('/reportes/subir', payload);
    tipoMensajeReporte.value = 'bg-green-100 text-green-800 border-green-400';
    mensajeReporte.value = '¡Reporte guardado exitosamente!';
    estadoReporte.value = 'PENDIENTE';
  } catch (error) {
    tipoMensajeReporte.value = 'bg-red-100 text-red-800 border-red-400';
    mensajeReporte.value = error.response?.data?.detail || 'Error al procesar el reporte.';
  } finally {
    isLoadingReporte.value = false;
  }
};

// --- FUNCIÓN PARA DESCARGAR EL PDF ---
const descargarPDF = async () => {
  if (!asistenciaActualId.value) return;

  try {
    const response = await api.get(`/reportes/descargar/${asistenciaActualId.value}`, { responseType: 'blob' });
    let nombreArchivo = 'ReporteDiario_Asistencia.pdf';
    const disposition = response.headers['content-disposition'];
    if (disposition && disposition.includes('filename=')) {
      nombreArchivo = disposition.split('filename=')[1].replace(/["']/g, '');
    }
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
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
  localStorage.removeItem('asistencia_actual'); // Limpiamos la memoria del día
  router.push('/');
};
</script>