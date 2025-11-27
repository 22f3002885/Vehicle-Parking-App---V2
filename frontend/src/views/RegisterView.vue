<template>
  <div class="container mt-4">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input v-model="email" type="email" class="form-control" id="email" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" id="password" required />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
  </div>
</template>

<script>
import api from '../api/axios'

export default {
  name: 'RegisterView',
  data() {
    return {
      email: '',
      password: '',
      error: null,
      success: null,
    }
  },
  methods: {
    async handleRegister() {
      this.error = null
      this.success = null
      try {
        const response = await api.post('/api/register', {
          email: this.email,
          password: this.password,
        })
        this.success = 'Registration successful! Please login.'
        this.email = ''
        this.password = ''
      } catch (err) {
        this.error = err.response?.data?.message || 'Registration failed'
      }
    },
  },
}
</script>
