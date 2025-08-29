<template>
  <v-container fluid class="pa-0" style="height: 100vh;">
    <v-row no-gutters style="height: 100%;">
      <v-col cols="2" class="d-flex flex-column align-start pa-0" style="background: var(--v-theme-surface); min-width: 200px; max-width: 260px; height: 100vh;">
        <v-list nav dense style="height: calc(100vh - 48px); position: fixed; left: 0; top: 48px; z-index: 100; min-width: 260px; max-width: 280px;">
          <v-list-item
              v-for="item in sidebarItems"
              :key="item.title"
              @click="selectedTab = item.title"
              :active="selectedTab === item.title"
              :class="selectedTab === item.title ? 'sidebar-selected' : ''"
          >
              <v-list-item-title style="font-size: 1.25rem;">{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="10" class="pa-6">
        <div v-if="selectedTab === 'Events'">
          <h2>Events</h2>
          <!-- Events management UI here -->
        </div>
        <div v-else-if="selectedTab === 'Emails'">
          <h2>Emails</h2>
          <!-- Emails management UI here -->
        </div>
        <div v-else-if="selectedTab === 'Users'">
          <h2>Users</h2>
          <!-- Users management UI here -->
        </div>
        <div v-else-if="selectedTab === 'Dashboard'">
          <h2>Dashboard</h2>
          <!-- Dashboard UI here -->
        </div>
        <div v-else-if="selectedTab === 'RSVPs'">
          <h2>RSVPs</h2>
          <!-- RSVPs management UI here -->
        </div>
        <div v-else-if="selectedTab === 'Settings'">
          <h2>Settings</h2>
          <!-- Settings UI here -->
        </div>
        <div v-else-if="selectedTab === 'Logs'">
          <h2>Logs</h2>
          <!-- Logs/Audit UI here -->
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const sidebarItems = [
  { title: 'Events' },
  { title: 'Emails' },
  { title: 'Users' },
  { title: 'Dashboard' },
  { title: 'RSVPs' },
  { title: 'Settings' },
  { title: 'Logs' },
]
const selectedTab = ref('Events')
</script>