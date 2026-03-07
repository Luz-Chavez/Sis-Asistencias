<template>
  <div class="min-h-screen bg-gray-100">

    <!-- NAV -->
    <nav class="bg-indigo-800 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-6">
            <h1 class="text-white font-bold text-xl hidden md:block">Panel del Encargado</h1>
            <div class="flex gap-2">
              <button
                @click="seccion = 'reportes'"
                :class="seccion === 'reportes' ? 'bg-indigo-900 text-white shadow-inner' : 'text-indigo-200 hover:bg-indigo-700 hover:text-white'"
                class="px-4 py-2 rounded-md text-sm font-medium transition">
                📝 Reportes
              </button>
              <button
                @click="seccion = 'usuarios'"
                :class="seccion === 'usuarios' ? 'bg-indigo-900 text-white shadow-inner' : 'text-indigo-200 hover:bg-indigo-700 hover:text-white'"
                class="px-4 py-2 rounded-md text-sm font-medium transition">
                👥 Mis Pasantes
              </button>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-indigo-200 text-sm hidden sm:block">
              {{ authStore.user?.nombres }} · <em class="font-mono text-xs">{{ authStore.user?.username }}</em>
            </span>
            <button @click="cerrarSesion"
              class="text-sm bg-indigo-700 text-white px-4 py-2 rounded-md hover:bg-indigo-900 transition shadow">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">

      <!-- ══════════════ REPORTES ══════════════ -->
      <template v-if="seccion === 'reportes'">
        <div class="bg-white rounded-lg shadow px-5 py-6 mb-6 border-l-4 border-indigo-600">
          <h2 class="text-2xl font-bold text-gray-800">Reportes Diarios</h2>
          <p class="text-gray-600 mt-1">Revisa y evalúa las actividades de los pasantes de tu carrera.</p>
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
                  <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="isLoadingReportes">
                  <td colspan="5" class="px-6 py-4 text-center text-gray-500">Cargando...</td>
                </tr>
                <tr v-else-if="reportes.length === 0">
                  <td colspan="5" class="px-6 py-4 text-center text-gray-500">No hay reportes por el momento.</td>
                </tr>
                <tr v-else v-for="reporte in reportes" :key="reporte.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 text-sm text-gray-900 font-medium">#{{ reporte.id }}</td>
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
                  <td class="px-6 py-4 text-center">
                    <button @click="abrirModalEvaluacion(reporte)"
                      class="text-indigo-600 hover:text-indigo-900 bg-indigo-50 px-3 py-1 rounded shadow-sm hover:shadow transition text-sm">
                      Revisar y Evaluar
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>

      <!-- ══════════════ USUARIOS ══════════════ -->
      <template v-if="seccion === 'usuarios'">
        <div class="flex flex-col md:flex-row justify-between items-center bg-white rounded-lg shadow
                    px-5 py-6 mb-6 border-l-4 border-indigo-600">
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Pasantes de mi Carrera</h2>
            <p class="text-gray-500 mt-1 text-sm">
              Carrera <strong>ID: {{ authStore.user?.carrera_id }}</strong> —
              {{ usuarios.length }} pasante{{ usuarios.length !== 1 ? 's' : '' }} registrado{{ usuarios.length !== 1 ? 's' : '' }}
            </p>
          </div>
          <button @click="abrirModalCrear"
            class="mt-4 md:mt-0 bg-indigo-600 text-white px-5 py-2 rounded shadow hover:bg-indigo-700 transition font-medium flex items-center gap-2">
            + Nuevo Pasante
          </button>
        </div>

        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pasante</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Username</th>
                  <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="isLoadingUsuarios">
                  <td colspan="5" class="px-6 py-4 text-center text-gray-400">Cargando...</td>
                </tr>
                <tr v-else-if="usuarios.length === 0">
                  <td colspan="5" class="px-6 py-4 text-center text-gray-400">No hay pasantes en tu carrera.</td>
                </tr>
                <tr v-else v-for="user in usuarios" :key="user.id"
                  :class="!user.estado ? 'opacity-50' : ''"
                  class="hover:bg-gray-50 transition">
                  <td class="px-6 py-4 text-sm text-gray-500">#{{ user.id }}</td>
                  <td class="px-6 py-4">
                    <div class="text-sm font-medium text-gray-900">{{ user.nombres }} {{ user.apellidos }}</div>
                    <div class="text-xs text-gray-400">{{ user.email }}</div>
                  </td>
                  <td class="px-6 py-4 text-sm font-mono text-indigo-700">{{ user.username }}</td>
                  <td class="px-6 py-4 text-center">
                    <span :class="user.estado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ user.estado ? 'ACTIVO' : 'INACTIVO' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-center">
                    <div class="flex items-center justify-center gap-2">

                      <!-- Ver -->
                      <button @click="abrirModalVer(user)" title="Ver detalles"
                        class="p-1.5 rounded-md text-gray-500 hover:bg-gray-100 hover:text-gray-800 transition">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7
                               -1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                        </svg>
                      </button>

                      <!-- Editar -->
                      <button @click="abrirModalEditar(user)" title="Editar"
                        class="p-1.5 rounded-md text-indigo-500 hover:bg-indigo-50 hover:text-indigo-800 transition">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5
                               m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>

                      <!-- Desactivar / Reactivar -->
                      <button
                        @click="confirmarCambioEstado(user)"
                        :title="user.estado ? 'Dar de baja' : 'Reactivar'"
                        :class="user.estado
                          ? 'text-red-400 hover:bg-red-50 hover:text-red-700'
                          : 'text-green-500 hover:bg-green-50 hover:text-green-700'"
                        class="p-1.5 rounded-md transition">
                        <!-- Icono baja -->
                        <svg v-if="user.estado" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                        </svg>
                        <!-- Icono reactivar -->
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                      </button>

                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>

    </main>

    <!-- ══════════════ MODAL: VER PASANTE ══════════════ -->
    <div v-if="showModalVer"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">

        <div class="bg-indigo-600 px-6 py-4 flex justify-between items-center">
          <h3 class="text-lg font-bold text-white">Datos del Pasante</h3>
          <button @click="showModalVer = false" class="text-white hover:text-gray-200 font-bold text-xl">&times;</button>
        </div>

        <div class="px-6 py-6 space-y-4" v-if="pasanteSeleccionado">

          <!-- Avatar inicial -->
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold text-xl">
              {{ pasanteSeleccionado.nombres?.[0] }}{{ pasanteSeleccionado.apellidos?.[0] }}
            </div>
            <div>
              <p class="font-bold text-gray-800 text-lg leading-tight">
                {{ pasanteSeleccionado.nombres }} {{ pasanteSeleccionado.apellidos }}
              </p>
              <span :class="pasanteSeleccionado.estado ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                class="text-xs font-semibold px-2 py-0.5 rounded-full">
                {{ pasanteSeleccionado.estado ? 'ACTIVO' : 'INACTIVO' }}
              </span>
            </div>
          </div>

          <hr class="border-gray-100" />

          <div class="grid grid-cols-2 gap-3 text-sm">
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-400 uppercase font-semibold mb-0.5">Username</p>
              <p class="font-mono text-indigo-700 font-bold">{{ pasanteSeleccionado.username }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-400 uppercase font-semibold mb-0.5">Carnet</p>
              <p class="font-medium text-gray-800">{{ pasanteSeleccionado.carnet_identidad || '—' }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-3 col-span-2">
              <p class="text-xs text-gray-400 uppercase font-semibold mb-0.5">Correo</p>
              <p class="font-medium text-gray-800">{{ pasanteSeleccionado.email }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-400 uppercase font-semibold mb-0.5">Carrera ID</p>
              <p class="font-medium text-gray-800">{{ pasanteSeleccionado.carrera_id || '—' }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-400 uppercase font-semibold mb-0.5">Rol</p>
              <p class="font-medium text-gray-800">{{ pasanteSeleccionado.rol }}</p>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 bg-gray-50 border-t flex justify-end gap-3">
          <button @click="abrirModalEditar(pasanteSeleccionado); showModalVer = false"
            class="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 transition font-medium">
            ✏️ Editar
          </button>
          <button @click="showModalVer = false"
            class="px-4 py-2 border border-gray-300 text-gray-700 text-sm rounded-md hover:bg-gray-100 transition">
            Cerrar
          </button>
        </div>
      </div>
    </div>

    <!-- ══════════════ MODAL: EDITAR PASANTE ══════════════ -->
    <div v-if="showModalEditar"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl my-8">

        <div class="bg-indigo-600 px-6 py-4 flex justify-between items-center rounded-t-2xl">
          <h3 class="text-lg font-bold text-white">
            Editar — {{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}
          </h3>
          <button @click="showModalEditar = false" class="text-white hover:text-gray-200 font-bold text-xl">&times;</button>
        </div>

        <form @submit.prevent="guardarEdicion" class="px-6 py-5 space-y-4">
          <p class="text-xs text-gray-400">Deja vacío cualquier campo que no desees modificar.</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-bold text-gray-700">Nombres</label>
              <input v-model="formEditar.nombres" type="text"
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm" />
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Apellidos</label>
              <input v-model="formEditar.apellidos" type="text"
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm" />
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Carnet de Identidad</label>
              <input v-model="formEditar.carnet_identidad" type="text"
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm" />
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Correo Electrónico</label>
              <input v-model="formEditar.email" type="email"
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm" />
            </div>
          </div>

          <div v-if="mensajeErrorEditar" class="text-red-600 bg-red-50 p-3 text-sm rounded-lg border border-red-200">
            {{ mensajeErrorEditar }}
          </div>

          <div class="flex justify-end gap-3 border-t pt-4">
            <button type="button" @click="showModalEditar = false"
              class="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 text-sm">Cancelar</button>
            <button type="submit" :disabled="isSubmittingEditar"
              class="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 text-sm font-medium">
              {{ isSubmittingEditar ? 'Guardando...' : '💾 Guardar Cambios' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ══════════════ MODAL: CONFIRMAR BAJA ══════════════ -->
    <div v-if="showModalBaja"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden">

        <div :class="pasanteSeleccionado?.estado ? 'bg-red-600' : 'bg-green-600'"
          class="px-6 py-4 flex justify-between items-center">
          <h3 class="text-lg font-bold text-white">
            {{ pasanteSeleccionado?.estado ? 'Dar de Baja' : 'Reactivar Pasante' }}
          </h3>
          <button @click="showModalBaja = false" class="text-white hover:text-gray-200 font-bold text-xl">&times;</button>
        </div>

        <div class="px-6 py-6 text-center">
          <div :class="pasanteSeleccionado?.estado ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'"
            class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
            {{ pasanteSeleccionado?.estado ? '⚠️' : '✅' }}
          </div>
          <p class="text-gray-800 font-semibold text-base">
            {{ pasanteSeleccionado?.estado ? '¿Dar de baja a este pasante?' : '¿Reactivar a este pasante?' }}
          </p>
          <p class="text-gray-500 text-sm mt-2">
            <strong>{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</strong>
            <br />
            <span v-if="pasanteSeleccionado?.estado">
              Su cuenta quedará inactiva y no podrá fichar ni acceder al sistema.
            </span>
            <span v-else>
              Su cuenta volverá a estar activa.
            </span>
          </p>
        </div>

        <div class="px-6 py-4 bg-gray-50 border-t flex justify-center gap-3">
          <button @click="showModalBaja = false"
            class="px-4 py-2 border border-gray-300 text-gray-700 text-sm rounded-lg hover:bg-gray-100 transition">
            Cancelar
          </button>
          <button @click="ejecutarCambioEstado" :disabled="isSubmittingBaja"
            :class="pasanteSeleccionado?.estado
              ? 'bg-red-600 hover:bg-red-700'
              : 'bg-green-600 hover:bg-green-700'"
            class="px-5 py-2 text-white text-sm rounded-lg font-medium disabled:opacity-50 transition">
            {{ isSubmittingBaja ? 'Procesando...' : (pasanteSeleccionado?.estado ? 'Sí, dar de baja' : 'Sí, reactivar') }}
          </button>
        </div>
      </div>
    </div>

    <!-- ══════════════ MODAL: EVALUAR REPORTE ══════════════ -->
    <div v-if="showModalEvaluacion"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 px-4 backdrop-blur-sm">
      <div class="relative bg-white rounded-lg shadow-2xl w-full max-w-lg overflow-hidden">
        <div class="bg-indigo-600 px-6 py-4 flex justify-between items-center">
          <h3 class="text-lg font-bold text-white">Evaluación del Reporte #{{ reporteSeleccionado?.id }}</h3>
          <button @click="cerrarModalEvaluacion" class="text-white hover:text-gray-200 font-bold text-xl">&times;</button>
        </div>
        <div class="px-6 py-5">
          <p class="text-sm font-bold text-gray-700 mb-2">Actividades Reportadas:</p>
          <div class="bg-indigo-50 p-3 rounded border border-indigo-100 text-sm text-gray-800 mb-5 whitespace-pre-wrap shadow-inner">
            {{ reporteSeleccionado?.actividades_realizadas }}
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-1">Decisión</label>
              <select v-model="evaluacion.estado"
                class="w-full border border-gray-300 rounded-md shadow-sm py-2.5 px-3 bg-white cursor-pointer focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                <option value="APROBADO">✅ Aprobar Reporte</option>
                <option value="RECHAZADO">❌ Rechazar Reporte</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-1">Comentarios (Opcional)</label>
              <textarea v-model="evaluacion.comentarios" rows="3"
                class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Retroalimentación para el pasante..."></textarea>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-6 py-4 flex justify-end gap-3 border-t">
          <button @click="cerrarModalEvaluacion"
            class="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">Cancelar</button>
          <button @click="enviarEvaluacion" :disabled="isSubmittingEval"
            class="px-4 py-2 bg-indigo-600 rounded-md text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50">
            {{ isSubmittingEval ? 'Guardando...' : 'Guardar Evaluación' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ══════════════ MODAL: CREAR PASANTE ══════════════ -->
    <div v-if="showModalCrear"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl my-8">
        <div class="bg-indigo-600 px-6 py-4 flex justify-between items-center rounded-t-2xl">
          <h3 class="text-lg font-bold text-white">Registrar Nuevo Pasante</h3>
          <button @click="showModalCrear = false" class="text-white hover:text-gray-200 font-bold text-xl">&times;</button>
        </div>

        <div v-if="usernamePreview" class="mx-6 mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200 text-sm text-blue-800">
          🔑 Username que se generará: <strong class="font-mono">{{ usernamePreview }}</strong>
        </div>
        <div class="mx-6 mt-3 p-3 bg-amber-50 rounded-lg border border-amber-200 text-sm text-amber-800">
          ⚠️ El pasante será asignado a tu carrera <strong>(ID: {{ authStore.user?.carrera_id }})</strong>.
        </div>

        <form @submit.prevent="registrarPasante" class="px-6 py-5 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-bold text-gray-700">Nombres</label>
              <input v-model="formulario.nombres" type="text" required
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm" />
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Apellidos</label>
              <input v-model="formulario.apellidos" type="text" required
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm" />
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Carnet de Identidad</label>
              <input v-model="formulario.carnet_identidad" type="text" required
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm" />
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Correo Electrónico</label>
              <input v-model="formulario.email" type="email" required
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm" />
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Contraseña (Temporal)</label>
              <input v-model="formulario.password" type="password" required
                class="mt-1 w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-400 outline-none text-sm"
                placeholder="Mín. 6 caracteres" />
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700">Carrera</label>
              <input type="text" :value="'Tu carrera — ID ' + authStore.user?.carrera_id" disabled
                class="mt-1 w-full border border-gray-200 rounded-lg p-2.5 bg-gray-100 text-gray-500 cursor-not-allowed text-sm" />
            </div>
          </div>

          <div v-if="mensajeError" class="text-red-600 bg-red-50 p-3 text-sm rounded-lg border border-red-200">
            {{ mensajeError }}
          </div>

          <div class="flex justify-end gap-3 border-t pt-4">
            <button type="button" @click="showModalCrear = false"
              class="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 text-sm">Cancelar</button>
            <button type="submit" :disabled="isSubmittingCrear"
              class="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 text-sm font-medium">
              {{ isSubmittingCrear ? 'Guardando...' : 'Registrar Pasante' }}
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

// ── Sección activa ────────────────────────────────────────────────────────────
const seccion = ref('reportes')

// ── Reportes ──────────────────────────────────────────────────────────────────
const reportes            = ref([])
const isLoadingReportes   = ref(true)
const showModalEvaluacion = ref(false)
const reporteSeleccionado = ref(null)
const isSubmittingEval    = ref(false)
const evaluacion          = ref({ estado: 'APROBADO', comentarios: '' })

const estadoClass = (estado) => {
  if (estado === 'APROBADO')  return 'bg-green-100 text-green-800'
  if (estado === 'RECHAZADO') return 'bg-red-100 text-red-800'
  return 'bg-yellow-100 text-yellow-800'
}

const cargarReportes = async () => {
  isLoadingReportes.value = true
  try {
    const { data } = await api.get('/reportes/listar')
    reportes.value = data
  } catch (e) {
    if (e.response?.status === 401) cerrarSesion()
  } finally {
    isLoadingReportes.value = false
  }
}

const abrirModalEvaluacion = (reporte) => {
  reporteSeleccionado.value    = reporte
  evaluacion.value.estado      = reporte.estado && reporte.estado !== 'PENDIENTE' ? reporte.estado : 'APROBADO'
  evaluacion.value.comentarios = reporte.comentarios_director || ''
  showModalEvaluacion.value    = true
}
const cerrarModalEvaluacion = () => {
  showModalEvaluacion.value = false
  reporteSeleccionado.value = null
}
const enviarEvaluacion = async () => {
  isSubmittingEval.value = true
  try {
    await api.put(`/reportes/evaluar/${reporteSeleccionado.value.id}`, {
      estado: evaluacion.value.estado,
      comentarios_director: evaluacion.value.comentarios
    })
    await cargarReportes()
    cerrarModalEvaluacion()
    alert('¡Evaluación guardada con éxito!')
  } catch { alert('Error al guardar la evaluación.') }
  finally { isSubmittingEval.value = false }
}

// ── Usuarios ──────────────────────────────────────────────────────────────────
const usuarios          = ref([])
const isLoadingUsuarios = ref(false)
const pasanteSeleccionado = ref(null)

// Ver
const showModalVer = ref(false)
const abrirModalVer = (user) => {
  pasanteSeleccionado.value = user
  showModalVer.value = true
}

// Editar
const showModalEditar     = ref(false)
const isSubmittingEditar  = ref(false)
const mensajeErrorEditar  = ref('')
const formEditar = ref({ nombres: '', apellidos: '', carnet_identidad: '', email: '' })

const abrirModalEditar = (user) => {
  pasanteSeleccionado.value = user
  formEditar.value = {
    nombres:          user.nombres,
    apellidos:        user.apellidos,
    carnet_identidad: user.carnet_identidad || '',
    email:            user.email,
  }
  mensajeErrorEditar.value = ''
  showModalEditar.value = true
}

const guardarEdicion = async () => {
  isSubmittingEditar.value = true
  mensajeErrorEditar.value = ''
  try {
    // Enviamos solo los campos no vacíos
    const payload = {}
    Object.entries(formEditar.value).forEach(([k, v]) => {
      if (v && v.toString().trim() !== '') payload[k] = v
    })
    await api.put(`/usuarios/editar/${pasanteSeleccionado.value.id}`, payload)
    await cargarUsuarios()
    showModalEditar.value = false
    alert('¡Datos actualizados correctamente!')
  } catch (e) {
    mensajeErrorEditar.value = e.response?.data?.detail || 'Error al guardar los cambios.'
  } finally {
    isSubmittingEditar.value = false
  }
}

// Baja / Reactivar
const showModalBaja    = ref(false)
const isSubmittingBaja = ref(false)

const confirmarCambioEstado = (user) => {
  pasanteSeleccionado.value = user
  showModalBaja.value = true
}

const ejecutarCambioEstado = async () => {
  isSubmittingBaja.value = true
  try {
    if (pasanteSeleccionado.value.estado) {
      // Dar de baja → DELETE /desactivar
      await api.delete(`/usuarios/desactivar/${pasanteSeleccionado.value.id}`)
    } else {
      // Reactivar → PUT /editar con estado: true
      await api.put(`/usuarios/editar/${pasanteSeleccionado.value.id}`, { estado: true })
    }
    await cargarUsuarios()
    showModalBaja.value = false
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al cambiar el estado.')
  } finally {
    isSubmittingBaja.value = false
  }
}

// Crear
const showModalCrear    = ref(false)
const isSubmittingCrear = ref(false)
const mensajeError      = ref('')
const formulario = ref({
  nombres: '', apellidos: '', carnet_identidad: '',
  email: '', password: '', rol_id: 3, carrera_id: null
})

const usernamePreview = computed(() => {
  const n  = formulario.value.nombres?.trim()
  const a  = formulario.value.apellidos?.trim()
  const ci = formulario.value.carnet_identidad?.trim()
  if (!n || !a || !ci) return ''
  return `${n[0].toLowerCase()}${a[0].toLowerCase()}${ci}`
})

const abrirModalCrear = () => {
  formulario.value = {
    nombres: '', apellidos: '', carnet_identidad: '',
    email: '', password: '', rol_id: 3,
    carrera_id: authStore.user?.carrera_id
  }
  mensajeError.value = ''
  showModalCrear.value = true
}

const registrarPasante = async () => {
  isSubmittingCrear.value = true
  mensajeError.value = ''
  try {
    await api.post('/usuarios/registro', {
      ...formulario.value,
      rol_id:     3,
      carrera_id: authStore.user?.carrera_id
    })
    alert('¡Pasante registrado exitosamente!')
    showModalCrear.value = false
    await cargarUsuarios()
  } catch (e) {
    mensajeError.value = e.response?.data?.detail || 'Error al registrar el pasante.'
  } finally {
    isSubmittingCrear.value = false
  }
}

const cargarUsuarios = async () => {
  isLoadingUsuarios.value = true
  try {
    const { data } = await api.get('/usuarios/listar')
    usuarios.value = data
  } catch (e) {
    console.error('Error al cargar usuarios:', e)
  } finally {
    isLoadingUsuarios.value = false
  }
}

// ── Sesión ────────────────────────────────────────────────────────────────────
const cerrarSesion = () => {
  authStore.logout()
  router.push('/')
}

onMounted(async () => {
  await Promise.all([cargarReportes(), cargarUsuarios()])
})
</script>