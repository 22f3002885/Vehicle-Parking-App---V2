<template>
  <div>
    <AppNavbar />
    <div class="container-fluid mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1><i class="fas fa-home me-2 text-primary"></i>My Active Bookings</h1>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <!-- Empty State -->
      <div v-else-if="activeReservations.length === 0" class="row justify-content-center">
        <div class="col-md-6 text-center py-5">
          <i class="fas fa-car fa-5x text-muted mb-4"></i>
          <h3 class="text-muted">No Active Bookings</h3>
          <p class="lead text-muted">Book a parking spot to get started</p>
          <router-link to="/user/lots" class="btn btn-primary btn">
            <i class="fas fa-parking me-2"></i>Find Parking
          </router-link>
        </div>
      </div>

      <!-- Active Reservations -->
      <div v-else class="row g-4">
        <div v-for="reservation in activeReservations" :key="reservation.reservation_id" class="col-lg-6 col-xl-4">
          <div class="card shadow-sm h-100 border-warning">
            <div class="card-header bg-warning text-dark">
              <div class="d-flex justify-content-between align-items-center">
                <h6 class="mb-0">
                  <i class="fas fa-map-marker-alt me-2"></i>{{ reservation.lot_name }}
                </h6>
                <span class="badge bg-warning text-dark">Active</span>
              </div>
            </div>
            <div class="card-body">
              <div class="row text-center">
                <div class="col-6 border-end">
                  <div class="h4 mb-0 fw-bold text-primary">{{ reservation.spot_id }}</div>
                  <small class="text-muted">Spot #</small>
                </div>
                <div class="col-6">
                  <div class="h5 mb-0 fw-bold">{{ reservation.vehicle_number }}</div>
                  <small class="text-muted">Vehicle</small>
                </div>
              </div>
              <hr>
              <p class="mb-1"><i class="fas fa-clock me-1"></i>{{ formatDate(reservation.entry_time) }}</p>
              <p class="mb-3"><i class="fas fa-map-pin me-2"></i>{{ reservation.address }}</p>
              <router-link 
                :to="`/user/reservations/${reservation.reservation_id}/release`" 
                class="btn btn-warning w-100"
              >
                <i class="fas fa-sign-out-alt me-2"></i>Release Spot
              </router-link>
            </div>
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
  name: 'UserHome',
  components: { AppNavbar },
  data() {
    return {
      activeReservations: [],
      loading: true
    }
  },
  async created() {
    await this.fetchActiveReservations()
  },
  methods: {
    async fetchActiveReservations() {
      this.loading = true
      try {
        const response = await api.get('/api/user/dashboard')
        this.activeReservations = response.data.active_reservations
      } catch (error) {
        console.error('Failed to fetch active reservations:', error)
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
