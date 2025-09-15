<template>
  <div class="input-button-wrapper">
    <button
      :type="type"
      class="input-button"
      :style="{ backgroundColor: inputColor, borderColor: borderColor }"
      @click="$emit('click', $event)"
    >
      <slot>Button</slot>
    </button>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

defineProps<{
  type?: 'button' | 'submit' | 'reset',
  inputColor?: string,
  borderColor?: string
}>();

defineEmits(['click']);
</script>

<style scoped>
.input-button {
  width: 100%;
  background-color: #f5f5f5;
  border: 1px solid #616161;
  border-radius: 4px;
  padding: 10px 14px;
  font-size: 1rem;
  color: #333;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.input-button:focus,
.input-button:hover {
  border-color: #424242;
  outline: none;
  box-shadow: 0 0 0 2px #e0e0e0;
}
</style>
