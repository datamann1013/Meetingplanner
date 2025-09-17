import { computed } from 'vue'

export function EventCard(event: any, strapiBaseUrl: string) {
  const coverImageStyle = computed(() => {
    if (event.Coverimage?.url) {
      return {
        backgroundImage: `url(${strapiBaseUrl}${event.Coverimage.url})`,
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

  return {
    coverImageStyle,
    formatDate,
  }
}
