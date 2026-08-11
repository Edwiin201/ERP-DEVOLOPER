<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2>{{ isEdit ? 'Editar Centro de Trabajo' : 'Nuevo Centro de Trabajo' }}</h2>
      <router-link to="/centros-trabajo" class="btn btn-gray">Volver</router-link>
    </div>

    <div class="table-container p-4" style="max-width: 600px;">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Nombre *</label>
          <input v-model="form.nombre" type="text" required placeholder="Nombre del centro" />
        </div>

        <div class="form-group">
          <label>Codigo *</label>
          <input v-model="form.codigo" type="text" required placeholder="CT-001" />
        </div>

        <div class="form-group">
          <label>Capacidad</label>
          <input v-model.number="form.capacidad" type="number" step="0.01" min="0" />
        </div>

        <div class="form-group">
          <label>Costo por Hora</label>
          <input v-model.number="form.costo_hora" type="number" step="0.01" min="0" />
        </div>

        <div class="form-group">
          <label>
            <input v-model="form.activo" type="checkbox" />
            Activo
          </label>
        </div>

        <div class="form-group">
          <label>Notas</label>
          <textarea v-model="form.notas" rows="3" placeholder="Observaciones..."></textarea>
        </div>

        <div class="flex gap-2">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
          <router-link to="/centros-trabajo" class="btn btn-gray">Cancelar</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api/index.js'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const error = ref(null)

const isEdit = computed(() => !!route.params.id)

const form = ref({
  nombre: '',
  codigo: '',
  capacidad: 1.0,
  costo_hora: 0.0,
  activo: true,
  notas: '',
})

async function loadCentro() {
  if (!isEdit.value) return
  try {
    const data = await api.get(`/api/centros-trabajo/${route.params.id}`)
    form.value = {
      nombre: data.nombre,
      codigo: data.codigo,
      capacidad: parseFloat(data.capacidad),
      costo_hora: parseFloat(data.costo_hora),
      activo: data.activo,
      notas: data.notas || '',
    }
  } catch (err) {
    error.value = err.message
    alert('Error al cargar el centro de trabajo')
  }
}

async function handleSubmit() {
  loading.value = true
  try {
    if (isEdit.value) {
      await api.put(`/api/centros-trabajo/${route.params.id}`, form.value)
    } else {
      await api.post('/api/centros-trabajo', form.value)
    }
    router.push('/centros-trabajo')
  } catch (err) {
    alert(err.message)
  } finally {
    loading.value = false
  }
}

onMounted(loadCentro)
</script>
