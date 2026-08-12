<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2>{{ isEdit ? 'Editar Orden de Trabajo' : 'Nueva Orden de Trabajo' }}</h2>
      <router-link to="/ordenes-trabajo" class="btn btn-gray">Volver</router-link>
    </div>

    <div class="table-container p-4" style="max-width: 700px;">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Codigo</label>
          <input v-model="form.nombre" type="text" readonly class="input-readonly" placeholder="Se genera automaticamente" />
        </div>

        <div class="flex gap-4">
          <div class="form-group" style="flex: 1;">
            <label>Produccion *</label>
            <select v-model.number="form.produccion_id" required>
              <option :value="null">Seleccionar...</option>
              <option v-for="prod in producciones" :key="prod.id" :value="prod.id">
                {{ prod.nombre }}
              </option>
            </select>
          </div>
          <div class="form-group" style="flex: 1;">
            <label>Centro de Trabajo</label>
            <select v-model.number="form.centro_trabajo_id">
              <option :value="null">Seleccionar...</option>
              <option v-for="ct in centros" :key="ct.id" :value="ct.id">
                {{ ct.nombre }}
              </option>
            </select>
            <a v-if="centros.length === 0" href="/centros-trabajo/nuevo" class="link-action">Crear centro</a>
          </div>
        </div>

        <div class="flex gap-4">
          <div class="form-group" style="flex: 1;">
            <label>Duracion Esperada (min)</label>
            <input v-model.number="form.duracion_esperada" type="number" step="0.01" min="0" />
          </div>
          <div class="form-group" style="flex: 1;">
            <label>Secuencia</label>
            <input v-model.number="form.secuencia" type="number" />
          </div>
        </div>

        <div class="form-group">
          <label>Notas</label>
          <textarea v-model="form.notas" rows="3" placeholder="Observaciones..."></textarea>
        </div>

        <div class="flex gap-2">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
          <router-link to="/ordenes-trabajo" class="btn btn-gray">Cancelar</router-link>
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
const producciones = ref([])
const centros = ref([])

const isEdit = computed(() => !!route.params.id)

const form = ref({
  nombre: '',
  produccion_id: null,
  centro_trabajo_id: null,
  duracion_esperada: null,
  secuencia: 10,
  notas: '',
})

async function loadFormData() {
  try {
    const [prodsData, centrosData] = await Promise.all([
      api.get('/api/producciones'),
      api.get('/api/centros-trabajo'),
    ])
    producciones.value = prodsData
    centros.value = centrosData
    if (!isEdit.value) {
      const next = await api.get('/api/ordenes-trabajo/next-code')
      form.value.nombre = next.codigo
    }
  } catch (err) {
    console.error('Error cargando datos auxiliares:', err)
  }
}

async function loadOrden() {
  if (!isEdit.value) return
  try {
    const data = await api.get(`/api/ordenes-trabajo/${route.params.id}`)
    form.value = {
      nombre: data.nombre,
      produccion_id: data.produccion_id,
      centro_trabajo_id: data.centro_trabajo_id,
      duracion_esperada: data.duracion_esperada ? parseFloat(data.duracion_esperada) : null,
      secuencia: data.secuencia,
      notas: data.notas || '',
    }
  } catch (err) {
    alert('Error al cargar la orden de trabajo')
  }
}

async function handleSubmit() {
  loading.value = true
  try {
    const payload = {
      ...form.value,
      centro_trabajo_id: form.value.centro_trabajo_id || null,
      duracion_esperada: form.value.duracion_esperada || null,
    }

    if (isEdit.value) {
      await api.put(`/api/ordenes-trabajo/${route.params.id}`, payload)
    } else {
      await api.post('/api/ordenes-trabajo', payload)
    }
    router.push('/ordenes-trabajo')
  } catch (err) {
    alert(err.message)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadFormData()
  await loadOrden()
})
</script>

<style scoped>
.link-action {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: var(--color-primary);
}

.link-action:hover {
  text-decoration: underline;
}
</style>
