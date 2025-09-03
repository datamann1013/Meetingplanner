<template>
  <div style="display: flex; height: 100vh;">
  <div style="width: 260px; background: #C8DAA6; display: flex; flex-direction: column; align-items: flex-start; padding-top: 48px; height: calc(100vh - 48px); position: fixed; top: 48px; left: 0;">
  <div style="width: 100%; height: 100%; display: flex; flex-direction: column;">
        <div>
          <div v-for="item in sidebarItems.filter(i => i.title !== 'Settings' && i.title !== 'Logs')" :key="item.title"
            class="admin-sidebar-item"
            :style="selectedTab === item.title ? 'background: #A3B18A; color: #222;' : 'color: #222;'"
            style="font-size: 1.25rem; padding: 16px; text-align: left; cursor: pointer;"
            @click="selectedTab = item.title">
            {{ item.title }}
          </div>
        </div>
        <div style="flex: 1;"></div>
        <div style="border-top: 1px solid #b5c9a3; margin-top: 16px; padding-top: 8px;">
          <div v-for="item in sidebarItems.filter(i => i.title === 'Settings' || i.title === 'Logs')" :key="item.title"
            class="admin-sidebar-item"
            :style="selectedTab === item.title ? 'background: #A3B18A; color: #222;' : 'color: #222;'"
            style="font-size: 1.25rem; padding: 16px; text-align: left; cursor: pointer;"
            @click="selectedTab = item.title">
            {{ item.title }}
          </div>
        </div>
      </div>
    </div>
    <div style="flex: 1; padding: 48px 32px;">
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