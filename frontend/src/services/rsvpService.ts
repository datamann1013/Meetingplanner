import { ref } from 'vue'

export interface RsvpStatus {
  accepted: number
  declined: number
  maybe: number
  total: number
}

export interface EventWithRsvps {
  id: number
  name: string
  date: string
  status: string
  rsvp_stats: RsvpStatus
}

export interface RsvpEntry {
  id: number
  status_answer: 'yes' | 'no' | 'mabye/unsure'
  user: {
    id: number
    username?: string
    email?: string
  }
  event: {
    id: number
    name: string
  }
}

class RsvpService {
  private events = ref<EventWithRsvps[]>([
    {
      id: 1,
      name: 'Annual Company Meeting',
      date: '2025-10-15T14:00:00.000Z',
      status: 'Published',
      rsvp_stats: {
        accepted: 15,
        declined: 3,
        maybe: 2,
        total: 20
      }
    },
    {
      id: 2,
      name: 'Team Building Workshop',
      date: '2025-10-20T10:00:00.000Z',
      status: 'Published',
      rsvp_stats: {
        accepted: 8,
        declined: 1,
        maybe: 1,
        total: 10
      }
    },
    {
      id: 3,
      name: 'Holiday Party Planning',
      date: '2025-11-01T16:00:00.000Z',
      status: 'Draft',
      rsvp_stats: {
        accepted: 0,
        declined: 0,
        maybe: 0,
        total: 0
      }
    },
    {
      id: 4,
      name: 'Quarterly Review Meeting',
      date: '2025-10-25T11:00:00.000Z',
      status: 'Published',
      rsvp_stats: {
        accepted: 12,
        declined: 2,
        maybe: 3,
        total: 17
      }
    }
  ])

  private rsvps = ref<RsvpEntry[]>([
    {
      id: 1,
      status_answer: 'yes',
      user: { id: 1, username: 'john.doe', email: 'john@example.com' },
      event: { id: 1, name: 'Annual Company Meeting' }
    },
    {
      id: 2,
      status_answer: 'yes',
      user: { id: 2, username: 'jane.smith', email: 'jane@example.com' },
      event: { id: 1, name: 'Annual Company Meeting' }
    },
    {
      id: 3,
      status_answer: 'no',
      user: { id: 3, username: 'alice.brown', email: 'alice@example.com' },
      event: { id: 1, name: 'Annual Company Meeting' }
    },
    {
      id: 4,
      status_answer: 'mabye/unsure',
      user: { id: 4, username: 'bob.wilson', email: 'bob@example.com' },
      event: { id: 1, name: 'Annual Company Meeting' }
    },
    {
      id: 5,
      status_answer: 'yes',
      user: { id: 5, username: 'carol.davis', email: 'carol@example.com' },
      event: { id: 2, name: 'Team Building Workshop' }
    },
    {
      id: 6,
      status_answer: 'no',
      user: { id: 6, username: 'david.miller', email: 'david@example.com' },
      event: { id: 2, name: 'Team Building Workshop' }
    }
  ])

  async getEventsWithRsvpStats(): Promise<EventWithRsvps[]> {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 300))
    return this.events.value
  }

  async getRsvpsForEvent(eventId: number): Promise<RsvpEntry[]> {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 200))
    return this.rsvps.value.filter(rsvp => rsvp.event.id === eventId)
  }

  async updateRsvpStatus(rsvpId: number, newStatus: 'yes' | 'no' | 'mabye/unsure'): Promise<RsvpEntry> {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const rsvp = this.rsvps.value.find(r => r.id === rsvpId)
    if (!rsvp) {
      throw new Error('RSVP not found')
    }

    const oldStatus = rsvp.status_answer
    rsvp.status_answer = newStatus

    // Update event statistics
    const event = this.events.value.find(e => e.id === rsvp.event.id)
    if (event) {
      // Decrease old status count
      if (oldStatus === 'yes') event.rsvp_stats.accepted--
      else if (oldStatus === 'no') event.rsvp_stats.declined--
      else if (oldStatus === 'mabye/unsure') event.rsvp_stats.maybe--

      // Increase new status count
      if (newStatus === 'yes') event.rsvp_stats.accepted++
      else if (newStatus === 'no') event.rsvp_stats.declined++
      else if (newStatus === 'mabye/unsure') event.rsvp_stats.maybe++
    }

    return rsvp
  }

  formatDateTime(dateString: string): string {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  formatStatus(status: string): string {
    switch (status) {
      case 'yes': return 'Accepted'
      case 'no': return 'Declined'
      case 'mabye/unsure': return 'Maybe/Unsure'
      default: return status
    }
  }
}

export const rsvpService = new RsvpService()