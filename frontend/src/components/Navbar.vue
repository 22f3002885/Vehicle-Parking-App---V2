<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container-fluid">
      <!-- Brand - Plain text only -->
      <span class="navbar-brand fw-bold">
        <i class="fas fa-parking me-2 text-primary"></i>ParkEase
      </span>

      <!-- Navigation Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <!-- Admin Links -->
          <template v-if="isAdmin">
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/admin/dashboard' }" to="/admin/dashboard">
                <i class="fas fa-home me-1"></i>Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/admin/users' }" to="/admin/users">
                <i class="fas fa-users me-1"></i>Users
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/admin/reservations' }" to="/admin/reservations">
                <i class="fas fa-calendar-check me-1"></i>Reservations
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/admin/summary' }" to="/admin/summary">
                <i class="fas fa-chart-bar me-1"></i>Summary
              </router-link>
            </li>
          </template>

          <!-- User Links -->
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/user/dashboard' }" to="/user/dashboard">
                <i class="fas fa-home me-1"></i>Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/user/lots' }" to="/user/lots">
                <i class="fas fa-parking me-1"></i>Parking Lots
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/user/history' }" to="/user/history">
                <i class="fas fa-history me-1"></i>History
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/user/summary' }" to="/user/summary">
                <i class="fas fa-chart-pie me-1"></i>Summary
              </router-link>
            </li>
          </template>
        </ul>

        <!-- Right Side: Logout Button Only -->
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="logout">
              <i class="fas fa-sign-out-alt me-1"></i> Logout
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar',
  computed: {
    isAdmin() {
      const roles = JSON.parse(localStorage.getItem('user_roles') || '[]')
      return roles.includes('admin')
    },
  },
  methods: {
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>
