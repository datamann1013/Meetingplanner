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
        <v-card
            :style="event.Coverimage?.url
              ? `background-image: url(${strapiBaseUrl}${event.Coverimage.url}); background-size: cover; background-position: center;`
              : ''"
          class="d-flex flex-column"
        >
          <v-card-title class="text-white" style="background: rgba(0,0,0,0.5);">
            {{ event.title }}
          </v-card-title>
          <v-card-subtitle class="text-white" style="background: rgba(0,0,0,0.3);">
            {{ formatDate(event.date) }} • {{ event.location }}
          </v-card-subtitle>
          <v-card-text style="background: rgba(255,255,255,0.7);">
            <p>{{ truncateText(event.description, 100) }}</p>
            <p>Capacity: {{ event.capacity }}</p>
            <pre>{{ event }}</pre> 
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
import { StrapiResponse, Event } from '@/types'
import { useAuthStore } from '@/stores/auth'

const events = ref<Event[]>([])
const loading = ref<boolean>(true)
const authStore = useAuthStore()
const strapiBaseUrl = import.meta.env.VITE_STRAPI_API_URL || 'http://localhost:1337'

onMounted(async (): Promise<void> => {
  try {
    const response = await strapi.get<StrapiResponse<StrapiEntity<Event>[]>>('/events', {
      params: {
        populate: 'Coverimage',
        sort: 'date:asc'
      }
    })
  events.value = response.data.data
  console.log('Fetched events:', events.value)
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