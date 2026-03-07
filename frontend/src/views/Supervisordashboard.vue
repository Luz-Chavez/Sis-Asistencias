<template>
  <div class="min-h-screen" style="background: #f3f4f6; font-family: inherit;">
    
    <!-- SIDEBAR -->
    <aside :class="['sidebar', sidebarOpen ? 'sidebar-open' : 'sidebar-closed']">
      <div class="sidebar-header">
        <div class="logo-mark">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect width="12" height="12" rx="3" fill="#6EE7B7"/>
            <rect x="16" width="12" height="12" rx="3" fill="#34D399" opacity="0.6"/>
            <rect y="16" width="12" height="12" rx="3" fill="#34D399" opacity="0.6"/>
            <rect x="16" y="16" width="12" height="12" rx="3" fill="#6EE7B7" opacity="0.3"/>
          </svg>
        </div>
        <div class="logo-text" v-show="sidebarOpen">
          <span class="logo-title">SisCont</span>
          <span class="logo-sub">Supervisor</span>
        </div>
        <button class="sidebar-toggle" @click="sidebarOpen = !sidebarOpen">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path v-if="sidebarOpen" d="M11 19l-7-7 7-7M18 19l-7-7 7-7"/>
            <path v-else d="M13 5l7 7-7 7M6 5l7 7-7 7"/>
          </svg>
        </button>
      </div>

      <nav class="sidebar-nav">
        <button 
          v-for="tab in tabs" :key="tab.id"
          @click="activeTab = tab.id"
          :class="['nav-item', activeTab === tab.id ? 'nav-item-active' : '']"
        >
          <span class="nav-icon" v-html="tab.icon"></span>
          <span class="nav-label" v-show="sidebarOpen">{{ tab.label }}</span>
          <span v-if="tab.badge && sidebarOpen" class="nav-badge">{{ tab.badge }}</span>
          <span v-if="tab.badge && !sidebarOpen" class="nav-badge-dot"></span>
        </button>
      </nav>

      <div class="sidebar-footer" v-show="sidebarOpen">
        <div class="user-card">
          <div class="user-avatar">{{ iniciales }}</div>
          <div class="user-info">
            <span class="user-name">{{ authStore.user?.nombres }}</span>
            <span class="user-role">SUPERVISOR</span>
          </div>
        </div>
        <button @click="cerrarSesion" class="logout-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
          </svg>
          Salir
        </button>
      </div>
      <div v-if="!sidebarOpen" class="sidebar-footer-mini">
        <button @click="cerrarSesion" class="logout-btn-mini" title="Cerrar sesión">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
          </svg>
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <div :class="['main-content', sidebarOpen ? 'main-expanded' : 'main-collapsed']">
      
      <!-- TOP BAR -->
      <header class="topbar">
        <div class="topbar-left">
          <h1 class="page-title">{{ currentTab?.label }}</h1>
          <span class="page-breadcrumb">Facultad de Ciencias Sociales · UMSA</span>
        </div>
        <div class="topbar-right">
          <div class="date-chip">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            {{ fechaHoy }}
          </div>
        </div>
      </header>

      <!-- VIEWS -->
      <main class="page-body">

        <!-- ===== TAB: INICIO ===== -->
        <div v-if="activeTab === 'inicio'" class="fade-in">
          <div class="stats-grid">
            <div class="stat-card stat-green">
              <div class="stat-icon">👥</div>
              <div class="stat-data">
                <span class="stat-number">{{ pasantes.length }}</span>
                <span class="stat-label">Pasantes Activos</span>
              </div>
            </div>
            <div class="stat-card stat-blue">
              <div class="stat-icon">✅</div>
              <div class="stat-data">
                <span class="stat-number">{{ asistenciasHoy }}</span>
                <span class="stat-label">Asistencias Hoy</span>
              </div>
            </div>
            <div class="stat-card stat-yellow">
              <div class="stat-icon">📝</div>
              <div class="stat-data">
                <span class="stat-number">{{ reportesPendientes }}</span>
                <span class="stat-label">Reportes Pendientes</span>
              </div>
            </div>
            <div class="stat-card stat-red">
              <div class="stat-icon">⚠️</div>
              <div class="stat-data">
                <span class="stat-number">{{ pasantesSinEntrada }}</span>
                <span class="stat-label">Sin Entrada Hoy</span>
              </div>
            </div>
          </div>

          <div class="two-col">
            <div class="panel">
              <div class="panel-header">
                <h3 class="panel-title">Actividad Reciente</h3>
              </div>
              <div class="activity-list">
                <div v-if="actividadReciente.length === 0" class="empty-state-sm">Sin actividad reciente</div>
                <div v-for="act in actividadReciente" :key="act.id" class="activity-item">
                  <div class="activity-dot" :class="act.color"></div>
                  <div class="activity-text">
                    <span class="activity-name">{{ act.nombre }}</span>
                    <span class="activity-desc">{{ act.descripcion }}</span>
                  </div>
                  <span class="activity-time">{{ act.hora }}</span>
                </div>
              </div>
            </div>

            <div class="panel">
              <div class="panel-header">
                <h3 class="panel-title">Reportes por Revisar</h3>
                <button @click="activeTab = 'reportes'" class="panel-link">Ver todos →</button>
              </div>
              <div class="review-list">
                <div v-if="reportes.filter(r => r.estado === 'PENDIENTE').length === 0" class="empty-state-sm">
                  ¡Todo al día! Sin pendientes.
                </div>
                <div 
                  v-for="r in reportes.filter(r => r.estado === 'PENDIENTE').slice(0,4)" 
                  :key="r.id" 
                  class="review-item"
                  @click="abrirEvaluacion(r)"
                >
                  <div class="review-badge">PENDIENTE</div>
                  <div class="review-info">
                    <span class="review-name">{{ r.nombre_pasante || 'Pasante #' + r.asistencia_id }}</span>
                    <span class="review-preview">{{ r.actividades_realizadas?.substring(0, 60) }}...</span>
                  </div>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="review-arrow">
                    <path d="M9 18l6-6-6-6"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ===== TAB: PASANTES ===== -->
        <div v-if="activeTab === 'pasantes'" class="fade-in">
          <div class="toolbar">
            <div class="search-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
              </svg>
              <input v-model="searchPasante" placeholder="Buscar por nombre o CI..." class="search-input">
            </div>
            <div class="toolbar-actions">
              <select v-model="filterEstado" class="filter-select">
                <option value="">Todos los estados</option>
                <option value="true">Activos</option>
                <option value="false">Inactivos</option>
              </select>
              <button @click="abrirModalPasante(null)" class="btn-primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 5v14M5 12h14"/>
                </svg>
                Nuevo Pasante
              </button>
            </div>
          </div>

          <div class="data-table-wrap">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Pasante</th>
                  <th>Carnet</th>
                  <th>Correo</th>
                  <th>Estado</th>
                  <th>Asistencias</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="isLoadingPasantes">
                  <td colspan="6" class="loading-row">
                    <div class="spinner"></div> Cargando pasantes...
                  </td>
                </tr>
                <tr v-else-if="pasantesFiltrados.length === 0">
                  <td colspan="6" class="empty-row">No se encontraron pasantes.</td>
                </tr>
                <tr v-else v-for="p in pasantesFiltrados" :key="p.id" class="table-row">
                  <td>
                    <div class="user-cell">
                      <div class="mini-avatar">{{ (p.nombres?.[0] || '') + (p.apellidos?.[0] || '') }}</div>
                      <div>
                        <div class="cell-name">{{ p.nombres }} {{ p.apellidos }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="cell-mono">{{ p.carnet_identidad }}</td>
                  <td class="cell-email">{{ p.email }}</td>
                  <td>
                    <span :class="['status-badge', p.estado ? 'status-active' : 'status-inactive']">
                      {{ p.estado ? 'ACTIVO' : 'INACTIVO' }}
                    </span>
                  </td>
                  <td>
                    <button @click="verAsistencias(p)" class="link-btn">Ver historial →</button>
                  </td>
                  <td>
                    <div class="action-btns">
                      <button @click="abrirModalPasante(p)" class="action-btn action-edit" title="Editar">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                      </button>
                      <button @click="toggleEstadoPasante(p)" :class="['action-btn', p.estado ? 'action-deactivate' : 'action-activate']" :title="p.estado ? 'Desactivar' : 'Activar'">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path v-if="p.estado" d="M18.36 6.64a9 9 0 11-12.73 0M12 2v10"/>
                          <path v-else d="M12 22V12M4.93 4.93l14.14 14.14"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ===== TAB: ASISTENCIAS ===== -->
        <div v-if="activeTab === 'asistencias'" class="fade-in">
          <div class="toolbar">
            <div class="search-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
              </svg>
              <input v-model="searchAsistencia" placeholder="Buscar pasante..." class="search-input">
            </div>
            <div class="toolbar-actions">
              <input v-model="filterFecha" type="date" class="filter-select" style="color: #a3aab8;">
              <button @click="exportarAsistencias" class="btn-secondary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
                </svg>
                Exportar
              </button>
            </div>
          </div>

          <div class="data-table-wrap">
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Pasante</th>
                  <th>Fecha</th>
                  <th>Entrada</th>
                  <th>Salida</th>
                  <th>Horas</th>
                  <th>Ubicación</th>
                  <th>Reporte</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="isLoadingAsistencias">
                  <td colspan="8" class="loading-row"><div class="spinner"></div> Cargando...</td>
                </tr>
                <tr v-else-if="asistenciasFiltradas.length === 0">
                  <td colspan="8" class="empty-row">No hay asistencias para mostrar.</td>
                </tr>
                <tr v-else v-for="a in asistenciasFiltradas" :key="a.id" class="table-row">
                  <td class="cell-mono">#{{ a.id }}</td>
                  <td>
                    <div class="cell-name">{{ nombrePasante(a.pasante_id) }}</div>
                  </td>
                  <td class="cell-mono">{{ formatFecha(a.fecha) }}</td>
                  <td>
                    <span class="time-badge time-entrada">{{ formatHora(a.hora_entrada) }}</span>
                  </td>
                  <td>
                    <span v-if="a.hora_salida" class="time-badge time-salida">{{ formatHora(a.hora_salida) }}</span>
                    <span v-else class="time-badge time-pending">—</span>
                  </td>
                  <td>
                    <span v-if="a.horas_trabajadas" class="hours-badge">{{ a.horas_trabajadas }}h</span>
                    <span v-else class="cell-dim">—</span>
                  </td>
                  <td>
                    <button @click="verUbicacion(a)" class="map-btn" title="Ver en mapa">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>
                      </svg>
                      GPS
                    </button>
                  </td>
                  <td>
                    <span v-if="tieneReporte(a.id)" class="has-report">✓ Sí</span>
                    <span v-else class="no-report">✗ No</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ===== TAB: REPORTES ===== -->
        <div v-if="activeTab === 'reportes'" class="fade-in">
          <div class="toolbar">
            <div class="search-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
              </svg>
              <input v-model="searchReporte" placeholder="Buscar pasante o actividad..." class="search-input">
            </div>
            <div class="toolbar-actions">
              <select v-model="filterEstadoReporte" class="filter-select">
                <option value="">Todos los estados</option>
                <option value="PENDIENTE">Pendientes</option>
                <option value="APROBADO">Aprobados</option>
                <option value="RECHAZADO">Rechazados</option>
              </select>
            </div>
          </div>

          <!-- KANBAN VIEW -->
          <div class="kanban-board">
            <div v-for="col in kanbanCols" :key="col.estado" class="kanban-col">
              <div class="kanban-header" :class="col.class">
                <span class="kanban-title">{{ col.label }}</span>
                <span class="kanban-count">{{ reportesPorEstado(col.estado).length }}</span>
              </div>
              <div class="kanban-cards">
                <div v-if="reportesPorEstado(col.estado).length === 0" class="kanban-empty">Sin reportes</div>
                <div 
                  v-for="r in reportesPorEstado(col.estado)" 
                  :key="r.id" 
                  class="kanban-card"
                  @click="abrirEvaluacion(r)"
                >
                  <div class="kanban-card-header">
                    <span class="kanban-id">#{{ r.id }}</span>
                    <span class="kanban-date">{{ formatFechaCorta(r.creado_en) }}</span>
                  </div>
                  <div class="kanban-pasante">{{ r.nombre_pasante || 'Asistencia #' + r.asistencia_id }}</div>
                  <p class="kanban-preview">{{ r.actividades_realizadas?.substring(0, 80) }}...</p>
                  <div class="kanban-footer">
                    <span class="kanban-action">{{ col.estado === 'PENDIENTE' ? 'Clic para evaluar →' : 'Ver detalles →' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>

    <!-- ====== MODAL: PASANTE CRUD ====== -->
    <div v-if="showModalPasante" class="modal-overlay" @click.self="showModalPasante = false">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">{{ pasanteEditando ? 'Editar Pasante' : 'Registrar Nuevo Pasante' }}</h3>
          <button @click="showModalPasante = false" class="modal-close">&times;</button>
        </div>
        <form @submit.prevent="guardarPasante" class="modal-body">
          <div class="form-grid">
            <div class="form-field">
              <label class="form-label">Nombres *</label>
              <input v-model="formPasante.nombres" type="text" required class="form-input" placeholder="Ej. Juan Carlos">
            </div>
            <div class="form-field">
              <label class="form-label">Apellidos *</label>
              <input v-model="formPasante.apellidos" type="text" required class="form-input" placeholder="Ej. Mamani Quispe">
            </div>
            <div class="form-field">
              <label class="form-label">Carnet de Identidad *</label>
              <input v-model="formPasante.carnet_identidad" type="text" required class="form-input" placeholder="Ej. 9876543">
            </div>
            <div class="form-field">
              <label class="form-label">Correo Electrónico *</label>
              <input v-model="formPasante.email" type="email" required class="form-input" placeholder="correo@umsa.bo">
            </div>
            <div class="form-field" v-if="!pasanteEditando">
              <label class="form-label">Contraseña Temporal *</label>
              <input v-model="formPasante.password" type="password" required class="form-input" placeholder="Mínimo 6 caracteres">
            </div>
            <div class="form-field">
              <label class="form-label">Carrera</label>
              <input type="text" :value="'ID: ' + authStore.user?.carrera_id" disabled class="form-input form-input-disabled">
            </div>
          </div>

          <div v-if="modalError" class="form-error">{{ modalError }}</div>

          <div class="modal-footer">
            <button type="button" @click="showModalPasante = false" class="btn-ghost">Cancelar</button>
            <button type="submit" :disabled="isSubmittingPasante" class="btn-primary">
              <span v-if="isSubmittingPasante">Guardando...</span>
              <span v-else>{{ pasanteEditando ? 'Actualizar' : 'Registrar Pasante' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ====== MODAL: EVALUACIÓN REPORTE ====== -->
    <div v-if="showModalEvaluacion" class="modal-overlay" @click.self="showModalEvaluacion = false">
      <div class="modal modal-lg">
        <div class="modal-header modal-header-purple">
          <div>
            <h3 class="modal-title">Evaluar Reporte <span class="modal-id">#{{ reporteEvaluando?.id }}</span></h3>
            <p class="modal-subtitle">{{ reporteEvaluando?.nombre_pasante }}</p>
          </div>
          <button @click="showModalEvaluacion = false" class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div class="report-content">
            <label class="form-label">Actividades Reportadas</label>
            <div class="report-text">{{ reporteEvaluando?.actividades_realizadas }}</div>
          </div>
          <div class="form-grid">
            <div class="form-field">
              <label class="form-label">Decisión *</label>
              <div class="decision-btns">
                <button 
                  type="button"
                  @click="formEvaluacion.estado = 'APROBADO'"
                  :class="['decision-btn', formEvaluacion.estado === 'APROBADO' ? 'decision-approve-active' : 'decision-inactive']"
                >
                  ✅ Aprobar
                </button>
                <button 
                  type="button"
                  @click="formEvaluacion.estado = 'RECHAZADO'"
                  :class="['decision-btn', formEvaluacion.estado === 'RECHAZADO' ? 'decision-reject-active' : 'decision-inactive']"
                >
                  ❌ Rechazar
                </button>
              </div>
            </div>
          </div>
          <div class="form-field">
            <label class="form-label">Comentarios para el Pasante (opcional)</label>
            <textarea 
              v-model="formEvaluacion.comentarios_director" 
              rows="3" 
              class="form-input" 
              placeholder="Escribe retroalimentación útil para el pasante..."
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showModalEvaluacion = false" class="btn-ghost">Cancelar</button>
          <button @click="enviarEvaluacion" :disabled="isSubmittingEval" class="btn-primary">
            {{ isSubmittingEval ? 'Guardando...' : 'Guardar Evaluación' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ====== MODAL: ASISTENCIAS DEL PASANTE ====== -->
    <div v-if="showModalAsistencias" class="modal-overlay" @click.self="showModalAsistencias = false">
      <div class="modal modal-xl">
        <div class="modal-header">
          <div>
            <h3 class="modal-title">Historial de Asistencias</h3>
            <p class="modal-subtitle">{{ pasanteViendoAsistencias?.nombres }} {{ pasanteViendoAsistencias?.apellidos }}</p>
          </div>
          <button @click="showModalAsistencias = false" class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="isLoadingHistorial" class="loading-center"><div class="spinner"></div></div>
          <div v-else-if="historialPasante.length === 0" class="empty-state-sm">Sin registros de asistencia.</div>
          <table v-else class="data-table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Entrada</th>
                <th>Salida</th>
                <th>Horas</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in historialPasante" :key="a.id" class="table-row">
                <td class="cell-mono">{{ formatFecha(a.fecha) }}</td>
                <td><span class="time-badge time-entrada">{{ formatHora(a.hora_entrada) }}</span></td>
                <td>
                  <span v-if="a.hora_salida" class="time-badge time-salida">{{ formatHora(a.hora_salida) }}</span>
                  <span v-else class="time-badge time-pending">Sin salida</span>
                </td>
                <td>
                  <span v-if="a.horas_trabajadas" class="hours-badge">{{ a.horas_trabajadas }}h</span>
                  <span v-else class="cell-dim">—</span>
                </td>
                <td>
                  <span :class="['status-badge', a.hora_salida ? 'status-active' : 'status-warning']">
                    {{ a.hora_salida ? 'Completa' : 'Incompleta' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Resumen -->
          <div v-if="historialPasante.length > 0" class="historial-summary">
            <div class="summary-item">
              <span class="summary-label">Total días</span>
              <span class="summary-value">{{ historialPasante.length }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Horas totales</span>
              <span class="summary-value">{{ totalHorasPasante }}h</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Asistencias completas</span>
              <span class="summary-value">{{ historialPasante.filter(a => a.hora_salida).length }}</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showModalAsistencias = false" class="btn-ghost">Cerrar</button>
        </div>
      </div>
    </div>

    <!-- ====== MODAL: MAPA GPS ====== -->
    <div v-if="showModalMapa" class="modal-overlay" @click.self="showModalMapa = false">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">Ubicación GPS</h3>
          <button @click="showModalMapa = false" class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div class="gps-grid">
            <div class="gps-card gps-entrada">
              <div class="gps-icon">📍</div>
              <div class="gps-label">Entrada</div>
              <div class="gps-coords">
                <span>Lat: {{ asistenciaGPS?.latitud_entrada }}</span>
                <span>Lon: {{ asistenciaGPS?.longitud_entrada }}</span>
              </div>
              <a :href="`https://www.google.com/maps?q=${asistenciaGPS?.latitud_entrada},${asistenciaGPS?.longitud_entrada}`" target="_blank" class="gps-link">
                Ver en Google Maps →
              </a>
            </div>
            <div v-if="asistenciaGPS?.latitud_salida" class="gps-card gps-salida">
              <div class="gps-icon">🏁</div>
              <div class="gps-label">Salida</div>
              <div class="gps-coords">
                <span>Lat: {{ asistenciaGPS?.latitud_salida }}</span>
                <span>Lon: {{ asistenciaGPS?.longitud_salida }}</span>
              </div>
              <a :href="`https://www.google.com/maps?q=${asistenciaGPS?.latitud_salida},${asistenciaGPS?.longitud_salida}`" target="_blank" class="gps-link">
                Ver en Google Maps →
              </a>
            </div>
            <div v-else class="gps-card gps-no-salida">
              <div class="gps-icon">—</div>
              <div class="gps-label">Sin datos de salida</div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showModalMapa = false" class="btn-ghost">Cerrar</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

const router = useRouter();
const authStore = useAuthStore();

// ---- SIDEBAR ----
const sidebarOpen = ref(true);

const tabs = ref([
  { id: 'inicio', label: 'Inicio', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>' },
  { id: 'pasantes', label: 'Pasantes', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>' },
  { id: 'asistencias', label: 'Asistencias', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>' },
  { id: 'reportes', label: 'Reportes', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>', badge: 0 },
]);

const activeTab = ref('inicio');
const currentTab = computed(() => tabs.value.find(t => t.id === activeTab.value));

// ---- DATA ----
const pasantes = ref([]);
const asistencias = ref([]);
const reportes = ref([]);
const isLoadingPasantes = ref(true);
const isLoadingAsistencias = ref(true);

// ---- FILTROS ----
const searchPasante = ref('');
const filterEstado = ref('');
const searchAsistencia = ref('');
const filterFecha = ref('');
const searchReporte = ref('');
const filterEstadoReporte = ref('');

// ---- MODALES ----
const showModalPasante = ref(false);
const showModalEvaluacion = ref(false);
const showModalAsistencias = ref(false);
const showModalMapa = ref(false);

const pasanteEditando = ref(null);
const reporteEvaluando = ref(null);
const pasanteViendoAsistencias = ref(null);
const historialPasante = ref([]);
const isLoadingHistorial = ref(false);
const asistenciaGPS = ref(null);

const isSubmittingPasante = ref(false);
const isSubmittingEval = ref(false);
const modalError = ref('');

const formPasante = ref({ nombres: '', apellidos: '', carnet_identidad: '', email: '', password: '', rol_id: 4, carrera_id: null });
const formEvaluacion = ref({ estado: 'APROBADO', comentarios_director: '' });

// ---- COMPUTED ----
const iniciales = computed(() => {
  const u = authStore.user;
  return u ? (u.nombres?.[0] || '') + (u.apellidos?.[0] || '') : 'SU';
});

const fechaHoy = computed(() => new Date().toLocaleDateString('es-BO', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }));

const pasantesFiltrados = computed(() => {
  return pasantes.value.filter(p => {
    const matchSearch = !searchPasante.value || 
      `${p.nombres} ${p.apellidos}`.toLowerCase().includes(searchPasante.value.toLowerCase()) ||
      p.carnet_identidad?.includes(searchPasante.value);
    const matchEstado = filterEstado.value === '' || String(p.estado) === filterEstado.value;
    return matchSearch && matchEstado;
  });
});

const asistenciasFiltradas = computed(() => {
  return asistencias.value.filter(a => {
    const nombre = nombrePasante(a.pasante_id).toLowerCase();
    const matchSearch = !searchAsistencia.value || nombre.includes(searchAsistencia.value.toLowerCase());
    const matchFecha = !filterFecha.value || a.fecha?.startsWith(filterFecha.value);
    return matchSearch && matchFecha;
  });
});

const asistenciasHoy = computed(() => {
  const hoy = new Date().toISOString().split('T')[0];
  return asistencias.value.filter(a => a.fecha?.startsWith(hoy)).length;
});

const reportesPendientes = computed(() => reportes.value.filter(r => r.estado === 'PENDIENTE').length);

const pasantesSinEntrada = computed(() => {
  const hoy = new Date().toISOString().split('T')[0];
  const conEntradaHoy = new Set(asistencias.value.filter(a => a.fecha?.startsWith(hoy)).map(a => a.pasante_id));
  return pasantes.value.filter(p => p.estado && !conEntradaHoy.has(p.id)).length;
});

const actividadReciente = computed(() => {
  return asistencias.value.slice(0, 5).map(a => ({
    id: a.id,
    nombre: nombrePasante(a.pasante_id),
    descripcion: a.hora_salida ? 'Marcó salida' : 'Marcó entrada',
    hora: formatHora(a.hora_entrada),
    color: a.hora_salida ? 'dot-blue' : 'dot-green'
  }));
});

const totalHorasPasante = computed(() => {
  return historialPasante.value.reduce((sum, a) => sum + (parseFloat(a.horas_trabajadas) || 0), 0).toFixed(1);
});

const reportesFiltrados = computed(() => {
  return reportes.value.filter(r => {
    const matchSearch = !searchReporte.value ||
      r.nombre_pasante?.toLowerCase().includes(searchReporte.value.toLowerCase()) ||
      r.actividades_realizadas?.toLowerCase().includes(searchReporte.value.toLowerCase());
    const matchEstado = !filterEstadoReporte.value || r.estado === filterEstadoReporte.value;
    return matchSearch && matchEstado;
  });
});

const kanbanCols = [
  { estado: 'PENDIENTE', label: '⏳ Pendientes', class: 'kanban-header-yellow' },
  { estado: 'APROBADO', label: '✅ Aprobados', class: 'kanban-header-green' },
  { estado: 'RECHAZADO', label: '❌ Rechazados', class: 'kanban-header-red' },
];

// ---- HELPERS ----
const nombrePasante = (id) => {
  const p = pasantes.value.find(p => p.id === id);
  return p ? `${p.nombres} ${p.apellidos}` : `Pasante #${id}`;
};

const tieneReporte = (asistenciaId) => reportes.value.some(r => r.asistencia_id === asistenciaId);

const formatFecha = (fecha) => {
  if (!fecha) return '—';
  return new Date(fecha).toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' });
};

const formatFechaCorta = (fecha) => {
  if (!fecha) return '—';
  return new Date(fecha).toLocaleDateString('es-BO', { day: '2-digit', month: 'short' });
};

const formatHora = (hora) => {
  if (!hora) return '—';
  return new Date(hora).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' });
};

const reportesPorEstado = (estado) => reportesFiltrados.value.filter(r => r.estado === estado);

// ---- CARGA DE DATOS ----
onMounted(async () => {
  await Promise.all([cargarPasantes(), cargarAsistencias(), cargarReportes()]);
});

const cargarPasantes = async () => {
  isLoadingPasantes.value = true;
  try {
    const res = await api.get('/usuarios/listar');
    pasantes.value = res.data.filter(u => u.rol_id === 4);
  } catch (e) {
    console.error(e);
  } finally {
    isLoadingPasantes.value = false;
  }
};

const cargarAsistencias = async () => {
  isLoadingAsistencias.value = true;
  try {
    const res = await api.get('/asistencias/todas');
    asistencias.value = res.data;
  } catch (e) {
    console.error(e);
  } finally {
    isLoadingAsistencias.value = false;
  }
};

const cargarReportes = async () => {
  try {
    const res = await api.get('/reportes/listar');
    reportes.value = res.data;
    // Actualizar badge
    const tab = tabs.value.find(t => t.id === 'reportes');
    if (tab) tab.badge = reportes.value.filter(r => r.estado === 'PENDIENTE').length || 0;
  } catch (e) {
    console.error(e);
  }
};

// ---- PASANTES CRUD ----
const abrirModalPasante = (pasante) => {
  modalError.value = '';
  pasanteEditando.value = pasante;
  if (pasante) {
    formPasante.value = {
      nombres: pasante.nombres,
      apellidos: pasante.apellidos,
      carnet_identidad: pasante.carnet_identidad,
      email: pasante.email,
      password: '',
      rol_id: 4,
      carrera_id: pasante.carrera_id
    };
  } else {
    formPasante.value = {
      nombres: '', apellidos: '', carnet_identidad: '', email: '',
      password: '', rol_id: 4, carrera_id: authStore.user?.carrera_id
    };
  }
  showModalPasante.value = true;
};

const guardarPasante = async () => {
  isSubmittingPasante.value = true;
  modalError.value = '';
  try {
    if (pasanteEditando.value) {
      const datos = { ...formPasante.value };
      delete datos.password;
      await api.put(`/usuarios/actualizar/${pasanteEditando.value.id}`, datos);
    } else {
      await api.post('/usuarios/registro', { ...formPasante.value });
    }
    showModalPasante.value = false;
    await cargarPasantes();
  } catch (e) {
    modalError.value = e.response?.data?.detail || 'Error al guardar el pasante.';
  } finally {
    isSubmittingPasante.value = false;
  }
};

const toggleEstadoPasante = async (pasante) => {
  const accion = pasante.estado ? 'desactivar' : 'activar';
  if (!confirm(`¿Confirmas ${accion} a ${pasante.nombres}?`)) return;
  try {
    if (pasante.estado) {
      await api.delete(`/usuarios/desactivar/${pasante.id}`);
    } else {
      await api.put(`/usuarios/actualizar/${pasante.id}`, { estado: true });
    }
    await cargarPasantes();
  } catch (e) {
    alert('Error al cambiar el estado del pasante.');
  }
};

// ---- ASISTENCIAS ----
const verAsistencias = async (pasante) => {
  pasanteViendoAsistencias.value = pasante;
  isLoadingHistorial.value = true;
  showModalAsistencias.value = true;
  try {
    const res = await api.get(`/asistencias/pasante/${pasante.id}`);
    historialPasante.value = res.data;
  } catch (e) {
    historialPasante.value = [];
  } finally {
    isLoadingHistorial.value = false;
  }
};

const verUbicacion = (asistencia) => {
  asistenciaGPS.value = asistencia;
  showModalMapa.value = true;
};

const exportarAsistencias = () => {
  const headers = ['ID', 'Pasante', 'Fecha', 'Entrada', 'Salida', 'Horas'];
  const rows = asistenciasFiltradas.value.map(a => [
    a.id,
    nombrePasante(a.pasante_id),
    formatFecha(a.fecha),
    formatHora(a.hora_entrada),
    formatHora(a.hora_salida),
    a.horas_trabajadas || '—'
  ]);
  const csv = [headers, ...rows].map(r => r.join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `asistencias_${new Date().toISOString().split('T')[0]}.csv`;
  link.click();
};

// ---- REPORTES ----
const abrirEvaluacion = (reporte) => {
  reporteEvaluando.value = reporte;
  formEvaluacion.value = {
    estado: reporte.estado !== 'PENDIENTE' ? reporte.estado : 'APROBADO',
    comentarios_director: reporte.comentarios_director || ''
  };
  showModalEvaluacion.value = true;
};

const enviarEvaluacion = async () => {
  isSubmittingEval.value = true;
  try {
    await api.put(`/reportes/evaluar/${reporteEvaluando.value.id}`, formEvaluacion.value);
    showModalEvaluacion.value = false;
    await cargarReportes();
  } catch (e) {
    alert('Error al guardar la evaluación.');
  } finally {
    isSubmittingEval.value = false;
  }
};

const cerrarSesion = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

/* ===== SIDEBAR ===== */
.sidebar {
  position: fixed; top: 0; left: 0; height: 100vh;
  background: #312e81;
  display: flex; flex-direction: column;
  transition: width 0.25s ease;
  z-index: 100;
  overflow: hidden;
}
.sidebar-open { width: 220px; }
.sidebar-closed { width: 60px; }

.sidebar-header {
  display: flex; align-items: center; gap: 10px;
  padding: 18px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  min-height: 64px;
}
.logo-mark { flex-shrink: 0; }
.logo-text { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.logo-title { font-size: 14px; font-weight: 700; color: #fff; white-space: nowrap; }
.logo-sub { font-size: 10px; font-weight: 500; color: #a5b4fc; letter-spacing: 0.1em; text-transform: uppercase; }
.sidebar-toggle {
  flex-shrink: 0;
  background: none; border: none; color: rgba(255,255,255,0.5); cursor: pointer;
  padding: 4px; border-radius: 6px; transition: color 0.2s;
}
.sidebar-toggle:hover { color: #fff; }

.sidebar-nav { flex: 1; padding: 12px 8px; display: flex; flex-direction: column; gap: 2px; }
.nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 10px; border-radius: 8px; border: none;
  background: none; color: rgba(255,255,255,0.6); cursor: pointer;
  font-size: 13px; font-weight: 500;
  transition: all 0.15s; white-space: nowrap; width: 100%;
  text-align: left; position: relative;
}
.nav-item:hover { background: rgba(255,255,255,0.1); color: #fff; }
.nav-item-active { background: rgba(255,255,255,0.15); color: #fff; }
.nav-icon { flex-shrink: 0; display: flex; }
.nav-label { flex: 1; }
.nav-badge { background: #f59e0b; color: #1a1a1a; font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 10px; }
.nav-badge-dot { width: 7px; height: 7px; background: #f59e0b; border-radius: 50%; position: absolute; top: 8px; right: 8px; }

.sidebar-footer { padding: 12px 8px; border-top: 1px solid rgba(255,255,255,0.1); }
.sidebar-footer-mini { padding: 12px 8px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: center; }
.user-card { display: flex; align-items: center; gap: 10px; padding: 8px; border-radius: 8px; margin-bottom: 8px; }
.user-avatar { width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #fff; flex-shrink: 0; }
.user-info { display: flex; flex-direction: column; overflow: hidden; }
.user-name { font-size: 12px; font-weight: 600; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 10px; color: #a5b4fc; font-weight: 500; letter-spacing: 0.05em; }
.logout-btn { display: flex; align-items: center; gap: 8px; width: 100%; padding: 8px 10px; border-radius: 8px; border: none; background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.7); cursor: pointer; font-size: 12px; transition: all 0.15s; }
.logout-btn:hover { background: rgba(255,255,255,0.2); color: #fff; }
.logout-btn-mini { display: flex; align-items: center; justify-content: center; padding: 8px; border-radius: 8px; border: none; background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.7); cursor: pointer; transition: all 0.15s; }
.logout-btn-mini:hover { background: rgba(255,255,255,0.2); color: #fff; }

/* ===== MAIN CONTENT ===== */
.main-content { transition: margin-left 0.25s ease; min-height: 100vh; background: #f3f4f6; }
.main-expanded { margin-left: 220px; }
.main-collapsed { margin-left: 60px; }

.topbar {
  position: sticky; top: 0; z-index: 50;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 28px;
  height: 64px; display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.topbar-left { display: flex; flex-direction: column; }
.page-title { font-size: 17px; font-weight: 700; color: #1f2937; }
.page-breadcrumb { font-size: 11px; color: #9ca3af; }
.topbar-right { display: flex; align-items: center; gap: 10px; }
.date-chip { display: flex; align-items: center; gap: 6px; padding: 6px 12px; background: #f3f4f6; border-radius: 20px; font-size: 11px; color: #6b7280; text-transform: capitalize; border: 1px solid #e5e7eb; }

.page-body { padding: 24px 28px; }

/* ===== FADE IN ===== */
.fade-in { animation: fadeIn 0.2s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

/* ===== STATS ===== */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }
.stat-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 18px; display: flex; align-items: center; gap: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.stat-green { border-left: 4px solid #10b981; }
.stat-blue { border-left: 4px solid #3b82f6; }
.stat-yellow { border-left: 4px solid #f59e0b; }
.stat-red { border-left: 4px solid #ef4444; }
.stat-icon { font-size: 24px; }
.stat-data { display: flex; flex-direction: column; }
.stat-number { font-size: 26px; font-weight: 700; color: #111827; line-height: 1; }
.stat-label { font-size: 11px; color: #6b7280; margin-top: 2px; }

/* ===== TWO COL ===== */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

/* ===== PANELS ===== */
.panel { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.panel-header { padding: 14px 18px; border-bottom: 1px solid #f3f4f6; display: flex; justify-content: space-between; align-items: center; }
.panel-title { font-size: 13px; font-weight: 600; color: #374151; }
.panel-link { font-size: 12px; color: #4f46e5; background: none; border: none; cursor: pointer; }
.panel-link:hover { text-decoration: underline; }

/* ===== ACTIVITY ===== */
.activity-list { padding: 8px 0; }
.activity-item { display: flex; align-items: center; gap: 12px; padding: 10px 18px; transition: background 0.15s; }
.activity-item:hover { background: #f9fafb; }
.activity-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-green { background: #10b981; }
.dot-blue { background: #3b82f6; }
.activity-text { flex: 1; display: flex; flex-direction: column; }
.activity-name { font-size: 12px; font-weight: 600; color: #111827; }
.activity-desc { font-size: 11px; color: #9ca3af; }
.activity-time { font-size: 11px; color: #d1d5db; }

/* ===== REVIEW LIST ===== */
.review-list { padding: 8px 0; }
.review-item { display: flex; align-items: center; gap: 10px; padding: 10px 18px; cursor: pointer; transition: background 0.15s; }
.review-item:hover { background: #f9fafb; }
.review-badge { font-size: 9px; font-weight: 700; color: #d97706; background: #fef3c7; border: 1px solid #fde68a; padding: 2px 6px; border-radius: 4px; white-space: nowrap; }
.review-info { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.review-name { font-size: 12px; font-weight: 600; color: #111827; }
.review-preview { font-size: 11px; color: #9ca3af; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.review-arrow { color: #d1d5db; }

/* ===== TOOLBAR ===== */
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; gap: 12px; flex-wrap: wrap; }
.search-box { display: flex; align-items: center; gap: 8px; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px 12px; flex: 1; max-width: 340px; }
.search-box svg { color: #9ca3af; flex-shrink: 0; }
.search-input { background: none; border: none; color: #374151; font-size: 13px; width: 100%; outline: none; }
.search-input::placeholder { color: #9ca3af; }
.toolbar-actions { display: flex; align-items: center; gap: 10px; }
.filter-select { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px 12px; color: #374151; font-size: 13px; cursor: pointer; outline: none; }

/* ===== BUTTONS ===== */
.btn-primary { display: flex; align-items: center; gap: 6px; padding: 9px 16px; background: #4f46e5; color: #fff; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s; }
.btn-primary:hover { background: #4338ca; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-secondary { display: flex; align-items: center; gap: 6px; padding: 9px 16px; background: #fff; color: #374151; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.15s; }
.btn-secondary:hover { background: #f3f4f6; }
.btn-ghost { padding: 9px 16px; background: none; color: #6b7280; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 13px; cursor: pointer; transition: all 0.15s; }
.btn-ghost:hover { background: #f3f4f6; }
.link-btn { background: none; border: none; color: #4f46e5; font-size: 12px; cursor: pointer; padding: 0; }
.link-btn:hover { text-decoration: underline; }

/* ===== DATA TABLE ===== */
.data-table-wrap { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.data-table { width: 100%; border-collapse: collapse; }
.data-table thead th { padding: 12px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid #f3f4f6; background: #f9fafb; }
.table-row { transition: background 0.15s; }
.table-row:hover { background: #f9fafb; }
.data-table td { padding: 12px 16px; font-size: 13px; color: #6b7280; border-bottom: 1px solid #f3f4f6; }
.loading-row, .empty-row { text-align: center; padding: 32px 16px !important; color: #9ca3af !important; }
.loading-row { display: flex; align-items: center; justify-content: center; gap: 10px; }

.user-cell { display: flex; align-items: center; gap: 10px; }
.mini-avatar { width: 30px; height: 30px; border-radius: 8px; background: #e0e7ff; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: #4f46e5; flex-shrink: 0; }
.cell-name { font-size: 13px; font-weight: 600; color: #111827; }
.cell-mono { font-size: 12px; color: #6b7280; }
.cell-email { font-size: 12px; color: #9ca3af; }
.cell-dim { color: #d1d5db; }

.status-badge { font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; }
.status-active { background: #d1fae5; color: #065f46; }
.status-inactive { background: #fee2e2; color: #991b1b; }
.status-warning { background: #fef3c7; color: #92400e; }

.time-badge { font-size: 11px; padding: 3px 8px; border-radius: 4px; }
.time-entrada { background: #dbeafe; color: #1d4ed8; }
.time-salida { background: #d1fae5; color: #065f46; }
.time-pending { color: #d1d5db; }
.hours-badge { font-size: 12px; color: #d97706; font-weight: 600; }
.has-report { color: #059669; font-size: 12px; font-weight: 600; }
.no-report { color: #d1d5db; font-size: 12px; }

.action-btns { display: flex; gap: 6px; }
.action-btn { width: 28px; height: 28px; border-radius: 6px; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
.action-edit { background: #e0e7ff; color: #4f46e5; }
.action-edit:hover { background: #c7d2fe; }
.action-deactivate { background: #fee2e2; color: #dc2626; }
.action-deactivate:hover { background: #fecaca; }
.action-activate { background: #d1fae5; color: #059669; }
.action-activate:hover { background: #a7f3d0; }

.map-btn { display: flex; align-items: center; gap: 4px; padding: 4px 8px; background: #dbeafe; color: #2563eb; border: none; border-radius: 6px; font-size: 11px; cursor: pointer; transition: all 0.15s; }
.map-btn:hover { background: #bfdbfe; }

/* ===== KANBAN ===== */
.kanban-board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; align-items: start; }
.kanban-col { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.kanban-header { padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; }
.kanban-header-yellow { background: #fffbeb; border-bottom: 2px solid #f59e0b; }
.kanban-header-green { background: #f0fdf4; border-bottom: 2px solid #10b981; }
.kanban-header-red { background: #fff5f5; border-bottom: 2px solid #ef4444; }
.kanban-title { font-size: 12px; font-weight: 700; color: #374151; }
.kanban-count { font-size: 11px; font-weight: 700; color: #6b7280; background: #f3f4f6; padding: 1px 7px; border-radius: 10px; border: 1px solid #e5e7eb; }
.kanban-cards { padding: 10px; display: flex; flex-direction: column; gap: 8px; min-height: 80px; }
.kanban-empty { text-align: center; padding: 20px; font-size: 12px; color: #d1d5db; }
.kanban-card { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; cursor: pointer; transition: all 0.15s; }
.kanban-card:hover { border-color: #a5b4fc; box-shadow: 0 2px 8px rgba(79,70,229,0.08); transform: translateY(-1px); }
.kanban-card-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.kanban-id { font-size: 11px; color: #9ca3af; }
.kanban-date { font-size: 11px; color: #9ca3af; }
.kanban-pasante { font-size: 13px; font-weight: 600; color: #111827; margin-bottom: 4px; }
.kanban-preview { font-size: 11px; color: #6b7280; line-height: 1.5; margin-bottom: 8px; }
.kanban-footer { border-top: 1px solid #e5e7eb; padding-top: 8px; }
.kanban-action { font-size: 11px; color: #4f46e5; }

/* ===== MODALES ===== */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 200; display: flex; align-items: center; justify-content: center; padding: 20px; backdrop-filter: blur(2px); }
.modal { background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; width: 100%; max-width: 540px; overflow: hidden; animation: modalIn 0.2s ease; box-shadow: 0 20px 60px rgba(0,0,0,0.15); }
.modal-lg { max-width: 600px; }
.modal-xl { max-width: 760px; max-height: 80vh; display: flex; flex-direction: column; }
@keyframes modalIn { from { opacity: 0; transform: scale(0.96); } to { opacity: 1; transform: scale(1); } }
.modal-header { padding: 18px 22px; border-bottom: 1px solid #f3f4f6; display: flex; justify-content: space-between; align-items: flex-start; background: #4f46e5; }
.modal-header-purple { background: #4f46e5; }
.modal-title { font-size: 15px; font-weight: 700; color: #fff; }
.modal-id { color: rgba(255,255,255,0.6); }
.modal-subtitle { font-size: 12px; color: #c7d2fe; margin-top: 2px; }
.modal-close { background: none; border: none; color: rgba(255,255,255,0.7); cursor: pointer; font-size: 20px; line-height: 1; padding: 0; transition: color 0.15s; }
.modal-close:hover { color: #fff; }
.modal-body { padding: 20px 22px; overflow-y: auto; }
.modal-footer { padding: 14px 22px; border-top: 1px solid #f3f4f6; display: flex; justify-content: flex-end; gap: 10px; background: #f9fafb; }

/* ===== FORMS ===== */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 16px; }
.form-field { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }
.form-field:last-child { margin-bottom: 0; }
.form-label { font-size: 12px; font-weight: 600; color: #374151; }
.form-input { background: #fff; border: 1px solid #d1d5db; border-radius: 8px; padding: 9px 12px; color: #111827; font-size: 13px; outline: none; transition: border 0.15s; width: 100%; }
.form-input:focus { border-color: #4f46e5; box-shadow: 0 0 0 3px rgba(79,70,229,0.1); }
.form-input::placeholder { color: #9ca3af; }
.form-input-disabled { background: #f9fafb; color: #9ca3af; cursor: not-allowed; }
.form-error { background: #fee2e2; border: 1px solid #fecaca; color: #dc2626; font-size: 12px; padding: 8px 12px; border-radius: 8px; margin-top: 8px; }
textarea.form-input { resize: vertical; }

.report-content { margin-bottom: 16px; }
.report-text { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; font-size: 13px; color: #374151; line-height: 1.6; white-space: pre-wrap; }

.decision-btns { display: flex; gap: 10px; }
.decision-btn { flex: 1; padding: 10px; border-radius: 8px; border: 2px solid transparent; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.15s; }
.decision-approve-active { background: #d1fae5; border-color: #10b981; color: #065f46; }
.decision-reject-active { background: #fee2e2; border-color: #ef4444; color: #991b1b; }
.decision-inactive { background: #f3f4f6; color: #9ca3af; border-color: transparent; }
.decision-inactive:hover { background: #e5e7eb; }

/* ===== HISTORIAL SUMMARY ===== */
.historial-summary { display: flex; gap: 16px; margin-top: 16px; padding: 14px; background: #f3f4f6; border-radius: 10px; border: 1px solid #e5e7eb; }
.summary-item { flex: 1; text-align: center; }
.summary-label { display: block; font-size: 11px; color: #9ca3af; margin-bottom: 4px; }
.summary-value { display: block; font-size: 20px; font-weight: 700; color: #4f46e5; }

/* ===== GPS MODAL ===== */
.gps-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.gps-card { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 16px; text-align: center; }
.gps-entrada { border-top: 3px solid #3b82f6; }
.gps-salida { border-top: 3px solid #10b981; }
.gps-no-salida { border-top: 3px solid #d1d5db; }
.gps-icon { font-size: 24px; margin-bottom: 8px; }
.gps-label { font-size: 12px; font-weight: 700; color: #374151; margin-bottom: 10px; }
.gps-coords { display: flex; flex-direction: column; gap: 4px; font-size: 11px; color: #6b7280; margin-bottom: 12px; }
.gps-link { font-size: 11px; color: #2563eb; text-decoration: none; }
.gps-link:hover { text-decoration: underline; }

/* ===== SPINNER ===== */
.spinner { width: 18px; height: 18px; border: 2px solid #e5e7eb; border-top-color: #4f46e5; border-radius: 50%; animation: spin 0.7s linear infinite; display: inline-block; }
.loading-center { display: flex; justify-content: center; padding: 40px; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ===== EMPTY STATES ===== */
.empty-state-sm { padding: 24px; text-align: center; font-size: 13px; color: #9ca3af; }

/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .two-col { grid-template-columns: 1fr; }
  .kanban-board { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .main-expanded, .main-collapsed { margin-left: 0; }
  .sidebar { display: none; }
  .stats-grid { grid-template-columns: 1fr 1fr; }
  .page-body { padding: 16px; }
}
</style>