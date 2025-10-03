<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <!-- Header section with optional title and close button -->
      <div v-if="title || !hideDefaultClose" class="modal-header">
        <h3 v-if="title" class="modal-title">{{ title }}</h3>
        <div v-else class="modal-title-spacer"></div>
        <button 
          v-if="!hideDefaultClose" 
          class="modal-close-btn" 
          @click="close" 
          aria-label="Close"
        >
          ×
        </button>
      </div>
      
      <!-- Content section -->
      <div class="modal-body" :class="{ 'with-header': title || !hideDefaultClose }">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineEmits } from 'vue';

interface Props {
  modelValue: boolean
  hideDefaultClose?: boolean
  title?: string
}

defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

function close() {
  emit('update:modelValue', false);
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  border-radius: 8px;
  min-width: 320px;
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.2);
  position: relative;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem 0.5rem 1.5rem;
  border-bottom: 1px solid var(--color-table-border, #e0e0e0);
  flex-shrink: 0;
}

.modal-title {
  margin: 0;
  color: var(--v-theme-on-surface, #000);
  font-size: 1.25rem;
  font-weight: 600;
  flex: 1;
}

.modal-title-spacer {
  flex: 1;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--v-theme-on-surface, #000);
  padding: 0.25rem;
  line-height: 1;
  border-radius: 4px;
  transition: background-color 0.2s, color 0.2s;
}

.modal-close-btn:hover {
  background-color: var(--color-table-hover, #f5f5f5);
  color: var(--v-theme-on-surface-variant, #666);
}

.modal-close-btn:focus {
  outline: 2px solid var(--color-focus, #1976d2);
  outline-offset: 2px;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.modal-body.with-header {
  padding-top: 1rem;
}
</style>
