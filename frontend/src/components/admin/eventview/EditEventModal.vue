
<template>
  <div class="event-admin-box event-modal">
    <button class="close-btn" @click="$emit('close')">×</button>
    <h3 class="event-section-title">Edit Event</h3>
    <div class="modal-content">
      <div v-if="events && events.length">
        <div v-for="event in events" :key="event.id" class="event-list-item">
          <strong>{{ event.title }}</strong>
          <button class="select-btn" @click="openEditModal(event)">Select</button>
        </div>
      </div>
      <div v-else>
        <em>No events for this date.</em>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ date: string, events: any[] }>()
const emit = defineEmits(['close', 'editEvent'])

function openEditModal(event: any) {
  emit('editEvent', event)
  emit('close')
}
</script>

<style scoped>
.event-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  min-width: 340px;
  max-width: 95vw;
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 18px;
  background: var(--color-table-header-bg, #f5f5f5);
  border: 1.5px solid var(--color-primary-border, #b5c9a3);
  border-radius: 4px;
  padding: 4px 12px;
  cursor: pointer;
  font-weight: bold;
  color: var(--color-accent, #76944C);
  font-size: 1.2rem;
}
.modal-content {
  margin-top: 1.5rem;
}
.event-list-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-primary-border, #b5c9a3);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.select-btn {
  background: var(--color-accent, #76944C);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: 600;
}
</style>
