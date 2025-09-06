import { strapi } from './strapi'
import type { AxiosResponse } from 'axios'

export async function fetchEvents() {
  try {
    const res: AxiosResponse<any> = await strapi.get('/events?populate=*');
    console.log('Raw event response:', res.data);
    // Defensive: check if res.data and res.data.data exist
    if (!res.data || !Array.isArray(res.data.data)) return []
    return res.data.data.map((item: any) => ({
      id: item.id,
      name: item.attributes.title,
      date: item.attributes.date,
      status: item.attributes.status || 'Draft',
      rsvp: item.attributes.rsvp_count || '0/0',
      tag: item.attributes.tag || '',
      signup_deadline: item.attributes.signup_deadline,
      description: item.attributes.description,
      coverImage: item.attributes.Coverimage?.url || null,
    }))
  } catch (e) {
    return []
  }
}
