<template>
  <div>
    <AppNavbar />
    <div class="container mt-5" style="max-width: 600px; margin: 2rem auto;">
      <h1 class="fas fa-home me-2 text-primary">User Summary Charts</h1>
      <h2 class="mb-4">Parking Spot Status Summary</h2>
      <div v-if="!loading && (releasedCount || occupiedCount)" style="position: relative; height: 400px;">
        <canvas ref="spotStatusChart"></canvas>
      </div>
      <div v-else class="p-4">Loading chart...</div>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/Navbar.vue'
import api from '@/api/axios'
import Chart from 'chart.js/auto'

export default {
  name: 'UserSummary',
  components: { AppNavbar },
  data() {
    return {
      releasedCount: 0,
      occupiedCount: 0,
      chart: null,
      loading: true
    }
  },
  async created() {
    await this.fetchSummary()
  },
  watch: {
    loading(newVal) {
      if (!newVal && (this.releasedCount || this.occupiedCount)) {
        // Wait for DOM to update, then render
        this.$nextTick(() => {
          this.renderChart()
        })
      }
    }
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
      this.chart = null
    }
  },
  methods: {
    async fetchSummary() {
      this.loading = true
      try {
        const response = await api.get('/api/user/summary_spot_status')
        this.releasedCount = response.data.released
        this.occupiedCount = response.data.occupied
      } catch (error) {
        console.error('Failed to fetch user summary:', error)
        alert('Failed to load user summary')
      } finally {
        this.loading = false
      }
    },
    renderChart() {
      // Safety check: ensure canvas ref exists
      if (!this.$refs.spotStatusChart) {
        console.warn('Spot status chart ref not found')
        return
      }

      if (this.chart) {
        this.chart.destroy()
      }

      try {
        const ctx = this.$refs.spotStatusChart.getContext('2d')
        const data = {
          labels: ['Available', 'Occupied'],
          datasets: [{
            data: [this.releasedCount, this.occupiedCount],
            backgroundColor: [
              'rgba(75, 192, 192, 0.7)',
              'rgba(255, 99, 132, 0.7)'
            ],
            borderColor: [
              'rgba(75, 192, 192, 1)',
              'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
          }]
        }
        const options = {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' },
            title: {
              display: true,
              text: 'Available vs Occupied Parking Spots'
            }
          }
        }
        this.chart = new Chart(ctx, {
          type: 'doughnut',
          data,
          options
        })
      } catch (error) {
        console.error('Error rendering spot status chart:', error)
      }
    }
  }
}
</script>
