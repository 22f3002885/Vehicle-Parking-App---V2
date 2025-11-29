<template>
  <div>
    <AppNavbar />
    <div class="container-fluid mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1><i class="fas fa-parking me-2 text-success"></i>Available Parking Lots</h1>
        <router-link to="/user/dashboard" class="btn btn-outline-secondary">
          <i class="fas fa-home me-1"></i>My Bookings
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status">
          <span class="visually-hidden">Loading parking lots...</span>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="parkingLots.length === 0" class="row justify-content-center">
        <div class="col-md-6 text-center py-5">
          <i class="fas fa-parking fa-5x text-muted mb-4"></i>
          <h3 class="text-muted">No Parking Lots Available</h3>
          <p class="lead text-muted">Check back later for available parking</p>
        </div>
      </div>

      <!-- Parking Lots Grid -->
      <div v-else class="row g-4">
        <div v-for="lot in parkingLots" :key="lot.lot_id" class="col-lg-4 col-xl-3">
          <div class="card shadow-sm h-100 border-success hover-lift">
            <div class="card-body text-center">
              <!-- Lot Header -->
              <div class="mb-4">
                <i class="fas fa-parking fa-3x text-success mb-2"></i>
                <h5 class="card-title fw-bold">{{ lot.name }}</h5>
              </div>

              <!-- Availability Badge -->
              <div class="mb-3">
                <span class="badge fs-6 px-3 py-2" :class="lot.available_spots > 0 ? 'bg-success' : 'bg-danger'">
                  {{ lot.available_spots }} {{ lot.available_spots === 1 ? 'spot' : 'spots' }} available
                </span>
              </div>

              <!-- Details -->
              <div class="text-start mb-4">
                <p class="mb-2">
                  <i class="fas fa-map-pin me-2 text-muted"></i>
                  <small>{{ lot.address }}</small>
                </p>
                <p class="mb-0 text-success fw-bold fs-5">
                  <i class="fas fa-rupee-sign me-1"></i>{{ lot.price_per_hour }}/hr
                </p>
              </div>

              <!-- Book Button -->
              <router-link 
                :to="`/user/lots/${lot.lot_id}/book`" 
                class="btn btn-success w-100 btn-lg"
                :class="{ 'disabled opacity-50': lot.available_spots === 0 }"
              >
                <i class="fas fa-car me-2"></i>
                {{ lot.available_spots > 0 ? 'Book Spot' : 'No Spots Available' }}
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
  name: 'UserParkingLots',
  components: { AppNavbar },
  data() {
    return {
      parkingLots: [],
      loading: true
    }
  },
  async created() {
    await this.fetchParkingLots()
  },
  methods: {
    async fetchParkingLots() {
      this.loading = true
      try {
        const response = await api.get('/api/user/parkinglots')
        this.parkingLots = response.data.parking_lots
      } catch (error) {
        console.error('Failed to fetch parking lots:', error)
        alert('Failed to load parking lots')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
