<template>
  <div class="dual-interactive-container">
    <div class="dashboard-row">
      <DashboardBox variant="primary" :flex="1">
        <EventActionsBox
          :actions="actions"
          :selectedAction="selectedAction"
          @updateAction="updateAction"
        />
      </DashboardBox>
      <DashboardBox variant="secondary" :flex="2">
        <component :is="currentComponent" />
      </DashboardBox>
    </div>
    <div v-if="$slots.bottom" class="dashboard-row">
      <DashboardBox variant="long" :flex="1">
        <slot name="bottom" />
      </DashboardBox>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, h } from 'vue'
import DashboardBox from './DashboardBox.vue'
import EventActionsBox from "./eventview/EventActionsBox.vue";
import EventCreateDuplicate from "./eventview/EventCreateDuplicate.vue";

const props = defineProps<{
  actions: string[];
  contentMap: Record<string, any>;
  initialAction?: string;
}>()
const emit = defineEmits(['actionChanged'])
const selectedAction = ref<string>(props.initialAction ?? props.actions[0])

const currentComponent = computed(() => {
  if (selectedAction.value === 'Create Event') {
    return {
      render() {
        return h(EventCreateDuplicate, { mode: 'create' })
      }
    }
  }
  if (selectedAction.value === 'Duplicate Previous Event') {
    return {
      render() {
        return h(EventCreateDuplicate, { mode: 'duplicate' })
      }
    }
  }
  return props.contentMap[selectedAction.value] || {
    render() {
      return h('h2', 'Choose an action')
    }
  }
})

function updateAction(action: string) {
  selectedAction.value = action
  emit('actionChanged', action)
}

watch(() => props.initialAction, (newVal) => {
  if (typeof newVal === 'string') {
    selectedAction.value = newVal
  }
})
</script>

<style scoped>
.dashboard-row {
  display: flex;
  gap: 1rem;
}
</style>
