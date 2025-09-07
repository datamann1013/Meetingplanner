import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_STRAPI_API_URL || 'http://localhost:1337/api'
})

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const jwt = localStorage.getItem('jwt')
    if (jwt && config.headers) {
      config.headers.Authorization = `Bearer ${jwt}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

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