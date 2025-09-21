<template>
  <div class="input-button-wrapper">
    <button
      :type="type"
      class="input-button compact-input"
      :style="buttonStyle"
      @click="$emit('click', $event)"
    >
      <slot>Button</slot>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps, defineEmits } from 'vue';
const props = defineProps<{
  type?: 'button' | 'submit' | 'reset',
  inputColor?: string,
  borderColor?: string
}>();
defineEmits(['click']);
const buttonStyle = computed(() => ({
  backgroundColor: 'var(--color-table-header-bg, #f5f5f5)',
  borderColor: 'var(--color-primary-border, #b5c9a3)',
  color: 'var(--color-input-text, #4b3f2a)',
}));
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/vuetify@3.0.0/dist/vuetify.min.css');
.input-button-wrapper {
  margin-bottom: 1rem;
}
  .input-button {
    width: 100%;
    border: 1px solid var(--color-primary-border, #b5c9a3);
    border-radius: 4px;
    padding: 0 14px;
    font-size: 1rem;
    color: var(--color-input-text, #4b3f2a);
    background-color: var(--color-table-header-bg, #f5f5f5);
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
.input-button:focus,
.input-button:hover {
  border-color: #424242;
  outline: none;
  box-shadow: 0 0 0 2px #e0e0e0;
  background-color: var(--color-table-header-bg, #f5f5f5);
}
.compact-input {
  min-height: 40px !important;
}
</style>
