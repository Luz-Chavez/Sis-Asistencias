<template>
  <div class="min-h-screen bg-slate-50 font-sans">

    <nav class="bg-slate-900 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-900 to-slate-800 rounded-xl flex items-center justify-center shadow-md border border-slate-700">
                <span class="text-amber-400 font-extrabold text-xs tracking-wider">UMSA</span>
              </div>
              <div class="hidden md:block border-l-2 border-white/10 pl-4 py-1">
                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Facultad de Cs. Sociales</p>
                <p class="text-sm font-extrabold text-white tracking-tight">Sistema de Pasantías</p>
              </div>
            </div>

            <div class="hidden md:flex gap-2 ml-4">
              <button class="bg-white/10 text-white px-4 py-2 rounded-lg text-sm font-bold cursor-default shadow-sm border border-white/10 flex items-center gap-1.5">
                <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Todos los Reportes
              </button>
              <button @click="router.push('/usuarios')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                </svg>
                Gestión de Usuarios
              </button>
              <button @click="router.push('/programas')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Programas
              </button>
              <button @click="router.push('/carreras')"
                class="text-slate-300 hover:bg-white/10 hover:text-white px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
                </svg>
                Carreras y Logos
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
        <button class="flex-1 bg-white/10 text-white shadow-sm border border-white/10 px-3 py-2 rounded-lg text-xs font-bold">
          Reportes
        </button>
        <button @click="router.push('/usuarios')" class="flex-1 bg-transparent text-slate-400 hover:bg-white/10 px-3 py-2 rounded-lg text-xs font-semibold transition-all">
          Usuarios
        </button>
        <button @click="router.push('/programas')" class="flex-1 bg-transparent text-slate-400 hover:bg-white/10 px-3 py-2 rounded-lg text-xs font-semibold transition-all">
          Programas
        </button>
        <button @click="router.push('/carreras')" class="flex-1 bg-transparent text-slate-400 hover:bg-white/10 px-3 py-2 rounded-lg text-xs font-semibold transition-all">
          Carreras
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
            <p class="text-xs font-bold text-amber-300 uppercase tracking-widest">Monitor de Actividades</p>
          </div>
          <h2 class="text-3xl lg:text-4xl font-extrabold mb-3 tracking-tight leading-tight">
            Resumen de <span class="text-amber-400">Reportes Diarios</span>
          </h2>
          <p class="text-blue-100/80 text-sm lg:text-base font-medium leading-relaxed">
            Revisa las actividades de los pasantes y aprueba sus horas de trabajo.
          </p>
        </div>

        <div class="relative z-10 flex gap-4 w-full md:w-auto flex-wrap">
          <div class="flex-1 md:flex-none bg-white/10 backdrop-blur-md border border-white/20 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-white drop-shadow-md mb-1">{{ reportes.length }}</p>
            <p class="text-[10px] text-blue-200 uppercase tracking-widest font-bold">Total Reportes</p>
          </div>
          <div class="flex-1 md:flex-none bg-gradient-to-b from-amber-500/20 to-amber-600/20 backdrop-blur-md border border-amber-400/30 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-amber-400 drop-shadow-md mb-1">{{ totalPendientes }}</p>
            <p class="text-[10px] text-amber-200 uppercase tracking-widest font-bold">Por Evaluar</p>
          </div>
          <div class="flex-1 md:flex-none bg-gradient-to-b from-emerald-500/20 to-emerald-600/20 backdrop-blur-md border border-emerald-400/30 p-5 rounded-2xl text-center min-w-[110px] shadow-inner">
            <p class="text-4xl font-black text-emerald-400 drop-shadow-md mb-1">{{ totalAprobados }}</p>
            <p class="text-[10px] text-emerald-200 uppercase tracking-widest font-bold">Aprobados</p>
          </div>
        </div>
      </div>

      <!-- Filtros y buscador -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-2 flex flex-col lg:flex-row justify-between items-center gap-3">
        <div class="flex w-full lg:w-auto p-1 bg-slate-100 rounded-xl overflow-x-auto">
          <button
            @click="filtroActual = 'TODOS'"
            :class="filtroActual === 'TODOS' ? 'bg-white text-blue-900 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-6 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Todos
          </button>
          <button
            @click="filtroActual = 'PENDIENTE'"
            :class="filtroActual === 'PENDIENTE' ? 'bg-white text-amber-600 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-6 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Pendientes
            <span v-if="totalPendientes > 0" class="ml-1.5 bg-amber-100 text-amber-700 py-0.5 px-2 rounded-full text-xs">{{ totalPendientes }}</span>
          </button>
          <button
            @click="filtroActual = 'VERIFICADO'"
            :class="filtroActual === 'VERIFICADO' ? 'bg-white text-blue-700 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-6 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Verificados
            <span v-if="totalVerificados > 0" class="ml-1.5 bg-blue-100 text-blue-700 py-0.5 px-2 rounded-full text-xs">{{ totalVerificados }}</span>
          </button>
          <button
            @click="filtroActual = 'APROBADO'"
            :class="filtroActual === 'APROBADO' ? 'bg-white text-emerald-600 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-6 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Aprobados
          </button>
          <button
            @click="filtroActual = 'RECHAZADO'"
            :class="filtroActual === 'RECHAZADO' ? 'bg-white text-rose-600 shadow-sm border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
            class="flex-1 lg:flex-none px-6 py-2.5 rounded-lg text-sm font-bold border border-transparent transition-all whitespace-nowrap">
            Rechazados
          </button>
        </div>

        <div class="relative w-full lg:w-80">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por nombre o actividad..."
            class="block w-full pl-11 pr-4 py-3 border border-slate-200 rounded-xl bg-slate-50 text-sm font-medium placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"/>
        </div>
      </div>

      <!-- Tabla -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-100">
            <thead class="bg-slate-50 border-b border-slate-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider">Pasante & Fecha</th>
                <th class="px-6 py-4 text-left text-xs font-extrabold text-slate-500 uppercase tracking-wider w-1/3">Actividades</th>
                <th class="px-6 py-4 text-center text-xs font-extrabold text-slate-500 uppercase tracking-wider">Horas Totales</th>
                <th class="px-6 py-4 text-center text-xs font-extrabold text-slate-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-4 text-center text-xs font-extrabold text-slate-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-100/80">

              <!-- Loading -->
              <tr v-if="isLoading">
                <td colspan="5" class="px-6 py-20 text-center">
                  <div class="flex flex-col items-center justify-center text-slate-400">
                    <svg class="animate-spin h-10 w-10 mb-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <p class="font-bold text-slate-500">Cargando reportes...</p>
                  </div>
                </td>
              </tr>

              <!-- Empty state -->
              <tr v-else-if="filteredReportes.length === 0">
                <td colspan="5" class="px-6 py-20 text-center">
                  <div class="flex flex-col items-center justify-center text-slate-400">
                    <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-4 border border-slate-100">
                      <svg class="w-10 h-10 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                    </div>
                    <p class="font-extrabold text-slate-600 text-lg">No hay reportes para mostrar</p>
                    <p class="text-sm mt-1 text-slate-400 font-medium">Intenta cambiar los filtros o la búsqueda.</p>
                  </div>
                </td>
              </tr>

              <!-- Filas -->
              <tr v-else v-for="reporte in filteredReportes" :key="reporte.id" class="hover:bg-slate-50/80 transition-colors group">
                <td class="px-6 py-5 whitespace-nowrap">
                  <div class="flex items-center gap-4">
                    <div class="w-11 h-11 bg-amber-50 rounded-xl flex items-center justify-center text-amber-700 font-bold text-sm border border-amber-200/60 shadow-sm flex-shrink-0">
                      {{ obtenerIniciales(reporte.nombre_pasante, '') }}
                    </div>
	                    <div class="flex flex-col">
	                      <span class="text-sm font-extrabold text-slate-800">{{ reporte.nombre_pasante || 'Pasante Desconocido' }}</span>
	                      <span v-if="reporte.proyecto_nombre" class="text-[11px] text-slate-500 font-bold mt-1">
	                        Proyecto: {{ reporte.proyecto_nombre }}
	                      </span>
	                      <span class="text-xs text-slate-500 mt-1 flex items-center gap-1.5 font-medium">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                        {{ reporte.creado_en ? new Date(reporte.creado_en).toLocaleDateString('es-BO', { day: '2-digit', month: 'short', year: 'numeric' }) : '—' }}
                      </span>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-5">
                  <p class="text-sm text-slate-600 font-medium line-clamp-2 leading-relaxed" :title="reporte.actividades_realizadas">
                    {{ reporte.actividades_realizadas }}
                  </p>
                </td>
                <td class="px-6 py-5 whitespace-nowrap text-center">
                  <div class="inline-flex flex-col items-center gap-1 bg-slate-100 px-3 py-2 rounded-lg border border-slate-200">
                    <span class="text-sm font-black text-slate-800">
                      {{ reporte.horas_totales ?? reporte.horas_trabajadas ?? '0' }} <span class="text-[10px] text-slate-500 font-extrabold uppercase tracking-wider">tot</span>
                    </span>
                    <span class="text-xs font-extrabold text-emerald-700">
                      {{ reporte.horas_validadas ?? '0' }}h <span class="text-[10px] font-extrabold uppercase tracking-wider">val</span>
                    </span>
                    <span class="text-[11px] font-extrabold text-blue-700">
                      {{ reporte.horas_verificadas ?? '0' }}h <span class="text-[10px] font-extrabold uppercase tracking-wider">ver</span>
                    </span>
                  </div>
                </td>
                <td class="px-6 py-5 whitespace-nowrap text-center">
                  <span :class="estadoBadgeClass(reporte.estado)" class="px-3 py-1.5 inline-flex items-center gap-2 text-[11px] font-bold rounded-full border uppercase tracking-wider">
                    <span class="w-1.5 h-1.5 rounded-full" :class="estadoDotClass(reporte.estado)"></span>
                    {{ reporte.estado || 'PENDIENTE' }}
                  </span>
                </td>
                <td class="px-6 py-5 whitespace-nowrap text-center">
                  <div class="flex justify-center gap-2 opacity-100 sm:opacity-40 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="abrirModalEvaluar(reporte)"
                      :class="reporte.estado === 'PENDIENTE'
                        ? 'bg-amber-500 text-white hover:bg-amber-600 shadow-md border-transparent'
                        : 'bg-white text-slate-500 hover:bg-blue-50 hover:text-blue-700 border-slate-200 shadow-sm'"
                      class="px-4 py-2 rounded-xl border text-sm font-bold transition-all flex items-center gap-2"
                      :title="reporte.estado === 'PENDIENTE' ? 'Revisar y Evaluar' : 'Ver Detalles'">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      {{ reporte.estado === 'PENDIENTE' ? 'Evaluar' : 'Ver' }}
                    </button>
                    <button
                      @click="descargarPDF(reporte)"
                      class="p-2 bg-white text-slate-400 border border-slate-200 hover:text-rose-600 hover:border-rose-200 hover:bg-rose-50 rounded-xl transition-all shadow-sm"
                      title="Descargar Comprobante PDF">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                    </button>
                    <button
                      @click="abrirHistorial(reporte)"
                      class="p-2 bg-white text-slate-400 border border-slate-200 hover:text-slate-800 hover:border-slate-300 hover:bg-slate-50 rounded-xl transition-all shadow-sm"
                      title="Ver historial de evaluaciones">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>

            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- Modal de evaluación -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-xl my-8 overflow-hidden transform transition-all">

        <!-- Header del modal -->
        <div class="px-8 py-6 bg-slate-900 flex justify-between items-center border-b border-slate-800">
          <h3 class="text-xl font-black text-white tracking-tight flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            </div>
            Evaluación de Actividades
          </h3>
          <button @click="showModal = false" class="text-slate-400 hover:text-white transition-colors bg-white/5 hover:bg-white/10 p-2 rounded-xl">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Cuerpo del modal -->
        <div class="p-8">

          <!-- Datos del reporte -->
          <div class="mb-8 bg-slate-50 p-6 rounded-2xl border border-slate-200/80 shadow-inner">
            <div class="flex justify-between items-start mb-5 pb-5 border-b border-slate-200">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-white rounded-xl border border-slate-200 flex items-center justify-center text-slate-700 font-black shadow-sm">
                  {{ obtenerIniciales(reporteAEvaluar?.nombre_pasante, '') }}
                </div>
                <div>
                  <p class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest mb-1">Pasante</p>
                  <p class="text-lg font-black text-slate-800 leading-none">{{ reporteAEvaluar?.nombre_pasante }}</p>
                </div>
              </div>
              <div class="text-right bg-white px-4 py-2 rounded-xl border border-slate-200 shadow-sm">
                <p class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest mb-1">Horas Totales</p>
                <p class="text-base font-black text-blue-700">{{ reporteAEvaluar?.horas_totales ?? reporteAEvaluar?.horas_trabajadas ?? '0' }} hrs</p>
              </div>
            </div>
            <div>
              <p class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
                </svg>
                Actividades Realizadas
              </p>
              <div class="text-sm text-slate-700 leading-relaxed bg-white p-5 rounded-xl border border-slate-200 shadow-sm max-h-48 overflow-y-auto font-medium">
                {{ reporteAEvaluar?.actividades_realizadas }}
              </div>
            </div>
          </div>

          <!-- Formulario -->
          <form @submit.prevent="guardarEvaluacion" class="space-y-6">

            <div>
              <label class="block text-sm font-extrabold text-slate-800 mb-3">¿Aprobar estas actividades?</label>
              <div class="flex gap-4">
                <label class="flex-1 cursor-pointer">
                  <input type="radio" v-model="formEvaluacion.estado" value="APROBADO" class="peer sr-only">
                  <div class="text-center p-4 rounded-2xl border-2 border-slate-200 peer-checked:border-emerald-500 peer-checked:bg-emerald-50 text-slate-400 peer-checked:text-emerald-700 hover:bg-slate-50 transition-all shadow-sm">
                    <div class="text-3xl mb-2">✅</div>
                    <div class="font-bold text-sm">Aprobar Horas</div>
                  </div>
                </label>
                <label class="flex-1 cursor-pointer">
                  <input type="radio" v-model="formEvaluacion.estado" value="RECHAZADO" class="peer sr-only">
                  <div class="text-center p-4 rounded-2xl border-2 border-slate-200 peer-checked:border-rose-500 peer-checked:bg-rose-50 text-slate-400 peer-checked:text-rose-700 hover:bg-slate-50 transition-all shadow-sm">
                    <div class="text-3xl mb-2">❌</div>
                    <div class="font-bold text-sm">Rechazar</div>
                  </div>
                </label>
              </div>
              <p class="text-xs text-slate-500 mt-3">
                Nota: para aprobar un reporte, primero debe estar <strong>VERIFICADO</strong> por un Encargado.
              </p>
            </div>

            <div>
              <div class="flex justify-between items-end mb-2">
	                <label class="block text-sm font-extrabold text-slate-800">Comentario (obligatorio)</label>
	                <span class="text-[10px] font-bold text-blue-700 uppercase tracking-widest bg-blue-50 px-2 py-1 rounded-md">Obligatorio</span>
              </div>
              <p class="text-xs text-slate-500 mb-2">Explica la decision para el registro y el pasante.</p>
              <textarea
                v-model="formEvaluacion.comentarios_director"
                rows="3"
                class="w-full border border-slate-300 rounded-2xl p-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all text-sm bg-slate-50 focus:bg-white resize-none font-medium placeholder:font-normal"
                placeholder="Escribe tu mensaje aquí...">
              </textarea>
            </div>

            <div v-if="mensajeError" class="text-rose-700 bg-rose-50 p-4 text-sm rounded-2xl border border-rose-200 flex items-center gap-3 font-bold">
              <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {{ mensajeError }}
            </div>

            <div class="flex justify-end gap-3 pt-6 border-t border-slate-100">
              <button type="button" @click="showModal = false"
                class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 font-bold hover:bg-slate-50 transition-colors">
                Cancelar
              </button>
              <button type="submit" :disabled="isSubmitting || !formEvaluacion.comentarios_director.trim()"
                class="px-8 py-3 bg-blue-900 text-white rounded-xl font-bold hover:bg-blue-800 disabled:opacity-50 transition-all shadow-lg flex items-center gap-2">
                <span v-if="isSubmitting" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                {{ isSubmitting ? 'Procesando...' : 'Confirmar Decisión' }}
              </button>
            </div>

          </form>
        </div>
      </div>
	    </div>

	    <!-- Modal historial -->
	    <div v-if="showHistorialModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 px-4 backdrop-blur-sm overflow-y-auto">
	      <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-2xl my-8 overflow-hidden transform transition-all">
	        <div class="px-8 py-6 bg-slate-900 flex justify-between items-center border-b border-slate-800">
	          <h3 class="text-lg font-black text-white tracking-tight">Historial</h3>
	          <button @click="showHistorialModal = false" class="text-slate-300 hover:text-white">✕</button>
	        </div>

	        <div class="p-6 space-y-3">
	          <p v-if="historialTitulo" class="text-sm font-bold text-slate-700">{{ historialTitulo }}</p>

	          <div v-if="isLoadingHistorial" class="py-10 text-center text-slate-400">
	            Cargando...
	          </div>
	          <div v-else-if="errorHistorial" class="text-rose-700 bg-rose-50 p-4 text-sm rounded-2xl border border-rose-200 font-bold">
	            {{ errorHistorial }}
	          </div>
	          <div v-else-if="historialItems.length === 0" class="py-10 text-center text-slate-400">
	            Sin registros.
	          </div>
	          <div v-else class="divide-y divide-slate-100 border border-slate-200 rounded-2xl overflow-hidden">
	            <div v-for="h in historialItems" :key="h.id" class="p-4 bg-white">
	              <div>
	                <p class="text-sm font-extrabold text-slate-800">
	                  {{ h.estado_anterior || '—' }} → {{ h.estado_nuevo }}
	                </p>
	                <p class="text-xs text-slate-500 mt-1">
	                  {{ formatearFechaHora(h.creado_en) }} · {{ h.actor_nombre || ('Usuario #' + h.actor_id) }}
	                </p>
	              </div>
	              <p class="text-sm text-slate-700 mt-2 whitespace-pre-wrap">{{ h.comentarios }}</p>
	            </div>
	          </div>
	        </div>

	        <div class="px-8 py-5 bg-slate-50 border-t border-slate-200 flex justify-end">
	          <button @click="showHistorialModal = false" class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 font-bold hover:bg-slate-100 transition-colors">
	            Cerrar
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
import api from '../services/api'

const router    = useRouter()
const authStore = useAuthStore()

const reportes     = ref([])
const searchQuery  = ref('')
const filtroActual = ref('TODOS')
const isLoading    = ref(true)
const showModal    = ref(false)
const isSubmitting = ref(false)
const mensajeError = ref('')

const reporteAEvaluar = ref(null)
const formEvaluacion  = ref({ estado: 'APROBADO', comentarios_director: '' })

const showHistorialModal = ref(false)
const historialItems = ref([])
const isLoadingHistorial = ref(false)
const errorHistorial = ref('')
const historialTitulo = ref('')

// KPIs
const totalPendientes = computed(() => reportes.value.filter(r => r.estado === 'PENDIENTE').length)
const totalVerificados = computed(() => reportes.value.filter(r => r.estado === 'VERIFICADO').length)
const totalAprobados  = computed(() => reportes.value.filter(r => r.estado === 'APROBADO').length)

// Genera iniciales para los avatares
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

// Filtros + buscador
const filteredReportes = computed(() => {
  let resultado = reportes.value
  if (filtroActual.value !== 'TODOS') {
    resultado = resultado.filter(r => r.estado === filtroActual.value)
  }
  if (searchQuery.value) {
    const lower = searchQuery.value.toLowerCase()
    resultado = resultado.filter(r =>
      (r.nombre_pasante || '').toLowerCase().includes(lower) ||
      (r.proyecto_nombre || '').toLowerCase().includes(lower) ||
      r.actividades_realizadas.toLowerCase().includes(lower) ||
      r.estado.toLowerCase().includes(lower)
    )
  }
  return resultado
})

const estadoBadgeClass = (estado) => {
  if (estado === 'APROBADO')  return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  if (estado === 'VERIFICADO') return 'bg-blue-50 text-blue-700 border-blue-200'
  if (estado === 'RECHAZADO') return 'bg-rose-50 text-rose-700 border-rose-200'
  return 'bg-amber-50 text-amber-700 border-amber-200'
}

const estadoDotClass = (estado) => {
  if (estado === 'APROBADO')  return 'bg-emerald-500'
  if (estado === 'VERIFICADO') return 'bg-blue-500'
  if (estado === 'RECHAZADO') return 'bg-rose-500'
  return 'bg-amber-500'
}

onMounted(async () => {
  await cargarReportes()
})

const cargarReportes = async () => {
  isLoading.value = true
  try {
    const response = await api.get('/reportes/listar')
    reportes.value = response.data
  } catch (error) {
    console.error('Error al cargar reportes:', error)
  } finally {
    isLoading.value = false
  }
}

const abrirModalEvaluar = (reporte) => {
  reporteAEvaluar.value = reporte
  formEvaluacion.value = {
    estado: reporte.estado === 'VERIFICADO' ? 'APROBADO' : 'APROBADO',
    comentarios_director: reporte.comentarios_director || ''
  }
  mensajeError.value = ''
  showModal.value = true
}

const guardarEvaluacion = async () => {
  if (!formEvaluacion.value.comentarios_director?.trim()) {
    mensajeError.value = 'El comentario es obligatorio.'
    return
  }
  isSubmitting.value = true
  mensajeError.value = ''
  try {
    await api.put(`/reportes/evaluar/${reporteAEvaluar.value.id}`, {
      ...formEvaluacion.value,
      comentarios_director: formEvaluacion.value.comentarios_director.trim(),
    })
    showModal.value = false
    await cargarReportes()
  } catch (error) {
    console.error(error)
    mensajeError.value = error.response?.data?.detail || 'Error al evaluar el reporte. Revisa tus permisos.'
  } finally {
    isSubmitting.value = false
  }
}

const formatearFechaHora = (dt) => {
  if (!dt) return '—'
  return new Date(dt).toLocaleString('es-BO', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const abrirHistorial = async (reporte) => {
  showHistorialModal.value = true
  historialItems.value = []
  errorHistorial.value = ''
  historialTitulo.value = `Reporte #${reporte?.id || ''} - ${reporte?.nombre_pasante || ''}`.trim()
  isLoadingHistorial.value = true
  try {
    const { data } = await api.get(`/reportes/historial/${reporte.id}`)
    historialItems.value = data || []
  } catch (e) {
    errorHistorial.value = e.response?.data?.detail || 'No se pudo cargar el historial.'
    historialItems.value = []
  } finally {
    isLoadingHistorial.value = false
  }
}

const descargarPDF = async (reporte) => {
  try {
    const response = await api.get(`/reportes/descargar/${reporte.id}`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    const nombre = reporte.nombre_pasante ? reporte.nombre_pasante.replace(/\s+/g, '') : 'Pasante'
    link.setAttribute('download', `Reporte_${nombre}_${reporte.id}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error al descargar el PDF:', error)
    alert('Ocurrió un error al intentar descargar el documento.')
  }
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/login')
}
</script>
