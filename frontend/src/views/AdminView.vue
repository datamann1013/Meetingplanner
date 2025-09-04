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
        <DashboardLayout
          v-if="dashboardConfigs[selectedTab.toLowerCase()]"
          :title="sidebarItems.find(i => i.title === selectedTab)?.title"
          :layoutConfig="dashboardConfigs[selectedTab.toLowerCase()]"
        />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DashboardLayout from '../components/DashboardLayout.vue'
const sidebarItems = [
  { title: 'Dashboard', tag: 'dashboard' },
  { title: 'Events', tag: 'events' },
  { title: 'Emails', tag: 'emails' },
  { title: 'Users', tag: 'users' },
  { title: 'RSVPs', tag: 'rsvps' },
  { title: 'Logs', tag: 'logs' },
  { title: 'Settings', tag: 'settings' },
]
const selectedTab = ref('events')

const dashboardConfigs = {
  dashboard: [
    [
      { size: 'primary', label: 'Short Left', flex: 1 },
      { size: 'secondary', label: 'Middle Left', flex: 2 }
    ],
    [
      { size: 'primary', label: 'Main Table', flex: 2, content: 'TableDemo' },
      { size: 'secondary', label: 'Actions', flex: 1, content: 'ButtonDemo' }
    ],
    [{ size: 'long', label: 'Overview' }],
  ],
  events: [
  [
      { size: 'primary', label: 'Short Left', flex: 1 },
      { size: 'secondary', label: 'Middle Left', flex: 2 }
    ],
    [{ size: 'long', label: 'Overview' }],
  ],
  emails: [
    [{ size: 'primary', label: 'Inbox', flex: 1 }, { size: 'secondary', label: 'Sent', flex: 1 }],
    [{ size: 'long', label: 'Compose Email' }],
  ],
  users: [
    [{ size: 'primary', label: 'User List', flex: 2 }, { size: 'accent', label: 'User Roles', flex: 1 }],
    [{ size: 'secondary', label: 'Add User' }],
  ],
  rsvps: [
    [{ size: 'primary', label: 'Pending RSVPs', flex: 1 }, { size: 'secondary', label: 'Confirmed RSVPs', flex: 1 }],
  ],
  logs: [
    [{ size: 'long', label: 'System Logs' }],
  ],
  settings: [
    [{ size: 'primary', label: 'General Settings', flex: 1 }, { size: 'secondary', label: 'Advanced Settings', flex: 1 }],
  ],
}
// Demo components for content
const TableDemo = {
  template: `<div style='width:100%;height:100%;display:flex;align-items:center;justify-content:center;'><table style='width:90%;background:#fff;border-radius:8px;box-shadow:0 1px 4px #ccc;'><tr><th>Name</th><th>Status</th></tr><tr><td>Event 1</td><td>Active</td></tr><tr><td>Event 2</td><td>Inactive</td></tr></table></div>`
}
const ButtonDemo = {
  template: `<div style='display:flex;flex-direction:column;gap:8px;align-items:center;'><button style='padding:8px 16px;border-radius:6px;background:#ede3d2;color:#4b3f2a;border:none;'>Action 1</button><button style='padding:8px 16px;border-radius:6px;background:#ede3d2;color:#4b3f2a;border:none;'>Action 2</button></div>`
}
</script>