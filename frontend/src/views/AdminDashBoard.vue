<template>
  <div class="admin-dashboard">
    <AppNavbar />

    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Parking Lots</h1>
        <router-link to="/admin/create-lot" class="btn btn-success">
          <i class="fas fa-plus me-1"></i> Add Parking Lot
        </router-link>
      </div>

      <!-- Lots list -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="lots.length === 0" class="alert alert-info">
        No parking lots found. Click "Add Parking Lot" to create one.
      </div>

      <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div class="col" v-for="lot in lots" :key="lot.id">
          <div class="card h-100 shadow-sm">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ lot.name }}</h5>
              <p class="card-text mb-1">
                <strong>Price/hour:</strong> ₹{{ lot.price_per_hour }}
              </p>
              <p class="card-text mb-1">
                <strong>Address:</strong> {{ lot.address }}
              </p>
              <p class="card-text mb-1">
                <strong>Pincode:</strong> {{ lot.pincode }}
              </p>
              <p class="card-text mb-3">
                <strong>Max spots:</strong> {{ lot.max_spots }}
              </p>

              <div class="mt-auto d-flex justify-content-between gap-1">
                <button class="btn btn-warning btn-sm flex-fill" @click="viewSpots(lot.id)">
                  <i class="fas fa-search me-1"></i> View spots
                </button>
                <router-link 
                  :to="`/admin/edit-lot/${lot.id}`" 
                  class="btn btn-primary btn-sm flex-fill"
                >
                  <i class="fas fa-edit me-1"></i> Edit
                </router-link>
                <button class="btn btn-danger btn-sm flex-fill" @click="deleteLot(lot.id)">
                  <i class="fas fa-trash me-1"></i> Delete
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
  name: 'AdminDashboard',
  components: { AppNavbar },
  data() {
    return {
      lots: [],
      loading: false
    }
  },
  created() {
    this.fetchLots()
  },
  methods: {
    async fetchLots() {
      this.loading = true
      try {
        const res = await api.get('/api/admin/lots')
        this.lots = res.data
      } catch (err) {
        console.error(err)
        alert('Failed to load parking lots')
      } finally {
        this.loading = false
      }
    },
    async deleteLot(lotId) {
      if (!confirm('Are you sure you want to delete this parking lot? All spots will be removed.')) return
      try {
        await api.delete(`/api/admin/lots/${lotId}`)
        await this.fetchLots()
      } catch (err) {
        console.error(err)
        alert(err.response?.data?.message || 'Error deleting parking lot')
      }
    },
    viewSpots(lotId) {
      this.$router.push(`/admin/lots/${lotId}/spots`)
    }
  }
}
</script>
