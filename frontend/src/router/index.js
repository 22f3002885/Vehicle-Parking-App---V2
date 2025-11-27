import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashBoardView.vue'      // corrected import
import UserDashboard from '../views/UserDashBoardView.vue' 

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/admin-dashboard', component: AdminDashboard },  
  { path: '/user-dashboard', component: UserDashboard },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = !!localStorage.getItem('auth_token')

  if (authRequired && !loggedIn) {
    return next('/login')
  }
  next()
})


export default router
