<template>
  <div class="number-input-wrapper">
    <input
      type="number"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :style="{ backgroundColor: inputColor, borderColor: borderColor }"
      class="number-input"
      :placeholder="placeholder"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: number
  inputColor?: string
  borderColor?: string
  placeholder?: string
}>()
defineEmits(['update:modelValue'])
</script>

<style scoped>
.number-input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.number-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--color-border, #ccc);
}
</style>
