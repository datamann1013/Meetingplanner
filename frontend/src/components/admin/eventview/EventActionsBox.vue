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
const emit = defineEmits(['updateAction'])
const props = defineProps<{ actions: string[]; selectedAction: string }>()
function selectAction(action: string) {
  emit('updateAction', action)
}
</script>

<style scoped>
.event-actions-list-wrapper {
  margin-top: 12px;
}
</style>

