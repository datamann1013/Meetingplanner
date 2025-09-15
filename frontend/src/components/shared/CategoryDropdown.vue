<template>
  <div class="category-dropdown-wrapper">
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      :style="{ backgroundColor: inputColor, borderColor: borderColor }"
      class="category-dropdown"
    >
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ label: string; modelValue: string; categories: Array<{ id: string; name: string }>; inputColor?: string; borderColor?: string }>()
defineEmits(['update:modelValue'])

const inputStyle = computed(() => ({
  background: props.inputColor || '',
  borderColor: props.borderColor || '',
}))
</script>

<style scoped>
.category-dropdown-wrapper { margin-bottom: 1rem; }
.category-dropdown { width: 100%; padding: 0.5rem; border: 1px solid var(--color-border, #ccc); }
</style>
