<template>
  <div class="rsvp-events-table-wrapper">
    <h3 class="rsvp-section-title">Event RSVPs</h3>
    <div class="rsvp-list-top-bar">
      <TextInput
        class="rsvp-search-input"
        id="rsvp-search"
        label="Search events..."
        v-model="searchQuery"
      />
      <InputButton @click="showFilter = true">Filter</InputButton>
      <InputButton @click="refreshEvents">Refresh</InputButton>
    </div>
    
    <Modal v-model="showFilter">
      <h3>Filter Events</h3>
      <p>Here you can add filter options for events.</p>
    </Modal>
    
    <div v-if="loading" class="rsvp-list-loading">Loading events...</div>
    <div v-else-if="error" class="rsvp-list-error">Error loading events: {{ error.message }}</div>
    
    <div class="rsvp-table-inner-bg">
      <TableEntry
        :columns="columns"
        :rows="filteredEvents"
        @row-click="openRsvpModal"
        @row-hover="handleRowHover"
        @row-leave="handleRowLeave"
      >
        <template #name="{ row }">
          <span class="hoverable-cell">{{ row.name }}</span>
        </template>
        <template #date="{ row }">
          <span class="hoverable-cell">{{ formatDateTime(row.date || '') }}</span>
        </template>
        <template #rsvp_count="{ row }">
          <span class="hoverable-cell">
            <div class="rsvp-summary">
              <span class="rsvp-accepted">{{ row.rsvp_stats?.accepted || 0 }} ✓</span>
              <span class="rsvp-declined">{{ row.rsvp_stats?.declined || 0 }} ✗</span>
              <span class="rsvp-maybe">{{ row.rsvp_stats?.maybe || 0 }} ?</span>
            </div>
          </span>
        </template>
        <template #total_rsvps="{ row }">
          <span class="hoverable-cell">{{ row.rsvp_stats?.total || 0 }}</span>
        </template>
        <template #status="{ row }">
          <span class="hoverable-cell">{{ row.status }}</span>
        </template>
        <template #after-rows="{ hoveredRow }">
          <div v-if="hoveredRow && popupCoords" class="popup-modal" :style="popupPositionStyle">
            <strong>Event:</strong> {{ hoveredRow.name }}<br />
            <strong>Date:</strong> {{ formatDateTime(hoveredRow.date || '') }}<br />
            <strong>Status:</strong> {{ hoveredRow.status }}<br />
            <strong>RSVPs:</strong><br />
            <div class="popup-rsvp-details">
              <span class="popup-accepted">Accepted: {{ hoveredRow.rsvp_stats?.accepted || 0 }}</span><br />
              <span class="popup-declined">Declined: {{ hoveredRow.rsvp_stats?.declined || 0 }}</span><br />
              <span class="popup-maybe">Maybe: {{ hoveredRow.rsvp_stats?.maybe || 0 }}</span><br />
              <span class="popup-total">Total: {{ hoveredRow.rsvp_stats?.total || 0 }}</span>
            </div>
            <em>Click to view detailed RSVPs</em>
          </div>
        </template>
      </TableEntry>
    </div>
    
    <RsvpEventModal 
      v-model="showRsvpModal" 
      :selected-event="selectedEvent"
      @update-rsvp="handleRsvpUpdate"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import TableEntry from '@/components/shared/TableEntry.vue'
import TextInput from '@/components/shared/TextInput.vue'
import InputButton from '@/components/shared/InputButton.vue'
import Modal from '@/components/shared/Modal.vue'
import RsvpEventModal from './RsvpEventModal.vue'
import { rsvpService, type EventWithRsvps } from '@/services/rsvpService'

const searchQuery = ref('')
const showFilter = ref(false)
const showRsvpModal = ref(false)
const loading = ref(false)
const error = ref(null as any)
const selectedEvent = ref<EventWithRsvps | null>(null)
const events = ref<EventWithRsvps[]>([])

const columns = [
  { key: 'name', label: 'Event Name' },
  { key: 'date', label: 'Date' },
  { key: 'rsvp_count', label: 'RSVP Status' },
  { key: 'total_rsvps', label: 'Total RSVPs' },
  { key: 'status', label: 'Event Status' }
]

const filteredEvents = computed(() => {
  if (!searchQuery.value) return events.value
  return events.value.filter(event =>
    event.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

onMounted(() => {
  loadEvents()
})

async function loadEvents() {
  loading.value = true
  error.value = null
  try {
    events.value = await rsvpService.getEventsWithRsvpStats()
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
}

function openRsvpModal(event: EventWithRsvps) {
  selectedEvent.value = event
  showRsvpModal.value = true
}

function handleRsvpUpdate(rsvp: any, newStatus: string) {
  // The service handles updating the statistics automatically
  console.log('RSVP updated:', rsvp, 'to status:', newStatus)
  // Refresh events to get updated statistics
  loadEvents()
}

async function refreshEvents() {
  await loadEvents()
}

function formatDateTime(dateString: string) {
  return rsvpService.formatDateTime(dateString)
}

// Popup position logic
const popupCoords = ref<{ x: number; y: number } | null>(null)

function handleRowHover(row: any, event: MouseEvent) {
  if (row && event) {
    popupCoords.value = { x: event.clientX, y: event.clientY }
  }
}

function handleRowLeave() {
  popupCoords.value = null
}

const popupPositionStyle = computed(() => {
  if (!popupCoords.value) return { display: 'none' }
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
  }
})
</script>

<style scoped>
.rsvp-events-table-wrapper {
  width: 100%;
}

.rsvp-section-title {
  margin: 0 0 1rem 0;
  color: var(--color-on-surface, #2E2E2E);
  font-size: 1.5rem;
  font-weight: 600;
}

.rsvp-list-top-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: flex-end;
}

.rsvp-search-input {
  flex: 1;
  max-width: 300px;
}

.rsvp-list-loading,
.rsvp-list-error {
  padding: 2rem;
  text-align: center;
  color: var(--color-on-surface, #666);
}

.rsvp-list-error {
  color: var(--color-error, #d32f2f);
}

.rsvp-table-inner-bg {
  background: var(--color-creme-bg, #fff);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-table-border, #e0e0e0);
}

.hoverable-cell {
  cursor: pointer;
}

.rsvp-summary {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.rsvp-accepted,
.rsvp-declined,
.rsvp-maybe {
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  min-width: 35px;
  text-align: center;
}

.rsvp-accepted {
  background-color: #e8f5e8;
  color: #2e7d32;
}

.rsvp-declined {
  background-color: #ffebee;
  color: #c62828;
}

.rsvp-maybe {
  background-color: #fff3e0;
  color: #ef6c00;
}

.popup-modal {
  position: fixed;
  background: var(--color-popup-bg, white);
  border: 1px solid var(--color-table-border, #e0e0e0);
  border-radius: 8px;
  padding: 1rem;
  box-shadow: var(--color-box-shadow, 0 2px 8px rgba(0,0,0,0.15));
  z-index: 20;
  font-size: 0.875rem;
}

.popup-rsvp-details {
  margin: 0.5rem 0;
  padding-left: 0.5rem;
}

.popup-accepted {
  color: #2e7d32;
}

.popup-declined {
  color: #c62828;
}

.popup-maybe {
  color: #ef6c00;
}

.popup-total {
  font-weight: bold;
  color: var(--color-on-surface, #2E2E2E);
}
</style>