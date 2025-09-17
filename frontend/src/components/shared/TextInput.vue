<template>
  <div class="text-input-wrapper">
    <v-text-field
      :model-value="modelValue"
      @update:modelValue="$emit('update:modelValue', $event)"
      :label="label"
      :placeholder="placeholder"
      outlined
      density="compact"
      hide-details
      class="text-input compact-input"
      :style="inputStyle"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{
  modelValue: string
  label?: string
  inputColor?: string
  borderColor?: string
  placeholder?: string
}>()
defineEmits(['update:modelValue'])
const inputStyle = computed(() => ({
  backgroundColor: 'var(--color-table-header-bg, #f5f5f5)',
  borderColor: 'var(--color-primary-border, #b5c9a3)',
  color: 'var(--color-input-text, #4b3f2a)'
}))
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/vuetify@3.0.0/dist/vuetify.min.css');
.text-input-wrapper {
  margin-bottom: 1rem;
}
.text-input {
  width: 100%;
}
.compact-input .v-input__control {
  min-height: 36px !important;
}
</style>
