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
  <div class="admin-main" ref="adminMainRef">
        <template v-if="selectedTab === 'Events'">
          <DualInteractiveBoxes
            :actions="['Calendar', 'Create Event', 'Duplicate Previous Event', 'Import Events', 'Upload Images/Attachments', 'Send Mass Email']"
            :contentMap="{
              'Calendar': { render() { return h(CalendarEventSelector) } },
              'Create Event': { render() { return h('h2', 'Create Event') } },
              'Duplicate Previous Event': { render() { return h('h2', 'Duplicate Previous Event') } },
              'Import Events': { render() { return h(FileUploadBox, { mode: 'import', onFileSelected: onImportFileSelected }) } },
              'Upload Images/Attachments': { render() { return h(FileUploadBox, { mode: 'attachment', folders: strapiFolders, onFileSelected: onAttachmentFileSelected, onCreateFolder: onCreateStrapiFolder }) } },
              'Send Mass Email': { render() { return h(EmailSenderBox) } }
            }"
            initialAction="Calendar"
          >
            <template #bottom>
              <EventTable
                :events="events"
                :columns="eventColumns"
                :topBarProps="eventTopBarProps"
                @edit="onEditEvent"
                @delete="onDeleteEvent"
              />
            </template>
          </DualInteractiveBoxes>
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
import { ref, h } from 'vue'
import DashboardLayout from "../../components/admin/DashboardLayout.vue";
import SidebarItem from "../../components/admin/SidebarItem.vue";
import DualInteractiveBoxes from "../../components/admin/DualInteractiveBoxes.vue";
import EventActionsBox from "../../components/admin/eventview/EventActionsBox.vue";
import EventTable from "../../components/admin/eventview/EventTable.vue";
import CalendarEventSelector from "../../components/shared/CalendarEventSelector.vue";
import FileUploadBox from "../../components/shared/FileUploadBox.vue";
import EmailSenderBox from "../../components/admin/eventview/EmailSenderBox.vue";

// Example folders for Strapi, replace with real fetch if needed
const strapiFolders = ref(["uploads", "images", "attachments"]);

function onImportFileSelected({ files }: { files: FileList }) {
  // Handle import file selection (CSV/UML etc)
  // Placeholder: just log
  console.log("Import file selected", files);
}

function onAttachmentFileSelected({ files, folder }: { files: FileList, folder: string }) {
  // Handle attachment/image file selection
  // Placeholder: just log
  console.log("Attachment(s) selected", files, "in folder", folder);
}

function onCreateStrapiFolder(folderName: string) {
  // Placeholder for folder creation logic
  // For now, just log and add to folders
  if (folderName && !strapiFolders.value.includes(folderName)) {
    strapiFolders.value.push(folderName);
  }
  console.log("Create folder:", folderName);
}

const sidebarItems = [
  { title: 'Dashboard', tag: 'dashboard', hoverColor: '#A3B18A' },
  { title: 'Events', tag: 'events', hoverColor: '#A3B18A' },
  { title: 'Emails', tag: 'emails', hoverColor: '#A3B18A' },
  { title: 'Users', tag: 'users', hoverColor: '#A3B18A' },
  { title: 'RSVPs', tag: 'rsvps', hoverColor: '#A3B18A' },
  { title: 'Logs', tag: 'logs', hoverColor: '#A3B18A' },
  { title: 'Settings', tag: 'settings', hoverColor: '#A3B18A' },
]


import { watch, nextTick } from 'vue'
const selectedTab = ref('Dashboard')
const adminMainRef = ref<HTMLElement | null>(null)

// Scroll to top of main content when selectedTab changes
watch(selectedTab, async () => {
  await nextTick()
  if (adminMainRef.value) {
    adminMainRef.value.scrollTop = 0
    adminMainRef.value.scrollTo?.({ top: 0, behavior: 'auto' })
  }
})

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
      { size: 'secondary', label: 'Middle Left', flex: 2, content: "Box" }
    ],
    [{ size: 'long', label: 'Overview', content: EventTable }],
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

const events = [] // Replace with your event data
const eventColumns = [
  { key: 'name', label: 'Name' },
  { key: 'date', label: 'Date' },
  { key: 'location', label: 'Location' },
  { key: 'actions', label: 'Actions' }
]
const eventTopBarProps = {}
function onEditEvent(event) {
  // Handle edit
}
function onDeleteEvent(event) {
  // Handle delete
}
</script>