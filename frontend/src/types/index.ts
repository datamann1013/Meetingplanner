// ─── API response wrappers ───────────────────────────────────────────────────

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

// ─── Auth ────────────────────────────────────────────────────────────────────

export interface User {
  id: number
  email: string
  username: string
  is_active: boolean
  roles: string[]          // list of role names, e.g. ["Board", "Member"]
  created_at?: string
}

export interface LoginResponse {
  token: string
  user: User
}

// ─── Events ──────────────────────────────────────────────────────────────────

export interface EventType {
  id: number
  name: string
}

export interface Category {
  id: number
  name: string
}

export interface Event {
  id: number
  title: string
  description: string | null
  date: string
  location: string | null
  capacity: number | null
  signup_deadline: string | null
  contact_info: string | null
  cover_image_url: string | null
  is_published: boolean
  slug: string | null
  fee_charged: number | null
  fee_received: number | null
  fee_currency: string | null
  fee_notes: string | null
  event_type: EventType | null
  creator: { id: number; username: string } | null
  categories: Category[]
  created_at: string
  updated_at: string
}

// ─── RSVPs ───────────────────────────────────────────────────────────────────

export type RSVPStatus = 'yes' | 'no' | 'maybe'

export interface RSVP {
  id: number
  status: RSVPStatus
  user_id: number
  event_id: number
  created_at: string
  updated_at: string
}

// ─── Chat ────────────────────────────────────────────────────────────────────

export interface ChatMessage {
  id: number
  message: string
  user_id: number
  event_id: number
  created_at: string
}

// ─── Roles & permissions ─────────────────────────────────────────────────────

export interface Permission {
  id: number
  resource: string
  action: string
}

export interface Role {
  id: number
  name: string
  description: string
  is_system: boolean
  permissions: Permission[]
}

// ─── Auth state (Pinia store) ─────────────────────────────────────────────────

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}
