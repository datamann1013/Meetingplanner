<template>
  <v-card
    :style="event.Coverimage?.url
      ? `background-image: url(${strapiBaseUrl}${event.Coverimage.url}); background-size: cover; background-position: center;`
      : `background-color: var(--v-theme-surface);`
    "
    class="d-flex flex-column justify-end card-relative event-card"
    height="250"
  >
    <div class="event-info-bar">
      <span style="color: #212121; font-size: 1.7rem; font-weight: 900; text-shadow: 0 2px 8px rgba(0,0,0,0.25);">{{ event.title }}</span>
      <span class="event-date-bottomright" style="color: #212121; font-weight: bold; text-shadow: 0 2px 8px rgba(0,0,0,0.25);">{{ formatDate(event.date) }}</span>
    </div>
    <v-btn icon color="primary" size="small" class="event-info-btn-topright">
      <v-icon color="secondary">mdi-information</v-icon>
    </v-btn>
    <div class="event-hover-overlay">
      <div class="event-info-bar event-info-bar-hover">
        <span style="color: #212121; font-size: 1.7rem; font-weight: 900; text-shadow: 0 2px 8px rgba(0,0,0,0.25);">{{ event.title }}</span>
      </div>
      <span class="event-date-bottomright" style="color: #212121; font-weight: bold; text-shadow: 0 2px 8px rgba(0,0,0,0.25);">{{ formatDate(event.date) }}</span>
      <span class="event-deadline-bottomleft" style="color: #212121; font-weight: bold;">Signup: {{ formatDate(event.signup_deadline) }}</span>
      <v-btn icon color="primary" size="small" class="event-info-btn-topright">
        <v-icon color="secondary">mdi-information</v-icon>
      </v-btn>
      <span style="color: #212121; font-weight: bold; margin-top: 32px;">Description</span>
      <p style="color: #212121; margin-top: 8px;">{{ event.description }}</p>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
const props = defineProps<{ event: any, strapiBaseUrl: string }>()
function formatDate(date: string) {
  return new Date(date).toLocaleDateString()
}
</script>
