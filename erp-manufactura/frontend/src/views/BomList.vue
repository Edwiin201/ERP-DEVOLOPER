<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2>Listas de Materiales (BOM)</h2>
      <router-link to="/boms/nuevo" class="btn btn-primary">+ Nuevo BOM</router-link>
    </div>

    <div class="flex gap-2 mb-4">
      <select v-model="filtroEstado" class="btn btn-gray" @change="loadBoms">
        <option value="">Todos los estados</option>
        <option value="activo">Activo</option>
        <option value="borrador">Borrador</option>
        <option value="archivado">Archivado</option>
      </select>
    </div>

    <div class="table-container">
      <div class="table-wrapper">
        <table>
        <thead>
          <tr>
            <th>Codigo</th>
            <th>Nombre</th>
            <th>Producto ID</th>
            <th>Cantidad</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bom in boms" :key="bom.id">
            <td>{{ bom.codigo || '-' }}</td>
            <td>{{ bom.nombre }}</td>
            <td>{{ bom.producto_id }}</td>
            <td>{{ bom.cantidad }}</td>
            <td><StatusBadge :status="bom.estado" type="bom" /></td>
            <td>
              <div class="flex gap-2">
                <router-link :to="`/boms/${bom.id}/editar`" class="btn btn-sm btn-primary">
                  Editar
                </router-link>
                <button
                  v-if="bom.estado !== 'archivado'"
                  class="btn btn-sm btn-warning"
                  @click="archivarBom(bom.id)"
                >
                  Archivar
                </button>
                <button
                  v-if="bom.estado === 'archivado'"
                  class="btn btn-sm btn-success"
                  @click="activarBom(bom.id)"
                >
                  Activar
                </button>
                <button class="btn btn-sm btn-danger" @click="confirmDelete(bom)">
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="boms.length === 0">
            <td colspan="6" style="text-align: center; color: var(--color-gray);">
              No hay BOMs registrados
            </td>
          </tr>
        </tbody>
        </table>
      </div>
    </div>

    <ConfirmDialog
      :visible="showConfirm"
      title="Eliminar BOM"
      :message="`Se eliminara el BOM '${bomSeleccionado?.nombre}'. Desea continuar?`"
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

const boms = ref([])
const filtroEstado = ref('')
const showConfirm = ref(false)
const bomSeleccionado = ref(null)

async function loadBoms() {
  try {
    const params = filtroEstado.value ? { estado: filtroEstado.value } : {}
    boms.value = await api.get('/api/boms', params)
  } catch (err) {
    alert(err.message)
  }
}

async function activarBom(id) {
  try {
    await api.post(`/api/boms/${id}/activar`)
    await loadBoms()
  } catch (err) {
    alert(err.message)
  }
}

async function archivarBom(id) {
  try {
    await api.post(`/api/boms/${id}/archivar`)
    await loadBoms()
  } catch (err) {
    alert(err.message)
  }
}

function confirmDelete(bom) {
  bomSeleccionado.value = bom
  showConfirm.value = true
}

async function handleDelete() {
  try {
    await api.delete(`/api/boms/${bomSeleccionado.value.id}`)
    showConfirm.value = false
    await loadBoms()
  } catch (err) {
    alert(err.message)
    showConfirm.value = false
  }
}

onMounted(loadBoms)
</script>
