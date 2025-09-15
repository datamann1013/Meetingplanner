<template>
  <div class="text-input-wrapper">
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :style="{ backgroundColor: inputColor, borderColor: borderColor }"
      class="text-input"
      :placeholder="placeholder"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: string
  inputColor?: string
  borderColor?: string
  placeholder?: string
}>()
defineEmits(['update:modelValue'])
</script>

<style scoped>
.text-input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.text-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--color-border, #ccc);
}
</style>
