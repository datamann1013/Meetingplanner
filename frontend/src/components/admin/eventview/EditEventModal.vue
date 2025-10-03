
<template>
  <Modal v-model="isOpen" title="Edit Event">
    <EventCreateDuplicate :mode="'edit'" />
  </Modal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Modal from '../../shared/Modal.vue'
import EventCreateDuplicate from './EventCreateDuplicate.vue'

interface Props {
  modelValue: boolean
}

interface Emits {
  'update:modelValue': [value: boolean]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const isOpen = ref(props.modelValue)

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  isOpen.value = newValue
})

// Watch for internal changes
watch(isOpen, (newValue) => {
  emit('update:modelValue', newValue)
})
</script>

