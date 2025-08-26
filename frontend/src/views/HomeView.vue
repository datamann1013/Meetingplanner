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
        md="6"
        lg="4"
      >
        <v-card>
          <v-card-title>{{ event.title }}</v-card-title>
          <v-card-subtitle>
            {{ formatDate(event.date) }} • {{ event.location }}
          </v-card-subtitle>
          <v-card-text>
            <p>{{ truncateText(event.description, 100) }}</p>
            <p>Capacity: {{ event.capacity }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn :to="`/event/${event.id}`" color="primary">View Details</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { strapi } from '@/services/strapi'
import { StrapiResponse, StrapiEntity, Event } from '@/types'
import { useAuthStore } from '@/stores/auth' // <-- Add this import

const events = ref<StrapiEntity<Event>[]>([])
const loading = ref<boolean>(true)
const authStore = useAuthStore() // <-- Initialize the store

onMounted(async (): Promise<void> => {
  try {
    const response = await strapi.get<StrapiResponse<StrapiEntity<Event>[]>>('/events', {
      params: {
        populate: '*',
        sort: 'date:asc'
      }
    })
    events.value = response.data.data
    console.log('Fetched events:', events.value) // <-- Add this line
  } catch (error) {
    console.error('Error fetching events:', error)
  } finally {
    loading.value = false
  }
})

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString()
}

const truncateText = (text: string, maxLength: number): string => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>