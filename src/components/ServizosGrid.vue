<template>
  <div class="servizos-grid">
    <h1>Servizos Forestais</h1>
    
    <div class="grid-controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          @input="handleSearch"
          placeholder="Search servizos..."
          class="search-input"
        />
      </div>
      <button @click="loadData" class="refresh-btn">Refresh</button>
    </div>

    <div class="loading" v-if="loading">Loading...</div>
    
    <div class="grid-container" v-else>
      <table class="data-table">
        <thead>
          <tr>
            <th @click="sortBy('pk')">ID</th>
            <th @click="sortBy('concello')">Concello</th>
            <th @click="sortBy('poligono')">Polígono</th>
            <th @click="sortBy('parcela')">Parcela</th>
            <th @click="sortBy('m2_permiso')">M² Permiso</th>
            <th>Permiso</th>
            <th>Comezo</th>
            <th>Entrada Grupo</th>
            <th>Saída PECL</th>
            <th>Código PECL</th>
            <th>Código NORFOR</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="servizo in paginatedData" :key="servizo.id">
            <td>{{ servizo.cell[0] }}</td>
            <td>{{ servizo.cell[1] }}</td>
            <td>{{ servizo.cell[2] }}</td>
            <td>{{ servizo.cell[3] }}</td>
            <td>{{ servizo.cell[4] }}</td>
            <td>{{ formatDate(servizo.cell[5]) }}</td>
            <td>{{ formatDate(servizo.cell[6]) }}</td>
            <td>{{ formatDate(servizo.cell[7]) }}</td>
            <td>{{ formatDate(servizo.cell[8]) }}</td>
            <td>{{ servizo.cell[9] }}</td>
            <td>{{ servizo.cell[10] }}</td>
            <td>
              <button @click="editServizo(servizo)" class="btn-edit">Edit</button>
              <button @click="viewTrips(servizo)" class="btn-view">Trips</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1" class="btn-page">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="btn-page">Next</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ServizosGrid',
  data() {
    return {
      servizos: [],
      loading: false,
      currentPage: 1,
      pageSize: 15,
      searchQuery: '',
      sortField: '',
      sortOrder: 'asc'
    }
  },
  computed: {
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.servizos.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.servizos.length / this.pageSize)
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          rows: this.pageSize,
          sidx: this.sortField || 'pk',
          sord: this.sortOrder,
          _search: false
        }
        
        const response = await this.$http.get('grid', { params })
        this.servizos = response.data.rows || []
      } catch (error) {
        console.error('Error loading servizos:', error)
        this.servizos = []
      } finally {
        this.loading = false
      }
    },
    
    async handleSearch() {
      if (this.searchQuery.trim()) {
        this.loading = true
        try {
          const params = {
            page: 1,
            rows: this.pageSize,
            sidx: this.sortField || 'pk',
            sord: this.sortOrder,
            _search: true,
            filters: JSON.stringify({
              groupOp: 'OR',
              rules: [
                { field: 'concello', op: 'cn', data: this.searchQuery },
                { field: 'codigoPECL', op: 'cn', data: this.searchQuery },
                { field: 'codigoNORFOR', op: 'cn', data: this.searchQuery }
              ]
            })
          }
          
          const response = await this.$http.get('grid', { params })
          this.servizos = response.data.rows || []
          this.currentPage = 1
        } catch (error) {
          console.error('Error searching servizos:', error)
        } finally {
          this.loading = false
        }
      } else {
        this.loadData()
      }
    },
    
    sortBy(field) {
      if (this.sortField === field) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortOrder = 'asc'
      }
      this.loadData()
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.loadData()
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.loadData()
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    
    editServizo(servizo) {
      window.open(`/admin/fincas/tala/${servizo.id}/change/`, '_blank')
    },
    
    viewTrips(servizo) {
      this.$router.push(`/trips/${servizo.id}`)
    }
  }
}
</script>

<style scoped>
.servizos-grid h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.grid-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.search-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 300px;
}

.refresh-btn {
  padding: 0.5rem 1rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.refresh-btn:hover {
  background: #2980b9;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.data-table {
  width: 100%;
  background: white;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.data-table th,
.data-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background: #f8f9fa;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.875rem;
}

.data-table th:hover {
  background: #e9ecef;
}

.data-table td {
  font-size: 0.875rem;
}

.data-table tbody tr:hover {
  background: #f8f9fa;
}

.btn-edit,
.btn-view {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
  margin-right: 0.5rem;
}

.btn-edit {
  background: #28a745;
  color: white;
}

.btn-edit:hover {
  background: #218838;
}

.btn-view {
  background: #17a2b8;
  color: white;
}

.btn-view:hover {
  background: #138496;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-page {
  padding: 0.5rem 1rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-page:disabled {
  background: #dee2e6;
  cursor: not-allowed;
}

.btn-page:not(:disabled):hover {
  background: #5a6268;
}
</style>