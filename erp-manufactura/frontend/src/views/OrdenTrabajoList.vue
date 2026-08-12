<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2>Ordenes de Trabajo</h2>
      <router-link to="/ordenes-trabajo/nueva" class="btn btn-primary">+ Nueva Orden</router-link>
    </div>

    <div class="flex gap-2 mb-4">
      <select v-model="filtroEstado" class="btn btn-gray" @change="loadOrdenes">
        <option value="">Todos los estados</option>
        <option value="pendiente">Pendiente</option>
        <option value="listo">Listo</option>
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
            <th>Nombre</th>
            <th>Produccion</th>
            <th>Centro Trabajo</th>
            <th>Estado</th>
            <th>Duracion Esperada</th>
            <th>Duracion Real</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="orden in ordenes" :key="orden.id">
            <td><strong>{{ orden.nombre }}</strong></td>
            <td>MO-{{ orden.produccion_id }}</td>
            <td>{{ getCentroNombre(orden.centro_trabajo_id) }}</td>
            <td><StatusBadge :status="orden.estado" type="orden_trabajo" /></td>
            <td>{{ orden.duracion_esperada ? `${orden.duracion_esperada} min` : '-' }}</td>
            <td>{{ orden.duracion_real ? `${orden.duracion_real} min` : '-' }}</td>
            <td>
              <div class="flex gap-2">
                <button
                  v-if="['pendiente', 'listo'].includes(orden.estado)"
                  class="btn btn-sm btn-warning"
                  @click="accionOrden(orden.id, 'iniciar')"
                >
                  Iniciar
                </button>
                <button
                  v-if="orden.estado === 'en_proceso'"
                  class="btn btn-sm btn-success"
                  @click="accionOrden(orden.id, 'terminar')"
                >
                  Terminar
                </button>
                <button
                  v-if="orden.estado !== 'terminado'"
                  class="btn btn-sm btn-danger"
                  @click="accionOrden(orden.id, 'cancelar')"
                >
                  Cancelar
                </button>
                <router-link :to="`/ordenes-trabajo/${orden.id}/editar`" class="btn btn-sm btn-primary">
                  Editar
                </router-link>
                <button
                  v-if="['pendiente', 'cancelado'].includes(orden.estado)"
                  class="btn btn-sm btn-danger"
                  @click="confirmDelete(orden)"
                >
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="ordenes.length === 0">
            <td colspan="7" style="text-align: center; color: var(--color-gray);">
              No hay ordenes de trabajo registradas
            </td>
          </tr>
        </tbody>
        </table>
      </div>
    </div>

    <ConfirmDialog
      :visible="showConfirm"
      title="Eliminar Orden de Trabajo"
      :message="`Se eliminara la orden '${ordenSeleccionado?.nombre}'. Desea continuar?`"
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

const ordenes = ref([])
const centros = ref([])
const filtroEstado = ref('')
const showConfirm = ref(false)
const ordenSeleccionado = ref(null)

async function loadOrdenes() {
  try {
    const params = filtroEstado.value ? { estado: filtroEstado.value } : {}
    ordenes.value = await api.get('/api/ordenes-trabajo', params)
  } catch (err) {
    alert(err.message)
  }
}

async function loadCentros() {
  try {
    centros.value = await api.get('/api/centros-trabajo')
  } catch (err) {
    console.error('Error cargando centros:', err)
  }
}

function getCentroNombre(id) {
  if (!id) return '-'
  const centro = centros.value.find(c => c.id === id)
  return centro ? centro.nombre : `CT-${id}`
}

async function accionOrden(id, accion) {
  try {
    await api.post(`/api/ordenes-trabajo/${id}/${accion}`)
    await loadOrdenes()
  } catch (err) {
    alert(err.message)
  }
}

function confirmDelete(orden) {
  ordenSeleccionado.value = orden
  showConfirm.value = true
}

async function handleDelete() {
  try {
    await api.delete(`/api/ordenes-trabajo/${ordenSeleccionado.value.id}`)
    showConfirm.value = false
    await loadOrdenes()
  } catch (err) {
    alert(err.message)
    showConfirm.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadOrdenes(), loadCentros()])
})
</script>
