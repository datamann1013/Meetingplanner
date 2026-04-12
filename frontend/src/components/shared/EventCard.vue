<template>
  <v-card
    :style="coverImageStyle"
    class="d-flex flex-column justify-end card-relative event-card"
    height="250"
  >
    <div class="event-info-bar">
      <span class="event-title">{{ event.title }}</span>
      <span class="event-date event-date-bottomright">{{ formatDate(event.date) }}</span>
    </div>
    <v-btn icon color="primary" size="small" class="event-info-btn-topright">
      <v-icon color="secondary">mdi-information</v-icon>
    </v-btn>
    <div class="event-hover-overlay">
      <div class="event-info-bar event-info-bar-hover">
        <span class="event-title">{{ event.title }}</span>
      </div>
      <span class="event-date event-date-bottomright">{{ formatDate(event.date) }}</span>
      <span class="event-deadline event-deadline-bottomleft">
        Signup: {{ event.signup_deadline ? formatDate(event.signup_deadline) : 'No deadline' }}
      </span>
      <v-btn icon color="primary" size="small" class="event-info-btn-topright">
        <v-icon color="secondary">mdi-information</v-icon>
      </v-btn>
      <span class="event-description-label">Description</span>
      <p class="event-description">{{ event.description }}</p>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import type { Event } from '@/types'
import { useEventCard } from '@/composables/EventCard'

const props = defineProps<{ event: Event }>()
const { coverImageStyle, formatDate } = useEventCard(props.event)
</script>
