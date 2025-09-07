<template>
  <div class="event-table-wrapper">
    <div class="event-list-top-bar">
      <input class="event-search-input" type="text" placeholder="Search events..." />
      <button class="event-topbar-btn" disabled>Advanced Search</button>
      <button class="event-topbar-btn" disabled>Filter</button>
      <button class="event-topbar-btn" disabled>Bulk Edit</button>
      <button class="event-topbar-btn" disabled>Bulk Delete</button>
    </div>
    <div v-if="loading" class="event-list-loading">Loading events...</div>
    <div v-else-if="error" class="event-list-error">Error loading events: {{ error.message }}
    </div>
    <TableEntry :columns="columns" :rows="events">
      <template #select="{ row }">
        <input type="checkbox" :value="row.id" v-model="selectedEvents" />
      </template>
      <template #name="{ row }">
        <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'name'" @mouseleave="hoveredEvent = null; hoveredField = null">
          {{ row.name }}
          <div v-if="hoveredEvent === row.id && hoveredField === 'name'" class="popup-info">
            <strong>Name:</strong> {{ row.name }}
          </div>
        </span>
      </template>
      <template #date="{ row }">
        <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'date'" @mouseleave="hoveredEvent = null; hoveredField = null">
          {{ formatDateTime(row.date || '') }}
          <div v-if="hoveredEvent === row.id && hoveredField === 'date'" class="popup-info">
            <strong>Date:</strong> {{ formatDateTime(row.date || '') }}
          </div>
        </span>
      </template>
      <template #status="{ row }">
        <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'status'" @mouseleave="hoveredEvent = null; hoveredField = null">
          {{ row.status }}
          <div v-if="hoveredEvent === row.id && hoveredField === 'status'" class="popup-info">
            <strong>Status:</strong> {{ row.status }}
          </div>
        </span>
      </template>
      <template #rsvp="{ row }">
        <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'rsvp'" @mouseleave="hoveredEvent = null; hoveredField = null">
          {{ row.rsvp }}
          <div v-if="hoveredEvent === row.id && hoveredField === 'rsvp'" class="popup-info">
            <strong>RSVP:</strong> {{ row.rsvp }}
          </div>
        </span>
      </template>
      <template #signup_deadline="{ row }">
        <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'signup_deadline'" @mouseleave="hoveredEvent = null; hoveredField = null">
          {{ formatDateTime(row.signup_deadline || '') }}
          <div v-if="hoveredEvent === row.id && hoveredField === 'signup_deadline'" class="popup-info">
            <strong>Signup Deadline:</strong> {{ formatDateTime(row.signup_deadline || '') }}
          </div>
        </span>
      </template>
      <template #description="{ row }">
        <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'description'" @mouseleave="hoveredEvent = null; hoveredField = null">
          {{ row.description }}
          <div v-if="hoveredEvent === row.id && hoveredField === 'description'" class="popup-info">
            <strong>Description:</strong> {{ row.description }}
          </div>
        </span>
      </template>
    </TableEntry>
    <div v-if="hoveredEvent" class="event-row-details">
      <strong>Details for:</strong> {{ events.find(e => e.id === hoveredEvent)?.name }}<br>
      RSVP: {{ events.find(e => e.id === hoveredEvent)?.rsvp }}<br>
      Status: {{ events.find(e => e.id === hoveredEvent)?.status }}
      <br />Signup Deadline: {{ events.find(e => e.id === hoveredEvent)?.signup_deadline }}
      <br />Description: {{ events.find(e => e.id === hoveredEvent)?.description }}
      <br />Date: {{ formatDateTime(events.find(e => e.id === hoveredEvent)?.date || '') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import TableEntry from "../../shared/TableEntry.vue";
import { strapi } from '../../../services/strapi';
import { formatDateTime } from '../../DateUtils';

defineProps<{
  topBarProps?: Record<string, any>
}>()

const events = ref<any[]>([]);
const loading = ref(true);
const error = ref<Error | null>(null);
const selectedEvents = ref<(string | number)[]>([])
const selectAll = ref(false)
const hoveredEvent = ref<string | number | null>(null)
const hoveredField = ref<string | null>(null)

const columns = [
  { key: 'select', label: '' },
  { key: 'name', label: 'Event Name' },
  { key: 'date', label: 'Date' },
  { key: 'status', label: 'Status' },
  { key: 'rsvp', label: 'RSVP' },
  { key: 'signup_deadline', label: 'Signup Deadline' },
  { key: 'description', label: 'Description' }
]

onMounted(async () => {
  try {
    const res: any = await strapi.get('/events?populate=*');
    if (res.data && Array.isArray(res.data.data)) {
      events.value = res.data.data.map((item: any) => ({
        id: item.id,
        name: item.title,
        date: item.date,
        status: item.status || 'Draft',
        rsvp: item.rsvp_count || '0/0',
        tag: item.tag || '',
        signup_deadline: item.signup_deadline,
        description: item.description,
        coverImage: item.Coverimage?.url || null,
      }));
    } else {
      events.value = [];
    }
  } catch (err) {
    error.value = err instanceof Error ? err : new Error(String(err));
    events.value = [];
  } finally {
    loading.value = false;
  }
})

function toggleAll() {
  if (selectAll.value) {
    selectedEvents.value = events.value.map(e => e.id)
  } else {
    selectedEvents.value = []
  }
}
</script>

<style scoped>
.event-table-wrapper {
  background: none;
  padding: 0;
}
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
.event-list-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background: none;
}
.table-entry th, .table-entry td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e0e0e0;
  text-align: left;
  background: none;
}
.table-entry th {
  background: #f8f3e6;
  color: #4b3f2a;
}
.event-row-selected {
  background: #f5eee6;
}
.event-tag-placeholder {
  color: #aaa;
  font-style: italic;
}
.event-status-placeholder {
  color: #76944C;
  font-weight: 500;
}
.event-row-details {
  margin-top: 1rem;
  padding: 1rem;
  background: #FBF5DB;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  color: #2E2E2E;
}
.event-list-loading, .event-list-error {
  padding: 1rem;
  text-align: center;
}
.event-list-error {
  color: #e74c3c;
}
.hoverable-cell {
  position: relative;
  cursor: pointer;
}
.popup-info {
  position: absolute;
  left: 100%;
  top: 50%;
  transform: translateY(-50%);
  background: #FBF5DB;
  color: #2E2E2E;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  padding: 0.5rem 1rem;
  min-width: 180px;
  z-index: 10;
  white-space: pre-line;
}
</style>
