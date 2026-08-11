<template>
  <span :class="['badge', badgeClass]">
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: 'produccion',
  },
})

// Mapeo de estados a labels y clases CSS
const statusMap = {
  produccion: {
    borrador: { label: 'Borrador', class: 'badge-gray' },
    confirmado: { label: 'Confirmado', class: 'badge-info' },
    en_proceso: { label: 'En Proceso', class: 'badge-warning' },
    terminado: { label: 'Terminado', class: 'badge-success' },
    cancelado: { label: 'Cancelado', class: 'badge-danger' },
  },
  orden_trabajo: {
    pendiente: { label: 'Pendiente', class: 'badge-gray' },
    listo: { label: 'Listo', class: 'badge-info' },
    en_proceso: { label: 'En Proceso', class: 'badge-warning' },
    terminado: { label: 'Terminado', class: 'badge-success' },
    cancelado: { label: 'Cancelado', class: 'badge-danger' },
  },
  bom: {
    borrador: { label: 'Borrador', class: 'badge-gray' },
    activo: { label: 'Activo', class: 'badge-success' },
    archivado: { label: 'Archivado', class: 'badge-gray' },
  },
}

const badgeClass = computed(() => {
  const map = statusMap[props.type]
  return map[props.status]?.class || 'badge-gray'
})

const label = computed(() => {
  const map = statusMap[props.type]
  return map[props.status]?.label || props.status
})
</script>
