<template>
  <DashboardBox variant="long">
    <h3 class="rsvp-section-title">RSVPs</h3>
    <div class="rsvp-list-top-bar">
      <TextInput
        class="rsvp-search-input"
        id="rsvp-search"
        label="Search RSVPs..."
        v-model="searchQuery"
      />
      <InputButton @click="showFilter = true">Filter</InputButton>
    </div>
    <Modal v-model="showFilter">
      <h3>Filter RSVPs</h3>
      <p>Here you can add filter options.</p>
    </Modal>
    <div v-if="loading" class="rsvp-list-loading">Loading RSVPs...</div>
    <div v-else-if="error" class="rsvp-list-error">Error loading RSVPs: {{ error.message }}</div>
    <div class="rsvp-table-inner-bg">
      <TableEntry
        :columns="columns"
        :rows="filteredRsvps"
        @row-click="openRsvpModal"
      >
        <template #name="{ row }">
          <span class="hoverable-cell">{{ row.name }}</span>
        </template>
        <template #event="{ row }">
          <span class="hoverable-cell">{{ row.event }}</span>
        </template>
        <template #status="{ row }">
          <span class="hoverable-cell">{{ row.status }}</span>
        </template>
      </TableEntry>
    </div>
    <Modal v-model="showRsvpModal">
      <h3>RSVP Details</h3>
      <div v-if="selectedRsvp">
        <p><strong>Name:</strong> {{ selectedRsvp.name }}</p>
        <p><strong>Event:</strong> {{ selectedRsvp.event }}</p>
        <p><strong>Status:</strong> {{ selectedRsvp.status }}</p>
        <div class="rsvp-status-actions">
          <InputButton @click="updateStatus('Yes')">Yes</InputButton>
          <InputButton @click="updateStatus('No')">No</InputButton>
          <InputButton @click="updateStatus('Not Answered')">Not Answered</InputButton>
        </div>
      </div>
    </Modal>
  </DashboardBox>
</template>


<script setup lang="ts">
import { ref, computed } from 'vue'
import TableEntry from '@/components/shared/TableEntry.vue'
import TextInput from '@/components/shared/TextInput.vue'
import InputButton from '@/components/shared/InputButton.vue'
import Modal from '@/components/shared/Modal.vue'
import DashboardBox from '@/components/admin/DashboardBox.vue'

const searchQuery = ref('')
const showFilter = ref(false)
const showRsvpModal = ref(false)
const loading = ref(false)
const error = ref(null as any)
const selectedRsvp = ref<any>(null)

const columns = [
  { key: 'name', label: 'Name' },
  { key: 'event', label: 'Event' },
  { key: 'status', label: 'Status' }
]

const rsvps = ref([
  { id: 1, name: 'John Doe', event: 'Annual Meeting', status: 'Pending' },
  { id: 2, name: 'Jane Smith', event: 'Annual Meeting', status: 'Confirmed' },
  { id: 3, name: 'Alice Brown', event: 'Annual Meeting', status: 'Declined' }
])

const filteredRsvps = computed(() => {
  if (!searchQuery.value) return rsvps.value
  return rsvps.value.filter(rsvp =>
    rsvp.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    rsvp.event.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

function openRsvpModal(row: any) {
  selectedRsvp.value = row
  showRsvpModal.value = true
}

function updateStatus(status: string) {
  if (selectedRsvp.value) {
    selectedRsvp.value.status = status
    showRsvpModal.value = false
  }
}
</script>

<style scoped>
.rsvp-table-wrapper {
  background: #f5eee6;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.rsvp-section-title {
  margin-bottom: 16px;
}
.rsvp-list-top-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
.rsvp-table-inner-bg {
  border-radius: 8px;
  padding: 12px;
}
.rsvp-status-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}
</style>
