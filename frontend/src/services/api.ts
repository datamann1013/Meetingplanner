/**
 * Centralised API client for the FastAPI backend.
 *
 * Base URL is set via the VITE_API_URL environment variable.
 * Defaults to http://localhost:8000/api for local development.
 *
 * JWT token is automatically attached from localStorage on every request.
 * A 401 response clears the token and redirects to /login.
 */

import axios, { type AxiosInstance, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'

const instance: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
})

// Attach JWT to every request
instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// Auto-logout on 401
instance.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

export const api = {
  get: <T>(url: string, params?: Record<string, unknown>): Promise<AxiosResponse<T>> =>
    instance.get(url, { params }),
  post: <T>(url: string, data?: unknown): Promise<AxiosResponse<T>> =>
    instance.post(url, data),
  put: <T>(url: string, data?: unknown): Promise<AxiosResponse<T>> =>
    instance.put(url, data),
  delete: <T>(url: string): Promise<AxiosResponse<T>> =>
    instance.delete(url),
}
