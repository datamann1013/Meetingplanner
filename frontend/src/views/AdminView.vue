<template>
  <div class="admin-layout">
    <div class="admin-sidebar">
      <div class="admin-sidebar-list">
        <AdminSidebarItem
          v-for="item in sidebarItems.filter(i => i.title !== 'Settings' && i.title !== 'Logs')"
          :key="item.title"
          :title="item.title"
          :selected="selectedTab === item.title"
          @click="selectedTab = item.title"
        />
      </div>
      <div class="admin-sidebar-spacer"></div>
      <div class="admin-sidebar-bottom">
        <AdminSidebarItem
          v-for="item in sidebarItems.filter(i => i.title === 'Settings' || i.title === 'Logs')"
          :key="item.title"
          :title="item.title"
          :selected="selectedTab === item.title"
          @click="selectedTab = item.title"
        />
      </div>
    </div>
    <div class="admin-main">
        <DashboardLayout
          v-if="dashboardConfigs[selectedTab.toLowerCase()]"
          :title="sidebarItems.find(i => i.title === selectedTab)?.title"
          :layoutConfig="dashboardConfigs[selectedTab.toLowerCase()]"
        >
          <!-- Use DashboardLayout's default slot for other tabs, but let DashboardLayout handle dynamic content for Events tab -->
        </DashboardLayout>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DashboardLayout from '../components/DashboardLayout.vue'
import AdminSidebarItem from '../components/AdminSidebarItem.vue'
import EventActionsBox from '../components/EventActionsBox.vue'
import EventCalendarBox from '../components/EventCalendarBox.vue'

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
      { size: 'primary', label: 'Short Left', flex: 1, content: EventActionsBox },
      { size: 'secondary', label: 'Middle Left', flex: 2, content: EventCalendarBox }
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
</script>