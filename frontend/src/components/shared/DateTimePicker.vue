<template>
  <div class="date-time-picker-wrapper">
    <input
      type="datetime-local"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :style="{ backgroundColor: inputColor, borderColor: borderColor }"
      class="date-time-picker"
      :placeholder="placeholder"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ label: string; modelValue: string; inputColor?: string; borderColor?: string }>()
defineEmits(['update:modelValue'])

function onInput(e: Event) {
  const value = (e.target as HTMLInputElement).value
  // emit update:modelValue
  // @ts-ignore
  emit('update:modelValue', value)
}

const inputStyle = computed(() => ({
  background: props.inputColor || '',
  borderColor: props.borderColor || '',
}))
</script>

<style scoped>
.date-time-picker-wrapper { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
.date-time-picker { flex: 1; padding: 0.5rem; border: 1px solid var(--color-border, #ccc); }
</style>
