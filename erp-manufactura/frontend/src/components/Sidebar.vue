<template>
  <aside :class="['sidebar', { 'sidebar-open': open }]">
    <button class="sidebar-close" @click="$emit('close')">&times;</button>
    <nav class="sidebar-nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="sidebar-link"
        active-class="active"
        @click="$emit('close')"
      >
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
defineProps({
  open: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['close'])

const menuItems = [
  { path: '/producciones', label: 'Producciones' },
  { path: '/boms', label: 'Listas de Materiales' },
  { path: '/ordenes-trabajo', label: 'Ordenes de Trabajo' },
  { path: '/centros-trabajo', label: 'Centros de Trabajo' },
]
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  width: 240px;
  background: var(--color-white);
  border-right: 1px solid #e5e7eb;
  padding: 16px 0;
  overflow-y: auto;
  z-index: 50;
  transition: transform 0.3s;
}

.sidebar-close {
  display: none;
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  font-size: 24px;
  color: var(--color-gray);
  cursor: pointer;
  padding: 4px 8px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 8px;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  border-radius: var(--border-radius);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-dark);
  transition: all 0.2s;
}

.sidebar-link:hover {
  background: var(--color-light);
}

.sidebar-link.active {
  background: var(--color-primary);
  color: var(--color-white);
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar.sidebar-open {
    transform: translateX(0);
  }

  .sidebar-close {
    display: block;
  }
}
</style>
