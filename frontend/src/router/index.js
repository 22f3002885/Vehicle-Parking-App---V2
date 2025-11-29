import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

import UserDashboard from '../views/UserDashBoard.vue'
import UserLotsView from '../views/UserLotsView.vue'
import UserBookings from '../views/UserBookings.vue'
import UserHistory from '../views/UserHistory.vue'
import UserSummary from '../views/UserSummary.vue'

import AdminDashboard from '../views/AdminDashBoard.vue' 
import AdminUsers from '../views/AdminUsers.vue'
import AdminReservations from '../views/AdminReservations.vue'
import AdminSummary from '../views/AdminSummary.vue'
import CreateLotView from '../views/AdminCreateLotView.vue'
import EditLotView from '../views/AdminEditLotView.vue'
import AdminLotSpots from '../views/AdminLotSpots.vue'
import AdminSpotDetail from '@/views/AdminSpotDetails.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/user/dashboard', component: UserDashboard },
  { path: '/user/lots', component: UserLotsView },
  { path: '/user/bookings', component: UserBookings },
  { path: '/user/history', component: UserHistory },
  { path: '/user/summary', component: UserSummary },
  { path: '/admin/dashboard', component: AdminDashboard },
  { path: '/admin/users', component: AdminUsers },
  { path: '/admin/reservations', component: AdminReservations },
  { path: '/admin/summary', component: AdminSummary },
  { path: '/admin/create-lot', component: CreateLotView },
  { path: '/admin/edit-lot/:lotId', component: EditLotView },
  { path: '/admin/lots/:lotId/spots', component: AdminLotSpots },
  { path: '/admin/lots/:lotId/spots/:spotId', component: AdminSpotDetail }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// src/router/index.js
router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register']
  const loggedIn = !!localStorage.getItem('auth_token')
  
  // Public pages: always allow
  if (publicPages.includes(to.path)) {
    next()
    return
  }
  
  // Protected pages: check auth
  if (!loggedIn) {
    next('/login')
    return
  }
  
  // Role-based redirects (after login saves token)
  const roles = JSON.parse(localStorage.getItem('user_roles') || '[]')
  const isAdmin = roles.includes('admin')
  
  if (to.path.startsWith('/admin') && !isAdmin) {
    next('/user/dashboard')
  } else if (to.path.startsWith('/user') && isAdmin) {
    next('/admin/dashboard')
  } else {
    next()
  }
})

export default router
