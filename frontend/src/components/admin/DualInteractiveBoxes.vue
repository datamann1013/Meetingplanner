<template>
  <div>
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
import { ref, computed, watch, defineProps, defineEmits, h } from 'vue'
import DashboardBox from './DashboardBox.vue'
import EventActionsBox from '../EventActionsBox.vue'

const props = defineProps<{
  actions: string[];
  contentMap: Record<string, any>;
  initialAction?: string;
}>()
const emit = defineEmits(['actionChanged'])
const selectedAction = ref<string>(props.initialAction ?? props.actions[0])

const currentComponent = computed(() => {
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
