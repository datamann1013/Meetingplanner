
<template>
  <v-app>
    <v-app-bar color="primary" density="compact">
      <v-app-bar-title>Event Manager</v-app-bar-title>
      <v-spacer></v-spacer>
      
      <v-btn to="/" variant="text">Events</v-btn>
      
      <template v-if="authStore.isAuthenticated">
        <v-btn v-if="authStore.user?.role?.name === 'Board'" to="/admin" variant="text">Admin</v-btn>
        <v-btn variant="text" @click="authStore.logout">Logout</v-btn>
      </template>
      <template v-else>
        <v-btn to="/login" variant="text">Login</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>