<template>
  <div class="event-create-duplicate-box">
    <h3>{{ mode === 'create' ? 'Create Event' : 'Duplicate Event' }}</h3>
    <div v-if="mode === 'duplicate'">
      <input v-model="search" placeholder="Search events by tag, name, or date..." class="event-search-input" />
      <ul class="event-list">
        <li v-for="event in filteredEvents" :key="event.id" @click="selectEvent(event)" class="event-list-item">
          <strong>{{ event.title }}</strong> <span>({{ event.date }})</span> <span>{{ event.tag }}</span>
        </li>
      </ul>
      <div v-if="selectedEvent">
        <p>Selected: <strong>{{ selectedEvent.title }}</strong> ({{ selectedEvent.date }})</p>
      </div>
    </div>
    <div v-else>
      <p>Fill in event details below:</p>
      <!-- Simple placeholder for event creation form -->
      <input placeholder="Event Title" class="event-input" />
      <input placeholder="Event Date" class="event-input" />
      <input placeholder="Event Tag" class="event-input" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { EventTable } from '@/composables/event/EventTable'

const props = defineProps<{ mode: 'create' | 'duplicate' }>()
const { events } = EventTable()
const search = ref('')
const selectedEvent = ref<any | null>(null)

const filteredEvents = computed(() => {
  if (!search.value) return events.value
  const s = search.value.toLowerCase()
  return events.value.filter(e =>
    (e.title && e.title.toLowerCase().includes(s)) ||
    (e.tag && e.tag.toLowerCase().includes(s)) ||
    (e.date && e.date.toLowerCase().includes(s))
  )
})

function selectEvent(event: any) {
  selectedEvent.value = event
}
</script>

<style scoped>
.event-create-duplicate-box {
  padding: 1.5rem;
  background: var(--color-primary-bg);
  border-radius: var(--border-radius);
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.event-search-input {
  margin-bottom: 1rem;
  padding: 0.5rem;
  width: 100%;
}
.event-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem 0;
}
.event-list-item {
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}
.event-list-item:hover {
  background: var(--color-secondary-bg);
}
.event-input {
  display: block;
  margin-bottom: 0.75rem;
  padding: 0.5rem;
  width: 100%;
}
</style>
