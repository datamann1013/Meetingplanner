<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Upcoming Events</h1>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary" />
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
        <EventCard :event="event" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import EventCard from '@/components/shared/EventCard.vue'
import { useEventTable } from '@/composables/EventTable'

const { events, loading } = useEventTable()
</script>
