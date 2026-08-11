import { createRouter, createWebHistory } from 'vue-router'

// Importar vistas
import CentroTrabajoList from '../views/CentroTrabajoList.vue'
import CentroTrabajoForm from '../views/CentroTrabajoForm.vue'
import BomList from '../views/BomList.vue'
import BomForm from '../views/BomForm.vue'
import ProduccionList from '../views/ProduccionList.vue'
import ProduccionForm from '../views/ProduccionForm.vue'
import OrdenTrabajoList from '../views/OrdenTrabajoList.vue'
import OrdenTrabajoForm from '../views/OrdenTrabajoForm.vue'

const routes = [
  { path: '/', redirect: '/producciones' },
  { path: '/centros-trabajo', component: CentroTrabajoList },
  { path: '/centros-trabajo/nuevo', component: CentroTrabajoForm },
  { path: '/centros-trabajo/:id/editar', component: CentroTrabajoForm, props: true },
  { path: '/boms', component: BomList },
  { path: '/boms/nuevo', component: BomForm },
  { path: '/boms/:id/editar', component: BomForm, props: true },
  { path: '/producciones', component: ProduccionList },
  { path: '/producciones/nueva', component: ProduccionForm },
  { path: '/producciones/:id/editar', component: ProduccionForm, props: true },
  { path: '/ordenes-trabajo', component: OrdenTrabajoList },
  { path: '/ordenes-trabajo/nueva', component: OrdenTrabajoForm },
  { path: '/ordenes-trabajo/:id/editar', component: OrdenTrabajoForm, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
