<template>
  <div class="app-layout">
    <Navbar @toggle-sidebar="sidebarOpen = !sidebarOpen" />
    <div class="app-body">
      <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false"></div>
      <Sidebar :open="sidebarOpen" @close="sidebarOpen = false" />
      <main class="app-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'

const sidebarOpen = ref(false)
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-body {
  display: flex;
  flex: 1;
  position: relative;
}

.app-content {
  flex: 1;
  padding: 24px;
  margin-left: 240px;
  margin-top: 60px;
  transition: margin-left 0.3s;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  top: 60px;
  background: rgba(0, 0, 0, 0.4);
  z-index: 40;
}

@media (max-width: 768px) {
  .app-content {
    margin-left: 0;
    padding: 16px;
  }

  .sidebar-overlay {
    display: block;
  }
}
</style>
