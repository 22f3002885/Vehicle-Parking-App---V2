<template>
  <div>
    <AppNavbar />
    <div class="container-fluid mt-4">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card shadow-sm">
            <div class="card-header" :class="spotStatus === 'O' ? 'bg-danger text-white' : 'bg-success text-white'">
              <div class="d-flex justify-content-between align-items-center">
                <h4 class="mb-0">
                  <i :class="spotStatus === 'O' ? 'fas fa-car' : 'fas fa-parking'" class="me-2"></i>
                  Spot {{ spotId }} - {{ spotStatus === 'O' ? 'Occupied' : 'Available' }}
                </h4>
                <router-link :to="`/admin/lots/${lotId}/spots`" class="btn btn-sm" :class="spotStatus === 'O' ? 'btn-light' : 'btn-outline-light'">
                  <i class="fas fa-arrow-left me-1"></i>Back to Spots
                </router-link>
              </div>
            </div>
            <div class="card-body">
              <!-- Loading -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border" :class="spotStatus === 'O' ? 'text-danger' : 'text-success'" role="status"></div>
              </div>

              <!-- Error -->
              <div v-else-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <!-- Occupied Spot Details -->
              <div v-else-if="spotStatus === 'O'">
                <div class="row g-4">
                  <div class="col-md-6">
                    <div class="info-card bg-light p-4 rounded">
                      <h6><i class="fas fa-car text-primary me-2"></i>Reservation Details</h6>
                      <hr>
                      <p><strong>Vehicle Number:</strong> {{ spotDetails.vehicle_number }}</p>
                      <p><strong>Entry Time:</strong> {{ formatDate(spotDetails.entry_time) }}</p>
                      <p><strong>User ID:</strong> {{ spotDetails.user_id }}</p>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="info-card bg-light p-4 rounded">
                      <h6><i class="fas fa-info-circle text-info me-2"></i>Spot Info</h6>
                      <hr>
                      <p><strong>Status:</strong> <span class="badge bg-danger">Occupied</span></p>
                      <p><strong>Spot ID:</strong> {{ spotId }}</p>
                      <p><strong>Lot ID:</strong> {{ lotId }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Available Spot -->
              <div v-else class="text-center py-5">
                <i class="fas fa-parking fa-5x text-success mb-4"></i>
                <div class="mb-4">
                  <h3 class="text-success">Spot Available</h3>
                  <p class="text-muted lead">This spot is free and ready for parking.</p>
                </div>
                <div class="alert alert-warning">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  <strong>Admin Action:</strong> You can permanently delete this spot to reduce lot capacity.
                </div>
              </div>
            </div>
            <div class="card-footer" v-if="spotStatus === 'A'">
              <div class="d-flex justify-content-center">
                <button 
                  class="btn btn-danger btn-lg px-5" 
                  @click="deleteSpot"
                >
                  <i class="fas fa-trash me-2"></i>Delete This Spot
                </button>
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
  name: 'AdminSpotDetail',
  components: { AppNavbar },
  data() {
    return {
      spotId: null,
      lotId: null,
      spotStatus: null,
      spotDetails: {},
      loading: true,
      error: null
    }
  },
  async created() {
    this.spotId = this.$route.params.spotId
    // Extract lotId from previous route or set default
    const lotIdMatch = this.$route.fullPath.match(/\/lots\/(\d+)/)
    this.lotId = lotIdMatch ? lotIdMatch[1] : 'N/A'
    await this.fetchSpotDetails()
  },
  methods: {
    async fetchSpotDetails() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get(`/api/admin/spots/${this.spotId}`)
        
        if (response.data.message === 'Spot is available.') {
          this.spotStatus = 'A'
        } else {
          this.spotStatus = 'O'
          this.spotDetails = response.data
        }
      } catch (error) {
        console.error('Failed to fetch spot details:', error)
        this.error = 'Failed to load spot details'
      } finally {
        this.loading = false
      }
    },
    async deleteSpot() {
      if (!confirm('Delete this available spot? This cannot be undone and will reduce lot capacity.')) return
      
      try {
        await api.delete(`/api/admin/spots/${this.spotId}`)
        alert('Spot deleted successfully')
        this.$router.push(`/admin/lots/${this.lotId}/spots`)
      } catch (error) {
        console.error('Failed to delete spot:', error)
        alert(error.response?.data?.message || 'Failed to delete spot')
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('en-IN')
    }
  }
}
</script>

<style scoped>
.info-card {
  border-left: 4px solid #dee2e6;
}
</style>
