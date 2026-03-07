import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Pantalla pública de quiosco (página de inicio)
    {
      path: '/',
      name: 'kiosk',
      component: () => import('../views/KioskView.vue'),
    },

    // Login — solo para usuarios NO logueados
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true }
    },

    // Panel del Pasante
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true, allowedRoles: ['PASANTE'] }
    },

    // Panel del Director / Decano
    {
      path: '/director',
      name: 'director-dashboard',
      component: () => import('../views/DirectorDashboard.vue'),
      meta: { requiresAuth: true, allowedRoles: ['DIRECTOR', 'DECANO'] }
    },

    // Gestión de usuarios (Director y Decano)
    {
      path: '/usuarios',
      name: 'admin-usuarios',
      component: () => import('../views/AdminUsuarios.vue'),
      meta: { requiresAuth: true, allowedRoles: ['DIRECTOR', 'DECANO'] }
    },

    // Panel del Supervisor (COORDINADOR)
    {
      path: '/supervisor',
      name: 'supervisor-dashboard',
      component: () => import('../views/SupervisorDashboard.vue'),
      meta: { requiresAuth: true, allowedRoles: ['COORDINADOR'] }
    },
  ]
})

// === GUARDIÁN DE RUTAS ===
router.beforeEach((to, from) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.token
  const userRole = authStore.user?.rol

  // Helper: a qué ruta pertenece cada rol
  const rutaPorRol = (rol) => {
    if (rol === 'PASANTE') return '/dashboard'
    if (rol === 'COORDINADOR') return '/supervisor'
    if (['DIRECTOR', 'DECANO'].includes(rol)) return '/director'
    return '/login'
  }

  // 1. Ruta pública del quiosco — siempre accesible, sin redirección
  if (to.name === 'kiosk') return true

  // 2. Si ya está logueado e intenta ir al Login, lo mandamos a su panel
  if (to.meta.requiresGuest && isAuthenticated) {
    return rutaPorRol(userRole)
  }

  // 3. Ruta protegida sin sesión → al login
  if (to.meta.requiresAuth && !isAuthenticated) {
    return '/login'
  }

  // 4. Ruta protegida pero con rol incorrecto → a su panel correcto
  if (to.meta.requiresAuth && to.meta.allowedRoles) {
    if (!to.meta.allowedRoles.includes(userRole)) {
      return rutaPorRol(userRole)
    }
  }

  // 5. Todo OK
  return true
})

export default router