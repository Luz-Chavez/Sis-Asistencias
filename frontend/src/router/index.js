import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/DashboardView.vue')
    }
  ]
})

// GUARDIA DE NAVEGACIÓN (Protección de rutas)
router.beforeEach((to, from, next) => {
  // Verificamos si existe el token en el almacenamiento local
  const isAuthenticated = !!localStorage.getItem('token')

  if (to.name !== 'Login' && !isAuthenticated) {
    // Si intenta ir a cualquier lado sin estar logueado, lo mandamos al Login
    next({ name: 'Login' })
  } else if (to.name === 'Login' && isAuthenticated) {
    // Si intenta ir al Login pero ya tiene sesión abierta, lo mandamos al Dashboard
    next({ name: 'Dashboard' })
  } else {
    // Si todo está en orden, lo dejamos pasar
    next()
  }
})

export default router