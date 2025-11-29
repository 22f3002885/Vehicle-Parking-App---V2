<template>
  <div>
    <AppNavbar />
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-sm">
            <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">
                <i class="fas fa-parking me-2"></i>Reserve Spot - {{ lot.name }}
              </h5>
              <router-link :to="'/user/lots'" class="btn btn-light btn-sm">
                <i class="fas fa-arrow-left me-1"></i>Back to Lots
              </router-link>
            </div>
            <div class="card-body">
              <form @submit.prevent="submitForm" novalidate>
                <!-- Lot info -->
                <p><strong>Address:</strong> {{ lot.address }}</p>
                <p><strong>Price per hour:</strong> ₹{{ lot.price_per_hour }}</p>
                <p>
                  <strong>Available spots:</strong>
                  <span :class="lot.available_spots > 0 ? 'text-success' : 'text-danger'">
                    {{ lot.available_spots }}
                  </span>
                </p>

                <!-- Vehicle Number Input -->
                <div class="mb-3">
                  <label for="vehicleNumber" class="form-label">Vehicle Number</label>
                  <input
                    id="vehicleNumber"
                    v-model.trim="vehicleNumber"
                    type="text"
                    class="form-control"
                    placeholder="Enter vehicle number"
                    required
                  />
                  <div v-if="submitted && !vehicleNumber" class="form-text text-danger">
                    Vehicle number is required
                  </div>
                </div>

                <button type="submit" class="btn btn-success w-100" :disabled="submitLoading">
                  <span v-if="submitLoading" class="spinner-border spinner-border-sm me-2"></span>
                  Book Spot
                </button>
              </form>
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
  name: 'UserBookSpot',
  components: { AppNavbar },
  data() {
    return {
      lotId: null,
      lot: {
        name: '',
        address: '',
        price_per_hour: 0,
        available_spots: 0
      },
      vehicleNumber: '',
      submitted: false,
      submitLoading: false
    }
  },
  async created() {
    this.lotId = this.$route.params.lot_id
    await this.fetchParkingLot()
  },
  methods: {
    async fetchParkingLot() {
      try {
        const response = await api.get(`/api/user/parkinglots/${this.lotId}`)
        this.lot = response.data.lot
      } catch (error) {
        console.error('Failed to fetch parking lot:', error)
        alert('Failed to load parking lot information.')
        this.$router.push('/user/lots')
      }
    },
    async submitForm() {
      this.submitted = true
      if (!this.vehicleNumber) {
        return
      }
      this.submitLoading = true
      try {
        await api.post(`/api/user/reserve/${this.lotId}`, {
          vehicle_number: this.vehicleNumber
        })
        alert('Spot reserved successfully!')
        this.$router.push('/user/dashboard')
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to reserve spot.')
      } finally {
        this.submitLoading = false
      }
    }
  }
}
</script>
