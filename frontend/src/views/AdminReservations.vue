<template>
  <div>
    <AppNavbar />
    <div class="container-fluid mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Reservations Management</h1>
      </div>

      <div class="card shadow-sm">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Lot Name</th>
                  <th>Vehicle Number</th>
                  <th>Entry Time</th>
                  <th>Exit Time</th>
                  <th>Total Cost</th>
                  <th>Address</th>
                  <th>User ID</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="loading">
                  <td colspan="9" class="text-center py-4">
                    <div class="spinner-border" role="status">
                      <span class="visually-hidden">Loading...</span>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="reservations.length === 0">
                  <td colspan="9" class="text-center py-4 text-muted">
                    No reservations found
                  </td>
                </tr>
                <tr v-else v-for="reservation in reservations" :key="reservation.reservation_id">
                  <td>{{ reservation.reservation_id }}</td>
                  <td>
                    <strong>{{ reservation.lot_name }}</strong>
                  </td>
                  <td>{{ reservation.vehicle_number }}</td>
                  <td>{{ formatDate(reservation.entry_time) }}</td>
                  <td>
                    {{ reservation.exit_time ? formatDate(reservation.exit_time) : 'Active' }}
                  </td>
                  <td>₹{{ reservation.total_cost || 0 }}</td>
                  <td>{{ reservation.address }}</td>
                  <td>{{ reservation.user_id }}</td>
                  <td>
                    <span 
                      v-if="reservation.exit_time" 
                      class="badge bg-success"
                    >
                      Completed
                    </span>
                    <span 
                      v-else 
                      class="badge bg-warning"
                    >
                      Active
                    </span>
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
  name: 'AdminReservations',
  components: { AppNavbar },
  data() {
    return {
      reservations: [],
      loading: true
    }
  },
  async created() {
    await this.fetchReservations()
  },
  methods: {
    async fetchReservations() {
      this.loading = true
      try {
        const response = await api.get('/api/admin/reservations')
        this.reservations = response.data
      } catch (error) {
        console.error('Failed to fetch reservations:', error)
        alert('Failed to load reservations')
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('en-IN')
    }
  }
}
</script>
