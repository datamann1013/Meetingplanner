<template>
  <div class="centered-content content-with-bars">
    <v-card class="login-card" elevation="12">
      <v-toolbar color="primary" dark flat>
        <v-toolbar-title>Login</v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <v-form @submit.prevent="handleLogin">
          <v-text-field
            v-model="identifier"
            label="Email or Username"
            type="text"
            required
            :disabled="authStore.isLoading"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            required
            :disabled="authStore.isLoading"
          ></v-text-field>
          <v-alert v-if="authStore.error" type="error" class="mb-4">
            {{ authStore.error }}
          </v-alert>
          <v-btn 
            type="submit" 
            color="primary" 
            block 
            :loading="authStore.isLoading"
          >
            Login
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

const identifier = ref<string>('')
const password = ref<string>('')

const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async (): Promise<void> => {
  try {
    await authStore.login(identifier.value, password.value)
    router.push('/')
  } catch (err) {
    console.error('Login error:', err)
  }
}
</script>

<style scoped>
.login-card {
  width: 90%;
  max-width: 400px;
}
</style>