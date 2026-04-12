import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import type { User, LoginResponse } from '@/types'
import { api } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token') || null)
  const isAuthenticated = ref<boolean>(false)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const isInitialized = ref<boolean>(false)
  const router = useRouter()

  /** True if the user has the Board role (or SuperAdmin). */
  const isBoardMember = ref<boolean>(false)

  function _setUser(u: User): void {
    user.value = u
    isAuthenticated.value = true
    isBoardMember.value = u.roles.includes('Board') || u.roles.includes('SuperAdmin')
  }

  function _clearSession(): void {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    isBoardMember.value = false
    localStorage.removeItem('token')
  }

  /** Called on app startup — validates any stored token. */
  async function init(): Promise<void> {
    if (!token.value) {
      isInitialized.value = true
      return
    }
    try {
      const res = await api.get<User>('/auth/me')
      _setUser(res.data)
    } catch {
      _clearSession()
    } finally {
      isInitialized.value = true
    }
  }

  async function login(email: string, password: string): Promise<void> {
    isLoading.value = true
    error.value = null
    try {
      const res = await api.post<LoginResponse>('/auth/login', { email, password })
      const data = res.data
      localStorage.setItem('token', data.token)
      token.value = data.token
      _setUser(data.user)
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function logout(): void {
    _clearSession()
    router.push('/login')
  }

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    isBoardMember,
    isInitialized,
    init,
    login,
    logout,
  }
})
