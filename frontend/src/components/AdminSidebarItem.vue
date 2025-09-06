<template>
  <div
    class="admin-sidebar-item"
    :class="{ 'admin-sidebar-item-selected': selected }"
    @click="onClick"
    @mouseover="hovered = true"
    @mouseleave="hovered = false"
    :style="itemStyle"
  >
    <span class="admin-sidebar-item-text" :style="{ paddingLeft: leftPadding }">{{ title }}</span>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, computed } from 'vue'
const props = defineProps({
  title: String,
  selected: Boolean,
  hoverColor: {
    type: String,
    default: '#f0f0f0'
  },
  leftPadding: {
    type: String,
    default: '1.5rem'
  }
})
const hovered = ref(false)
const emit = defineEmits(['click'])
function onClick() {
  emit('click')
}

const itemStyle = computed(() => {
  return hovered.value
    ? { backgroundColor: props.hoverColor, cursor: 'pointer' }
    : { cursor: 'pointer' }
})
const leftPadding = props.leftPadding
</script>

<style scoped>
.admin-sidebar-item {
  border-radius: 0;
  padding: 0.75rem 0;
  transition: background 0.2s;
  font-weight: 500;
  user-select: none;
  background: none;
  width: 100%;
  box-sizing: border-box;
}
.admin-sidebar-item-text {
  display: block;
  padding-right: 2rem;
}
</style>
