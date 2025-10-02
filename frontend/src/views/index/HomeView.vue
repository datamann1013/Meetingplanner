<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Upcoming Events</h1>
      </v-col>
    </v-row>
    
    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>
    
    <v-row v-else-if="events.length === 0">
      <v-col cols="12" class="text-center">
        <p>No events found.</p>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col
        v-for="event in events"
        :key="event.id"
        cols="12"
        md="12"
        lg="4"
        class="mb-4"
      >
        <EventCard :event="event" :strapiBaseUrl="strapiBaseUrl" />
      </v-col>
    </v-row>
      <Modal v-model="showError" :hide-default-close="true">
        <div class="modal-header-row">
          <h3 class="modal-title">Error</h3>
          <button class="modal-close-btn" @click="showError = false" aria-label="Close">×</button>
        </div>
        <div class="modal-body">
          <div>You don't have access to this resource.</div>
          <div class="mt-2"><strong>Query:</strong> {{ lastFailedQuery }}</div>
        </div>
      </Modal>
  </v-container>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import { EventTable } from '@/composables/EventTable'
import EventCard from '../../components/shared/EventCard.vue'
import Modal from '../../components/shared/Modal.vue'

const {
  events: rawEvents,
  loading,
} = EventTable()

// Ensure events have the expected structure with a title property
import { computed } from 'vue'
const events = computed(() =>
  rawEvents.value.map(event =>
    event.title
      ? event
      : event.attributes && event.attributes.title
        ? { ...event, title: event.attributes.title }
        : event // fallback, may need more mapping depending on actual structure
  )
)
const showError = ref(false)
const lastFailedQuery = ref('')
const strapiBaseUrl = import.meta.env.VITE_STRAPI_API_URL || 'http://localhost:1337'
</script>

<style scoped>
.modal-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-title {
  margin: 0;
  color: var(--v-theme-on-surface, #000);
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--v-theme-on-surface, #000);
  padding: 0.25rem;
  line-height: 1;
}

.modal-close-btn:hover {
  color: var(--v-theme-on-surface-variant, #666);
}

.modal-body {
  margin-top: 0;
}

.mt-2 {
  margin-top: 0.5rem;
}
</style>