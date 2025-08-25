import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_STRAPI_API_URL || 'http://localhost:1337/api'
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = localStorage.getItem('jwt')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('jwt')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const strapi = {
  get: <T>(url: string, params?: unknown): Promise<AxiosResponse<T>> => 
    api.get(url, { params }),
  post: <T>(url: string, data?: unknown): Promise<AxiosResponse<T>> => 
    api.post(url, data),
  put: <T>(url: string, data?: unknown): Promise<AxiosResponse<T>> => 
    api.put(url, data),
  delete: <T>(url: string): Promise<AxiosResponse<T>> => 
    api.delete(url)
}