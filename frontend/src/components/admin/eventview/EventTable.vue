<template>
  <div class="event-table-wrapper">
    <h3 class="event-section-title">Event List</h3>
    <div class="event-list-top-bar">
      <TextInput
        class="event-search-input"
        id="event-search"
        label="Search events..."
        v-model="searchQuery"
      />
      <InputButton disabled>Advanced Search</InputButton>
      <InputButton disabled>Filter</InputButton>
      <InputButton disabled>Bulk Edit</InputButton>
      <InputButton disabled>Bulk Delete</InputButton>
    </div>
    <div v-if="loading" class="event-list-loading">Loading events...</div>
    <div v-else-if="error" class="event-list-error">Error loading events: {{ error.message }}
    </div>
    <div class="event-table-inner-bg">
      <TableEntry :columns="columns" :rows="events">
        <template #select="{ row }">
          <input type="checkbox" :value="row.id" v-model="selectedEvents" />
        </template>
        <template #name="{ row }">
          <span class="hoverable-cell">{{ row.name }}</span>
        </template>
        <template #date="{ row }">
          <span class="hoverable-cell">{{ formatDateTime(row.date || '') }}</span>
        </template>
        <template #status="{ row }">
          <span class="hoverable-cell">{{ row.status }}</span>
        </template>
        <template #rsvp="{ row }">
          <span class="hoverable-cell">{{ row.rsvp }}</span>
        </template>
        <template #signup_deadline="{ row }">
          <span class="hoverable-cell">{{ formatDateTime(row.signup_deadline || '') }}</span>
        </template>
        <template #description="{ row }">
          <span class="hoverable-cell">{{ row.description }}</span>
        </template>
        <template #after-rows="{ hoveredRow }">
          <div v-if="hoveredRow" class="popup-modal" :style="popupPositionStyle as any">
            <strong>Name:</strong> {{ hoveredRow.name }}<br />
            <strong>Date:</strong> {{ formatDateTime(hoveredRow.date || '') }}<br />
            <strong>Status:</strong> {{ hoveredRow.status }}<br />
            <strong>RSVP:</strong> {{ hoveredRow.rsvp }}<br />
            <strong>Signup Deadline:</strong> {{ formatDateTime(hoveredRow.signup_deadline || '') }}<br />
            <strong>Description:</strong> {{ hoveredRow.description }}
          </div>
        </template>
      </TableEntry>
    </div>
  </div>
</template>

<script setup lang="ts">

import TableEntry from "../../shared/TableEntry.vue";
import TextInput from "../../shared/TextInput.vue";
import InputButton from "../../shared/InputButton.vue";

import { ref } from "vue";
import { EventTable } from "@/composables/EventTable";

const searchQuery = ref("");
const {
  events,
  loading,
  error,
  selectedEvents,
  columns,
  formatDateTime,
} = EventTable();



import { computed } from "vue";

// Optional: You can compute popup position if you want to position it near the hovered row
const popupPositionStyle = computed(() => {
  // For now, just use a fixed style. You can enhance this to position near the row if needed.
  return {
    position: 'absolute',
    left: '50%',
    top: '30%',
    transform: 'translate(-50%, 0)',
    zIndex: 10,
    background: '#fff',
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '1rem',
    boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
  };
});
</script>

<style scoped>
.event-table-inner-bg {
  background: var(--color-table-header-bg, #f5f5f5);
  padding: 0.5rem 0.5rem 0.5rem 0.5rem;
  position: relative;
}

.popup-modal {
  pointer-events: none;
}
</style>
