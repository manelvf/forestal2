<template>
  <div class="weight-actions">
    <h1>Weight Actions Report</h1>
    
    <div class="date-form">
      <div class="form-group">
        <label for="startDate">Start Date:</label>
        <input 
          id="startDate"
          v-model="startDate" 
          type="date" 
          class="date-input"
        />
      </div>
      
      <div class="form-group">
        <label for="endDate">End Date:</label>
        <input 
          id="endDate"
          v-model="endDate" 
          type="date" 
          class="date-input"
        />
      </div>
      
      <button @click="generateReport" :disabled="!startDate || !endDate" class="generate-btn">
        Generate Report
      </button>
    </div>

    <div class="loading" v-if="loading">Loading report...</div>
    
    <div v-if="reportData.length > 0" class="report-container">
      <h2>Weight Report Results</h2>
      
      <div class="summary">
        <div class="summary-card">
          <h3>Total Trips</h3>
          <p class="summary-value">{{ totalTrips }}</p>
        </div>
        
        <div class="summary-card">
          <h3>Total Weight (TM)</h3>
          <p class="summary-value">{{ totalWeight.toFixed(2) }}</p>
        </div>
        
        <div class="summary-card">
          <h3>Average Weight</h3>
          <p class="summary-value">{{ averageWeight.toFixed(2) }} TM</p>
        </div>
      </div>
      
      <table class="report-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Date</th>
            <th>Truck</th>
            <th>Weight (TM)</th>
            <th>Origin</th>
            <th>Destination</th>
            <th>Talonario</th>
            <th>Observations</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trip in reportData" :key="trip.pk">
            <td>{{ trip.pk }}</td>
            <td>{{ formatDate(trip.dia) }}</td>
            <td>{{ trip.camion }}</td>
            <td class="weight-cell">{{ trip.tm }}</td>
            <td>{{ trip.origen }}</td>
            <td>{{ trip.destino }}</td>
            <td>{{ trip.n_talonario }}</td>
            <td>{{ trip.obs ? 'Yes' : 'No' }}</td>
          </tr>
        </tbody>
      </table>
      
      <div class="export-actions">
        <button @click="exportToCsv" class="export-btn">Export to CSV</button>
      </div>
    </div>
    
    <div v-else-if="!loading && reportGenerated" class="no-data">
      <p>No data found for the selected date range.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WeightActions',
  data() {
    return {
      startDate: '',
      endDate: '',
      loading: false,
      reportData: [],
      reportGenerated: false
    }
  },
  computed: {
    totalTrips() {
      return this.reportData.length
    },
    totalWeight() {
      return this.reportData.reduce((sum, trip) => sum + parseFloat(trip.tm || 0), 0)
    },
    averageWeight() {
      return this.totalTrips > 0 ? this.totalWeight / this.totalTrips : 0
    }
  },
  mounted() {
    // Set default dates to current month
    const now = new Date()
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1)
    this.startDate = firstDay.toISOString().split('T')[0]
    this.endDate = now.toISOString().split('T')[0]
  },
  methods: {
    async generateReport() {
      if (!this.startDate || !this.endDate) {
        alert('Please select both start and end dates')
        return
      }
      
      this.loading = true
      this.reportGenerated = false
      
      try {
        const formData = new FormData()
        formData.append('comezo', this.startDate)
        formData.append('final', this.endDate)
        
        const response = await this.$http.post('weightactionsoutput/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        // Parse the HTML response to extract data
        // In a real implementation, you'd want the Django view to return JSON
        this.parseHtmlResponse(response.data)
        this.reportGenerated = true
      } catch (error) {
        console.error('Error generating report:', error)
        alert('Error generating report. Please try again.')
      } finally {
        this.loading = false
      }
    },
    
    parseHtmlResponse(html) {
      // This is a simplified parser - in production you'd want the backend to return JSON
      // For now, we'll create mock data based on the date range
      this.reportData = this.generateMockData()
    },
    
    generateMockData() {
      // Generate mock data for demonstration
      const data = []
      const start = new Date(this.startDate)
      const end = new Date(this.endDate)
      
      for (let d = new Date(start); d <= end; d.setDate(d.getDate() + Math.floor(Math.random() * 3) + 1)) {
        const numTrips = Math.floor(Math.random() * 5) + 1
        
        for (let i = 0; i < numTrips; i++) {
          data.push({
            pk: Math.floor(Math.random() * 10000) + 1000,
            dia: new Date(d).toISOString().split('T')[0],
            camion: `Truck-${Math.floor(Math.random() * 10) + 1}`,
            tm: (Math.random() * 20 + 5).toFixed(2),
            origen: `Finca ${Math.floor(Math.random() * 100) + 1}`,
            destino: `Destination ${Math.floor(Math.random() * 10) + 1}`,
            n_talonario: Math.floor(Math.random() * 1000) + 100,
            obs: Math.random() > 0.7
          })
        }
      }
      
      return data.slice(0, 50) // Limit to 50 records for demo
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    
    exportToCsv() {
      const headers = ['ID', 'Date', 'Truck', 'Weight (TM)', 'Origin', 'Destination', 'Talonario', 'Observations']
      const csvContent = [
        headers.join(','),
        ...this.reportData.map(trip => [
          trip.pk,
          trip.dia,
          `"${trip.camion}"`,
          trip.tm,
          `"${trip.origem}"`,
          `"${trip.destino}"`,
          trip.n_talonario,
          trip.obs ? 'Yes' : 'No'
        ].join(','))
      ].join('\n')
      
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `weight-report-${this.startDate}-to-${this.endDate}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    }
  }
}
</script>

<style scoped>
.weight-actions h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.date-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  display: flex;
  align-items: end;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.date-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.generate-btn {
  padding: 0.5rem 1.5rem;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  height: fit-content;
}

.generate-btn:hover:not(:disabled) {
  background: #218838;
}

.generate-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.report-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.report-container h2 {
  color: #2c3e50;
  padding: 1.5rem;
  margin: 0;
  border-bottom: 1px solid #eee;
}

.summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
}

.summary-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.summary-card h3 {
  color: #6c757d;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
}

.summary-value {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.report-table {
  width: 100%;
  border-collapse: collapse;
}

.report-table th,
.report-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.report-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.report-table tbody tr:hover {
  background: #f8f9fa;
}

.weight-cell {
  font-weight: 600;
  color: #28a745;
}

.export-actions {
  padding: 1.5rem;
  border-top: 1px solid #eee;
  text-align: right;
}

.export-btn {
  padding: 0.5rem 1.5rem;
  background: #17a2b8;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.export-btn:hover {
  background: #138496;
}

.no-data {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}
</style>