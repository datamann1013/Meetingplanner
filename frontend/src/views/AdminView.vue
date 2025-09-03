<template>
  <div class="admin-layout">
    <div class="admin-sidebar">
      <div class="admin-sidebar-list">
        <div v-for="item in sidebarItems.filter(i => i.title !== 'Settings' && i.title !== 'Logs')" :key="item.title"
          class="admin-sidebar-item"
          :class="{ 'admin-sidebar-item-selected': selectedTab === item.title }"
          @click="selectedTab = item.title">
          {{ item.title }}
        </div>
      </div>
      <div class="admin-sidebar-spacer"></div>
      <div class="admin-sidebar-bottom">
        <div v-for="item in sidebarItems.filter(i => i.title === 'Settings' || i.title === 'Logs')" :key="item.title"
          class="admin-sidebar-item"
          :class="{ 'admin-sidebar-item-selected': selectedTab === item.title }"
          @click="selectedTab = item.title">
          {{ item.title }}
        </div>
      </div>
    </div>
    <div class="admin-main">
      <!-- Main content area (empty for now) -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const sidebarItems = [
  { title: 'Events' },
  { title: 'Emails' },
  { title: 'Users' },
  { title: 'Dashboard' },
  { title: 'RSVPs' },
  { title: 'Logs' },
  { title: 'Settings' },
]
const selectedTab = ref('Events')
</script>