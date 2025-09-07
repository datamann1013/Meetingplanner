<template>
  <div class="event-list-top-bar">
    <input class="event-search-input" type="text" placeholder="Search events..." />
    <button class="event-topbar-btn" disabled>Advanced Search</button>
    <button class="event-topbar-btn" disabled>Filter</button>
    <button class="event-topbar-btn" disabled>Bulk Edit</button>
    <button class="event-topbar-btn" disabled>Bulk Delete</button>
  </div>
</template>

<script setup lang="ts">
// No logic yet, just base layout
</script>

<style scoped>
.event-list-top-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #e0e0e0;
  background: none;
}
.event-search-input {
  flex: 1;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f8f3e6;
  color: #4b3f2a;
}
.event-topbar-btn {
  padding: 0.5rem 1.25rem;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  background: #e0e0e0;
  color: #888;
  cursor: not-allowed;
  opacity: 0.7;
}
</style>
