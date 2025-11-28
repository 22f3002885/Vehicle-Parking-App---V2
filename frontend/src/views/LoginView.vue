<template>
  <div class="container mt-4">
    <home-navbar />
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input v-model="email" type="email" class="form-control" id="email" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" id="password" required />
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import HomeNavbar from '@/components/HomeNavbar.vue';
import api from '../api/axios'  // your preconfigured Axios instance

export default {
  name: 'LoginView',
  components: { HomeNavbar },
  data() {
    return {
      email: '',
      password: '',
      error: null,
    }
  },
  methods: {
    async handleLogin() {
      this.error = null
      try {
        const response = await api.post('/api/login', {
          email: this.email,
          password: this.password,
        })

        const userDetails = response.data.user_details
        const roles = userDetails.roles || []

        localStorage.setItem('auth_token', userDetails.auth_token)
        localStorage.setItem('user_email', userDetails.email)
        localStorage.setItem('user_roles', JSON.stringify(roles))

        if (roles.includes('admin')) {
          this.$router.push('/admin/dashboard')
        } else {
          this.$router.push('/user/dashboard')
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Login failed'
      }
    },
  },
}
</script>
