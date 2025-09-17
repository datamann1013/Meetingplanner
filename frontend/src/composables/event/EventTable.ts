import { ref, onMounted } from 'vue'
import { strapi } from '../../services/strapi'
import { formatDateTime } from '../DateUtils'

export function EventTable() {
  const events = ref<any[]>([])
  const loading = ref(true)
  const error = ref<Error | null>(null)
  const selectedEvents = ref<(string | number)[]>([])
  const hoveredEvent = ref<string | number | null>(null)
  const hoveredField = ref<string | null>(null)

  const columns = [
    { key: 'select', label: '' },
    { key: 'name', label: 'Event Name' },
    { key: 'date', label: 'Date' },
    { key: 'status', label: 'Status' },
    { key: 'rsvp', label: 'RSVP' },
    { key: 'signup_deadline', label: 'Signup Deadline' },
    { key: 'description', label: 'Description' }
  ]

  onMounted(async () => {
    try {
      const res: any = await strapi.get('/events?populate=*')
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
          Coverimage: item.Coverimage || null,
        }))
      } else {
        events.value = []
      }
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err))
      events.value = []
    } finally {
      loading.value = false
    }
  })

  return {
    events,
    loading,
    error,
    selectedEvents,
    hoveredEvent,
    hoveredField,
    columns,
    formatDateTime,
  }
}
