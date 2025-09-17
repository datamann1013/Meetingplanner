
<template>
  <div class="category-dropdown-wrapper">
    <v-select
      :items="categoryOptions"
      :label="label"
      :model-value="modelValue"
      @update:modelValue="$emit('update:modelValue', $event)"
  outlined
  density="compact"
  hide-details
  class="category-dropdown compact-input"
  :style="inputStyle"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ label: string; modelValue: string; categories: Array<{ id: string; name: string }>; inputColor?: string; borderColor?: string }>()
defineEmits(['update:modelValue'])

const categoryOptions = computed(() => props.categories.map(cat => ({ text: cat.name, value: cat.id })))
const inputStyle = computed(() => ({
  backgroundColor: 'var(--color-table-header-bg, #f5f5f5)',
  borderColor: 'var(--color-primary-border, #b5c9a3)',
  color: 'var(--color-input-text, #4b3f2a)'
}))
</script>

<style scoped>
.category-dropdown-wrapper {
  margin-bottom: 1rem;
}
.category-dropdown {
  width: 100%;
}
.compact-input .v-input__control {
  min-height: 36px !important;
}
</style>
