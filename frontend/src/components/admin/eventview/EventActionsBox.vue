<template>
  <div>
    <h3 class="event-actions-title">Event Actions</h3>
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

<!-- Styles moved to global stylesheet -->
