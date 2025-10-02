
<template>
  <Modal v-model="isOpen" :hide-default-close="true">
    <div class="modal-header-row">
      <h3 class="modal-title">Edit Event</h3>
      <button class="modal-close-btn" @click="closeModal" aria-label="Close">×</button>
    </div>
    <div class="modal-body">
      <EventCreateDuplicate :mode="'edit'" />
    </div>
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

function closeModal() {
  isOpen.value = false
}
</script>

<style scoped>
.modal-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-title {
  margin: 0;
  color: var(--color-accent, #76944C);
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-accent, #76944C);
  padding: 0.25rem;
  line-height: 1;
}

.modal-close-btn:hover {
  color: var(--color-accent-dark, #5a7139);
}

.modal-body {
  margin-top: 0;
}
</style>

