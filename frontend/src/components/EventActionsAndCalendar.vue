<template>
  <div>
    <div class="dashboard-row">
      <DashboardBox variant="primary" :flex="1">
        <EventActionsBox :selectedAction="selectedAction" @updateAction="updateAction" />
      </DashboardBox>
      <DashboardBox variant="secondary" :flex="2">
        <component :is="currentComponent" />
      </DashboardBox>
    </div>
    <div class="dashboard-row">
      <DashboardBox variant="long" :flex="1">
        <EventListTable />
      </DashboardBox>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, defineProps, defineEmits, h } from 'vue'
import EventListTable from './EventListTable.vue'
import DashboardBox from './DashboardBox.vue'
import EventActionsBox from './EventActionsBox.vue'
import EventCalendarBox from './EventCalendarBox.vue'

const props = defineProps({
  initialAction: {
    type: String,
    default: 'Calendar'
  }
})
const emit = defineEmits(['actionChanged'])
const selectedAction = ref(props.initialAction)

const currentComponent = computed(() => {
  switch (selectedAction.value) {
    case 'Calendar':
      return EventCalendarBox
    case 'Create Event':
      return {
        render() {
          return h('h2', 'Create Event')
        }
      }
    case 'Duplicate Previous Event':
      return {
        render() {
          return h('h2', 'Duplicate Previous Event')
        }
      }
    case 'Import Events':
      return {
        render() {
          return h('h2', 'Import Events')
        }
      }
    case 'Upload Images/Attachments':
      return {
        render() {
          return h('h2', 'Upload Images/Attachments')
        }
      }
    case 'Email Attendees':
      return {
        render() {
          return h('h2', 'Email Attendees')
        }
      }
    default:
      return {
        render() {
          return h('h2', 'Choose an action')
        }
      }
  }
})

function updateAction(action) {
  selectedAction.value = action
  emit('actionChanged', action)
}

watch(() => props.initialAction, (newVal) => {
  selectedAction.value = newVal
})
</script>

<style scoped>
.dashboard-row {
  display: flex;
  gap: 1rem;
}
</style>
