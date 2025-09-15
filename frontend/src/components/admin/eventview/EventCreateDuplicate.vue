<template>
  <div class="event-create-duplicate-box">
    <h3>{{ mode === 'create' ? 'Create Event' : 'Duplicate Event' }}</h3>
    <form class="event-grid">
      <!-- Full-length fields first -->
      <label class="grid-label" for="title">Title</label>
      <div class="grid-span-3">
        <TextInput id="title" label="Title" v-model="form.title" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <label class="grid-label" for="description">Description</label>
      <div class="grid-span-3">
        <TextArea id="description" label="Description" v-model="form.description" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <label class="grid-label" for="location">Location</label>
      <div class="grid-span-3">
        <TextInput id="location" label="Location" v-model="form.location" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <label class="grid-label" for="contact_info">Contact Info</label>
      <div class="grid-span-3">
        <TextInput id="contact_info" label="Contact Info" v-model="form.contact_info" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <label class="grid-label">Cover Image</label>
      <div class="grid-span-3">
        <button type="button" @click="openMediaPicker">Choose Cover Image</button>
      </div>

      <!-- Split fields after -->
      <label class="grid-label" for="date">Date</label>
      <DateTimePicker id="date" label="Date" v-model="form.date" inputColor="#f5f5f5" borderColor="#616161" />
      <label class="grid-label" for="signup_deadline">Signup Deadline</label>
      <DateTimePicker id="signup_deadline" label="Signup Deadline" v-model="form.signup_deadline" inputColor="#f5f5f5" borderColor="#616161" />

      <label class="grid-label" for="capacity">Capacity</label>
      <NumberInput id="capacity" label="Capacity" v-model="form.capacity" inputColor="#f5f5f5" borderColor="#616161" />
      <label class="grid-label" for="category">Categories</label>
      <CategoryDropdown id="category" label="Categories" v-model="form.category" :categories="categories" inputColor="#f5f5f5" borderColor="#616161" />
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TextInput from '../../shared/TextInput.vue'
import TextArea from '../../shared/TextArea.vue'
import DateTimePicker from '../../shared/DateTimePicker.vue'
import NumberInput from '../../shared/NumberInput.vue'
import CategoryDropdown from '../../shared/CategoryDropdown.vue'

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
  category: ''
})
const categories = ref([
  { id: '1', name: 'Conference' },
  { id: '2', name: 'Workshop' },
  { id: '3', name: 'Meetup' }
])
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
  grid-template-columns: 0.7fr 1.3fr 0.7fr 1.3fr;
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
</style>
