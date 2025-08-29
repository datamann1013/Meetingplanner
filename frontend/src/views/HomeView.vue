<template>
  <v-container>
    <v-row>
      <v-col cols="20">
        <h1 class="text-h4 mb-4">Upcoming Events</h1>
      </v-col>
    </v-row>
    
    <v-row v-if="loading">
      <v-col cols="20" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>
    
    <v-row v-else-if="events.length === 0">
      <v-col cols="20" class="text-center">
        <p>No events found.</p>
      </v-col>
    </v-row>
    <v-row v-else :cols="20">
      <v-col
        v-for="event in events"
        :key="event.id"
        cols="20"
        md="10"
        lg="4"
        class="mb-4"
      >
        <EventCard :event="event" :strapiBaseUrl="strapiBaseUrl" />
      </v-col>
    </v-row>
      <v-dialog v-model="showError" max-width="400">
        <v-card style="position: relative;">
          <v-btn icon @click="showError = false" style="position: absolute; top: 8px; right: 8px; z-index: 10; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-card-title class="d-flex align-center">
            <span>Error</span>
          </v-card-title>
          <v-card-text>
            <div>You don't have access to this resource.</div>
            <div class="mt-2"><strong>Query:</strong> {{ lastFailedQuery }}</div>
          </v-card-text>
        </v-card>
      </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import EventCard from '@/components/EventCard.vue'
import { ref, onMounted } from 'vue'
import { strapi } from '@/services/strapi'
import { StrapiResponse, Event } from '@/types'

const events = ref<Event[]>([])
const loading = ref<boolean>(true)
const showError = ref(false)
const lastFailedQuery = ref('')

const strapiBaseUrl = import.meta.env.VITE_STRAPI_API_URL || 'http://localhost:1337'

onMounted(async (): Promise<void> => {
  try {
    const response = await strapi.get<StrapiResponse<Event[]>>('/events?populate=Coverimage&sort=date:asc')
    events.value = response.data.data
  } catch (error: any) {
    if (error.response?.status === 403) {
      showError.value = true
      lastFailedQuery.value = '/events?populate=Coverimage&sort=date:asc'
    }
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