<template>
  <div>
    <AppNavbar />
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white">
              <h4 class="mb-0">
                <i class="fas fa-plus me-2"></i>Create New Parking Lot
              </h4>
            </div>
            <div class="card-body">
              <form @submit.prevent="createLot" novalidate>
                <div class="mb-3">
                  <label class="form-label">Lot Name <span class="text-danger">*</span></label>
                  <input v-model="form.name" type="text" class="form-control" 
                         :class="{ 'is-invalid': errors.name }" required />
                  <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
                </div>

                <div class="mb-3">
                  <label class="form-label">Price per Hour (₹) <span class="text-danger">*</span></label>
                  <input v-model.number="form.price_per_hour" type="number" step="0.01" min="0" 
                         class="form-control" :class="{ 'is-invalid': errors.price_per_hour }" required />
                  <div v-if="errors.price_per_hour" class="invalid-feedback">{{ errors.price_per_hour }}</div>
                </div>

                <div class="mb-3">
                  <label class="form-label">Address <span class="text-danger">*</span></label>
                  <textarea v-model="form.address" class="form-control" rows="3" 
                            :class="{ 'is-invalid': errors.address }" required></textarea>
                  <div v-if="errors.address" class="invalid-feedback">{{ errors.address }}</div>
                </div>

                <div class="mb-3">
                  <label class="form-label">Pincode <span class="text-danger">*</span></label>
                  <input v-model="form.pincode" type="text" class="form-control" maxlength="6"
                         :class="{ 'is-invalid': errors.pincode }" required />
                  <div v-if="errors.pincode" class="invalid-feedback">{{ errors.pincode }}</div>
                </div>

                <div class="mb-4">
                  <label class="form-label">Max Spots <span class="text-danger">*</span></label>
                  <input v-model.number="form.max_spots" type="number" min="1" max="1000"
                         class="form-control" :class="{ 'is-invalid': errors.max_spots }" required />
                  <div v-if="errors.max_spots" class="invalid-feedback">{{ errors.max_spots }}</div>
                </div>

                <div class="d-grid gap-2 d-md-flex justify-content-between">
                  <router-link to="/admin/dashboard" class="btn btn-secondary">
                    <i class="fas fa-arrow-left me-1"></i> Back to Dashboard
                  </router-link>
                  <button type="submit" class="btn btn-primary px-4" :disabled="loading">
                    <i v-if="loading" class="fas fa-spinner fa-spin me-1"></i>
                    <i v-else class="fas fa-save me-1"></i>
                    {{ loading ? 'Creating...' : 'Create Lot' }}
                  </button>
                </div>
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
  name: 'CreateLotView',
  components: { AppNavbar },
  data() {
    return {
      form: {
        name: '',
        price_per_hour: null,
        address: '',
        pincode: '',
        max_spots: 1
      },
      errors: {},
      loading: false
    }
  },
  methods: {
    async createLot() {
      this.errors = {}
      this.loading = true

      try {
        await api.post('/api/admin/lots', this.form)
        this.$router.push('/admin/dashboard')
      } catch (err) {
        if (err.response?.status === 400) {
          this.errors = err.response.data || {}
        } else {
          alert(err.response?.data?.message || 'Failed to create parking lot')
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
