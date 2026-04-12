import type { Event, PaginatedResponse } from '@/types'
import { api } from './api'

export async function fetchEvents(page = 1, pageSize = 25): Promise<Event[]> {
  try {
    const res = await api.get<PaginatedResponse<Event>>('/events', { page, page_size: pageSize })
    return res.data.items
  } catch {
    return []
  }
}
