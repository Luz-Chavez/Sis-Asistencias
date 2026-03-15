import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      // requireGuest: Solo para usuarios NO logueados
      meta: { requiresGuest: true } 
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      // Solo el Pasante puede ver su propio panel
      meta: { requiresAuth: true, allowedRoles: ['PASANTE'] }
    },
    {
      path: '/director',
      name: 'director-dashboard',
      component: () => import('../views/DirectorDashboard.vue'),
      // Autoridades permitidas en este panel
      meta: { requiresAuth: true, allowedRoles: ['DIRECTOR', 'DECANO', 'COORDINADOR'] }
    },
    {
      path: '/usuarios',
      name: 'admin-usuarios',
      component: () => import('../views/AdminUsuarios.vue'),
      // Mismos permisos que el director/decano
      meta: { requiresAuth: true, allowedRoles: ['DIRECTOR', 'DECANO', 'COORDINADOR'] }
    }
  ]
})

// === EL GUARDIÁN DE RUTAS (Modo Moderno Vue 3) ===
router.beforeEach((to, from) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.token
  const userRole = authStore.user?.rol

  // 1. Si intenta ir al Login pero ya tiene la sesión iniciada
  if (to.meta.requiresGuest && isAuthenticated) {
    if (['DIRECTOR', 'DECANO', 'COORDINADOR'].includes(userRole)) {
      return '/director' // Lo mandamos a su panel
    }
    return '/dashboard' // Lo mandamos al panel de pasante
  }

  // 2. Si intenta entrar a una ruta protegida sin haber iniciado sesión
  if (to.meta.requiresAuth && !isAuthenticated) {
    return '/login'
  }

  // 3. Si intenta entrar a una ruta protegida pero NO tiene el rol correcto
  if (to.meta.requiresAuth && to.meta.allowedRoles) {
    if (!to.meta.allowedRoles.includes(userRole)) {
      // Lo devolvemos a su lugar correspondiente de forma silenciosa
      if (['DIRECTOR', 'DECANO', 'COORDINADOR'].includes(userRole)) {
        return '/director'
      } else if (userRole === 'PASANTE') {
        return '/dashboard'
      } else {
        // Si por alguna razón el rol está corrupto o no existe
        authStore.logout()
        return '/login'
      }
    }
  }

  // 4. Si pasa todas las pruebas de seguridad, le abrimos la puerta
  return true
})

export default router