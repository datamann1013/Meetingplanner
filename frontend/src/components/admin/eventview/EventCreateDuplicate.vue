<template>
  <div class="event-create-duplicate-box">
  <!-- Removed redundant section title -->
    <form class="event-grid">
      <!-- Full-length fields first -->
      <div class="grid-span-3">
        <TextInput id="title" label="Title" v-model="form.title" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <div class="grid-span-3">
        <TextArea id="description" label="Description" v-model="form.description" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <div class="grid-span-3">
        <TextInput id="location" label="Location" v-model="form.location" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <!-- Split fields: Date & Signup Deadline -->
      <DateTimePicker id="date" label="Date" v-model="form.date" inputColor="#f5f5f5" borderColor="#616161" />
      <DateTimePicker id="signup_deadline" label="Signup Deadline" v-model="form.signup_deadline" inputColor="#f5f5f5" borderColor="#616161" />

      <!-- Split fields: Capacity & Categories -->
      <NumberInput id="capacity" label="Capacity" v-model="form.capacity" inputColor="#f5f5f5" borderColor="#616161" />
      <Dropdown id="category" label="Categories" v-model="form.category" :options="categoryOptions" inputColor="#f5f5f5" borderColor="#616161" />

      <!-- Split fields: Cover Image & Contact Info -->
      <div>
        <InputButton type="button" inputColor="#f5f5f5" borderColor="#616161" @click="openMediaPicker">Choose Cover Image</InputButton>
      </div>
      <TextInput id="contact_info" label="Contact Info" v-model="form.contact_info" inputColor="#f5f5f5" borderColor="#616161" />
  <Dropdown id="status" label="Status" v-model="form.status" :options="statusOptions" inputColor="#f5f5f5" borderColor="#616161" />
      <!-- Create Event Button -->
      <div class="button-row grid-span-3 grid-col-2-4">
        <InputButton type="submit" inputColor="#f5f5f5" borderColor="#616161" class="full-width-button">Create Event</InputButton>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import TextInput from '../../shared/TextInput.vue'
import TextArea from '../../shared/TextArea.vue'
import DateTimePicker from '../../shared/DateTimePicker.vue'
import NumberInput from '../../shared/NumberInput.vue'
import Dropdown from '../../shared/Dropdown.vue'
import InputButton from '../../shared/InputButton.vue'

const props = defineProps<{ mode: 'create' | 'duplicate' }>()
const form = ref({
  title: '',
  description: '',
  date: '',
  location: '',
  capacity: 0,
  signup_deadline: '',
  contact_info: '',
  coverimage: '',
  category: '',
  status: ''
})
const statusOptions = [
  { text: 'Unpublished', value: 'unpublished' },
  { text: 'Published', value: 'published' },
  { text: 'Draft', value: 'draft' },
  { text: 'Blueprint', value: 'blueprint' }
]
const categories = ref([
  { id: '1', name: 'Conference' },
  { id: '2', name: 'Workshop' },
  { id: '3', name: 'Meetup' }
])
const categoryOptions = computed(() => categories.value.map(cat => ({ text: cat.name, value: cat.id })))
function openMediaPicker() {
  // Placeholder for media picker modal
  alert('Media picker modal will be implemented soon.')
}
</script>

<style scoped>
.event-create-duplicate-box {
  /* Remove all custom box-shadow and border-radius to inherit from parent */
}
.event-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 16px;
  align-items: center;
}
.grid-label {
  grid-column: span 1;
  font-weight: 500;
  margin-bottom: 4px;
}
.grid-span-3 {
  grid-column: span 3;
}
.grid-span-4 {
  grid-column: span 4;
}
.button-row {
  display: flex;
  justify-content: center;
}
.grid-col-2-4 {
  grid-column: 2 / 5;
}
.full-width-button {
  width: 100%;
}
.event-section-title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 24px;
  margin-top: 0;
}
</style>
