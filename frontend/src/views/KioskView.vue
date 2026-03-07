<template>
  <div class="kiosk">

    <!-- FONDO INSTITUCIONAL -->
    <div class="kiosk-bg">
      <div class="bg-shape shape-1"></div>
      <div class="bg-shape shape-2"></div>
    </div>

    <!-- CABECERA INSTITUCIONAL -->
    <header class="kiosk-header">
      <div class="header-inner">
        <div class="institution-info">
          <span class="institution-name">Facultad de Ciencias Sociales · UMSA</span>
        </div>
        <!-- Botón Login esquina superior derecha -->
        <button @click="irAlLogin" class="login-corner-btn">
          Iniciar sesión
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/>
          </svg>
        </button>
      </div>
    </header>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="kiosk-main">

      <!-- PANEL CENTRAL -->
      <div class="kiosk-card">

        <!-- RELOJ -->
        <div class="clock-section">
          <div class="clock-time">{{ horaActual }}</div>
          <div class="clock-date">{{ fechaActual }}</div>
        </div>

        <div class="divider"></div>

        <!-- RESULTADO (se muestra después de registrar) -->
        <transition name="slide-up">
          <div v-if="resultado" :class="['result-box', resultado.tipo]">
            <div class="result-icon">{{ resultado.tipo === 'entrada' ? '✅' : '👋' }}</div>
            <div class="result-name">{{ resultado.nombre }}</div>
            <div class="result-label">{{ resultado.tipo === 'entrada' ? 'ENTRADA REGISTRADA' : 'SALIDA REGISTRADA' }}</div>
            <div class="result-hours" v-if="resultado.horas">
              Horas trabajadas hoy: <strong>{{ resultado.horas }}h</strong>
            </div>
          </div>
        </transition>

        <!-- FORMULARIO -->
        <div v-if="!resultado" class="form-section">

          <!-- SELECTOR ENTRADA / SALIDA -->
          <div class="tipo-selector">
            <button
              @click="tipoRegistro = 'entrada'"
              :class="['tipo-btn', tipoRegistro === 'entrada' ? 'tipo-active-entrada' : 'tipo-inactive']"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/>
              </svg>
              Entrada
            </button>
            <button
              @click="tipoRegistro = 'salida'"
              :class="['tipo-btn', tipoRegistro === 'salida' ? 'tipo-active-salida' : 'tipo-inactive']"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
              </svg>
              Salida
            </button>
          </div>

          <!-- INPUT USUARIO -->
          <div class="input-section">
            <label class="input-label">Ingresa tu carnet de identidad o correo</label>
            <div class="input-wrap">
              <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
              <input
                ref="inputRef"
                v-model="carnet_identidad"
                @keyup.enter="registrar"
                type="text"
                class="kiosk-input"
                :placeholder="tipoRegistro === 'entrada' ? 'Ej. 9876543' : 'Ej. 9876543'"
                autocomplete="off"
              >
            </div>
          </div>

          <!-- ERROR -->
          <transition name="fade">
            <div v-if="error" class="error-msg">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ error }}
            </div>
          </transition>

          <!-- BOTÓN ACEPTAR -->
          <button
            @click="registrar"
            :disabled="!carnet_identidad.trim() || isLoading"
            :class="['accept-btn', tipoRegistro === 'entrada' ? 'accept-entrada' : 'accept-salida']"
          >
            <span v-if="isLoading" class="btn-spinner"></span>
            <span v-else>
              {{ tipoRegistro === 'entrada' ? 'Registrar Entrada' : 'Registrar Salida' }}
            </span>
          </button>

        </div>

        <!-- BOTÓN NUEVO REGISTRO (después del resultado) -->
        <div v-if="resultado" class="new-register">
          <button @click="reiniciar" class="new-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 109-9 9.75 9.75 0 00-6.74 2.74L3 8"/><path d="M3 3v5h5"/>
            </svg>
            Nuevo registro
          </button>
        </div>

      </div><!-- /kiosk-card -->

    </main>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const router = useRouter();

// ---- RELOJ ----
const horaActual = ref('');
const fechaActual = ref('');
let clockInterval = null;

const actualizarReloj = () => {
  const ahora = new Date();
  horaActual.value = ahora.toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
  fechaActual.value = ahora.toLocaleDateString('es-BO', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
};

// ---- ESTADO ----
const tipoRegistro = ref('entrada');
const carnet_identidad = ref('');
const isLoading = ref(false);
const error = ref('');
const resultado = ref(null);
const inputRef = ref(null);

let autoResetTimer = null;

// ---- FUNCIONES ----
const registrar = async () => {
  if (!carnet_identidad.value.trim() || isLoading.value) return;
  isLoading.value = true;
  error.value = '';

  try {
    // 1. Buscar al usuario por carnet/email
    const resUsuarios = await api.get('/usuarios/listar');
    const todos = resUsuarios.data;
    const pasante = todos.find(u =>
      u.carnet_identidad === carnet_identidad.value.trim() ||
      u.email === carnet_identidad.value.trim()
    );

    if (!pasante) {
      error.value = 'No se encontró ningún pasante con ese carnet o correo.';
      isLoading.value = false;
      return;
    }

    // 2. Obtener ubicación GPS
    const coords = await obtenerGPS();

    if (tipoRegistro.value === 'entrada') {
      const payload = {
        pasante_id: pasante.id,
        latitud_entrada: coords.lat,
        longitud_entrada: coords.lon
      };
      const res = await api.post('/asistencias/entrada', payload);

      resultado.value = {
        tipo: 'entrada',
        nombre: `${pasante.nombres} ${pasante.apellidos}`,
        asistenciaId: res.data.id,
        horas: null
      };

    } else {
      // Para salida: buscar la asistencia activa de hoy
      const resAsistencias = await api.get(`/asistencias/pasante/${pasante.id}`);
      const hoy = new Date().toISOString().split('T')[0];
      const asistenciaHoy = resAsistencias.data.find(a =>
        a.fecha?.startsWith(hoy) && !a.hora_salida
      );

      if (!asistenciaHoy) {
        error.value = 'No se encontró una entrada activa para hoy.';
        isLoading.value = false;
        return;
      }

      const payload = {
        latitud_salida: coords.lat,
        longitud_salida: coords.lon
      };
      const res = await api.put(`/asistencias/salida/${asistenciaHoy.id}`, payload);

      resultado.value = {
        tipo: 'salida',
        nombre: `${pasante.nombres} ${pasante.apellidos}`,
        horas: res.data.horas_trabajadas
      };
    }

    // Auto-reset después de 5 segundos
    autoResetTimer = setTimeout(() => reiniciar(), 5000);

  } catch (e) {
    if (e.response?.status === 400) {
      error.value = tipoRegistro.value === 'entrada'
        ? 'Ya tienes una entrada registrada para hoy.'
        : 'La salida ya fue registrada anteriormente.';
    } else if (e.code === 'GPS_DENIED') {
      error.value = 'Se requiere acceso a la ubicación GPS para registrar asistencia.';
    } else {
      error.value = e.response?.data?.detail || 'Error al conectar con el servidor.';
    }
  } finally {
    isLoading.value = false;
  }
};

const obtenerGPS = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      // Si no hay GPS disponible, usamos coordenadas por defecto (la facultad)
      resolve({ lat: -16.5000, lon: -68.1193 });
      return;
    }
    navigator.geolocation.getCurrentPosition(
      pos => resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
      () => resolve({ lat: -16.5000, lon: -68.1193 }) // fallback silencioso
    );
  });
};

const reiniciar = () => {
  clearTimeout(autoResetTimer);
  resultado.value = null;
  carnet_identidad.value = '';
  error.value = '';
  nextTick(() => inputRef.value?.focus());
};

const irAlLogin = () => {
  router.push('/login');
};

// ---- LIFECYCLE ----
onMounted(() => {
  actualizarReloj();
  clockInterval = setInterval(actualizarReloj, 1000);
  nextTick(() => inputRef.value?.focus());
});

onUnmounted(() => {
  clearInterval(clockInterval);
  clearTimeout(autoResetTimer);
});
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ===== FONDO ===== */
.kiosk {
  min-height: 100vh;
  background: #f0f2f5;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.kiosk-bg { position: absolute; inset: 0; pointer-events: none; z-index: 0; }
.bg-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.07;
}
.shape-1 {
  width: 600px; height: 600px;
  background: #4338ca;
  top: -200px; right: -150px;
}
.shape-2 {
  width: 400px; height: 400px;
  background: #4338ca;
  bottom: -150px; left: -100px;
}

/* ===== HEADER ===== */
.kiosk-header {
  position: relative; z-index: 10;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.header-inner {
  max-width: 900px; margin: 0 auto;
  padding: 0 28px;
  height: 58px;
  display: flex; align-items: center; justify-content: space-between;
}
.institution-name {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  letter-spacing: 0.01em;
}
.login-corner-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 7px 14px;
  background: none;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  color: #6b7280;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.login-corner-btn:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
  color: #374151;
}

/* ===== MAIN ===== */
.kiosk-main {
  position: relative; z-index: 10;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 20px;
}

/* ===== CARD ===== */
.kiosk-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 480px;
  padding: 36px 40px;
}

/* ===== RELOJ ===== */
.clock-section {
  text-align: center;
  margin-bottom: 28px;
}
.clock-time {
  font-size: 72px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -2px;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.clock-date {
  font-size: 14px;
  color: #9ca3af;
  margin-top: 8px;
  text-transform: capitalize;
}

.divider {
  height: 1px;
  background: #f3f4f6;
  margin-bottom: 28px;
}

/* ===== TIPO SELECTOR ===== */
.tipo-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 24px;
}
.tipo-btn {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px;
  border-radius: 12px;
  border: 2px solid transparent;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.18s;
}
.tipo-inactive {
  background: #f9fafb;
  border-color: #e5e7eb;
  color: #9ca3af;
}
.tipo-inactive:hover {
  background: #f3f4f6;
  color: #6b7280;
}
.tipo-active-entrada {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #1d4ed8;
}
.tipo-active-salida {
  background: #f0fdf4;
  border-color: #22c55e;
  color: #15803d;
}

/* ===== INPUT ===== */
.input-section {
  margin-bottom: 20px;
}
.input-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.input-wrap {
  position: relative;
}
.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
}
.kiosk-input {
  width: 100%;
  padding: 14px 14px 14px 46px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 16px;
  color: #111827;
  background: #fff;
  outline: none;
  transition: border 0.15s, box-shadow 0.15s;
}
.kiosk-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 4px rgba(79,70,229,0.08);
}
.kiosk-input::placeholder { color: #d1d5db; }

/* ===== ERROR ===== */
.error-msg {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 14px;
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #dc2626;
  font-size: 13px;
  margin-bottom: 16px;
}

/* ===== BOTÓN ACEPTAR ===== */
.accept-btn {
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  letter-spacing: 0.02em;
}
.accept-btn:disabled { opacity: 0.45; cursor: not-allowed; }
.accept-entrada {
  background: #3b82f6;
  color: #fff;
  box-shadow: 0 4px 14px rgba(59,130,246,0.35);
}
.accept-entrada:not(:disabled):hover {
  background: #2563eb;
  box-shadow: 0 6px 20px rgba(59,130,246,0.45);
  transform: translateY(-1px);
}
.accept-salida {
  background: #22c55e;
  color: #fff;
  box-shadow: 0 4px 14px rgba(34,197,94,0.35);
}
.accept-salida:not(:disabled):hover {
  background: #16a34a;
  box-shadow: 0 6px 20px rgba(34,197,94,0.45);
  transform: translateY(-1px);
}

/* ===== SPINNER BOTÓN ===== */
.btn-spinner {
  width: 20px; height: 20px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ===== RESULTADO ===== */
.result-box {
  border-radius: 16px;
  padding: 28px 24px;
  text-align: center;
  margin-bottom: 24px;
}
.result-box.entrada {
  background: #eff6ff;
  border: 2px solid #93c5fd;
}
.result-box.salida {
  background: #f0fdf4;
  border: 2px solid #86efac;
}
.result-icon {
  font-size: 48px;
  margin-bottom: 12px;
  animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
@keyframes popIn {
  0% { transform: scale(0.5); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.result-name {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
}
.result-label {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.result-box.entrada .result-label { color: #2563eb; }
.result-box.salida .result-label { color: #16a34a; }
.result-hours {
  margin-top: 10px;
  font-size: 13px;
  color: #6b7280;
}
.result-hours strong { color: #111827; }

/* ===== NUEVO REGISTRO ===== */
.new-register {
  text-align: center;
}
.new-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 22px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  color: #374151;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.new-btn:hover {
  background: #e5e7eb;
  color: #111827;
}

/* ===== TRANSITIONS ===== */
.slide-up-enter-active { transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.slide-up-enter-from { opacity: 0; transform: translateY(20px) scale(0.97); }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ===== RESPONSIVE ===== */
@media (max-width: 520px) {
  .kiosk-card { padding: 28px 22px; }
  .clock-time { font-size: 56px; }
}
</style>