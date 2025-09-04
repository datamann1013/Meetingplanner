<template>
  <div>
    <h3 style="margin-bottom: 16px;">Event Actions</h3>
    <div style="display: flex; flex-direction: column; gap: 12px;">
      <AdminSidebarItem title="Create Event" :selected="false" />
      <AdminSidebarItem title="Duplicate Previous Event" :selected="false" />
      <AdminSidebarItem title="Import Events" :selected="false" />
      <AdminSidebarItem title="Upload Images/Attachments" :selected="false" />
      <AdminSidebarItem title="Email Attendees" :selected="false" />
    </div>
  </div>
</template>
<script setup lang="ts">
import AdminSidebarItem from './AdminSidebarItem.vue'
</script>
