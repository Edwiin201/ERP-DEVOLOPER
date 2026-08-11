<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2>{{ isEdit ? 'Editar Produccion' : 'Nueva Produccion' }}</h2>
      <router-link to="/producciones" class="btn btn-gray">Volver</router-link>
    </div>

    <div class="table-container p-4" style="max-width: 700px;">
      <form @submit.prevent="handleSubmit">
        <div class="flex gap-4">
          <div class="form-group" style="flex: 1;">
            <label>Producto ID *</label>
            <input v-model.number="form.producto_id" type="number" required />
          </div>
          <div class="form-group" style="flex: 1;">
            <label>Cantidad *</label>
            <input v-model.number="form.cantidad" type="number" step="0.01" min="0" required />
          </div>
        </div>

        <div class="flex gap-4">
          <div class="form-group" style="flex: 1;">
            <label>Unidad de Medida</label>
            <input v-model="form.producto_uom" type="text" placeholder="unidades" />
          </div>
          <div class="form-group" style="flex: 1;">
            <label>BOM</label>
            <select v-model.number="form.bom_id">
              <option :value="null">Sin BOM</option>
              <option v-for="bom in boms" :key="bom.id" :value="bom.id">
                {{ bom.nombre }}
              </option>
            </select>
          </div>
        </div>

        <div class="flex gap-4">
          <div class="form-group" style="flex: 1;">
            <label>Centro de Trabajo</label>
            <select v-model.number="form.centro_trabajo_id">
              <option :value="null">Sin centro</option>
              <option v-for="ct in centros" :key="ct.id" :value="ct.id">
                {{ ct.nombre }}
              </option>
            </select>
          </div>
          <div class="form-group" style="flex: 1;">
            <label>Fecha Inicio</label>
            <input v-model="form.fecha_inicio" type="datetime-local" />
          </div>
        </div>

        <div class="form-group">
          <label>Fecha Fin</label>
          <input v-model="form.fecha_fin" type="datetime-local" />
        </div>

        <div class="form-group">
          <label>Notas</label>
          <textarea v-model="form.notas" rows="3" placeholder="Observaciones..."></textarea>
        </div>

        <div class="flex gap-2">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
          <router-link to="/producciones" class="btn btn-gray">Cancelar</router-link>
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
const boms = ref([])
const centros = ref([])

const isEdit = computed(() => !!route.params.id)

const form = ref({
  producto_id: null,
  cantidad: 1.0,
  producto_uom: '',
  bom_id: null,
  centro_trabajo_id: null,
  fecha_inicio: '',
  fecha_fin: '',
  notas: '',
})

async function loadFormData() {
  try {
    const [bomsData, centrosData] = await Promise.all([
      api.get('/api/boms'),
      api.get('/api/centros-trabajo'),
    ])
    boms.value = bomsData
    centros.value = centrosData
  } catch (err) {
    console.error('Error cargando datos auxiliares:', err)
  }
}

async function loadProduccion() {
  if (!isEdit.value) return
  try {
    const data = await api.get(`/api/producciones/${route.params.id}`)
    form.value = {
      producto_id: data.producto_id,
      cantidad: parseFloat(data.cantidad),
      producto_uom: data.producto_uom || '',
      bom_id: data.bom_id,
      centro_trabajo_id: data.centro_trabajo_id,
      fecha_inicio: data.fecha_inicio ? data.fecha_inicio.slice(0, 16) : '',
      fecha_fin: data.fecha_fin ? data.fecha_fin.slice(0, 16) : '',
      notas: data.notas || '',
    }
  } catch (err) {
    alert('Error al cargar la produccion')
  }
}

function formatDateTimeLocal(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const pad = n => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

async function handleSubmit() {
  loading.value = true
  try {
    const payload = {
      ...form.value,
      bom_id: form.value.bom_id || null,
      centro_trabajo_id: form.value.centro_trabajo_id || null,
      fecha_inicio: form.value.fecha_inicio || null,
      fecha_fin: form.value.fecha_fin || null,
    }

    if (isEdit.value) {
      await api.put(`/api/producciones/${route.params.id}`, payload)
    } else {
      await api.post('/api/producciones', payload)
    }
    router.push('/producciones')
  } catch (err) {
    alert(err.message)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadFormData()
  await loadProduccion()
})
</script>
