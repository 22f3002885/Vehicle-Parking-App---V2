<template>
  <div>
    <AppNavbar />
    <div class="container-fluid mt-4">
      <div class="row mb-4">
        <div class="col-12">
          <h1>Admin Summary</h1>
        </div>
      </div>

      <!-- Revenue Chart -->
      <div class="row mb-5">
        <div class="col-12">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-chart-bar me-2"></i>Revenue from Parking Lots
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="chart-container">
                <canvas ref="revenueChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Spot Availability Chart -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-info text-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-parking me-2"></i>Parking Spot Availability
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="chart-container">
                <canvas ref="spotAvailabilityChart"></canvas>
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
import Chart from 'chart.js/auto'

export default {
  name: 'AdminSummary',
  components: { AppNavbar },
  data() {
    return {
      loading: true,
      revenueData: [],
      spotData: [],
      revenueChart: null,
      spotChart: null
    }
  },
  async created() {
    await this.fetchSummaryData()
  },
  watch: {
    // ✅ Render charts ONLY when data is available
    revenueData(newVal) {
      if (newVal.length > 0 && this.$refs.revenueChart) {
        this.renderRevenueChart()
      }
    },
    spotData(newVal) {
      if (newVal.length > 0 && this.$refs.spotAvailabilityChart) {
        this.renderSpotChart()
      }
    }
  },
  beforeUnmount() {
    if (this.revenueChart) {
      this.revenueChart.destroy()
      this.revenueChart = null
    }
    if (this.spotChart) {
      this.spotChart.destroy()
      this.spotChart = null
    }
  },
  methods: {
    async fetchSummaryData() {
      this.loading = true
      try {
        console.log('Fetching summary data...') // DEBUG
        const [revenueRes, spotRes] = await Promise.all([
          api.get('/api/admin/summary/revenue'),
          api.get('/api/admin/summary/spots')
        ])
        
        console.log('Revenue data:', revenueRes.data) // DEBUG
        console.log('Spot data:', spotRes.data) // DEBUG
        
        this.revenueData = revenueRes.data
        this.spotData = spotRes.data
        
      } catch (error) {
        console.error('Failed to fetch summary data:', error)
        alert('Failed to load summary data')
      } finally {
        this.loading = false
      }
    },
    
    renderRevenueChart() {
      // Destroy existing chart if it exists
      if (this.revenueChart) {
        this.revenueChart.destroy()
      }
      
      const revenueCtx = this.$refs.revenueChart.getContext('2d')
      this.revenueChart = new Chart(revenueCtx, {
        type: 'bar',
        data: {
          labels: this.revenueData.map(item => item.name),
          datasets: [{
            label: 'Revenue (₹)',
            data: this.revenueData.map(item => item.total_revenue),
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2,
            borderRadius: 8,
            borderSkipped: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return '₹' + Math.round(value).toLocaleString()
                }
              },
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          },
          plugins: {
            legend: {
              display: true,
              position: 'top'
            }
          }
        }
      })
    },

    renderSpotChart() {
      // Destroy existing chart if it exists
      if (this.spotChart) {
        this.spotChart.destroy()
      }
      
      const spotCtx = this.$refs.spotAvailabilityChart.getContext('2d')
      this.spotChart = new Chart(spotCtx, {
        type: 'bar',
        data: {
          labels: this.spotData.map(item => item.name),
          datasets: [
            {
              label: 'Available',
              data: this.spotData.map(item => item.available_spots),
              backgroundColor: 'rgba(75, 192, 192, 0.8)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 2,
              borderRadius: 8,
              borderSkipped: false
            },
            {
              label: 'Occupied',
              data: this.spotData.map(item => item.occupied_spots),
              backgroundColor: 'rgba(255, 99, 132, 0.8)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 2,
              borderRadius: 8,
              borderSkipped: false
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: true,
          scales: {
            x: {
              stacked: true,
              grid: {
                display: false
              }
            },
            y: {
              stacked: true,
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return value
                }
              },
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            }
          },
          plugins: {
            legend: {
              display: true,
              position: 'top'
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  padding: 20px;
}

.card-header {
  border-bottom: 1px solid rgba(255,255,255,0.2);
}
</style>
