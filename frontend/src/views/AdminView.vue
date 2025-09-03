<template>
  <div style="display: flex; height: 100vh;">
  <div style="width: 260px; background: #C8DAA6; display: flex; flex-direction: column; align-items: flex-start; padding-top: 48px; height: calc(100vh - 48px); position: fixed; top: 48px; left: 0;">
      <div style="width: 100%;">
  <div v-for="item in sidebarItems" :key="item.title" class="admin-sidebar-item" style="font-size: 1.25rem; padding: 16px; color: #222; text-align: left; cursor: pointer;">
          {{ item.title }}
        </div>
      </div>
    </div>
    <div style="flex: 1; padding: 48px 32px;">
      <!-- Main content area (empty for now) -->
    </div>
  </div>
</template>

<script setup lang="ts">
const sidebarItems = [
  { title: 'Events' },
  { title: 'Emails' },
  { title: 'Users' },
  { title: 'Dashboard' },
  { title: 'RSVPs' },
  { title: 'Settings' },
  { title: 'Logs' },
]
</script>