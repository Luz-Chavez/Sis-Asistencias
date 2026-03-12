<template>
  <div class="min-h-screen bg-slate-50 font-sans">

    <!-- Navbar -->
    <nav class="bg-slate-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <!-- Logo UMSA -->
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-900 to-slate-800 rounded-xl flex items-center justify-center shadow-md border border-slate-700">
                <span class="text-amber-400 font-extrabold text-xs tracking-wider">UMSA</span>
              </div>
              <div class="hidden md:block border-l-2 border-white/10 pl-4 py-1">
                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Facultad de Cs. Sociales</p>
                <p class="text-sm font-extrabold text-white tracking-tight">Sistema de Pasantías</p>
              </div>
            </div>

            <!-- Navegación -->
            <div class="hidden md:flex gap-2 ml-4">
              <button @click="router.push(esEncargado ? '/encargado' : '/admin')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Todos los Reportes
              </button>
              <button
                class="bg-white/10 text-white px-4 py-2 rounded-lg text-sm font-bold cursor-default shadow-sm border border-white/10 flex items-center gap-1.5">
                <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                </svg>
                Gestión de Usuarios
              </button>
            </div>
          </div>

          <div class="flex items-center gap-4">
            <div class="hidden sm:flex items-center gap-3">
              <div class="flex flex-col items-end">
                <span class="text-white text-sm font-bold leading-tight">{{ authStore.user?.nombres }}</span>
                <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider">{{ authStore.user?.rol }}</span>
              </div>
              <button @click="router.push('/perfil')" title="Perfil"
                class="w-9 h-9 bg-white/10 rounded-full flex items-center justify-center text-white font-bold text-sm border border-white/20 hover:bg-white/20 transition-colors">
                {{ obtenerIniciales(authStore.user?.nombres, authStore.user?.apellidos) }}
              </button>
            </div>
            <div class="h-6 w-px bg-white/10 hidden sm:block"></div>
            <button @click="cerrarSesion"
              class="flex items-center gap-2 text-sm font-semibold text-slate-300 hover:text-rose-400 transition-colors group">
              <span class="hidden sm:inline">Salir</span>
              <svg class="w-5 h-5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile nav -->
      <div class="md:hidden border-t border-white/10 bg-slate-900 px-4 py-2 flex gap-2">
        <button @click="router.push(esEncargado ? '/encargado' : '/admin')"
          class="flex-1 bg-transparent text-slate-400 hover:bg-white/10 px-3 py-2 rounded-lg text-xs font-semibold transition-all">
          Reportes
        </button>
        <button class="flex-1 bg-white/10 text-white border border-white/10 px-3 py-2 rounded-lg text-xs font-bold">
          Usuarios
        </button>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-6">

      <!-- Hero Banner con KPIs -->
      <div class="bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 rounded-2xl p-8 lg:p-10 text-white shadow-lg relative overflow-hidden flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
        <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500 opacity-20 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
        <div class="absolute bottom-0 left-10 w-32 h-32 bg-amber-500 opacity-20 rounded-full blur-2xl pointer-events-none"></div>

        <div class="relative z-10 max-w-xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/20 mb-4 backdrop-blur-md">
            <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
            <p class="text-xs font-bold text-amber-300 uppercase tracking-widest">Gestión de Cuentas</p>
          </div>
          <h2 class="text-3xl lg:text-4xl font-extrabold mb-3 tracking-tight leading-tight">
            Directorio del <span class="text-amber-400">Sistema</span>
          </h2>
          <p class="text-blue-100/80 text-sm lg:text-base font-medium leading-relaxed">
            <span v-if="esEncargado">Gestiona las cuentas y accesos de los pasantes de tu carrera.</span>
            <span v-else>Administra todas las cuentas, roles y accesos a nivel de Facultad.</span>
          </p>
        </div>

        <div class="relative z-10 flex gap-4 w-full md:w-auto flex-wrap">
          <div class="flex-1 md:flex-none bg-white/10 backdrop-blur-md border border-white/20 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-white drop-shadow-md mb-1">{{ usuarios.length }}</p>
            <p class="text-[10px] text-blue-200 uppercase tracking-widest font-bold">Total Usuarios</p>
          </div>
          <div class="flex-1 md:flex-none bg-gradient-to-b from-emerald-500/20 to-emerald-600/20 backdrop-blur-md border border-emerald-400/30 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-emerald-400 drop-shadow-md mb-1">{{ totalPasantes }}</p>
            <p class="text-[10px] text-emerald-200 uppercase tracking-widest font-bold">Pasantes</p>
          </div>
          <div v-if="!esEncargado" class="flex-1 md:flex-none bg-rose-500/10 backdrop-blur-md border border-rose-400/20 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-rose-300 drop-shadow-md mb-1">{{ totalInactivos }}</p>
            <p class="text-[10px] text-rose-200 uppercase tracking-widest font-bold">Inactivos</p>
          </div>
        </div>
      </div>

      <!-- Filtros y buscador -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-2 flex flex-col lg:flex-row justify-between items-center gap-3">

        <div class="flex w-full lg:w-auto p-1 bg-slate-100 rounded-xl overflow-x-auto">
          <button @click="filtroRol = 'TODOS'"
            :class="filtroRol === 'TODOS' ? 'bg-white text-blue-900 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-5 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Todos
          </button>
          <button v-if="!esEncargado" @click="filtroRol = 'ADMINISTRADOR'"
            :class="filtroRol === 'ADMINISTRADOR' ? 'bg-white text-slate-800 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-5 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Administradores
          </button>
          <button v-if="!esEncargado" @click="filtroRol = 'ENCARGADO'"
            :class="filtroRol === 'ENCARGADO' ? 'bg-white text-slate-800 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-5 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Encargados
          </button>
          <button @click="filtroRol = 'PASANTE'"
            :class="filtroRol === 'PASANTE' ? 'bg-white text-emerald-600 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-5 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Pasantes
          </button>
        </div>

        <div class="flex w-full lg:w-auto items-center gap-3">
          <div class="relative w-full lg:w-72">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <input v-model="searchQuery" type="text" placeholder="Buscar usuario..."
              class="block w-full pl-11 pr-4 py-3 border border-slate-200 rounded-xl bg-slate-50 text-sm font-medium placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"/>
          </div>

          <button @click="abrirModalCrear"
            class="hidden sm:flex bg-amber-500 hover:bg-amber-600 text-white px-5 py-3 rounded-xl shadow-md font-bold items-center justify-center gap-2 transition-all shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            Nuevo {{ esEncargado ? 'Pasante' : 'Usuario' }}
          </button>
        </div>
      </div>

      <!-- Tabla -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-100">
            <thead class="bg-slate-50 border-b border-slate-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Usuario</th>
                <th class="px-6 py-4 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Username</th>
                <th class="px-6 py-4 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Rol</th>
                <th class="px-6 py-4 text-center text-xs font-extrabold text-slate-500 uppercase tracking-wider">Carrera</th>
                <th class="px-6 py-4 text-center text-xs font-extrabold text-slate-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-4 text-center text-xs font-extrabold text-slate-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-100/80">

              <!-- Loading -->
              <tr v-if="isLoading">
                <td colspan="6" class="px-6 py-20 text-center">
                  <div class="flex flex-col items-center justify-center text-slate-400">
                    <svg class="animate-spin h-10 w-10 mb-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <p class="font-bold text-slate-500">Cargando directorio...</p>
                  </div>
                </td>
              </tr>

              <!-- Empty state -->
              <tr v-else-if="filteredUsuarios.length === 0">
                <td colspan="6" class="px-6 py-20 text-center">
                  <div class="flex flex-col items-center justify-center text-slate-400">
                    <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-4 border border-slate-100">
                      <svg class="w-10 h-10 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                      </svg>
                    </div>
                    <p class="font-extrabold text-slate-600 text-lg">No se encontraron usuarios</p>
                    <p class="text-sm mt-1 text-slate-400 font-medium">Verifica los filtros o el término de búsqueda.</p>
                  </div>
                </td>
              </tr>

              <!-- Filas -->
              <tr v-else v-for="user in filteredUsuarios" :key="user.id" class="hover:bg-slate-50/80 transition-colors group">
                <td class="px-6 py-5 whitespace-nowrap">
                  <div class="flex items-center gap-4">
                    <div class="flex-shrink-0 h-11 w-11 bg-slate-100 rounded-xl flex items-center justify-center text-blue-800 font-extrabold text-sm border border-slate-200 shadow-sm">
                      {{ obtenerIniciales(user.nombres, user.apellidos) }}
                    </div>
                    <div class="flex flex-col">
                      <div class="text-sm font-extrabold text-slate-800">{{ user.nombres }} {{ user.apellidos }}</div>
                      <div class="text-xs text-slate-500 font-medium mt-0.5">{{ user.email }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-5 whitespace-nowrap">
                  <span class="text-xs font-mono font-semibold text-slate-600 bg-slate-100 px-2.5 py-1.5 rounded-lg border border-slate-200">{{ user.username }}</span>
                </td>
                <td class="px-6 py-5 whitespace-nowrap">
                  <span :class="rolBadgeClass(user.rol)" class="px-3 py-1.5 inline-flex text-[10px] leading-none font-bold rounded-lg uppercase tracking-widest border shadow-sm">
                    {{ user.rol || 'Sin rol' }}
                  </span>
                </td>
                <td class="px-6 py-5 whitespace-nowrap text-center text-sm font-bold text-slate-600">
                  {{ user.carrera_nombre || user.carrera_id || 'N/A' }}
                </td>
                <td class="px-6 py-5 whitespace-nowrap text-center">
                  <div class="flex items-center justify-center">
                    <span :class="user.estado ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-rose-50 text-rose-700 border-rose-200'"
                      class="px-3 py-1.5 inline-flex items-center gap-2 text-[11px] font-bold rounded-full border shadow-sm uppercase tracking-wider">
                      <span class="w-1.5 h-1.5 rounded-full" :class="user.estado ? 'bg-emerald-500' : 'bg-rose-500'"></span>
                      {{ user.estado ? 'ACTIVO' : 'INACTIVO' }}
                    </span>
                  </div>
                </td>
                <td class="px-6 py-5 whitespace-nowrap text-center">
                  <div class="flex justify-center gap-2 opacity-100 sm:opacity-40 group-hover:opacity-100 transition-opacity">
                    <button @click="abrirModalEditar(user)"
                      class="p-2 text-slate-500 bg-white border border-slate-200 hover:text-blue-700 hover:border-blue-300 hover:bg-blue-50 rounded-xl transition-all shadow-sm"
                      title="Editar Información">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button @click="confirmarCambioEstado(user)"
                      class="p-2 bg-white border border-slate-200 rounded-xl transition-all shadow-sm"
                      :class="user.estado ? 'text-slate-500 hover:text-rose-600 hover:bg-rose-50 hover:border-rose-200' : 'text-slate-500 hover:text-emerald-600 hover:bg-emerald-50 hover:border-emerald-200'"
                      :title="user.estado ? 'Desactivar acceso' : 'Habilitar acceso'">
                      <svg v-if="user.estado" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                      </svg>
                      <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>

            </tbody>
          </table>
        </div>
      </div>

      <!-- FAB móvil -->
      <button @click="abrirModalCrear"
        class="sm:hidden fixed bottom-6 right-6 w-14 h-14 bg-amber-500 text-white rounded-full shadow-lg flex items-center justify-center hover:bg-amber-600 transition-colors z-40">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
        </svg>
      </button>

    </main>

    <!-- Modal crear/editar usuario -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-start sm:items-center justify-center bg-slate-900/60 px-4 py-8 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-2xl overflow-hidden transform transition-all flex flex-col max-h-[calc(100vh-4rem)]">

        <!-- Header del modal -->
        <div class="px-6 sm:px-8 py-4 sm:py-6 bg-slate-900 flex justify-between items-center border-b border-slate-800">
          <h3 class="text-xl font-black text-white tracking-tight flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
            </div>
            {{ isEditing ? 'Actualizar Perfil de Usuario' : (esEncargado ? 'Registrar Nuevo Pasante' : 'Registrar Nuevo Usuario') }}
          </h3>
          <button @click="cerrarModal" class="text-slate-400 hover:text-white transition-colors bg-white/5 hover:bg-white/10 p-2 rounded-xl">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="p-5 sm:p-8 overflow-y-auto">

          <!-- Preview username -->
          <div v-if="!isEditing && usernamePreview" class="mb-6 p-4 bg-slate-100 rounded-2xl border border-slate-200 text-sm text-slate-700 flex items-center gap-3 shadow-inner">
            <div class="w-8 h-8 rounded-lg bg-white shadow-sm flex items-center justify-center shrink-0">
              <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
              </svg>
            </div>
            <span>El <strong class="text-slate-900">Username</strong> generado será:
              <strong class="font-mono text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-100 ml-1">{{ usernamePreview }}</strong>
            </span>
          </div>

          <!-- Aviso encargado -->
          <div v-if="esEncargado && !isEditing" class="mb-6 p-4 bg-amber-50 rounded-2xl border border-amber-200 text-sm text-amber-800 flex items-start gap-3">
            <svg class="w-5 h-5 text-amber-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>Como Encargado, solo puedes registrar <strong>Pasantes</strong> en tu carrera <strong>(ID: {{ authStore.user?.carrera_id }})</strong>.</span>
          </div>

          <form @submit.prevent="guardarUsuario" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Nombres</label>
                <input v-model="formulario.nombres" type="text" required placeholder="Ej. Juan Carlos"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Apellidos</label>
                <input v-model="formulario.apellidos" type="text" required placeholder="Ej. Pérez Gómez"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Carnet de Identidad</label>
                <input v-model="formulario.carnet_identidad" type="text" required placeholder="Nro. de Documento"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">RU</label>
                <input v-model="formulario.ru" type="text" placeholder="Registro Universitario (opcional)"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Unidad asignada</label>
                <input v-model="formulario.unidad_asignada" type="text" placeholder="Ej. Biblioteca / Secretaría / Unidad X"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Correo Electrónico</label>
                <input v-model="formulario.email" type="email" required placeholder="correo@ejemplo.com"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Programa de pasantia</label>
                <div class="relative">
                  <select v-model.number="formulario.programa_id"
                    class="w-full border border-slate-300 rounded-2xl p-3.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all font-bold text-slate-700 appearance-none">
                    <option :value="null">Sin programa</option>
                    <option v-for="p in programas" :key="p.id" :value="p.id">{{ p.nombre }}</option>
                  </select>
                  <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </div>
                </div>
                <div v-if="programaSeleccionado" class="mt-2 text-xs text-slate-600 font-medium space-y-1">
                  <div v-if="programaSeleccionado.descripcion" class="text-slate-500">
                    {{ programaSeleccionado.descripcion }}
                  </div>
                  <a v-if="programaSeleccionado.documento_url" :href="resolveStaticUrl(programaSeleccionado.documento_url)" target="_blank" rel="noopener"
                    class="inline-flex items-center gap-1 text-blue-700 font-bold hover:underline">
                    Ver resolucion del programa
                  </a>
                </div>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Meta horas pasantia</label>
                <input v-model.number="formulario.meta_horas_pasantia" type="number" min="1" step="1" placeholder="240"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Celular</label>
                <input v-model="formulario.celular" type="tel" required placeholder="Ej. 70123456"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1 flex justify-between">
                  Contraseña
                  <span v-if="isEditing" class="text-[9px] bg-slate-200 text-slate-600 px-2 py-0.5 rounded-md normal-case tracking-normal">Vacío = No cambiar</span>
                </label>
                <input v-model="formulario.password" type="password" :required="!isEditing" placeholder="Mín. 6 caracteres"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal"/>
              </div>

              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Rol del Sistema</label>
                <div class="relative">
                  <select v-if="!esEncargado && !isEditing" v-model="formulario.rol_id" required
                    class="w-full border border-slate-300 rounded-2xl p-3.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all font-bold text-slate-700 appearance-none">
                    <option :value="idRol('ADMINISTRADOR')">Administrador</option>
                    <option :value="idRol('ENCARGADO')">Encargado</option>
                    <option :value="idRol('PASANTE')">Pasante</option>
                  </select>
                  <div v-if="!esEncargado && !isEditing" class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </div>
                  <input v-if="esEncargado || isEditing" type="text" :value="isEditing ? formulario.rol_nombre : 'Pasante'" disabled
                    class="w-full border border-slate-200 rounded-2xl p-3.5 bg-slate-100 text-slate-500 cursor-not-allowed font-bold"/>
                </div>
              </div>

              <div v-if="!esEncargado || isEditing">
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Asignación de Carrera</label>
                <div class="relative">
                  <select v-if="!esEncargado && requiereCarrera" v-model.number="formulario.carrera_id" required
                    class="w-full border border-slate-300 rounded-2xl p-3.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all font-bold text-slate-700 appearance-none">
                    <option :value="null" disabled>Selecciona una carrera</option>
                    <option v-for="c in carreras" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                  </select>
                  <div v-if="!esEncargado && requiereCarrera" class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </div>
                  <input v-if="!esEncargado && !requiereCarrera" type="text" value="No aplica" disabled
                    class="w-full border border-slate-200 rounded-2xl p-3.5 bg-slate-100 text-slate-500 cursor-not-allowed font-bold"/>
                  <div v-if="esEncargado" class="w-full border border-slate-200 rounded-2xl p-3.5 bg-slate-100 text-slate-500 cursor-not-allowed font-bold flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                    ID Carrera Restringida: {{ formulario.carrera_id || authStore.user?.carrera_id }}
                  </div>
                </div>
              </div>

            </div>

            <!-- Error -->
            <div v-if="mensajeError" class="text-rose-700 bg-rose-50 p-4 text-sm rounded-2xl border border-rose-200 font-bold flex items-center gap-3">
              <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {{ mensajeError }}
            </div>

            <!-- Acciones -->
            <div class="flex justify-end gap-3 pt-6">
              <button type="button" @click="cerrarModal"
                class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 font-bold hover:bg-slate-50 transition-colors">
                Cancelar
              </button>
              <button type="submit" :disabled="isSubmitting"
                class="px-8 py-3 bg-blue-900 text-white rounded-xl font-bold hover:bg-blue-800 disabled:opacity-50 transition-all shadow-lg flex items-center gap-2">
                <span v-if="isSubmitting" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                {{ isSubmitting ? 'Procesando...' : (isEditing ? 'Guardar Cambios' : 'Registrar Usuario') }}
              </button>
            </div>

          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'

const router    = useRouter()
const authStore = useAuthStore()

const usuarios     = ref([])
const searchQuery  = ref('')
const filtroRol    = ref('TODOS')
const isLoading    = ref(true)
const showModal    = ref(false)
const isEditing    = ref(false)
const idEditando   = ref(null)
const isSubmitting = ref(false)
const mensajeError = ref('')

const programas = ref([])
const isLoadingProgramas = ref(false)

const carreras          = ref([])
const isLoadingCarreras = ref(false)

const rolesMap = ref({ ADMINISTRADOR: 1, ENCARGADO: 2, PASANTE: 3 })
const idRol    = (nombre) => rolesMap.value[nombre] ?? null

const esEncargado = computed(() => authStore.user?.rol === 'ENCARGADO')

const requiereCarrera = computed(() => {
  const rolId = Number(formulario.value.rol_id)
  return rolId === idRol('PASANTE') || rolId === idRol('ENCARGADO')
})

const formulario = ref({
  nombres: '', apellidos: '', carnet_identidad: '',
  ru: '', unidad_asignada: '',
  programa_id: null,
  meta_horas_pasantia: 240,
  email: '', celular: '', password: '', rol_id: 3, carrera_id: null, rol_nombre: ''
})

// KPIs
const totalPasantes  = computed(() => usuarios.value.filter(u => u.rol === 'PASANTE').length)
const totalInactivos = computed(() => usuarios.value.filter(u => !u.estado).length)

// Iniciales para avatar
const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.trim().charAt(0) : ''
  const a = apellidos ? apellidos.trim().charAt(0) : ''
  if (!a && nombres) {
    const parts = nombres.trim().split(' ')
    if (parts.length > 1) return (parts[0][0] + parts[1][0]).toUpperCase()
    return nombres.substring(0, 2).toUpperCase()
  }
  return (n + a).toUpperCase() || 'U'
}

const resolveStaticUrl = (url) => {
  if (!url) return null
  const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`
  return s
}

const programaSeleccionado = computed(() => {
  const id = formulario.value.programa_id
  if (!id) return null
  return (programas.value || []).find(p => Number(p.id) === Number(id)) || null
})

// Preview username
const usernamePreview = computed(() => {
  const n  = formulario.value.nombres?.trim()
  const a  = formulario.value.apellidos?.trim()
  const ci = formulario.value.carnet_identidad?.trim()
  if (!n || !a || !ci) return ''
  return `${n[0].toLowerCase()}${a[0].toLowerCase()}${ci}`
})

// Filtros + buscador
const filteredUsuarios = computed(() => {
  let resultado = usuarios.value
  if (filtroRol.value !== 'TODOS') {
    resultado = resultado.filter(u => u.rol === filtroRol.value)
  }
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
  if (rol === 'ADMINISTRADOR') return 'bg-slate-800 text-white border-slate-700'
  if (rol === 'ENCARGADO')     return 'bg-blue-100 text-blue-800 border-blue-200'
  if (rol === 'PASANTE')       return 'bg-emerald-100 text-emerald-800 border-emerald-200'
  return 'bg-slate-100 text-slate-700 border-slate-200'
}

onMounted(async () => {
  await Promise.all([cargarUsuarios(), cargarCarreras()])
})

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

const cargarCarreras = async () => {
  isLoadingCarreras.value = true
  try {
    const res = await api.get('/carreras/')
    carreras.value = res.data || []
  } catch (e) {
    console.error('Error al cargar carreras:', e)
    carreras.value = []
  } finally {
    isLoadingCarreras.value = false
  }
}

const cargarProgramas = async () => {
  isLoadingProgramas.value = true
  try {
    const res = await api.get('/programas/listar')
    programas.value = res.data || []
  } catch (e) {
    console.error('Error al cargar programas:', e)
    programas.value = []
  } finally {
    isLoadingProgramas.value = false
  }
}

const abrirModalCrear = async () => {
  isEditing.value  = false
  idEditando.value = null
  formulario.value = {
    nombres: '', apellidos: '', carnet_identidad: '',
    ru: '', unidad_asignada: '',
    programa_id: null,
    meta_horas_pasantia: 240,
    email: '', celular: '', password: '',
    rol_id:     idRol('PASANTE'),
    carrera_id: esEncargado.value ? authStore.user?.carrera_id : null
  }
  mensajeError.value = ''
  await cargarProgramas()
  showModal.value    = true
}

const abrirModalEditar = async (usuario) => {
  isEditing.value  = true
  idEditando.value = usuario.id
  formulario.value = {
    nombres:          usuario.nombres,
    apellidos:        usuario.apellidos,
    carnet_identidad: usuario.carnet_identidad,
    ru:               usuario.ru || '',
    unidad_asignada:  usuario.unidad_asignada || '',
    programa_id:      usuario.programa_id ?? null,
    meta_horas_pasantia: Number(usuario.meta_horas_pasantia ?? 240),
    email:            usuario.email,
    celular:          usuario.celular || '',
    password:         '',
    rol_id:           idRol(usuario.rol) || idRol('PASANTE'),
    carrera_id:       usuario.carrera_id,
    rol_nombre:       usuario.rol
  }
  mensajeError.value = ''
  await cargarProgramas()
  showModal.value    = true
}

const cerrarModal = () => { showModal.value = false }

const validarCelular = (value) => {
  const raw    = String(value || '').trim()
  const digits = raw.replace(/\D/g, '')
  if (!raw) return 'El celular es obligatorio.'
  if (digits.length < 8) return 'El celular debe tener al menos 8 dígitos.'
  return null
}

const guardarUsuario = async () => {
  isSubmitting.value = true
  mensajeError.value = ''
  try {
    const errCel = validarCelular(formulario.value.celular)
    if (errCel) { mensajeError.value = errCel; return }

    if (requiereCarrera.value && !esEncargado.value && !formulario.value.carrera_id) {
      mensajeError.value = 'Debes seleccionar una carrera.'
      return
    }

    if (isEditing.value) {
      const payload = {
        nombres:          formulario.value.nombres,
        apellidos:        formulario.value.apellidos,
        carnet_identidad: formulario.value.carnet_identidad,
        ru:               (formulario.value.ru || '').trim() || null,
        unidad_asignada:  (formulario.value.unidad_asignada || '').trim() || null,
        programa_id:      formulario.value.programa_id || null,
        meta_horas_pasantia: formulario.value.meta_horas_pasantia ?? 240,
        email:            formulario.value.email,
        celular:          formulario.value.celular,
        carrera_id:       esEncargado.value ? authStore.user?.carrera_id : (formulario.value.carrera_id || null),
      }
      if (formulario.value.password) payload.password = formulario.value.password
      await api.put(`/usuarios/editar/${idEditando.value}`, payload)
      // Si había documento ya cargado, lo mantenemos; si se sube uno nuevo, se actualiza después.
    } else {
      const datos = { ...formulario.value }
      delete datos.rol_nombre
      if (esEncargado.value) {
        datos.rol_id     = idRol('PASANTE')
        datos.carrera_id = authStore.user?.carrera_id
      }
      if (!datos.carrera_id) datos.carrera_id = null
      if (!datos.programa_id) datos.programa_id = null
      datos.ru = (datos.ru || '').trim() || null
      datos.unidad_asignada = (datos.unidad_asignada || '').trim() || null
      if (datos.meta_horas_pasantia === '' || datos.meta_horas_pasantia === null || datos.meta_horas_pasantia === undefined) {
        datos.meta_horas_pasantia = 240
      }
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
  const accionText = usuario.estado ? 'desactivar el acceso del' : 'habilitar el acceso al'
  if (confirm(`¿Estás seguro de que deseas ${accionText} usuario ${usuario.username}?`)) {
    try {
      await api.put(`/usuarios/editar/${usuario.id}`, { estado: !usuario.estado })
      await cargarUsuarios()
    } catch (error) {
      console.error(error)
      alert('Hubo un error al intentar cambiar el estado del usuario.')
    }
  }
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/login')
}
</script>
