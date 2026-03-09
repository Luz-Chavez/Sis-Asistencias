<template>
  <div class="min-h-screen bg-slate-50 font-sans">
    
    <nav class="bg-slate-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-6">
            <h1 class="text-white font-bold text-xl hidden md:block tracking-wide">
              Panel de Administración
            </h1>
            <div class="flex gap-2">
              <button @click="router.push(esEncargado ? '/encargado' : '/admin')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all">
                <svg class="w-4 h-4 inline-block mr-1.5 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Todos los Reportes
              </button>
              <button class="bg-white/10 text-white px-4 py-2 rounded-lg text-sm font-bold cursor-default shadow-sm border border-white/5">
                <svg class="w-4 h-4 inline-block mr-1.5 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                Gestión de Usuarios
              </button>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-white text-sm font-medium">{{ authStore.user?.nombres }}</span>
              <span class="text-slate-400 text-xs">{{ authStore.user?.rol }}</span>
            </div>
            <button @click="cerrarSesion"
              class="text-sm bg-rose-600 hover:bg-rose-500 text-white px-4 py-2 rounded-lg transition-colors shadow-sm font-medium">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">

      <div class="mb-8">
        <h2 class="text-2xl font-bold text-slate-800 mb-2">Directorio del Sistema</h2>
        <p class="text-slate-500 text-sm mb-6">
          <span v-if="esEncargado">Gestiona las cuentas y accesos de los pasantes de tu carrera.</span>
          <span v-else>Administra todas las cuentas, roles y accesos a nivel de Facultad.</span>
        </p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div class="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            </div>
            <div>
              <p class="text-sm text-slate-500 font-medium">Usuarios Registrados</p>
              <p class="text-2xl font-bold text-slate-800">{{ usuarios.length }}</p>
            </div>
          </div>
          
          <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div class="p-3 bg-emerald-50 text-emerald-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
            </div>
            <div>
              <p class="text-sm text-slate-500 font-medium">Pasantes Activos</p>
              <p class="text-2xl font-bold text-slate-800">{{ totalPasantes }}</p>
            </div>
          </div>

          <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div class="p-3 bg-rose-50 text-rose-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg>
            </div>
            <div>
              <p class="text-sm text-slate-500 font-medium">Cuentas Inactivas</p>
              <p class="text-2xl font-bold text-slate-800">{{ totalInactivos }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-6 flex flex-col lg:flex-row justify-between items-center gap-4">
        
        <div class="flex flex-wrap gap-2 w-full lg:w-auto">
          <button @click="filtroRol = 'TODOS'" :class="filtroRol === 'TODOS' ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'" class="px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Todos
          </button>
          <button v-if="!esEncargado" @click="filtroRol = 'ADMINISTRADOR'" :class="filtroRol === 'ADMINISTRADOR' ? 'bg-indigo-100 text-indigo-800 border-indigo-200' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'" class="px-4 py-2 rounded-lg text-sm font-medium border border-transparent transition-colors">
            Administradores
          </button>
          <button v-if="!esEncargado" @click="filtroRol = 'ENCARGADO'" :class="filtroRol === 'ENCARGADO' ? 'bg-purple-100 text-purple-800 border-purple-200' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'" class="px-4 py-2 rounded-lg text-sm font-medium border border-transparent transition-colors">
            Encargados
          </button>
          <button @click="filtroRol = 'PASANTE'" :class="filtroRol === 'PASANTE' ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'" class="px-4 py-2 rounded-lg text-sm font-medium border border-transparent transition-colors">
            Pasantes
          </button>
        </div>

        <div class="flex flex-col sm:flex-row w-full lg:w-auto gap-3">
          <div class="relative w-full sm:w-64">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <input v-model="searchQuery" type="text" placeholder="Buscar usuario..."
              class="block w-full pl-10 pr-3 py-2.5 border border-slate-300 rounded-lg bg-slate-50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white sm:text-sm transition-colors" />
          </div>

          <button @click="abrirModalCrear"
            class="w-full sm:w-auto text-white px-5 py-2.5 rounded-lg shadow-sm font-medium flex items-center justify-center gap-2 transition duration-200 hover:shadow"
            :class="esEncargado ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-slate-800 hover:bg-slate-900'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
            Nuevo {{ esEncargado ? 'Pasante' : 'Usuario' }}
          </button>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50/80">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Usuario</th>
                <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Username</th>
                <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Rol</th>
                <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">Carrera</th>
                <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-100">
              
              <tr v-if="isLoading">
                <td colspan="6" class="px-6 py-16 text-center">
                  <div class="flex flex-col items-center justify-center text-slate-400">
                    <svg class="animate-spin h-8 w-8 mb-4 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    <p class="font-medium text-slate-500">Cargando directorio...</p>
                  </div>
                </td>
              </tr>

              <tr v-else-if="filteredUsuarios.length === 0">
                <td colspan="6" class="px-6 py-16 text-center">
                  <div class="flex flex-col items-center justify-center text-slate-400">
                    <svg class="w-16 h-16 mb-4 text-slate-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                    <p class="font-medium text-slate-500 text-lg">No se encontraron usuarios</p>
                    <p class="text-sm mt-1">Verifica los filtros o el término de búsqueda.</p>
                  </div>
                </td>
              </tr>

              <tr v-else v-for="user in filteredUsuarios" :key="user.id" class="hover:bg-slate-50 transition-colors group">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-700 font-bold border border-indigo-200">
                      {{ obtenerIniciales(user.nombres, user.apellidos) }}
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-bold text-slate-800">{{ user.nombres }} {{ user.apellidos }}</div>
                      <div class="text-xs text-slate-500">{{ user.email }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="text-sm font-mono text-slate-600 bg-slate-100 px-2 py-1 rounded">{{ user.username }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="rolBadgeClass(user.rol)" class="px-3 py-1 inline-flex text-xs leading-none font-bold rounded-full uppercase tracking-wide border">
                    {{ user.rol || 'Sin rol' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium text-slate-600">
                  {{ user.carrera_id || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center">
                  <div class="flex items-center justify-center">
                    <span :class="user.estado ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-rose-50 text-rose-700 border-rose-200'" class="px-3 py-1.5 inline-flex items-center gap-1.5 text-xs font-bold rounded-full border">
                      <span class="w-1.5 h-1.5 rounded-full" :class="user.estado ? 'bg-emerald-500' : 'bg-rose-500'"></span>
                      {{ user.estado ? 'ACTIVO' : 'INACTIVO' }}
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center">
                  <div class="flex justify-center gap-2 opacity-100 sm:opacity-70 group-hover:opacity-100 transition-opacity">
                    <button @click="abrirModalEditar(user)" 
                            class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-md transition-all" 
                            title="Editar Información">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                    </button>
                    <button @click="confirmarCambioEstado(user)" 
                            class="p-1.5 rounded-md transition-all"
                            :class="user.estado ? 'text-slate-400 hover:text-rose-600 hover:bg-rose-50' : 'text-slate-400 hover:text-emerald-600 hover:bg-emerald-50'"
                            :title="user.estado ? 'Desactivar acceso' : 'Habilitar acceso'">
                      <svg v-if="user.estado" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg>
                      <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl my-8 border border-slate-200 overflow-hidden transform transition-all">

        <div class="px-6 py-4 flex justify-between items-center"
             :class="esEncargado ? 'bg-indigo-700' : 'bg-slate-800'">
          <h3 class="text-lg font-bold text-white tracking-wide flex items-center gap-2">
            <svg class="w-5 h-5 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            {{ isEditing ? 'Editar Información del Usuario' : (esEncargado ? 'Registrar Nuevo Pasante' : 'Registrar Nuevo Usuario') }}
          </h3>
          <button @click="cerrarModal" class="text-white/70 hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <div v-if="!isEditing && usernamePreview" class="mx-6 mt-5 p-3.5 bg-indigo-50 rounded-xl border border-indigo-100 text-sm text-indigo-800 flex items-center gap-3">
          <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path></svg>
          <span>Username sugerido: <strong class="font-mono text-indigo-700 text-base ml-1">{{ usernamePreview }}</strong></span>
        </div>

        <div v-if="esEncargado && !isEditing" class="mx-6 mt-3 p-3.5 bg-amber-50 rounded-xl border border-amber-200 text-sm text-amber-800 flex items-start gap-3">
          <svg class="w-5 h-5 text-amber-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <span>Como Encargado, solo puedes registrar <strong>Pasantes</strong> en tu carrera <strong>(ID: {{ authStore.user?.carrera_id }})</strong>.</span>
        </div>

        <form @submit.prevent="guardarUsuario" class="px-6 py-5 space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">

            <div>
              <label class="block text-sm font-bold text-slate-700 mb-1">Nombres</label>
              <input v-model="formulario.nombres" type="text" required
                class="w-full border border-slate-300 rounded-xl p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50 focus:bg-white" />
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-700 mb-1">Apellidos</label>
              <input v-model="formulario.apellidos" type="text" required
                class="w-full border border-slate-300 rounded-xl p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50 focus:bg-white" />
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-700 mb-1">Carnet de Identidad</label>
              <input v-model="formulario.carnet_identidad" type="text" required
                class="w-full border border-slate-300 rounded-xl p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50 focus:bg-white" />
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-700 mb-1">Correo Electrónico</label>
              <input v-model="formulario.email" type="email" required
                class="w-full border border-slate-300 rounded-xl p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50 focus:bg-white" />
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-700 mb-1">
                Contraseña <span v-if="isEditing" class="text-xs font-normal text-slate-500">(Vacío para no cambiar)</span>
              </label>
              <input v-model="formulario.password" type="password" :required="!isEditing"
                class="w-full border border-slate-300 rounded-xl p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-slate-50 focus:bg-white"
                placeholder="Mín. 6 caracteres" />
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-700 mb-1">Rol</label>
              <select v-if="!esEncargado" v-model="formulario.rol_id" required
                class="w-full border border-slate-300 rounded-xl p-2.5 bg-white focus:ring-2 focus:ring-indigo-500 outline-none transition">
                <option :value="idRol('ADMINISTRADOR')">Administrador</option>
                <option :value="idRol('ENCARGADO')">Encargado</option>
                <option :value="idRol('PASANTE')">Pasante</option>
              </select>
              <input v-else type="text" :value="isEditing ? formulario.rol_nombre : 'Pasante'" disabled
                class="w-full border border-slate-200 rounded-xl p-2.5 bg-slate-100 text-slate-500 cursor-not-allowed font-medium" />
            </div>

            <div v-if="!esEncargado || isEditing">
              <label class="block text-sm font-bold text-slate-700 mb-1">Carrera ID</label>
              <input v-if="!esEncargado" v-model="formulario.carrera_id" type="number"
                class="w-full border border-slate-300 rounded-xl p-2.5 focus:ring-2 focus:ring-indigo-500 outline-none transition bg-slate-50 focus:bg-white"
                placeholder="Opcional (Ej. 1)" />
              <input v-else type="text" :value="'ID Carrera: ' + (formulario.carrera_id || authStore.user?.carrera_id)" disabled
                class="w-full border border-slate-200 rounded-xl p-2.5 bg-slate-100 text-slate-500 cursor-not-allowed font-medium" />
            </div>

          </div>

          <div v-if="mensajeError" class="text-rose-700 bg-rose-50 p-3.5 text-sm rounded-xl border border-rose-200 font-medium flex items-center gap-2">
            <svg class="w-5 h-5 text-rose-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {{ mensajeError }}
          </div>

          <div class="flex justify-end gap-3 border-t border-slate-100 pt-5 mt-2">
            <button type="button" @click="cerrarModal"
              class="px-6 py-2.5 border border-slate-300 rounded-xl text-slate-700 font-medium hover:bg-slate-50 transition duration-200">Cancelar</button>
            <button type="submit" :disabled="isSubmitting"
              class="px-6 py-2.5 text-white rounded-xl font-medium disabled:opacity-50 transition duration-200 shadow-md"
              :class="esEncargado ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-slate-800 hover:bg-slate-900'">
              {{ isSubmitting ? 'Procesando...' : (isEditing ? 'Actualizar Usuario' : 'Guardar Usuario') }}
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
const searchQuery  = ref('')
const filtroRol    = ref('TODOS') // NUEVO: TODOS, ADMINISTRADOR, ENCARGADO, PASANTE
const isLoading    = ref(true)
const showModal    = ref(false)
const isEditing    = ref(false)
const idEditando   = ref(null)
const isSubmitting = ref(false)
const mensajeError = ref('')

const rolesMap = ref({ ADMINISTRADOR: 1, ENCARGADO: 2, PASANTE: 3 })
const idRol = (nombre) => rolesMap.value[nombre] ?? null

const esEncargado = computed(() => authStore.user?.rol === 'ENCARGADO')

const formulario = ref({
  nombres: '', apellidos: '', carnet_identidad: '',
  email: '', password: '', rol_id: 3, carrera_id: null, rol_nombre: ''
})

// ── KPIs Computados ──
const totalPasantes = computed(() => usuarios.value.filter(u => u.rol === 'PASANTE').length)
const totalInactivos = computed(() => usuarios.value.filter(u => !u.estado).length)

// ── Generar Iniciales para el Avatar ──
const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.charAt(0).toUpperCase() : ''
  const a = apellidos ? apellidos.charAt(0).toUpperCase() : ''
  return `${n}${a}`
}

const usernamePreview = computed(() => {
  const n  = formulario.value.nombres?.trim()
  const a  = formulario.value.apellidos?.trim()
  const ci = formulario.value.carnet_identidad?.trim()
  if (!n || !a || !ci) return ''
  return `${n[0].toLowerCase()}${a[0].toLowerCase()}${ci}`
})

// ── Filtrado Inteligente ──
const filteredUsuarios = computed(() => {
  let resultado = usuarios.value

  // Filtrar por Pestaña de Rol
  if (filtroRol.value !== 'TODOS') {
    resultado = resultado.filter(u => u.rol === filtroRol.value)
  }

  // Filtrar por Texto
  if (searchQuery.value) {
    const lower = searchQuery.value.toLowerCase()
    resultado = resultado.filter(u =>
      (u.nombres + ' ' + u.apellidos).toLowerCase().includes(lower) ||
      u.username.toLowerCase().includes(lower) ||
      u.email.toLowerCase().includes(lower) ||
      (u.rol || '').toLowerCase().includes(lower)
    )
  }

  return resultado
})

const rolBadgeClass = (rol) => {
  if (rol === 'ADMINISTRADOR') return 'bg-slate-800 text-slate-100 border-slate-700'
  if (rol === 'ENCARGADO')     return 'bg-purple-50 text-purple-700 border-purple-200'
  if (rol === 'PASANTE')       return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  return 'bg-slate-50 text-slate-700 border-slate-200'
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
  isEditing.value = false
  idEditando.value = null
  formulario.value = {
    nombres: '', apellidos: '', carnet_identidad: '',
    email: '', password: '',
    rol_id:     esEncargado.value ? idRol('PASANTE') : idRol('PASANTE'),
    carrera_id: esEncargado.value ? authStore.user?.carrera_id : null
  }
  mensajeError.value = ''
  showModal.value = true
}

const abrirModalEditar = (usuario) => {
  isEditing.value = true
  idEditando.value = usuario.id
  formulario.value = {
    nombres: usuario.nombres,
    apellidos: usuario.apellidos,
    carnet_identidad: usuario.carnet_identidad,
    email: usuario.email,
    password: '', 
    rol_id: idRol(usuario.rol) || idRol('PASANTE'),
    carrera_id: usuario.carrera_id,
    rol_nombre: usuario.rol 
  }
  mensajeError.value = ''
  showModal.value = true
}

const cerrarModal = () => { showModal.value = false }

const guardarUsuario = async () => {
  isSubmitting.value = true
  mensajeError.value = ''
  try {
    const datos = { ...formulario.value }
    delete datos.rol_nombre 

    if (isEditing.value && !datos.password) {
      delete datos.password
    }

    if (esEncargado.value && !isEditing.value) {
      datos.rol_id     = idRol('PASANTE')
      datos.carrera_id = authStore.user?.carrera_id
    }
    if (!datos.carrera_id) datos.carrera_id = null

    if (isEditing.value) {
      await api.put(`/usuarios/editar/${idEditando.value}`, datos)
    } else {
      await api.post('/usuarios/registro', datos)
    }
    
    cerrarModal()
    await cargarUsuarios()
  } catch (error) {
    mensajeError.value = error.response?.data?.detail || 'Ocurrió un error al procesar la solicitud.'
  } finally {
    isSubmitting.value = false
  }
}

const confirmarCambioEstado = async (usuario) => {
  const accionText = usuario.estado ? 'desactivar el acceso del' : 'habilitar el acceso al';
  if (confirm(`¿Estás seguro de que deseas ${accionText} usuario ${usuario.username}?`)) {
    try {
      const nuevoEstado = !usuario.estado;
      await api.put(`/usuarios/editar/${usuario.id}`, { estado: nuevoEstado });
      await cargarUsuarios();
    } catch (error) {
      console.error(error)
      alert("Hubo un error al intentar cambiar el estado del usuario.")
    }
  }
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/login')
}
</script>