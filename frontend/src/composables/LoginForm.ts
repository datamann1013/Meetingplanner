import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export function LoginForm() {
  const identifier = ref('')
  const password = ref('')
  const authStore = useAuthStore()
  const router = useRouter()

  async function handleLogin() {
    try {
      await authStore.login(identifier.value, password.value)
      router.push('/')
    } catch (err) {
      console.error('Login error:', err)
    }
  }

  return {
    identifier,
    password,
    authStore,
    router,
    handleLogin,
  }
}
