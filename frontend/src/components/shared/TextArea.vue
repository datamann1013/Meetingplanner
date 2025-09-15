<template>
  <div class="text-area-wrapper">
    <textarea
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
      :style="{ backgroundColor: inputColor, borderColor: borderColor }"
      class="text-area"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ label: string; modelValue: string; inputColor?: string; borderColor?: string }>()
defineEmits(['update:modelValue'])

function onInput(e: Event) {
  const value = (e.target as HTMLTextAreaElement).value
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
.text-area-wrapper { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
.text-area { flex: 1; padding: 0.5rem; border: 1px solid var(--color-border, #ccc); }
</style>
