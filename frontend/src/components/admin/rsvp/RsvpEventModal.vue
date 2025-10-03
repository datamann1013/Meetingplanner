<template>
  <Modal v-model="isOpen" :title="`RSVPs for '${selectedEvent?.name || 'Event'}'`">
    <div>
      <div class="rsvp-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.key"
          :class="['tab-button', { 'active': activeTab === tab.key }]"
          @click="activeTab = tab.key"
        >
          {{ tab.label }} ({{ getTabCount(tab.key) }})
        </button>
      </div>
      
      <div class="tab-content">
        <div v-if="loading" class="rsvp-list-loading">Loading RSVPs...</div>
        <div v-else-if="error" class="rsvp-list-error">Error loading RSVPs: {{ error.message }}</div>
        <div v-else class="rsvp-table-container">
          <TableEntry
            :columns="rsvpColumns"
            :rows="filteredRsvpsByTab"
          >
            <template #user="{ row }">
              <span class="hoverable-cell">{{ row.user?.username || row.user?.email || 'Unknown User' }}</span>
            </template>
            <template #email="{ row }">
              <span class="hoverable-cell">{{ row.user?.email || 'No email' }}</span>
            </template>
            <template #status="{ row }">
              <span class="hoverable-cell status-badge" :class="getStatusClass(row.status_answer)">
                {{ formatStatus(row.status_answer) }}
              </span>
            </template>
            <template #actions="{ row }">
              <div class="action-buttons">
                <button 
                  v-if="asRsvpEntry(row).status_answer !== 'yes'"
                  @click="updateRsvpStatus(asRsvpEntry(row), 'yes')" 
                  class="action-btn accept-btn"
                  title="Mark as Accepted"
                >
                  ✓
                </button>
                <button 
                  v-if="asRsvpEntry(row).status_answer !== 'no'"
                  @click="updateRsvpStatus(asRsvpEntry(row), 'no')" 
                  class="action-btn decline-btn"
                  title="Mark as Declined"
                >
                  ✗
                </button>
                <button 
                  v-if="asRsvpEntry(row).status_answer !== 'mabye/unsure'"
                  @click="updateRsvpStatus(asRsvpEntry(row), 'mabye/unsure')" 
                  class="action-btn maybe-btn"
                  title="Mark as Maybe/Unsure"
                >
                  ?
                </button>
              </div>
            </template>
          </TableEntry>
          
          <div v-if="filteredRsvpsByTab.length === 0" class="no-rsvps">
            No RSVPs found for this status.
          </div>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import Modal from '../../shared/Modal.vue'
import TableEntry from '../../shared/TableEntry.vue'
import { rsvpService, type EventWithRsvps, type RsvpEntry } from '@/services/rsvpService'

interface Props {
  modelValue: boolean
  selectedEvent: EventWithRsvps | null
}

interface Emits {
  'update:modelValue': [value: boolean]
  'update-rsvp': [rsvp: RsvpEntry, status: string]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const isOpen = ref(props.modelValue)
const activeTab = ref('accepted')
const loading = ref(false)
const error = ref(null as any)
const rsvps = ref<RsvpEntry[]>([])

const tabs = [
  { key: 'accepted', label: 'Accepted', status: 'yes' },
  { key: 'declined', label: 'Declined', status: 'no' },
  { key: 'not-answered', label: 'Maybe/Unsure', status: 'mabye/unsure' }
]

const rsvpColumns = [
  { key: 'user', label: 'User' },
  { key: 'email', label: 'Email' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: 'Actions' }
]

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  isOpen.value = newValue
})

watch(() => props.selectedEvent, (newEvent) => {
  if (newEvent) {
    loadRsvpsForEvent(newEvent.id)
  }
})

// Watch for internal changes
watch(isOpen, (newValue) => {
  emit('update:modelValue', newValue)
})

const filteredRsvpsByTab = computed(() => {
  const currentTab = tabs.find(tab => tab.key === activeTab.value)
  if (!currentTab) return []
  
  return rsvps.value.filter(rsvp => rsvp.status_answer === currentTab.status)
})

function getTabCount(tabKey: string) {
  const tab = tabs.find(t => t.key === tabKey)
  if (!tab) return 0
  
  return rsvps.value.filter(rsvp => rsvp.status_answer === tab.status).length
}

function formatStatus(status: string) {
  return rsvpService.formatStatus(status)
}

function getStatusClass(status: string) {
  switch (status) {
    case 'yes': return 'status-accepted'
    case 'no': return 'status-declined'
    case 'mabye/unsure': return 'status-maybe'
    default: return ''
  }
}

async function updateRsvpStatus(rsvp: RsvpEntry, newStatus: 'yes' | 'no' | 'mabye/unsure') {
  try {
    await rsvpService.updateRsvpStatus(rsvp.id, newStatus)
    rsvp.status_answer = newStatus
    emit('update-rsvp', rsvp, newStatus)
  } catch (err) {
    console.error('Failed to update RSVP:', err)
    error.value = err
  }
}

async function loadRsvpsForEvent(eventId: number) {
  loading.value = true
  error.value = null
  
  try {
    rsvps.value = await rsvpService.getRsvpsForEvent(eventId)
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
}

// Helper function for template type casting
function asRsvpEntry(row: any): RsvpEntry {
  return row as RsvpEntry
}
</script>

<style scoped>
.rsvp-tabs {
  display: flex;
  border-bottom: 2px solid var(--color-table-border, #e0e0e0);
  margin-bottom: 1.5rem;
}

.tab-button {
  background: none;
  border: none;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 500;
  color: var(--color-on-surface, #666);
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.tab-button:hover {
  background-color: var(--color-row-selected-bg, #f5f5f5);
}

.tab-button.active {
  color: var(--color-primary-selected, #A3B18A);
  border-bottom-color: var(--color-primary-selected, #A3B18A);
  background-color: var(--color-row-selected-bg, #f9f9f9);
}

.tab-content {
  min-height: 300px;
}

.rsvp-table-container {
  background: var(--color-creme-bg, #fff);
  border-radius: 8px;
  overflow: hidden;
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

.no-rsvps {
  padding: 2rem;
  text-align: center;
  color: var(--color-on-surface-variant, #999);
  font-style: italic;
}

.hoverable-cell {
  cursor: default;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.875rem;
  font-weight: 500;
  text-align: center;
  display: inline-block;
  min-width: 80px;
}

.status-accepted {
  background-color: #e8f5e8;
  color: #2e7d32;
}

.status-declined {
  background-color: #ffebee;
  color: #c62828;
}

.status-maybe {
  background-color: #fff3e0;
  color: #ef6c00;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.accept-btn {
  background-color: #e8f5e8;
  color: #2e7d32;
}

.accept-btn:hover {
  background-color: #c8e6c9;
}

.decline-btn {
  background-color: #ffebee;
  color: #c62828;
}

.decline-btn:hover {
  background-color: #ffcdd2;
}

.maybe-btn {
  background-color: #fff3e0;
  color: #ef6c00;
}

.maybe-btn:hover {
  background-color: #ffe0b2;
}
</style>