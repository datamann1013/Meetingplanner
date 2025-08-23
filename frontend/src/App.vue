<template>
  <v-app>
    <!-- Always show the navigation bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Event Manager</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <!-- Show navigation links only when not on login page -->
      <div v-if="!isLoginPage">
        <!-- Navigation for authenticated users -->
        <div v-if="authStore.isAuthenticated">
          <v-btn to="/" text>Home</v-btn>
          <v-btn @click="authStore.logout" text>Logout</v-btn>
        </div>
        
        <!-- Navigation for unauthenticated users -->
        <v-btn v-else to="/login" text>Login</v-btn>
      </div>
      
      <!-- Show only the title on login page (no links) -->
      <div v-else>
        <!-- Empty div to maintain layout -->
      </div>
    </v-app-bar>
    
    <v-main>
      <router-view />
    </v-main>
    <v-footer app height="64" class="justify-center">
      <span>&copy; {{ new Date().getFullYear() }} Event Manager</span>
    </v-footer>
  </v-app>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const route = useRoute()

// Check if we're on the login page
const isLoginPage = computed(() => route.name === 'Login')
</script>