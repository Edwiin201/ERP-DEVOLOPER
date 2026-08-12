<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2>{{ isEdit ? 'Editar BOM' : 'Nuevo BOM' }}</h2>
      <router-link to="/boms" class="btn btn-gray">Volver</router-link>
    </div>

    <div class="table-container p-4">
      <form @submit.prevent="handleSubmit">
        <div class="flex gap-4">
          <div class="form-group" style="flex: 1;">
            <label>Codigo</label>
            <input v-model="form.codigo" type="text" readonly class="input-readonly" placeholder="Se genera automaticamente" />
          </div>
          <div class="form-group" style="flex: 2;">
            <label>Nombre *</label>
            <input v-model="form.nombre" type="text" required placeholder="Nombre del BOM" />
          </div>
        </div>

        <div class="flex gap-4">
          <div class="form-group" style="flex: 1;">
            <label>Producto *</label>
            <select v-model.number="form.producto_id" required>
              <option :value="null">Seleccionar producto...</option>
              <option v-for="prod in productos" :key="prod.id" :value="prod.id">
                {{ prod.nombre }} ({{ prod.tipo === 'producto_final' ? 'PF' : 'MP' }})
              </option>
            </select>
          </div>
          <div class="form-group" style="flex: 1;">
            <label>Cantidad</label>
            <input v-model.number="form.cantidad" type="number" step="0.01" min="0" />
          </div>
          <div class="form-group" style="flex: 1;">
            <label>Unidad de Medida</label>
            <input v-model="form.producto_uom" type="text" placeholder="ej: unidades, kg, litros, metros" />
          </div>
        </div>

        <!-- Lineas del BOM -->
        <div class="mt-4">
          <div class="flex items-center justify-between mb-4">
            <h3>Lineas de Materiales</h3>
            <button type="button" class="btn btn-sm btn-primary" @click="addLinea">
              + Agregar Linea
            </button>
          </div>

          <div class="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Secuencia</th>
                  <th>Producto</th>
                  <th>Cantidad</th>
                  <th>Unidad</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(linea, index) in form.lineas" :key="index">
                  <td>
                    <input v-model.number="linea.secuencia" type="number" style="width: 80px;" />
                  </td>
                  <td>
                    <select v-model.number="linea.producto_id" required style="width: 100%;">
                      <option :value="null">Seleccionar...</option>
                      <option v-for="prod in productos" :key="prod.id" :value="prod.id">
                        {{ prod.nombre }}
                      </option>
                    </select>
                  </td>
                  <td>
                    <input v-model.number="linea.cantidad" type="number" step="0.01" min="0" style="width: 100px;" />
                  </td>
                  <td>
                    <input v-model="linea.producto_uom" type="text" placeholder="ej: unidades, kg, litros" style="width: 120px;" />
                  </td>
                  <td>
                    <button type="button" class="btn btn-sm btn-danger" @click="removeLinea(index)">
                      X
                    </button>
                  </td>
                </tr>
                <tr v-if="form.lineas.length === 0">
                  <td colspan="5" style="text-align: center; color: var(--color-gray);">
                    Sin lineas. Haga clic en "+ Agregar Linea"
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="flex gap-2 mt-4">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
          <router-link to="/boms" class="btn btn-gray">Cancelar</router-link>
        </div>
      </form>
    </div>

    <button class="fab" @click="showProductoModal = true" title="Nuevo Producto">+</button>

    <CreateProductoModal
      :visible="showProductoModal"
      @confirm="onProductoCreated"
      @cancel="showProductoModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api/index.js'
import CreateProductoModal from '../components/CreateProductoModal.vue'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const productos = ref([])
const showProductoModal = ref(false)

const isEdit = computed(() => !!route.params.id)

const form = ref({
  codigo: '',
  nombre: '',
  producto_id: null,
  cantidad: 1.0,
  producto_uom: '',
  lineas: [],
})

async function loadFormData() {
  try {
    productos.value = await api.get('/api/productos')
    if (!isEdit.value) {
      const next = await api.get('/api/boms/next-code')
      form.value.codigo = next.codigo
    }
  } catch (err) {
    console.error('Error cargando datos:', err)
  }
}

async function loadBom() {
  if (!isEdit.value) return
  try {
    const data = await api.get(`/api/boms/${route.params.id}`)
    form.value = {
      codigo: data.codigo || '',
      nombre: data.nombre,
      producto_id: data.producto_id,
      cantidad: parseFloat(data.cantidad),
      producto_uom: data.producto_uom || '',
      lineas: data.lineas.map(l => ({
        producto_id: l.producto_id,
        cantidad: parseFloat(l.cantidad),
        producto_uom: l.producto_uom || '',
        secuencia: l.secuencia,
      })),
    }
  } catch (err) {
    alert('Error al cargar el BOM')
  }
}

function addLinea() {
  form.value.lineas.push({
    producto_id: null,
    cantidad: 1.0,
    producto_uom: '',
    secuencia: (form.value.lineas.length + 1) * 10,
  })
}

function removeLinea(index) {
  form.value.lineas.splice(index, 1)
}

function onProductoCreated(nuevo) {
  productos.value.push(nuevo)
  form.value.producto_id = nuevo.id
  showProductoModal.value = false
}

async function handleSubmit() {
  loading.value = true
  try {
    if (isEdit.value) {
      await api.put(`/api/boms/${route.params.id}`, form.value)
    } else {
      await api.post('/api/boms', form.value)
    }
    router.push('/boms')
  } catch (err) {
    alert(err.message)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadFormData()
  await loadBom()
})
</script>
