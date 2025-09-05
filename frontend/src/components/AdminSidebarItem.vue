<template>
  <div
    class="admin-sidebar-item"
    :class="{ 'admin-sidebar-item-selected': selected }"
    @click="onClick"
    @mouseover="hovered = true"
    @mouseleave="hovered = false"
    :style="itemStyle"
  >
    {{ title }}
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
const props = defineProps({
  title: String,
  selected: Boolean
})
const emit = defineEmits(['click'])
function onClick() {
  emit('click')
}
</script>

<style scoped>
/* You can keep or move sidebar item styles here if needed */
</style>
