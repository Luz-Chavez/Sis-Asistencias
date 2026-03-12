<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">

    <!-- NAVBAR INSTITUCIONAL -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          
          <!-- Logo Institucional -->
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-3">
              <!-- Logo UMSA -->
              <div class="w-11 h-11 rounded-xl flex items-center justify-center shadow-md bg-white/95 border border-white/50 ring-1 ring-slate-200 overflow-hidden">
                <img
                  v-if="authStore.user?.carrera_logo_url"
                  :src="resolveStaticUrl(authStore.user.carrera_logo_url)"
                  alt="Logo carrera"
                  class="w-full h-full object-contain p-1"
                />
                <span v-else class="text-blue-900 font-bold text-xs">UMSA</span>
              </div>
              <div class="hidden md:block border-l border-slate-300 pl-4">
                <p class="text-xs text-slate-500 font-medium uppercase tracking-wider">Facultad de Ciencias Sociales</p>
                <p class="text-sm font-bold text-slate-800">Sistema de Pasantias</p>
                <p v-if="authStore.user?.carrera_nombre" class="text-xs text-slate-500">Carrera: {{ authStore.user.carrera_nombre }}</p>
              </div>
            </div>
          </div>
          
          <!-- Navegacion Principal -->
          <nav class="hidden md:flex items-center gap-1">
            <button
              @click="seccion = 'dashboard'"
              :class="seccion === 'dashboard' 
                ? 'bg-blue-900 text-white' 
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200">
              Dashboard
            </button>
            <button
              @click="seccion = 'reportes'"
              :class="seccion === 'reportes' 
                ? 'bg-blue-900 text-white' 
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200">
              Reportes
            </button>
            <button
              @click="seccion = 'horas'"
              :class="seccion === 'horas' 
                ? 'bg-blue-900 text-white' 
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200">
              Horas
            </button>
            <button
              @click="seccion = 'usuarios'"
              :class="seccion === 'usuarios' 
                ? 'bg-blue-900 text-white' 
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200">
              Pasantes
            </button>
          </nav>

          <!-- Usuario y Acciones -->
          <div class="flex items-center gap-4">
            <div class="hidden sm:flex items-center gap-3 px-3 py-1.5 bg-slate-50 rounded-lg">
              <button @click="router.push('/perfil')" title="Perfil"
                class="w-8 h-8 bg-blue-900 rounded-full flex items-center justify-center text-white font-semibold text-xs hover:bg-blue-800 transition-colors">
                {{ getIniciales(authStore.user?.nombres || '', '') }}
              </button>
              <div class="text-right">
                <p class="text-xs font-semibold text-slate-700">{{ authStore.user?.nombres }}</p>
                <p class="text-xs text-slate-400">Encargado</p>
              </div>
            </div>
            <button @click="cerrarSesion"
              class="flex items-center gap-2 text-sm text-slate-600 hover:text-red-600 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
              <span class="hidden sm:inline">Salir</span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Navegacion Movil -->
      <div class="md:hidden border-t border-slate-200 bg-slate-50 px-4 py-2 flex gap-2">
        <button
          @click="seccion = 'dashboard'"
          :class="seccion === 'dashboard' ? 'bg-blue-900 text-white' : 'bg-white text-slate-600'"
          class="flex-1 px-3 py-2 rounded-lg text-xs font-medium transition-all">
          Dashboard
        </button>
        <button
          @click="seccion = 'reportes'"
          :class="seccion === 'reportes' ? 'bg-blue-900 text-white' : 'bg-white text-slate-600'"
          class="flex-1 px-3 py-2 rounded-lg text-xs font-medium transition-all">
          Reportes
        </button>
        <button
          @click="seccion = 'horas'"
          :class="seccion === 'horas' ? 'bg-blue-900 text-white' : 'bg-white text-slate-600'"
          class="flex-1 px-3 py-2 rounded-lg text-xs font-medium transition-all">
          Horas
        </button>
        <button
          @click="seccion = 'usuarios'"
          :class="seccion === 'usuarios' ? 'bg-blue-900 text-white' : 'bg-white text-slate-600'"
          class="flex-1 px-3 py-2 rounded-lg text-xs font-medium transition-all">
          Pasantes
        </button>
      </div>
    </header>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- DASHBOARD -->
      <template v-if="seccion === 'dashboard'">
        <div class="space-y-8">
          
          <!-- Bienvenida Institucional -->
          <div class="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-900 rounded-2xl p-8 text-white shadow-lg">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
              <div>
                <p class="text-blue-200 text-sm font-medium uppercase tracking-wider mb-1">Bienvenido(a)</p>
                <h1 class="text-3xl font-bold mb-2">{{ authStore.user?.nombres }}</h1>
                <p class="text-blue-100 text-sm">Panel de Control de Sistema de Gestion de Pasantias</p>
              </div>
              <div class="flex items-center gap-4">
                <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm">
                  <p class="text-3xl font-bold">{{ stats.totalPasantes }}</p>
                  <p class="text-xs text-blue-200 uppercase tracking-wider">Pasantes</p>
                </div>
                <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm">
                  <p class="text-3xl font-bold">{{ stats.pendientes }}</p>
                  <p class="text-xs text-blue-200 uppercase tracking-wider">Pendientes</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Metricas Principales -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
            
            <!-- Total Pasantes -->
            <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-300">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                  </svg>
                </div>
                <span class="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-full">TOTAL</span>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold text-slate-800">{{ stats.totalPasantes }}</p>
                <p class="text-sm text-slate-500 mt-1">Pasantes registrados</p>
              </div>
            </div>

            <!-- Pasantes Activos -->
            <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <span class="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">{{ stats.pctActivos }}%</span>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold text-slate-800">{{ stats.activos }}</p>
                <p class="text-sm text-slate-500 mt-1">Pasantes activos</p>
              </div>
              <div class="mt-3 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full" :style="{ width: stats.pctActivos + '%' }"></div>
              </div>
            </div>

            <!-- Total Reportes -->
            <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-violet-200 transition-all duration-300">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-violet-50 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                <span class="text-xs font-medium text-violet-600 bg-violet-50 px-2 py-1 rounded-full">TOTAL</span>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold text-slate-800">{{ stats.totalReportes }}</p>
                <p class="text-sm text-slate-500 mt-1">Reportes recibidos</p>
              </div>
            </div>

            <!-- Pendientes -->
            <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-amber-200 transition-all duration-300">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <span class="text-xs font-medium text-amber-600 bg-amber-50 px-2 py-1 rounded-full">PENDIENTE</span>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold text-slate-800">{{ stats.pendientes }}</p>
                <p class="text-sm text-slate-500 mt-1">Por evaluar</p>
              </div>
            </div>
          </div>

          <!-- Graficos y Analisis -->
          <div class="grid lg:grid-cols-2 gap-6">
            
            <!-- Estado de Pasantes -->
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
                <h2 class="text-lg font-semibold text-slate-800">Estado de Pasantes</h2>
                <p class="text-sm text-slate-500">Distribucion por estado actual</p>
              </div>
              <div class="p-6">
                <div class="flex items-center gap-8">
                  
                  <!-- Grafico Circular -->
                  <div class="relative w-32 h-32 flex-shrink-0">
                    <svg class="w-32 h-32 -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
                      <circle 
                        cx="50" cy="50" r="40" 
                        fill="none" 
                        stroke="#1e3a5f" 
                        stroke-width="12"
                        stroke-linecap="round"
                        :stroke-dasharray="2 * 3.1416 * 40"
                        :stroke-dashoffset="2 * 3.1416 * 40 * (1 - stats.pctActivos / 100)"
                        class="transition-all duration-1000"
                      />
                    </svg>
                    <div class="absolute inset-0 flex flex-col items-center justify-center">
                      <span class="text-2xl font-bold text-slate-800">{{ stats.pctActivos }}%</span>
                      <span class="text-xs text-slate-400">Activos</span>
                    </div>
                  </div>
                  
                  <!-- Leyenda y Detalles -->
                  <div class="flex-1 space-y-4">
                    <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                      <div class="flex items-center gap-3">
                        <div class="w-3 h-3 rounded-full bg-blue-900"></div>
                        <span class="text-sm text-slate-600">Activos</span>
                      </div>
                      <span class="font-semibold text-slate-800">{{ stats.activos }}</span>
                    </div>
                    <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                      <div class="flex items-center gap-3">
                        <div class="w-3 h-3 rounded-full bg-slate-300"></div>
                        <span class="text-sm text-slate-600">Inactivos</span>
                      </div>
                      <span class="font-semibold text-slate-800">{{ stats.inactivos }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Estado de Reportes -->
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
                <h2 class="text-lg font-semibold text-slate-800">Estado de Reportes</h2>
                <p class="text-sm text-slate-500">Evaluacion de reportes diarios</p>
              </div>
              <div class="p-6 space-y-4">
                
                <!-- Aprobados -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div class="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                      <span class="text-sm text-slate-600">Aprobados</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-semibold text-slate-800">{{ stats.aprobados }}</span>
                      <span class="text-xs text-slate-400">({{ stats.pctAprobados }}%)</span>
                    </div>
                  </div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-emerald-500 rounded-full transition-all duration-500" :style="{ width: stats.pctAprobados + '%' }"></div>
                  </div>
                </div>

                <!-- Rechazados -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div class="w-2.5 h-2.5 rounded-full bg-red-500"></div>
                      <span class="text-sm text-slate-600">Rechazados</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-semibold text-slate-800">{{ stats.rechazados }}</span>
                      <span class="text-xs text-slate-400">({{ stats.pctRechazados }}%)</span>
                    </div>
                  </div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-red-500 rounded-full transition-all duration-500" :style="{ width: stats.pctRechazados + '%' }"></div>
                  </div>
                </div>

                <!-- Pendientes -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div>
                      <span class="text-sm text-slate-600">Pendientes</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-semibold text-slate-800">{{ stats.pendientes }}</span>
                      <span class="text-xs text-slate-400">({{ stats.pctPendientes }}%)</span>
                    </div>
                  </div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-amber-500 rounded-full transition-all duration-500" :style="{ width: stats.pctPendientes + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Acciones Rapidas -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
              <h2 class="text-lg font-semibold text-slate-800">Acciones Rapidas</h2>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button @click="seccion = 'reportes'" 
                  class="group p-5 rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 transition-all duration-200 text-left">
                  <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-blue-200 transition-colors">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <p class="font-semibold text-slate-700 group-hover:text-blue-700">Ver Reportes</p>
                  <p class="text-xs text-slate-400 mt-1">{{ stats.totalReportes }} reportes</p>
                </button>
                
                <button @click="seccion = 'usuarios'"
                  class="group p-5 rounded-xl border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50/50 transition-all duration-200 text-left">
                  <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-emerald-200 transition-colors">
                    <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                    </svg>
                  </div>
                  <p class="font-semibold text-slate-700 group-hover:text-emerald-700">Ver Pasantes</p>
                  <p class="text-xs text-slate-400 mt-1">{{ stats.totalPasantes }} registrados</p>
                </button>
                
                <button @click="abrirModalCrear"
                  class="group p-5 rounded-xl border border-slate-200 hover:border-violet-300 hover:bg-violet-50/50 transition-all duration-200 text-left">
                  <div class="w-10 h-10 bg-violet-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-violet-200 transition-colors">
                    <svg class="w-5 h-5 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                    </svg>
                  </div>
                  <p class="font-semibold text-slate-700 group-hover:text-violet-700">Nuevo Pasante</p>
                  <p class="text-xs text-slate-400 mt-1">Registrar</p>
                </button>
                
                <button @click="evaluarPendiente"
                  class="group p-5 rounded-xl border border-slate-200 hover:border-amber-300 hover:bg-amber-50/50 transition-all duration-200 text-left">
                  <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-amber-200 transition-colors">
                    <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
                    </svg>
                  </div>
                  <p class="font-semibold text-slate-700 group-hover:text-amber-700">Evaluar</p>
                  <p class="text-xs text-slate-400 mt-1">{{ stats.pendientes }} pendientes</p>
                </button>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- REPORTES (delegado a componente) -->
      <EncargadoReportes v-if="seccion === 'reportes'" />

      <!-- HORAS (delegado a componente) -->
      <EncargadoHoras v-if="seccion === 'horas'" />

      <!-- PASANTES (delegado a componente) -->
      <EncargadoUsuarios v-if="seccion === 'usuarios'" />
      <template v-if="false">
        <div class="space-y-6">
          
          <!-- Header -->
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h1 class="text-2xl font-bold text-slate-800">Pasantes Registrados</h1>
              <p class="text-slate-500 mt-1">Gestiona los pasantes de la carrera â€” ID: {{ authStore.user?.carrera_id }}</p>
            </div>
            <button @click="abrirModalCrear"
              class="inline-flex items-center gap-2 bg-blue-900 text-white px-5 py-2.5 rounded-lg hover:bg-blue-800 transition-colors font-medium shadow-sm">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              Nuevo Pasante
            </button>
          </div>

          <!-- Grid de Pasantes -->
          <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <div v-for="user in usuarios" :key="user.id"
              :class="!user.estado ? 'opacity-60' : ''"
              class="bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md hover:border-slate-300 transition-all duration-200 overflow-hidden">
              
              <!-- Cabecera de tarjeta -->
              <div class="p-5 border-b border-slate-100">
                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 bg-gradient-to-br from-blue-800 to-blue-900 rounded-xl flex items-center justify-center text-white font-semibold shadow-sm">
                    {{ getIniciales(user.nombres, user.apellidos) }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <h3 class="font-semibold text-slate-800 truncate">{{ user.nombres }} {{ user.apellidos }}</h3>
                    <p class="text-xs text-slate-400 font-mono">@{{ user.username }}</p>
                  </div>
                  <span :class="user.estado ? 'bg-emerald-50 text-emerald-600 border-emerald-200' : 'bg-slate-100 text-slate-500 border-slate-200'"
                    class="text-xs font-medium px-2 py-0.5 rounded-full border">
                    {{ user.estado ? 'Activo' : 'Inactivo' }}
                  </span>
                </div>
              </div>
              
              <!-- Cuerpo de tarjeta -->
              <div class="p-5">
                <div class="space-y-2 mb-4">
                  <div class="flex items-center gap-2 text-sm text-slate-500">
                    <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                    <span class="truncate">{{ user.email }}</span>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-slate-500">
                    <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"/>
                    </svg>
                    <span>CI: {{ user.carnet_identidad }}</span>
                  </div>
                </div>
                
                <!-- Acciones -->
                <div class="flex gap-2">
                  <button @click="abrirModalVer(user)"
                    class="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 text-xs font-medium text-slate-600 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    Ver
                  </button>
                  <button @click="abrirModalEditar(user)"
                    class="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    Editar
                  </button>
                  <button @click="confirmarCambioEstado(user)"
                    :class="user.estado 
                      ? 'text-red-600 bg-red-50 hover:bg-red-100' 
                      : 'text-emerald-600 bg-emerald-50 hover:bg-emerald-100'"
                    class="inline-flex items-center justify-center px-3 py-2 text-xs font-medium rounded-lg transition-colors">
                    <svg v-if="user.estado" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M1 7h22M8 7V4a2 2 0 012-2h4a2 2 0 012 2v3"/>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582M19 20v-5h-.581M7.75 11.75a4 4 0 015.5-5.5l1.657 1.657"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Estado vacio -->
          <div v-if="!isLoadingUsuarios && usuarios.length === 0" class="text-center py-16 bg-white rounded-xl border border-slate-200">
            <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-slate-700 mb-1">No hay pasantes registrados</h3>
            <p class="text-slate-500 mb-4">Comienza agregando un nuevo pasante a tu carrera.</p>
            <button @click="abrirModalCrear" class="inline-flex items-center gap-2 bg-blue-900 text-white px-4 py-2 rounded-lg hover:bg-blue-800 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              Registrar Pasante
            </button>
          </div>
        </div>
      </template>
    </main>

    <!-- MODAL: VER PASANTE -->
    <div v-if="showModalVer" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
        
        <!-- Header -->
        <div class="umsa-header px-6 py-5">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-blue-200 text-xs font-medium uppercase tracking-wider">Informacion del Pasante</p>
              <h3 class="text-xl font-bold text-white mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</h3>
            </div>
            <button @click="showModalVer = false" class="text-blue-200 hover:text-white transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Contenido -->
        <div class="p-6" v-if="pasanteSeleccionado">
          <!-- historial -->
          <div v-if="historial.length" class="mb-6">
            <h4 class="text-sm font-semibold mb-2">Historial de asistencias</h4>
            <ul class="text-xs space-y-1">
              <li v-for="a in historial" :key="a.id">
                {{ a.fecha }} {{ a.hora_entrada }} - {{ a.hora_salida || '---' }}
              </li>
            </ul>
          </div>
          <div v-else class="mb-6 text-xs text-slate-500">
            Sin asistencias registradas.
          </div>
          <div class="flex items-center gap-4 mb-6">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-800 to-blue-900 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-md">
              {{ getIniciales(pasanteSeleccionado.nombres, pasanteSeleccionado.apellidos) }}
            </div>
            <div>
              <span :class="pasanteSeleccionado.estado ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'"
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium">
                <span :class="pasanteSeleccionado.estado ? 'bg-emerald-500' : 'bg-red-500'" class="w-1.5 h-1.5 rounded-full mr-1.5"></span>
                {{ pasanteSeleccionado.estado ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
          </div>

          <div class="space-y-3">
            <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
              <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              <div>
                <p class="text-xs text-slate-400">Username</p>
                <p class="font-mono text-sm font-semibold text-blue-600">{{ pasanteSeleccionado.username }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
              <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"/>
              </svg>
              <div>
                <p class="text-xs text-slate-400">Carnet de Identidad</p>
                <p class="text-sm font-semibold text-slate-700">{{ pasanteSeleccionado.carnet_identidad || 'â€”' }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
              <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <div>
                <p class="text-xs text-slate-400">Correo Electronico</p>
                <p class="text-sm font-semibold text-slate-700">{{ pasanteSeleccionado.email }}</p>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                </svg>
                <div>
                  <p class="text-xs text-slate-400">Carrera ID</p>
                  <p class="text-sm font-semibold text-slate-700">{{ pasanteSeleccionado.carrera_id }}</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
                <div>
                  <p class="text-xs text-slate-400">Rol</p>
                  <p class="text-sm font-semibold text-slate-700">{{ pasanteSeleccionado.rol }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-end gap-3">
          <button @click="showModalVer = false"
            class="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-800 transition-colors">
            Cerrar
          </button>
          <button @click="abrirModalEditar(pasanteSeleccionado); showModalVer = false"
            class="px-4 py-2 bg-blue-900 text-white text-sm font-medium rounded-lg hover:bg-blue-800 transition-colors">
            Editar Pasante
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: EDITAR PASANTE -->
    <div v-if="showModalEditar" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg my-8 animate-in fade-in zoom-in duration-200">
        
        <!-- Header -->
        <div class="umsa-header px-6 py-5">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-blue-200 text-xs font-medium uppercase tracking-wider">Formulario de Edicion</p>
              <h3 class="text-xl font-bold text-white mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</h3>
            </div>
            <button @click="showModalEditar = false" class="text-blue-200 hover:text-white transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="guardarEdicion" class="p-6">
          <p class="text-xs text-slate-400 mb-6">Deja vacio cualquier campo que no desees modificar.</p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Nombres</label>
              <input v-model="formEditar.nombres" type="text"
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Apellidos</label>
              <input v-model="formEditar.apellidos" type="text"
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Carnet de Identidad</label>
              <input v-model="formEditar.carnet_identidad" type="text"
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Correo Electronico</label>
              <input v-model="formEditar.email" type="email"
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all" />
            </div>
          </div>

          <div v-if="mensajeErrorEditar" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-600 text-sm">{{ mensajeErrorEditar }}</p>
          </div>

          <div class="mt-6 pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button type="button" @click="showModalEditar = false"
              class="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-800 transition-colors">
              Cancelar
            </button>
            <button type="submit" :disabled="isSubmittingEditar"
              class="px-5 py-2 bg-blue-900 text-white text-sm font-medium rounded-lg hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
              {{ isSubmittingEditar ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL: CREAR PASANTE -->
    <div v-if="showModalCrear" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg my-8 animate-in fade-in zoom-in duration-200">
        
        <!-- Header -->
        <div class="umsa-header px-6 py-5">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-white/80 text-xs font-medium uppercase tracking-wider">Registro de Pasante</p>
              <h3 class="text-xl font-bold text-white mt-1">Nuevo Pasante</h3>
            </div>
            <button @click="showModalCrear = false" class="text-white/80 hover:text-white transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="registrarPasante" class="p-6">
          
          <!-- Preview de username -->
          <div v-if="usernamePreview" class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="text-sm text-blue-700">Username generado: <strong class="font-mono">{{ usernamePreview }}</strong></span>
            </div>
          </div>

          <div class="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <span class="text-sm text-amber-700">El pasante sera asignado a la carrera <strong>ID: {{ authStore.user?.carrera_id }}</strong></span>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Nombres <span class="text-red-500">*</span></label>
              <input v-model="formulario.nombres" type="text" required
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Apellidos <span class="text-red-500">*</span></label>
              <input v-model="formulario.apellidos" type="text" required
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Carnet de Identidad <span class="text-red-500">*</span></label>
              <input v-model="formulario.carnet_identidad" type="text" required
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Correo Electronico <span class="text-red-500">*</span></label>
              <input v-model="formulario.email" type="email" required
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all" />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Celular <span class="text-red-500">*</span></label>
              <input v-model="formulario.celular" type="tel" required
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all"
                placeholder="Ej. 70123456" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1.5">ContraseÃ±a Temporal <span class="text-red-500">*</span></label>
              <input v-model="formulario.password" type="password" required
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all"
                placeholder="Minimo 6 caracteres" />
            </div>
          </div>

          <div v-if="mensajeError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-600 text-sm">{{ mensajeError }}</p>
          </div>

          <div class="mt-6 pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button type="button" @click="showModalCrear = false"
              class="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-800 transition-colors">
              Cancelar
            </button>
            <button type="submit" :disabled="isSubmittingCrear"
              class="px-5 py-2 bg-blue-900 text-white text-sm font-medium rounded-lg hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
              {{ isSubmittingCrear ? 'Registrando...' : 'Registrar Pasante' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL: CONFIRMAR CAMBIO DE ESTADO -->
    <div v-if="showModalBaja" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden animate-in fade-in zoom-in duration-200">
        
        <!-- Header -->
        <div :class="pasanteSeleccionado?.estado ? 'bg-red-600' : 'bg-emerald-600'" class="px-6 py-4">
          <h3 class="text-lg font-bold text-white">{{ pasanteSeleccionado?.estado ? 'Dar de Baja' : 'Reactivar Pasante' }}</h3>
        </div>

        <!-- Contenido -->
        <div class="p-6 text-center">
          <div :class="pasanteSeleccionado?.estado ? 'bg-red-100' : 'bg-emerald-100'"
            class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg v-if="pasanteSeleccionado?.estado" class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <svg v-else class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h4 class="text-lg font-semibold text-slate-800 mb-2">
            {{ pasanteSeleccionado?.estado ? 'Dar de baja a este pasante?' : 'Reactivar a este pasante?' }}
          </h4>
          <p class="text-slate-600 font-medium">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</p>
          <p class="text-sm text-slate-400 mt-2">
            {{ pasanteSeleccionado?.estado ? 'Su cuenta quedara inactiva y no podra acceder al sistema.' : 'Su cuenta volvera a estar activa.' }}
          </p>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-center gap-3">
          <button @click="showModalBaja = false"
            class="px-4 py-2 text-sm font-medium text-slate-600 border border-slate-300 rounded-lg hover:bg-slate-100 transition-colors">
            Cancelar
          </button>
          <button @click="ejecutarCambioEstado" :disabled="isSubmittingBaja"
            :class="pasanteSeleccionado?.estado ? 'bg-red-600 hover:bg-red-700' : 'bg-emerald-600 hover:bg-emerald-700'"
            class="px-5 py-2 text-white text-sm font-medium rounded-lg disabled:opacity-50 transition-colors">
            {{ isSubmittingBaja ? 'Procesando...' : (pasanteSeleccionado?.estado ? 'Si, dar de baja' : 'Si, reactivar') }}
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: EVALUAR REPORTE -->
    <div v-if="showModalEvaluacion" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden animate-in fade-in zoom-in duration-200">
        
        <!-- Header -->
        <div class="umsa-header px-6 py-5">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-blue-200 text-xs font-medium uppercase tracking-wider">Evaluacion</p>
              <h3 class="text-xl font-bold text-white mt-1">Reporte #{{ reporteSeleccionado?.id }}</h3>
            </div>
            <button @click="cerrarModalEvaluacion" class="text-blue-200 hover:text-white transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Contenido -->
        <div class="p-6">
          <div class="mb-4">
            <p class="text-sm text-slate-500">Pasante</p>
            <p class="font-semibold text-slate-800">{{ reporteSeleccionado?.nombre_pasante }}</p>
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium text-slate-700 mb-2">Actividades Realizadas</label>
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-600 whitespace-pre-wrap max-h-40 overflow-y-auto">
              {{ reporteSeleccionado?.actividades_realizadas }}
            </div>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Decision</label>
              <select v-model="evaluacion.estado"
                class="w-full border border-slate-300 rounded-lg p-3 bg-white cursor-pointer focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm">
                <option value="VERIFICADO">Verificar reporte</option>
                <option value="RECHAZADO">Rechazar reporte</option>
              </select>
            </div>
            <div>
	              <label class="block text-sm font-medium text-slate-700 mb-2">Comentario (obligatorio)</label>
              <textarea v-model="evaluacion.comentarios" rows="3"
                class="w-full border border-slate-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                placeholder="Retroalimentacion para el pasante..."></textarea>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-end gap-3">
          <button @click="cerrarModalEvaluacion"
            class="px-4 py-2 text-sm font-medium text-slate-600 border border-slate-300 rounded-lg hover:bg-slate-100 transition-colors">
            Cancelar
          </button>
	          <button @click="enviarEvaluacion" :disabled="isSubmittingEval || !evaluacion.comentarios.trim()"
	            class="px-5 py-2 bg-blue-900 text-white text-sm font-medium rounded-lg hover:bg-blue-800 disabled:opacity-50 transition-colors">
	            {{ isSubmittingEval ? 'Guardando...' : 'Guardar Evaluacion' }}
	          </button>
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

// componentes separados por seccion
import EncargadoReportes from '../components/EncargadoReportes.vue'
import EncargadoHoras from '../components/EncargadoHoras.vue'
import EncargadoUsuarios from '../components/EncargadoUsuarios.vue'

// CONFIGURACION
const router = useRouter()
const resolveStaticUrl = (url) => {
  if (!url) return null
  const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`
  return s
}

const authStore = useAuthStore()

// ESTADOS
const seccion = ref('dashboard')

// Reportes
const reportes = ref([])
const isLoadingReportes = ref(true)
const showModalEvaluacion = ref(false)
const reporteSeleccionado = ref(null)
const isSubmittingEval = ref(false)
const evaluacion = ref({ estado: 'VERIFICADO', comentarios: '' })

// Usuarios
const usuarios = ref([])
const isLoadingUsuarios = ref(false)
const pasanteSeleccionado = ref(null)

// Modales
const showModalVer = ref(false)
const showModalEditar = ref(false)
const showModalCrear = ref(false)
const showModalBaja = ref(false)

// historial asistencias
const historial = ref([])

const cargarHistorial = async (userId) => {
  try {
    const { data } = await api.get('/asistencias/mis-asistencias', { params: { pasante_id: userId } })
    historial.value = data
  } catch (e) {
    console.error('Error al cargar historial:', e)
    historial.value = []
  }
}

// Formularios
const formEditar = ref({ nombres: '', apellidos: '', carnet_identidad: '', email: '' })
const formulario = ref({
  nombres: '', apellidos: '', carnet_identidad: '',
  email: '', celular: '', password: '', rol_id: 3, carrera_id: null
})

// Estados de envio
const isSubmittingEditar = ref(false)
const isSubmittingCrear = ref(false)
const isSubmittingBaja = ref(false)
const mensajeErrorEditar = ref('')
const mensajeError = ref('')

// COMPUTADOS
const stats = computed(() => {
  const pasantes = usuarios.value.filter(u => String(u.rol || '').toUpperCase() === 'PASANTE')
  const totalPasantes = pasantes.length
  const activos = pasantes.filter(u => u.estado).length
  const inactivos = totalPasantes - activos
  const pctActivos = totalPasantes > 0 ? Math.round((activos / totalPasantes) * 100) : 0
  const totalReportes = reportes.value.length
  const aprobados = reportes.value.filter(r => r.estado === 'APROBADO').length
  const rechazados = reportes.value.filter(r => r.estado === 'RECHAZADO').length
  const pendientes = reportes.value.filter(r => r.estado === 'PENDIENTE').length
  
  return {
    totalPasantes, activos, inactivos, pctActivos,
    totalReportes, aprobados, rechazados, pendientes,
    pctAprobados: totalReportes > 0 ? Math.round((aprobados / totalReportes) * 100) : 0,
    pctRechazados: totalReportes > 0 ? Math.round((rechazados / totalReportes) * 100) : 0,
    pctPendientes: totalReportes > 0 ? Math.round((pendientes / totalReportes) * 100) : 0
  }
})

const usernamePreview = computed(() => {
  const n = formulario.value.nombres?.trim()
  const a = formulario.value.apellidos?.trim()
  const ci = formulario.value.carnet_identidad?.trim()
  if (!n || !a || !ci) return ''
  return `${n[0].toLowerCase()}${a[0].toLowerCase()}${ci}`
})

// UTILIDADES
const getIniciales = (nombres, apellidos) => {
  return `${nombres?.[0] || ''}${apellidos?.[0] || ''}`.toUpperCase()
}

const getInicialesFromName = (fullName) => {
  if (!fullName) return '?'
  const parts = fullName.split(' ')
  return `${parts[0]?.[0] || ''}${parts[1]?.[0] || ''}`.toUpperCase()
}

const getEstadoBadgeClass = (estado) => {
  if (estado === 'APROBADO') return 'bg-emerald-50 text-emerald-700'
  if (estado === 'RECHAZADO') return 'bg-red-50 text-red-700'
  return 'bg-amber-50 text-amber-700'
}

const getEstadoDotClass = (estado) => {
  if (estado === 'APROBADO') return 'bg-emerald-500'
  if (estado === 'RECHAZADO') return 'bg-red-500'
  return 'bg-amber-500'
}

// CARGA DE DATOS
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

// ACCIONES DE REPORTES
const abrirModalEvaluacion = (reporte) => {
  reporteSeleccionado.value = reporte
  evaluacion.value.estado = reporte.estado && reporte.estado !== 'PENDIENTE' ? reporte.estado : 'VERIFICADO'
  evaluacion.value.comentarios = reporte.comentarios_director || ''
  showModalEvaluacion.value = true
}

const cerrarModalEvaluacion = () => {
  showModalEvaluacion.value = false
  reporteSeleccionado.value = null
}

const enviarEvaluacion = async () => {
  if (!evaluacion.value.comentarios?.trim()) {
    alert('El comentario es obligatorio.')
    return
  }
  isSubmittingEval.value = true
  try {
    await api.put(`/reportes/evaluar/${reporteSeleccionado.value.id}`, {
      estado: evaluacion.value.estado,
      comentarios_director: evaluacion.value.comentarios.trim()
    })
    await cargarReportes()
    cerrarModalEvaluacion()
    alert('✅… Evaluacion guardada con exito')
  } catch {
    alert('Error al guardar la evaluacion.')
  } finally {
    isSubmittingEval.value = false
  }
}

const evaluarPendiente = () => {
  const pendiente = reportes.value.find(r => r.estado === 'PENDIENTE')
  if (pendiente) abrirModalEvaluacion(pendiente)
  else alert('No hay reportes pendientes.')
}

// ACCIONES DE PASANTES
const abrirModalVer = (user) => {
  pasanteSeleccionado.value = user
  showModalVer.value = true
  cargarHistorial(user.id)
}

const abrirModalEditar = (user) => {
  pasanteSeleccionado.value = user
  formEditar.value = {
    nombres: user.nombres,
    apellidos: user.apellidos,
    carnet_identidad: user.carnet_identidad || '',
    email: user.email
  }
  mensajeErrorEditar.value = ''
  showModalEditar.value = true
}

const guardarEdicion = async () => {
  isSubmittingEditar.value = true
  mensajeErrorEditar.value = ''
  try {
    const payload = {}
    Object.entries(formEditar.value).forEach(([k, v]) => {
      if (v && v.toString().trim() !== '') payload[k] = v
    })
    await api.put(`/usuarios/editar/${pasanteSeleccionado.value.id}`, payload)
    await cargarUsuarios()
    showModalEditar.value = false
    alert('✅… Datos actualizados correctamente')
  } catch (e) {
    mensajeErrorEditar.value = e.response?.data?.detail || 'Error al guardar.'
  } finally {
    isSubmittingEditar.value = false
  }
}

const confirmarCambioEstado = (user) => {
  pasanteSeleccionado.value = user
  showModalBaja.value = true
}

const ejecutarCambioEstado = async () => {
  isSubmittingBaja.value = true
  try {
    if (pasanteSeleccionado.value.estado) {
      await api.delete(`/usuarios/desactivar/${pasanteSeleccionado.value.id}`)
    } else {
      await api.put(`/usuarios/editar/${pasanteSeleccionado.value.id}`, { estado: true })
    }
    await cargarUsuarios()
    showModalBaja.value = false
    alert(pasanteSeleccionado.value.estado ? 'âš ï¸ Pasante dado de baja.' : '✅… Pasante reactivado.')
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al cambiar estado.')
  } finally {
    isSubmittingBaja.value = false
  }
}

const abrirModalCrear = () => {
  formulario.value = {
    nombres: '', apellidos: '', carnet_identidad: '',
    email: '', celular: '', password: '', rol_id: 3,
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
      rol_id: 3,
      carrera_id: authStore.user?.carrera_id
    })
    alert('✅… Pasante registrado exitosamente')
    showModalCrear.value = false
    await cargarUsuarios()
  } catch (e) {
    mensajeError.value = e.response?.data?.detail || 'Error al registrar.'
  } finally {
    isSubmittingCrear.value = false
  }
}

// SESION
const cerrarSesion = () => {
  authStore.logout()
  router.push('/')
}

// INICIALIZACION
onMounted(async () => {
  await Promise.all([cargarReportes(), cargarUsuarios()])
})
</script>
