
<template>
  <div class="event-modal">
    <button class="close-btn" @click="$emit('close')">Close</button>
    <div class="modal-content">
      <!-- Edit event form or content will go here -->
      <p>Edit Event Modal Placeholder</p>
      <div v-if="events && events.length">
        <div v-for="event in events" :key="event.id">
          <strong>{{ event.title }}</strong>
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
const emit = defineEmits(['close'])
</script>

<style scoped>
.event-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fffbe6;
  border: 1px solid #bfa77a;
  border-radius: 10px;
  box-shadow: 0 4px 24px #bfa77a44;
  padding: 24px 32px;
  z-index: 1000;
  min-width: 320px;
}
.close-btn {
  position: absolute;
  top: 8px;
  right: 12px;
  background: #ede3d2;
  border: 1px solid #bfa77a;
  border-radius: 4px;
  padding: 4px 10px;
  cursor: pointer;
  font-weight: bold;
}
.modal-content {
  margin-top: 2rem;
}
</style>
