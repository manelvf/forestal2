<template>
  <div class="facturas-grid">
    <h1>Facturas Management</h1>
    
    <div class="grid-controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          @input="handleSearch"
          placeholder="Search facturas..."
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
            <th @click="sortBy('empresa')">Empresa</th>
            <th @click="sortBy('cliente')">Cliente</th>
            <th @click="sortBy('tipo')">Tipo</th>
            <th @click="sortBy('numero')">Número</th>
            <th @click="sortBy('emision')">Emisión</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="factura in paginatedData" :key="factura.id">
            <td>{{ factura.cell[0] }}</td>
            <td>{{ factura.cell[1] }}</td>
            <td>{{ factura.cell[2] }}</td>
            <td>{{ factura.cell[3] }}</td>
            <td>{{ factura.cell[4] }}</td>
            <td>{{ formatDate(factura.cell[5]) }}</td>
            <td>
              <button @click="editFactura(factura)" class="btn-edit">Edit</button>
              <button @click="viewDetails(factura)" class="btn-view">Details</button>
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

    <!-- Invoice Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click="closeDetailsModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Invoice Details</h2>
          <button @click="closeDetailsModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div v-if="loadingDetails">Loading details...</div>
          <div v-else>
            <table class="details-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Servizo</th>
                  <th>Concepto</th>
                  <th>IVA</th>
                  <th>IRPF</th>
                  <th>Cantidad</th>
                  <th>Valor</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="detail in invoiceDetails" :key="detail.id">
                  <td>{{ detail.cell[0] }}</td>
                  <td>{{ detail.cell[1] }}</td>
                  <td>{{ detail.cell[2] }}</td>
                  <td>{{ detail.cell[3] }}</td>
                  <td>{{ detail.cell[4] }}</td>
                  <td>{{ detail.cell[5] }}</td>
                  <td>{{ detail.cell[6] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FacturasGrid',
  data() {
    return {
      facturas: [],
      loading: false,
      currentPage: 1,
      pageSize: 15,
      searchQuery: '',
      sortField: '',
      sortOrder: 'asc',
      showDetailsModal: false,
      loadingDetails: false,
      invoiceDetails: [],
      selectedFactura: null
    }
  },
  computed: {
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.facturas.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.facturas.length / this.pageSize)
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
        
        const response = await this.$http.get('gridfactura', { params })
        this.facturas = response.data.rows || []
      } catch (error) {
        console.error('Error loading facturas:', error)
        this.facturas = []
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
                { field: 'empresa', op: 'cn', data: this.searchQuery },
                { field: 'cliente', op: 'cn', data: this.searchQuery },
                { field: 'numero', op: 'cn', data: this.searchQuery }
              ]
            })
          }
          
          const response = await this.$http.get('gridfactura', { params })
          this.facturas = response.data.rows || []
          this.currentPage = 1
        } catch (error) {
          console.error('Error searching facturas:', error)
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
    
    editFactura(factura) {
      window.open(`/admin/empresas/factura/${factura.id}/change/`, '_blank')
    },
    
    async viewDetails(factura) {
      this.selectedFactura = factura
      this.showDetailsModal = true
      this.loadingDetails = true
      
      try {
        const params = {
          page: 1,
          rows: 100,
          sidx: 'pk',
          sord: 'asc',
          _search: false
        }
        
        const response = await this.$http.get(`griddetallefactura/${factura.id}/`, { params })
        this.invoiceDetails = response.data.rows || []
      } catch (error) {
        console.error('Error loading invoice details:', error)
        this.invoiceDetails = []
      } finally {
        this.loadingDetails = false
      }
    },
    
    closeDetailsModal() {
      this.showDetailsModal = false
      this.selectedFactura = null
      this.invoiceDetails = []
    }
  }
}
</script>

<style scoped>
.facturas-grid h1 {
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
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background: #f8f9fa;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.data-table th:hover {
  background: #e9ecef;
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
  font-size: 0.875rem;
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

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 90%;
  max-height: 90%;
  overflow: auto;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.btn-close:hover {
  color: #333;
}

.modal-body {
  padding: 1rem;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
}

.details-table th,
.details-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.details-table th {
  background: #f8f9fa;
  font-weight: 600;
}
</style>