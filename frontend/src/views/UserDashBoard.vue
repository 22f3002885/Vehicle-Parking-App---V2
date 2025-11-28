<template>
  <div class="dashboard-content">
    <app-navbar />
    <h2>UserDashboard</h2>
  </div>
</template>

<script>
import AppNavbar from '@/components/Navbar.vue'

export default {
  name: 'UserDashboard',
  components: { AppNavbar }
}
</script>