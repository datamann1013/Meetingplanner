<template>
  <div class="number-input-wrapper">
    <v-text-field
      type="number"
      :model-value="modelValue"
      @update:modelValue="$emit('update:modelValue', $event)"
      :label="label"
      :placeholder="placeholder"
      outlined
      density="compact"
      hide-details
      class="number-input compact-input"
      :style="inputStyle"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{
  modelValue: number
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
.number-input-wrapper {
  margin-bottom: 1rem;
}
.number-input {
  width: 100%;
}
.compact-input .v-input__control {
  min-height: 36px !important;
}
</style>
