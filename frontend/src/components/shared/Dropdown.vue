<template>
  <div class="dropdown-wrapper">
    <v-select
      :items="options"
      :label="label"
      :model-value="modelValue"
      @update:modelValue="$emit('update:modelValue', $event)"
      outlined
      density="compact"
      hide-details
      class="dropdown compact-input"
      :style="inputStyle"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ label: string; modelValue: string; options: Array<{ text: string; value: string }>; inputColor?: string; borderColor?: string }>()
defineEmits(['update:modelValue'])

const inputStyle = computed(() => ({
  backgroundColor: 'var(--color-table-header-bg, #f5f5f5)',
  borderColor: 'var(--color-primary-border, #b5c9a3)',
  color: 'var(--color-input-text, #4b3f2a)'
}))
</script>

<style scoped>
.dropdown-wrapper {
  margin-bottom: 1rem;
}
.dropdown {
  width: 100%;
}
.compact-input .v-input__control {
  min-height: 36px !important;
}
</style>
