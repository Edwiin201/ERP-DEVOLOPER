<template>
  <aside class="sidebar">
    <nav class="sidebar-nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="sidebar-link"
        active-class="active"
      >
        <span class="link-icon">{{ item.icon }}</span>
        <span class="link-text">{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
const menuItems = [
  { path: '/producciones', icon: '&#127993;', label: 'Producciones' },
  { path: '/boms', icon: '&#128203;', label: 'Listas de Materiales' },
  { path: '/ordenes-trabajo', icon: '&#128203;', label: 'Ordenes de Trabajo' },
  { path: '/centros-trabajo', icon: '&#127974;', label: 'Centros de Trabajo' },
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

.link-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}
</style>
