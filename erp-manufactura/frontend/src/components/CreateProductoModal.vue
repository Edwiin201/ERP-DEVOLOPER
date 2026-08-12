<template>
  <Teleport to="body">
    <div v-if="visible" class="modal-overlay" @click.self="$emit('cancel')">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="modal-close" @click="$emit('cancel')">&times;</button>
        </div>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Nombre *</label>
            <input v-model="form.nombre" type="text" required placeholder="Nombre del producto" />
          </div>
          <div class="form-group">
            <label>Tipo</label>
            <select v-model="form.tipo">
              <option value="producto_final">Producto Final</option>
              <option value="materia_prima">Materia Prima</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn btn-gray" @click="$emit('cancel')">Cancelar</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { api } from '../api/index.js'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: 'Nuevo Producto',
  },
})

const emit = defineEmits(['confirm', 'cancel'])

const loading = ref(false)
const form = ref({
  nombre: '',
  tipo: 'producto_final',
})

watch(() => props.visible, (val) => {
  if (val) {
    form.value = { nombre: '', tipo: 'producto_final' }
  }
})

async function handleSubmit() {
  loading.value = true
  try {
    const nuevo = await api.post('/api/productos', form.value)
    emit('confirm', nuevo)
  } catch (err) {
    alert(err.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.modal {
  background: var(--color-white);
  padding: 24px;
  border-radius: var(--border-radius);
  max-width: 400px;
  width: 90%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.modal-header h3 {
  font-size: 18px;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--color-gray);
  cursor: pointer;
  padding: 0 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 20px;
}
</style>
