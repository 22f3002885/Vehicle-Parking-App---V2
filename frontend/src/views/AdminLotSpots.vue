<template>
  <div>
    <AppNavbar />
    <div class="container-fluid mt-4">
      <!-- Header with Back button -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <router-link to="/admin/dashboard" class="btn btn-secondary me-2">
            <i class="fas fa-arrow-left me-1"></i> Back to Dashboard
          </router-link>
          <h1>Spots - {{ lotName }}</h1>
        </div>
        <div class="text-muted">
          Total Spots: {{ totalSpots }} | 
          Available: <span class="badge bg-success">{{ availableSpots }}</span> | 
          Occupied: <span class="badge bg-danger">{{ occupiedSpots }}</span>
        </div>
      </div>

      <!-- Spots Grid -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading spots...</span>
        </div>
      </div>

      <div v-else-if="spots.length === 0" class="alert alert-info text-center">
        No spots found for this parking lot
      </div>

      <div v-else class="row g-3">
        <div 
          v-for="spot in spots" 
          :key="spot.id" 
          class="col-xl-2 col-lg-3 col-md-4 col-sm-6"
        >
          <router-link 
            :to="`/admin/lots/${lotId}/spots/${spot.id}`"
            class="spot-card h-100 p-3 text-center border rounded-3 shadow-sm position-relative text-decoration-none d-block"
            :class="{
              'bg-success text-white border-success': spot.status === 'A',
              'bg-danger text-white border-danger': spot.status === 'O'
            }"
          >
            <!-- FIXED: Badge with proper contrast -->
            <div class="position-absolute top-0 end-0 m-2">
              <span 
                class="badge rounded-pill fs-2rem"
                :class="{
                  'bg-white text-success shadow': spot.status === 'A',
                  'bg-white text-danger shadow': spot.status === 'O'
                }"
              >
                {{ spot.status }}
              </span>
            </div>

            <!-- Spot Number -->
            <div class="spot-number h2 mb-1 mt-4">{{ spot.id }}</div>
            
            <!-- Status Text -->
            <div class="h6 mb-3 fw-bold">
              {{ spot.status === 'A' ? 'Free' : 'Taken' }}
            </div>
            
            <!-- Action Hint -->
            <div class="small opacity-75">
              {{ spot.status === 'A' ? 'Click to delete' : 'Click for details' }}
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/Navbar.vue'
import api from '@/api/axios'

export default {
  name: 'AdminLotSpots',
  components: { AppNavbar },
  data() {
    return {
      lotId: null,
      lotName: '',
      spots: [],
      loading: true,
      totalSpots: 0,
      availableSpots: 0,
      occupiedSpots: 0
    }
  },
  async created() {
    this.lotId = this.$route.params.lotId
    await this.fetchSpots()
  },
  methods: {
    async fetchSpots() {
      this.loading = true
      try {
        const response = await api.get(`/api/admin/lots/${this.lotId}`)
        const lotData = response.data.lot
        const spotsData = response.data.spots || []
        
        this.lotName = lotData.name
        this.spots = spotsData
        
        this.totalSpots = spotsData.length
        this.availableSpots = spotsData.filter(s => s.status === 'A').length
        this.occupiedSpots = spotsData.filter(s => s.status === 'O').length
        
      } catch (error) {
        console.error('Failed to fetch spots:', error)
        alert('Failed to load spots')
        this.$router.push('/admin/dashboard')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
