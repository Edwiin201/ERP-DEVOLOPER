<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <span class="logo-icon">&#9881;</span>
      <h1>ERP Manufactura</h1>
    </div>
    <div class="navbar-info">
      <span>v1.0.0</span>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: var(--color-dark);
  color: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 24px;
}

.navbar-brand h1 {
  font-size: 18px;
  font-weight: 600;
}

.navbar-info {
  font-size: 13px;
  opacity: 0.7;
}
</style>
