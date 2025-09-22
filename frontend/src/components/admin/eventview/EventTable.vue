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
  <InputButton @click="showAdvancedSearch = true">Advanced Search</InputButton>
  <InputButton @click="showFilter = true">Filter</InputButton>
  <InputButton @click="showBulkEdit = true">Bulk Edit</InputButton>
  <InputButton @click="showBulkDelete = true">Bulk Delete</InputButton>
    </div>
    <Modal v-model="showAdvancedSearch">
      <h3>Advanced Search</h3>
      <p>Here you can add advanced search options.</p>
      <!-- Add your advanced search form here -->
    </Modal>
    <Modal v-model="showFilter">
      <h3>Filter Events</h3>
      <p>Here you can add filter options.</p>
      <!-- Add your filter form here -->
    </Modal>
    <Modal v-model="showBulkEdit">
      <h3>Bulk Edit Events</h3>
      <p>Here you can add bulk edit options.</p>
      <!-- Add your bulk edit form here -->
    </Modal>
    <Modal v-model="showBulkDelete">
      <h3>Bulk Delete Events</h3>
      <p>Are you sure you want to delete the selected events?</p>
      <button @click="confirmBulkDelete">Yes, Delete</button>
      <button @click="showBulkDelete = false">Cancel</button>
    </Modal>
    <div v-if="loading" class="event-list-loading">Loading events...</div>
    <div v-else-if="error" class="event-list-error">Error loading events: {{ error.message }}
    </div>
    <div class="event-table-inner-bg">
      <TableEntry :columns="columns" :rows="events" @row-click="openEventModal">
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
    <Modal v-model="eventModal">
      <h3>{{ selectedEvent ? `Edit Event: ${selectedEvent.name}` : 'Edit Event' }}</h3>
      <div class="modal-body">
        <div>Event form fields go here (placeholder)</div>
        <div v-if="selectedEvent">
          <strong>Date:</strong> {{ formatDateTime(selectedEvent.date || '') }}<br />
          <strong>Status:</strong> {{ selectedEvent.status }}<br />
          <strong>RSVP:</strong> {{ selectedEvent.rsvp }}<br />
          <strong>Signup Deadline:</strong> {{ formatDateTime(selectedEvent.signup_deadline || '') }}<br />
          <strong>Description:</strong> {{ selectedEvent.description }}
        </div>
      </div>
      <div class="modal-actions">
        <button @click="eventModal = false">Cancel</button>
        <button>Save Changes</button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">


import TableEntry from "../../shared/TableEntry.vue";
import TextInput from "../../shared/TextInput.vue";
import InputButton from "../../shared/InputButton.vue";
import Modal from "../../shared/Modal.vue";

import { ref } from "vue";
import { EventTable } from "@/composables/EventTable";


const searchQuery = ref("");
const showAdvancedSearch = ref(false);
const showFilter = ref(false);
const showBulkEdit = ref(false);
const showBulkDelete = ref(false);

// Event modal state
const eventModal = ref(false)
const selectedEvent = ref<any>(null)
function openEventModal(event: any) {
  selectedEvent.value = event
  eventModal.value = true
}

const {
  events,
  loading,
  error,
  selectedEvents,
  columns,
  formatDateTime,
} = EventTable();

function confirmBulkDelete() {
  // Implement your bulk delete logic here
  showBulkDelete.value = false;
}



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
