<template>
  <div class="event-list-table-wrapper">
    <EventListTopBar />
    <div v-if="loading" class="event-list-loading">Loading events...</div>
    <div v-else-if="error" class="event-list-error">Error loading events: {{ error.message }}</div>
    <table v-else class="event-list-table">
      <thead>
        <tr>
          <th><input type="checkbox" v-model="selectAll" @change="toggleAll" /></th>
          <th>Event Name</th>
          <th>Date</th>
          <th>Status</th>
          <th>RSVP</th>
          <th>Signup Deadline</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="events.length === 0">
          <td colspan="7">
            No events found.<br>
            <span v-if="!loading && !error">Debug: {{ events }}</span>
          </td>
        </tr>
        <tr v-for="event in events" :key="event.id" :class="{ 'event-row-selected': selectedEvents.includes(event.id) }" @mouseover="hoveredEvent = event.id" @mouseleave="hoveredEvent = null">
          <td><input type="checkbox" :value="event.id" v-model="selectedEvents" /></td>
          <td>{{ event.name }}</td>
          <td>{{ formatDateTime(event.date || '') }}</td>
          <td>{{ event.status }}</td>
          <td>{{ event.rsvp }}</td>
          <td>{{ formatDateTime(event.signup_deadline || '') }}</td>
          <td>{{ event.description }}</td>
        </tr>
      </tbody>
    </table>
    <div v-if="hoveredEvent" class="event-row-details">
      <strong>Details for:</strong> {{ events.find(e => e.id === hoveredEvent)?.name }}<br>
      RSVP: {{ events.find(e => e.id === hoveredEvent)?.rsvp }}<br>
      Status: {{ events.find(e => e.id === hoveredEvent)?.status }}
      <br />Signup Deadline: {{ events.find(e => e.id === hoveredEvent)?.signup_deadline }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import EventListTopBar from './EventListTopBar.vue';
import { strapi } from '../services/strapi';
import { formatDate, formatDateTime } from './DateUtils';

interface EventItem {
  id: string | number;
  name: string;
  date?: string;
  status?: string;
  rsvp?: string;
  tag?: string;
  signup_deadline?: string;
  description?: string;
  coverImage?: string | null;
}
const events = ref<EventItem[]>([]);
const loading = ref(true);
const error = ref<Error | null>(null);
const selectedEvents = ref<(string | number)[]>([])
const selectAll = ref(false)
const hoveredEvent = ref<string | number | null>(null)

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
.event-list-table-wrapper {
  background: none;
  padding: 0;
}
.event-list-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background: none;
}
.event-list-table th, .event-list-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e0e0e0;
  text-align: left;
  background: none;
}
.event-list-table th {
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
</style>
