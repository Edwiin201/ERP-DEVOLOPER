<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2>Centros de Trabajo</h2>
      <router-link to="/centros-trabajo/nuevo" class="btn btn-primary">
        + Nuevo Centro
      </router-link>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Codigo</th>
            <th>Nombre</th>
            <th>Capacidad</th>
            <th>Costo/Hora</th>
            <th>Activo</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="centro in centros" :key="centro.id">
            <td>{{ centro.codigo }}</td>
            <td>{{ centro.nombre }}</td>
            <td>{{ centro.capacidad }}</td>
            <td>${{ centro.costo_hora }}</td>
            <td>{{ centro.activo ? 'Si' : 'No' }}</td>
            <td>
              <div class="flex gap-2">
                <router-link
                  :to="`/centros-trabajo/${centro.id}/editar`"
                  class="btn btn-sm btn-primary"
                >
                  Editar
                </router-link>
                <button class="btn btn-sm btn-danger" @click="confirmDelete(centro)">
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="centros.length === 0">
            <td colspan="6" style="text-align: center; color: var(--color-gray);">
              No hay centros de trabajo registrados
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <ConfirmDialog
      :visible="showConfirm"
      title="Eliminar Centro de Trabajo"
      :message="`Se eliminara '${centroSeleccionado?.nombre}'. Desea continuar?`"
      @confirm="handleDelete"
      @cancel="showConfirm = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index.js'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const centros = ref([])
const showConfirm = ref(false)
const centroSeleccionado = ref(null)
const error = ref(null)

async function loadCentros() {
  try {
    centros.value = await api.get('/api/centros-trabajo')
  } catch (err) {
    error.value = err.message
  }
}

function confirmDelete(centro) {
  centroSeleccionado.value = centro
  showConfirm.value = true
}

async function handleDelete() {
  try {
    await api.delete(`/api/centros-trabajo/${centroSeleccionado.value.id}`)
    showConfirm.value = false
    await loadCentros()
  } catch (err) {
    alert(err.message)
    showConfirm.value = false
  }
}

onMounted(loadCentros)
</script>
