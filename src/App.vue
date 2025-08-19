<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <h1>Forestal Management</h1>
      </div>
      <ul class="nav-menu">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/fincas">Fincas</router-link></li>
        <li><router-link to="/servizos">Servizos</router-link></li>
        <li><router-link to="/facturas">Facturas</router-link></li>
        <li><router-link to="/weight-actions">Weight Actions</router-link></li>
      </ul>
    </nav>
    
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-brand h1 {
  font-size: 1.5rem;
}

.nav-menu {
  list-style: none;
  display: flex;
  gap: 2rem;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  background-color: #34495e;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>