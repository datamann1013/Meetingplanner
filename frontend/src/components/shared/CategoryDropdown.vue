<template>
  <div class="input-row">
    <label>{{ label }}</label>
    <select :value="modelValue" @change="onChange($event)" class="input" :style="inputStyle">
      <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      <option value="__new">Create new category...</option>
    </select>
    <slot name="controls" />
  </div>
</template>
<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ label: string; modelValue: string; categories: Array<{ id: string; name: string }>; inputColor?: string; borderColor?: string }>()
defineEmits(['update:modelValue'])

function onChange(e: Event) {
  const value = (e.target as HTMLSelectElement).value
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
.input { flex: 1; border: 1px solid var(--color-border, #ccc); padding: 0.5rem; }
</style>
