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
import SidebarItem from '../SidebarItem.vue'
import { EventActions } from '@/composables/event/EventActions'
import { defineEmits } from 'vue'

const emit = defineEmits(['updateAction'])
const actions = [
  'Calendar',
  'Create Event',
  'Duplicate Previous Event',
  'Import Events',
  'Upload Images/Attachments',
  'Email Attendees'
]
const { selectedAction, selectAction } = EventActions('Calendar', actions, (action: string) => emit('updateAction', action))
</script>

