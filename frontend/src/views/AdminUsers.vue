<template>
  <div>
    <AppNavbar />
    <div class="container-fluid mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Users Management</h1>
      </div>

      <div class="card shadow-sm">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Email</th>
                  <th>Roles</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="loading">
                  <td colspan="6" class="text-center py-4">
                    <div class="spinner-border" role="status">
                      <span class="visually-hidden">Loading...</span>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="users.length === 0">
                  <td colspan="6" class="text-center py-4 text-muted">
                    No users found
                  </td>
                </tr>
                <tr v-else v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>
                    <strong>{{ user.email }}</strong>
                  </td>
                  <td>
                    <span class="badge bg-primary">{{ user.roles.join(', ') }}</span>
                  </td>
                  <td>
                    <span class="badge bg-success">Active</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/Navbar.vue'
import api from '@/api/axios'

export default {
  name: 'AdminUsers',
  components: { AppNavbar },
  data() {
    return {
      users: [],
      loading: true
    }
  },
  async created() {
    await this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await api.get('/api/admin/users')
        this.users = response.data
      } catch (error) {
        console.error('Failed to fetch users:', error)
        alert('Failed to load users')
      } finally {
        this.loading = false
      }
    },
    async deleteUser(userId) {
      if (!confirm('Are you sure you want to delete this user?')) return
      try {
        await api.delete(`/api/admin/users/${userId}`)
        await this.fetchUsers()
      } catch (error) {
        console.error('Delete failed:', error)
        alert('Failed to delete user')
      }
    }
  }
}
</script>
