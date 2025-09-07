export interface StrapiResponse<T> {
  data: T;
  meta?: {
    pagination?: {
      page: number;
      pageSize: number;
      pageCount: number;
      total: number;
    };
  };
}

export interface StrapiEntity<T> {
  id: number;
  attributes: T;
}

export interface User {
  id: number;
  username: string;
  email: string;
  provider: string;
  confirmed: boolean;
  blocked: boolean;
  createdAt: string;
  updatedAt: string;
  role?: {
    id: number;
    name: string;
    description: string;
    type: string;
  };
}

export interface LoginResponse {
  jwt: string;
  user: User;
}

export interface Event {
  id: number;
  title: string;
  description: string;
  date: string;
  location: string;
  capacity: number;
  signup_deadline: string;
  contact_info: string;
  createdAt: string;
  updatedAt: string;
  publishedAt: string;
  categories?: {
    data: StrapiEntity<Category>[];
  };
  responsible_person?: {
    data: StrapiEntity<User>;
  };
  chat_messages?: {
    data: StrapiEntity<ChatMessage>[];
  };
  rsvps?: {
    data: StrapiEntity<RSVP>[];
  };
  Coverimage?: {
    id?: number;
    url?: string;
    name?: string;
    alternativeText?: string | null;
    caption?: string | null;
    width?: number;
    height?: number;
    formats?: Record<string, any>;
    hash?: string;
    ext?: string;
    mime?: string;
    size?: number;
    previewUrl?: string | null;
    provider?: string;
    provider_metadata?: any;
    createdAt?: string;
    updatedAt?: string;
    publishedAt?: string;
  }
}

export interface Category {
  name: string;
  createdAt: string;
  updatedAt: string;
  publishedAt: string;
}

export interface ChatMessage {
  message: string;
  createdAt: string;
  updatedAt: string;
  publishedAt: string;
  event?: {
    data: StrapiEntity<Event>;
  };
  user?: {
    data: StrapiEntity<User>;
  };
}

export interface RSVP {
  status_answer: 'yes' | 'no' | 'maybe';
  createdAt: string;
  updatedAt: string;
  publishedAt: string;
  event?: {
    data: StrapiEntity<Event>;
  };
  user?: {
    data: StrapiEntity<User>;
  };
}

export interface AuthState {
  user: User | null;
  jwt: string | null;
  isAuthenticated: boolean;
}