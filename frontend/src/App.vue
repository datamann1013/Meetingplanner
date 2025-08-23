<template>
  <v-app>
    <v-app-bar app color="primary" dark v-if="showNavigation">
      <v-toolbar-title>Event Manager</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <!-- Navigation for authenticated users -->
      <div v-if="authStore.isAuthenticated">
        <v-btn to="/" text>Home</v-btn>
        <v-btn @click="authStore.logout" text>Logout</v-btn>
      </div>
      
      <!-- Navigation for unauthenticated users -->
      <v-btn v-else to="/login" text>Login</v-btn>
    </v-app-bar>
    
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const authStore = useAuthStore() // This should work now
const route = useRoute()

// Don't show navigation on login page
const showNavigation = computed(() => route.name !== 'Login')
</script>