<template>
  <div>
    <h3 style="margin-bottom: 16px;">Event Actions</h3>
    <div class="event-actions-list-wrapper">
      <div class="event-actions-list">
        <AdminSidebarItem title="Create Event" :selected="false" hoverColor="#d6bfa7" leftPadding="2.5rem" />
        <AdminSidebarItem title="Duplicate Previous Event" :selected="false" hoverColor="#d6bfa7" leftPadding="2.5rem" />
        <AdminSidebarItem title="Import Events" :selected="false" hoverColor="#d6bfa7" leftPadding="2.5rem" />
        <AdminSidebarItem title="Upload Images/Attachments" :selected="false" hoverColor="#d6bfa7" leftPadding="2.5rem" />
        <AdminSidebarItem title="Email Attendees" :selected="false" hoverColor="#d6bfa7" leftPadding="2.5rem" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AdminSidebarItem from './AdminSidebarItem.vue'
</script>

<style scoped>
.event-actions-list-wrapper {
  margin-left: -1.5rem;
  margin-right: -1.5rem;
}
.event-actions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.event-actions-list .admin-sidebar-item {
  width: 100%;
  box-sizing: border-box;
  padding-left: 0;
  padding-right: 0;
}
</style>
