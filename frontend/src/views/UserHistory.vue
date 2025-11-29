<template>
  <div>
    <AppNavbar />
    <div class="container-fluid mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1><i class="fas fa-home me-2 text-primary"></i>Past Reservations</h1>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-secondary" role="status"></div>
      </div>

      <div v-else-if="history.length === 0" class="text-center py-5 text-muted">
        <i class="fas fa-folder-open fa-4x mb-3"></i>
        <p class="lead">No past reservations found.</p>
        <router-link to="/user/home" class="btn btn-secondary mt-3">
          Go to Home
        </router-link>
      </div>

      <div v-else class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Lot</th>
              <th>Address</th>
              <th>Vehicle</th>
              <th>Entry Time</th>
              <th>Exit Time</th>
              <th>Total Cost (₹)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="res in history" :key="res.reservation_id">
              <td>{{ res.reservation_id }}</td>
              <td>{{ res.lot_name }}</td>
              <td>{{ res.address }}</td>
              <td>{{ res.vehicle_number }}</td>
              <td>{{ formatDateTime(res.entry_time) }}</td>
              <td>{{ formatDateTime(res.exit_time) }}</td>
              <td><strong>{{ res.total_cost.toFixed(2) }}</strong></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/Navbar.vue'
import api from '@/api/axios'

export default {
  name: 'UserHistory',
  components: { AppNavbar },
  data() {
    return {
      history: [],
      loading: true
    }
  },
  async created() {
    await this.fetchHistory()
  },
  methods: {
    async fetchHistory() {
      this.loading = true
      try {
        const res = await api.get('/api/user/history')
        this.history = res.data.past_reservations
      } catch (error) {
        console.error('Error loading history:', error)
      } finally {
        this.loading = false
      }
    },
    formatDateTime(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleString('en-IN')
    }
  }
}
</script>
