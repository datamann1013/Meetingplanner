<template>
  <div class="event-create-duplicate-box">
    <form class="event-grid">
      <div class="grid-span-4">
        <TextInput id="title" label="Title" v-model="form.title" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <div class="grid-span-4">
        <TextArea id="description" label="Description" v-model="form.description" inputColor="#f5f5f5" borderColor="#616161" />
      </div>

      <div>
        <TextInput id="location" label="Location" v-model="form.location" inputColor="#f5f5f5" borderColor="#616161" />
      </div>
      <div>
        <DateTimePicker id="date" label="Date" v-model="form.date" inputColor="#f5f5f5" borderColor="#616161" />
      </div>
      <div>
        <NumberInput id="capacity" label="Capacity" v-model="form.capacity" inputColor="#f5f5f5" borderColor="#616161" />
      </div>
      <div>
        <Dropdown 
          id="category" 
          label="Categories" 
          v-model="form.category" 
          :options="categoryOptionsWithCreate" 
          inputColor="#f5f5f5" 
          borderColor="#616161" 
          @update:modelValue="handleCategoryChange"
        />
      </div>
      <div>
        <TextInput id="contact_info" label="Contact Info" v-model="form.contact_info" inputColor="#f5f5f5" borderColor="#616161" />
      </div>
      <div>
        <DateTimePicker id="signup_deadline" label="Signup Deadline" v-model="form.signup_deadline" inputColor="#f5f5f5" borderColor="#616161" />
      </div>
      <div>
        <InputButton type="button" inputColor="#f5f5f5" borderColor="#616161" @click="openMediaPicker">Choose Cover Image</InputButton>
      </div>
      <div>
        <Dropdown id="status" label="Status" v-model="form.status" :options="statusOptions" inputColor="#f5f5f5" borderColor="#616161" />
      </div>
      <div class="button-row grid-span-4">
        <InputButton type="submit" inputColor="#f5f5f5" borderColor="#616161" class="full-width-button">{{ mode === 'edit' ? 'Confirm Changes' : 'Create Event' }}</InputButton>
      </div>
    </form>
    
    <!-- Category Create Modal -->
    <CategoryCreateModal 
      v-model="showCategoryModal"
      @categoryCreated="handleCategoryCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import TextInput from '../../shared/TextInput.vue'
import TextArea from '../../shared/TextArea.vue'
import DateTimePicker from '../../shared/DateTimePicker.vue'
import NumberInput from '../../shared/NumberInput.vue'
import Dropdown from '../../shared/Dropdown.vue'
import InputButton from '../../shared/InputButton.vue'
import CategoryCreateModal from '../../shared/CategoryCreateModal.vue'
import { categoryService, type Category } from '@/services/categoryService'

defineProps<{ mode: 'create' | 'duplicate' | 'edit' }>()

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

// Category state
const categories = ref<Category[]>([])
const loadingCategories = ref(false)
const showCategoryModal = ref(false)

// Category options with "Create New" option
const categoryOptionsWithCreate = computed(() => {
  console.log('Computing category options from:', categories.value)
  
  if (!categories.value || categories.value.length === 0) {
    console.log('No categories available')
    return [{ 
      text: '+ Create New Category',
      value: 'CREATE_NEW' 
    }]
  }
  
  const categoryOptions = categories.value.map(cat => {
    console.log('Processing category - full object:', cat)
    
    // Handle both direct property and nested attributes structure
    const categoryData = cat as any
    const name = categoryData.name || categoryData.attributes?.name || 'Unknown Category'
    const id = categoryData.id?.toString() || ''
    
    console.log('Final extracted values:', { name, id })
    
    return { 
      text: name,
      value: id 
    }
  }).filter(option => option.text !== 'Unknown Category' && option.value !== '')
  
  console.log('Final formatted category options:', categoryOptions)
  
  // Add "Create New Category" option at the end
  categoryOptions.push({ 
    text: '+ Create New Category',
    value: 'CREATE_NEW' 
  })
  
  return categoryOptions
})

// Load categories from Strapi
async function loadCategories() {
  loadingCategories.value = true
  try {
    console.log('Loading categories...')
    const response = await categoryService.getCategories()
    console.log('Categories loaded:', response)
    categories.value = response.data
    console.log('Categories set to:', categories.value)
  } catch (error) {
    console.error('Failed to load categories:', error)
    // Fallback to empty categories if API fails
    categories.value = []
  } finally {
    loadingCategories.value = false
  }
}

// Handle category selection change
function handleCategoryChange(value: string) {
  if (value === 'CREATE_NEW') {
    // Reset the dropdown and open modal
    form.value.category = ''
    showCategoryModal.value = true
  }
}

// Handle new category creation
function handleCategoryCreated(newCategory: Category) {
  // Add new category to the list
  categories.value.push(newCategory)
  // Select the newly created category
  form.value.category = newCategory.id.toString()
}

function openMediaPicker() {
  // Placeholder for media picker modal
  alert('Media picker modal will be implemented soon.')
}

// Load categories when component mounts
onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
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
