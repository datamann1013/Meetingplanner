import { computed } from 'vue'
import type { Event } from '@/types'

export function useEventCard(event: Event) {
  const coverImageStyle = computed(() => {
    if (event.cover_image_url) {
      return {
        backgroundImage: `url(${event.cover_image_url})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }
    }
    return {
      backgroundColor: 'var(--color-primary-bg)',
    }
  })

  function formatDate(date: string) {
    return new Date(date).toLocaleDateString()
  }

  return { coverImageStyle, formatDate }
}
