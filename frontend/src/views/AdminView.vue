<template>
  <div class="admin-layout">
    <div class="admin-sidebar">
      <div class="admin-sidebar-list">
        <SidebarItem
          v-for="item in sidebarItems.filter(i => i.title !== 'Settings' && i.title !== 'Logs')"
          :key="item.title"
          :title="item.title"
          :selected="selectedTab === item.title"
          :hoverColor="item.hoverColor || '#e0e7ff'"
          :leftPadding="'1.5rem'"
          @click="selectedTab = item.title"
        />
      </div>
      <div class="admin-sidebar-spacer"></div>
      <div class="admin-sidebar-bottom">
        <SidebarItem
          v-for="item in sidebarItems.filter(i => i.title === 'Settings' || i.title === 'Logs')"
          :key="item.title"
          :title="item.title"
          :selected="selectedTab === item.title"
          :hoverColor="item.hoverColor || '#fee2e2'"
          :leftPadding="'1.5rem'"
          @click="selectedTab = item.title"
        />
      </div>
    </div>
    <div class="admin-main">
        <template v-if="selectedTab === 'Events'">
          <EventActionsAndCalendar />
        </template>
        <template v-else>
          <DashboardLayout
            v-if="dashboardConfigs[selectedTab.toLowerCase() as keyof typeof dashboardConfigs]"
            :title="sidebarItems.find(i => i.title === selectedTab)?.title"
            :layoutConfig="dashboardConfigs[selectedTab.toLowerCase() as keyof typeof dashboardConfigs]"
          />
        </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DashboardLayout from '../components/DashboardLayout.vue'
import SidebarItem from '../components/admin/SidebarItem.vue'
import EventActionsBox from '../components/EventActionsBox.vue'
import EventCalendarBox from '../components/EventCalendarBox.vue'
import EventListTable from '../components/EventListTable.vue'
import EventActionsAndCalendar from '../components/EventActionsAndCalendar.vue'

const sidebarItems = [
  { title: 'Dashboard', tag: 'dashboard', hoverColor: '#A3B18A' },
  { title: 'Events', tag: 'events', hoverColor: '#A3B18A' },
  { title: 'Emails', tag: 'emails', hoverColor: '#A3B18A' },
  { title: 'Users', tag: 'users', hoverColor: '#A3B18A' },
  { title: 'RSVPs', tag: 'rsvps', hoverColor: '#A3B18A' },
  { title: 'Logs', tag: 'logs', hoverColor: '#A3B18A' },
  { title: 'Settings', tag: 'settings', hoverColor: '#A3B18A' },
]

const selectedTab = ref('Dashboard')

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
    [{ size: 'long', label: 'Overview', content: EventListTable }],
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