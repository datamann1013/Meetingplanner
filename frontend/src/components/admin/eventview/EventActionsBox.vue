<template>
  <div>
    <h3 style="margin-bottom: 16px;">Event Actions</h3>
    <div class="event-actions-list-wrapper">
      <div class="event-actions-list">
        <SidebarItem
          v-for="action in actions"
          :key="action"
          :title="action"
          :selected="selectedAction === action"
          hoverColor="#d6bfa7"
          leftPadding="2.5rem"
          @click="selectAction(action)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import SidebarItem from '../SidebarItem.vue'

const emit = defineEmits(['updateAction'])
const actions = [
  'Calendar',
  'Create Event',
  'Duplicate Previous Event',
  'Import Events',
  'Upload Images/Attachments',
  'Email Attendees'
]
const selectedAction = ref('Calendar')

function selectAction(action: string) {
  selectedAction.value = action
  emit('updateAction', action)
}
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
