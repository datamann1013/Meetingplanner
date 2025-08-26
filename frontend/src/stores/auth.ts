import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

interface Role {
  id: number
  name: string
  description: string
  type: string
}

interface User {
  id: number
  username: string
  email: string
  provider: string
  confirmed: boolean
  blocked: boolean
  createdAt: string
  updatedAt: string
  role?: Role
}

interface AuthResponse {
  jwt: string
  user: User
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token') || null)
  const isAuthenticated = ref<boolean>(false)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const isBoardMember = ref<boolean>(false)
  const isInitialized = ref<boolean>(false)
  const router = useRouter()


  function init(): void {
    if (token.value && !isInitialized.value) {
      validateToken().then(() => {
        isInitialized.value = true
      })
    } else {
      isInitialized.value = true
    }
  }

  async function login(identifier: string, password: string): Promise<AuthResponse> {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch('http://localhost:1337/api/auth/local', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ identifier, password }),
      })

      const data: AuthResponse & { error?: any } = await response.json()

      if (data.error) {
        throw new Error(data.error.message)
      }

      token.value = data.jwt
      user.value = data.user
      isAuthenticated.value = true
      localStorage.setItem('jwt', data.jwt)
      checkUserRole()
      
      return data
    } catch (err) {
      if (err instanceof Error) {
        error.value = err.message
      } else {
        error.value = 'An unknown error occurred'
      }
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function logout(): void {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    isBoardMember.value = false
    localStorage.removeItem('token')
    router.push('/login')
  }

  async function checkAuth(): Promise<void> {
    await validateToken()
  }

  async function validateToken(): Promise<boolean> {
    if (!token.value) return false

    try {
      const response = await fetch('http://localhost:1337/api/users/me?populate=role', {
        headers: {
          'Authorization': `Bearer ${token.value}`,
          'Content-Type': 'application/json'
        }
      })
      const data = await response.json()
      user.value = data
      isAuthenticated.value = true
      checkUserRole()
      return true
    } catch (err) {
      logout()
      return false
    }
  }

  function checkUserRole(): void {
    if (user.value && user.value.role?.name === 'Board') {
      isBoardMember.value = true
    } else {
      isBoardMember.value = false
    }
  }

  return { 
    user, 
    token, 
    isAuthenticated, 
    isLoading, 
    error, 
    isBoardMember,
    isInitialized,
    login, 
    logout, 
    init,
    checkUserRole,
    checkAuth
  }
})