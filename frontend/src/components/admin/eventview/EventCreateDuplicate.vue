<template>
  <div class="event-create-duplicate-box">
    <h3>{{ mode === 'create' ? 'Create Event' : 'Duplicate Event' }}</h3>
    <form>
      <TextInput label="Title" v-model="form.title" inputColor="#f5f5f5" borderColor="#616161" />
      <TextArea label="Description" v-model="form.description" inputColor="#f5f5f5" borderColor="#616161" />
      <DateTimePicker label="Date" v-model="form.date" inputColor="#f5f5f5" borderColor="#616161" />
      <TextInput label="Location" v-model="form.location" inputColor="#f5f5f5" borderColor="#616161" />
      <NumberInput label="Capacity" v-model="form.capacity" inputColor="#f5f5f5" borderColor="#616161" />
      <DateTimePicker label="Signup Deadline" v-model="form.signup_deadline" inputColor="#f5f5f5" borderColor="#616161" />
      <TextInput label="Contact Info" v-model="form.contact_info" inputColor="#f5f5f5" borderColor="#616161" />
      <button type="button" @click="openMediaPicker">Choose Cover Image</button>
      <CategoryDropdown label="Categories" v-model="form.category" :categories="categories" inputColor="#f5f5f5" borderColor="#616161" />
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
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
