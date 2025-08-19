<template>
  <div class="home">
    <h1>Forestal Management System</h1>
    <p>Welcome to the forest management application. Use the navigation menu to access different sections:</p>
    
    <div class="dashboard-cards">
      <div class="card" @click="$router.push('/fincas')">
        <h3>Fincas</h3>
        <p>Manage land properties and forest cuts</p>
      </div>
      
      <div class="card" @click="$router.push('/servizos')">
        <h3>Servizos</h3>
        <p>Forest service operations management</p>
      </div>
      
      <div class="card" @click="$router.push('/facturas')">
        <h3>Facturas</h3>
        <p>Invoice and billing management</p>
      </div>
      
      <div class="card" @click="$router.push('/weight-actions')">
        <h3>Weight Actions</h3>
        <p>Weight data and truck transport analytics</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

p {
  color: #7f8c8d;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.card p {
  color: #7f8c8d;
  margin: 0;
}
</style>