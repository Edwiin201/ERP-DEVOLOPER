<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <button class="hamburger" @click="$emit('toggle-sidebar')">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <span class="logo-icon">&#9881;</span>
      <h1>ERP Manufactura</h1>
    </div>
  </nav>
</template>

<script setup>
defineEmits(['toggle-sidebar'])
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

.hamburger {
  display: none;
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  flex-direction: column;
  gap: 4px;
}

.hamburger span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--color-white);
  border-radius: 2px;
}

.logo-icon {
  font-size: 24px;
}

.navbar-brand h1 {
  font-size: 18px;
  font-weight: 600;
}

@media (max-width: 768px) {
  .hamburger {
    display: flex;
  }

  .navbar {
    padding: 0 16px;
  }

  .navbar-brand h1 {
    font-size: 16px;
  }
}
</style>
