<template>
  <div>
    <AppNavbar />
    <div class="container mt-5" style="max-width: 600px; margin: 2rem auto;">
      <h1 class="fas fa-home me-2 text-primary">User Summary Charts</h1>
      <h2 class="mb-4">Parking Spot Status Summary</h2>
      <canvas ref="spotStatusChart" width="400" height="400"></canvas>
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
  mounted() {
    this.renderChart()
  },
  watch: {
    loading(newVal) {
      if (!newVal) {
        this.renderChart()
      }
    }
  },
  methods: {
    async fetchSummary() {
      this.loading = true
      try {
        // Assuming your backend API to get released and occupied counts:
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
      if (this.chart) {
        this.chart.destroy()
      }
      const ctx = this.$refs.spotStatusChart.getContext('2d')
      const data = {
        labels: ['Available', 'Occupied'],
        datasets: [{
          data: [this.releasedCount, this.occupiedCount],
          backgroundColor: [
            'rgba(75, 192, 192, 0.7)',  // teal-ish for released
            'rgba(255, 99, 132, 0.7)'   // red-ish for occupied
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
    }
  }
}
</script>
