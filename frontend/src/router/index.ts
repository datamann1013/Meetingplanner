import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Home from '../views/Home.vue'
import LoginView from '../views/LoginView.vue'


const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (!authStore.isInitialized && localStorage.getItem('token')) {
    authStore.init()
  }
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } 

  else if (to.meta.requiresBoard && !authStore.isBoardMember) {
    next('/')
  } 

  else if (to.name === 'Login' && authStore.isAuthenticated) {
    next('/')
  } 
  else {
    next()
  }
})

export default router