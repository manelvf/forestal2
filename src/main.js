import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import axios from 'axios'

// Import components
import FincasGrid from './components/FincasGrid.vue'
import ServizosGrid from './components/ServizosGrid.vue'
import FacturasGrid from './components/FacturasGrid.vue'
import WeightActions from './components/WeightActions.vue'
import Home from './components/Home.vue'

// Configure axios
axios.defaults.baseURL = '/api/'
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'

// Set up CSRF token for Django
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
if (csrftoken) {
  axios.defaults.headers.common['X-CSRFToken'] = csrftoken
}

// Router configuration
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/fincas', name: 'Fincas', component: FincasGrid },
  { path: '/servizos', name: 'Servizos', component: ServizosGrid },
  { path: '/facturas', name: 'Facturas', component: FacturasGrid },
  { path: '/weight-actions', name: 'WeightActions', component: WeightActions }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.config.globalProperties.$http = axios
app.mount('#app')