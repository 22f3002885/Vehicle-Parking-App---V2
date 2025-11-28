<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container-fluid">
      <span class="navbar-brand fw-bold">
        <i class="fas fa-parking me-2 text-primary"></i>ParkEase
      </span>

      <!-- Navigation Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/login">
              <i class="fas fa-sign-in-alt me-1"></i>Login
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/register">
              <i class="fas fa-user-plus me-1"></i>Register
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'HomeNavbar'
}
</script>
