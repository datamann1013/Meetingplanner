<template>
  <div class="input-row">
    <label>{{ label }}</label>
    <textarea :value="modelValue" @input="onInput($event)" class="input" :style="inputStyle" />
    <slot name="controls" />
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
.input-row { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
.input { flex: 1; padding: 0.5rem; border: 1px solid var(--color-border, #ccc); }
</style>
