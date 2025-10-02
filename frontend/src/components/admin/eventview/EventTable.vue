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
      <TableEntry
        :columns="columns"
        :rows="events"
        @row-click="openEventModal"
        @row-hover="handleRowHover"
        @row-leave="handleRowLeave"
      >
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
          <div v-if="hoveredRow && popupCoords" class="popup-modal" :style="popupPositionStyle as import('vue').CSSProperties">
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
    <Modal v-model="eventModal" :hide-default-close="true">
      <div class="modal-header-row">
        <h3 class="modal-title">Edit Event</h3>
        <button class="modal-close-btn" @click="eventModal = false" aria-label="Close">×</button>
      </div>
      <div class="modal-body">
        <EventCreateDuplicate :mode="'edit'" />
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">


import TableEntry from "../../shared/TableEntry.vue";
import TextInput from "../../shared/TextInput.vue";
import InputButton from "../../shared/InputButton.vue";
import Modal from "../../shared/Modal.vue";
import EventCreateDuplicate from "./EventCreateDuplicate.vue";

import { ref, computed } from "vue";
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

// Register EventCreateDuplicate as a local component for template usage
defineExpose({ EventCreateDuplicate });
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






// --- Popup position logic ---
const popupCoords = ref<{ x: number; y: number } | null>(null);

function handleRowHover(row: any, event: MouseEvent) {
  if (row && event) {
    popupCoords.value = { x: event.clientX, y: event.clientY };
  }
}
function handleRowLeave() {
  popupCoords.value = null;
}

const popupPositionStyle = computed(() => {
  if (!popupCoords.value) return { display: 'none' };
  return {
    position: 'fixed',
    left: popupCoords.value.x + 16 + 'px',
    top: popupCoords.value.y + 8 + 'px',
    zIndex: 20,
    background: '#fff',
    color: 'var(--color-on-surface, #2E2E2E)',
    border: '1px solid var(--color-table-border, #e0e0e0)',
    borderRadius: '8px',
    padding: '1rem',
    boxShadow: 'var(--color-box-shadow, 0 2px 8px rgba(0,0,0,0.15))',
    minWidth: '220px',
    maxWidth: '340px',
    pointerEvents: 'none' as const,
  };
});
</script>
