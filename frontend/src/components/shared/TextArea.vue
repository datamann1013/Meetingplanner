<template>
  <div class="text-area-wrapper">
    <v-textarea
      :model-value="modelValue"
      @update:modelValue="$emit('update:modelValue', $event)"
      :label="label"
      outlined
      density="compact"
      hide-details
      class="text-area compact-input"
      :style="inputStyle"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ label: string; modelValue: string; inputColor?: string; borderColor?: string }>()
defineEmits(['update:modelValue'])
const inputStyle = computed(() => ({
  backgroundColor: 'var(--color-table-header-bg, #f5f5f5)',
  borderColor: 'var(--color-primary-border, #b5c9a3)',
  color: 'var(--color-input-text, #4b3f2a)'
}))
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/vuetify@3.0.0/dist/vuetify.min.css');
.text-area-wrapper {
  margin-bottom: 1rem;
}
.text-area {
  width: 100%;
}
.compact-input .v-input__control {
  min-height: 36px !important;
}
</style>
