<template>
  <div class="container mt-4">
    <h2>User Dashboard</h2>
    <p>Welcome, {{ email }}</p>
    <p>Your roles: {{ roles.join(', ') }}</p>
    <button class="btn btn-danger" @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  name: 'UserDashboard',
  data() {
    return {
      email: localStorage.getItem('user_email') || '',
      roles: JSON.parse(localStorage.getItem('user_roles') || '[]'),
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_email')
      localStorage.removeItem('user_roles')
      this.$router.push('/login')
    },
  },
}
</script>
