<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2>Producciones</h2>
      <router-link to="/producciones/nueva" class="btn btn-primary">+ Nueva Produccion</router-link>
    </div>

    <div class="flex gap-2 mb-4">
      <select v-model="filtroEstado" class="btn btn-gray" @change="loadProducciones">
        <option value="">Todos los estados</option>
        <option value="borrador">Borrador</option>
        <option value="confirmado">Confirmado</option>
        <option value="en_proceso">En Proceso</option>
        <option value="terminado">Terminado</option>
        <option value="cancelado">Cancelado</option>
      </select>
    </div>

    <div class="table-container">
      <div class="table-wrapper">
        <table>
        <thead>
          <tr>
            <th>Codigo</th>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Centro</th>
            <th>Estado</th>
            <th>Fecha Inicio</th>
            <th>Fecha Fin</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prod in producciones" :key="prod.id">
            <td>{{ prod.nombre }}</td>
            <td>{{ getProductoNombre(prod.producto_id) }}</td>
            <td>{{ formatNumber(prod.cantidad) }} {{ prod.producto_uom || '' }}</td>
            <td>{{ getCentroNombre(prod.centro_trabajo_id) }}</td>
            <td><StatusBadge :status="prod.estado" type="produccion" /></td>
            <td>{{ formatDate(prod.fecha_inicio) }}</td>
            <td>{{ formatDate(prod.fecha_fin) }}</td>
            <td>
              <div class="flex gap-2 actions-cell">
                <button
                  v-if="prod.estado === 'borrador'"
                  class="btn btn-sm btn-info"
                  @click="accionProduccion(prod.id, 'confirmar')"
                >
                  Confirmar
                </button>
                <button
                  v-if="prod.estado === 'confirmado'"
                  class="btn btn-sm btn-warning"
                  @click="accionProduccion(prod.id, 'iniciar')"
                >
                  Iniciar
                </button>
                <button
                  v-if="prod.estado === 'en_proceso'"
                  class="btn btn-sm btn-success"
                  @click="accionProduccion(prod.id, 'terminar')"
                >
                  Terminar
                </button>
                <button
                  v-if="!['terminado', 'cancelado'].includes(prod.estado)"
                  class="btn btn-sm btn-danger"
                  @click="accionProduccion(prod.id, 'cancelar')"
                >
                  Cancelar
                </button>
                <router-link :to="`/producciones/${prod.id}/editar`" class="btn btn-sm btn-primary">
                  Editar
                </router-link>
                <button
                  v-if="['borrador', 'cancelado'].includes(prod.estado)"
                  class="btn btn-sm btn-danger"
                  @click="confirmDelete(prod)"
                >
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="producciones.length === 0">
            <td colspan="8" style="text-align: center; color: var(--color-gray);">
              No hay producciones registradas
            </td>
          </tr>
        </tbody>
        </table>
      </div>
    </div>

    <ConfirmDialog
      :visible="showConfirm"
      title="Eliminar Produccion"
      :message="`Se eliminara la produccion '${prodSeleccionado?.nombre}'. Desea continuar?`"
      @confirm="handleDelete"
      @cancel="showConfirm = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index.js'
import StatusBadge from '../components/StatusBadge.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { formatNumber } from '../utils/format.js'

const producciones = ref([])
const productos = ref([])
const centros = ref([])
const filtroEstado = ref('')
const showConfirm = ref(false)
const prodSeleccionado = ref(null)

async function loadProducciones() {
  try {
    const params = filtroEstado.value ? { estado: filtroEstado.value } : {}
    producciones.value = await api.get('/api/producciones', params)
  } catch (err) {
    alert(err.message)
  }
}

async function loadProductos() {
  try {
    productos.value = await api.get('/api/productos')
  } catch (err) {
    console.error('Error cargando productos:', err)
  }
}

function getProductoNombre(id) {
  if (!id) return '-'
  const prod = productos.value.find(p => p.id === id)
  return prod ? prod.nombre : `Prod-${id}`
}

function getCentroNombre(id) {
  if (!id) return '-'
  const centro = centros.value.find(c => c.id === id)
  return centro ? centro.nombre : `CT-${id}`
}

async function loadCentros() {
  try {
    centros.value = await api.get('/api/centros-trabajo')
  } catch (err) {
    console.error('Error cargando centros:', err)
  }
}

async function accionProduccion(id, accion) {
  try {
    await api.post(`/api/producciones/${id}/${accion}`)
    await loadProducciones()
  } catch (err) {
    alert(err.message)
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-ES')
}

function confirmDelete(prod) {
  prodSeleccionado.value = prod
  showConfirm.value = true
}

async function handleDelete() {
  try {
    await api.delete(`/api/producciones/${prodSeleccionado.value.id}`)
    showConfirm.value = false
    await loadProducciones()
  } catch (err) {
    alert(err.message)
    showConfirm.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadProducciones(), loadProductos(), loadCentros()])
})
</script>

<style scoped>
.btn-info {
  background: #3b82f6;
  color: white;
}
</style>
