<template>
  <div class="centered-content">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8" class="text-center">
          <h1 class="text-h3 mb-4">Welcome to Event Manager</h1>
          
          <div v-if="authStore.isAuthenticated">
            <p class="text-h6 mb-6">Hello, {{ authStore.user?.username }}!</p>
            <p>You are now logged in and can access the event management system.</p>
            
            <div v-if="authStore.isBoardMember" class="mt-8">
              <v-btn color="accent" disabled>
                Admin Panel (Coming Soon)
              </v-btn>
            </div>
          </div>
          
          <div v-else>
            <p class="text-h6 mb-6">Please log in to access the event management system</p>
            <v-btn to="/login" color="primary" size="large">
              Login
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>