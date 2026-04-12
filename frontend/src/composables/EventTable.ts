import { onMounted, ref } from 'vue'
import { fetchEvents } from '@/services/eventData'
import type { Event } from '@/types'
import { formatDateTime } from './DateUtils'

export function useEventTable() {
  const events = ref<Event[]>([])
  const loading = ref(true)
  const error = ref<Error | null>(null)
  const selectedEvents = ref<number[]>([])
  const hoveredEvent = ref<number | null>(null)
  const hoveredField = ref<string | null>(null)

  const columns = [
    { key: 'select', label: '' },
    { key: 'title', label: 'Event Name' },
    { key: 'date', label: 'Date' },
    { key: 'event_type', label: 'Type' },
    { key: 'rsvps', label: 'RSVPs' },
    { key: 'signup_deadline', label: 'Signup Deadline' },
    { key: 'description', label: 'Description' },
  ]

  onMounted(async () => {
    try {
      events.value = await fetchEvents()
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err))
    } finally {
      loading.value = false
    }
  })

  return { events, loading, error, selectedEvents, hoveredEvent, hoveredField, columns, formatDateTime }
}
