<template>
  <div>
    <AppNavbar />
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-sm">
            <div class="card-header bg-warning text-dark d-flex justify-content-between align-items-center">
              <h5 class="mb-0">
                <i class="fas fa-sign-out-alt me-2"></i>Release Parking Spot
              </h5>
              <router-link to="/user/dashboard" class="btn btn-light btn-sm">
                <i class="fas fa-arrow-left me-1"></i>Back to Home
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-warning" role="status"></div>
              </div>
              <div v-else-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              <div v-else>
                <form @submit.prevent="confirmRelease" novalidate>
                  <div class="mb-3">
                    <label class="form-label">Vehicle Number</label>
                    <input type="text" class="form-control" :value="reservation.vehicle_number" readonly />
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Entry Time</label>
                    <input type="text" class="form-control" :value="formatDate(reservation.entry_time)" readonly />
                  </div>
                  
                  <div v-if="reservation.exit_time" class="mb-3">
                    <label class="form-label">Exit Time</label>
                    <input type="text" class="form-control" :value="formatDate(reservation.exit_time)" readonly />
                  </div>

                  <div v-if="reservation.total_cost !== undefined" class="mb-3">
                    <label class="form-label">Total Cost (₹)</label>
                    <input type="text" class="form-control fw-bold" :value="reservation.total_cost" readonly />
                  </div>

                  <button type="submit" class="btn btn-warning w-100" :disabled="submitLoading || reservation.exit_time">
                    <span v-if="submitLoading" class="spinner-border spinner-border-sm me-2"></span>
                    {{ reservation.exit_time ? 'Spot Released' : 'Confirm Release' }}
                  </button>
                </form>
              </div>
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
  name: 'UserReleaseConfirm',
  components: { AppNavbar },
  data() {
    return {
      reservationId: null,
      reservation: null,
      loading: true,
      error: null,
      submitLoading: false
    }
  },
  async created() {
    this.reservationId = this.$route.params.reservation_id
    await this.loadReservationDetails()
  },
  methods: {
    async loadReservationDetails() {
      this.loading = true
      this.error = null
      try {
        const res = await api.get('/api/user/dashboard')
        const active = res.data.active_reservations
        this.reservation = active.find(r => r.reservation_id === parseInt(this.reservationId))
        if (!this.reservation) {
          this.error = 'Reservation not found or already released.'
        }
      } catch {
        this.error = 'Failed to fetch reservation details.'
      } finally {
        this.loading = false
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString('en-IN')
    },
    async confirmRelease() {
      this.submitLoading = true
      try {
        const res = await api.post(`/api/user/release/${this.reservationId}`)
        this.reservation = res.data.reservation_summary
        alert('Spot released successfully!\nTotal cost: ₹' + this.reservation.total_cost)
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to release spot.')
      } finally {
        this.submitLoading = false
      }
    }
  }
}
</script>
