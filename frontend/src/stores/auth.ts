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
    const jwt = ref<string | null>(localStorage.getItem('jwt') || null)
  const isAuthenticated = ref<boolean>(false)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const isBoardMember = ref<boolean>(false)
  const isInitialized = ref<boolean>(false)
  const router = useRouter()


  function init(): void {
    if (jwt.value && !isInitialized.value) {
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

    localStorage.setItem('jwt', data.jwt)
    jwt.value = data.jwt

      user.value = await fetchUserWithRole(data.jwt)
      isAuthenticated.value = true
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

  async function fetchUserWithRole(jwt: string): Promise<User> {
    const response = await fetch('http://localhost:1337/api/users/me?populate=role', {
      headers: {
        'Authorization': `Bearer ${jwt}`,
        'Content-Type': 'application/json'
      }
    })
    return await response.json()
  } 

  function logout(): void {
    user.value = null
    jwt.value = null
    isAuthenticated.value = false
    isBoardMember.value = false
    localStorage.removeItem('jwt')
    router.push('/login')
  }

  async function checkAuth(): Promise<void> {
    const jwt = localStorage.getItem('jwt')
    if (jwt) {
      user.value = await fetchUserWithRole(jwt)
      isAuthenticated.value = true
      checkUserRole()
    }
  }

  async function validateToken(): Promise<boolean> {
  if (!jwt.value) return false

    try {
      const response = await fetch('http://localhost:1337/api/users/me?populate=role', {
        headers: {
      'Authorization': `Bearer ${jwt.value}`,
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
    jwt, 
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