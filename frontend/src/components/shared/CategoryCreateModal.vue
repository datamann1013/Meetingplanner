<template>
  <Modal v-model="isOpen" :title="editingCategory ? 'Edit Category' : 'Create New Category'">
    <div>
      <TextInput
        v-model="categoryName"
        label="Category Name"
        placeholder="Enter category name..."
        :inputColor="'#f5f5f5'"
        :borderColor="'#616161'"
        @keyup.enter="saveCategory"
      />
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
    
    <div class="category-modal-actions">
      <InputButton 
        type="button" 
        @click="closeModal"
        :inputColor="'#f5f5f5'"
        :borderColor="'#616161'"
      >
        Cancel
      </InputButton>
      <InputButton 
        type="button" 
        @click="saveCategory"
        :disabled="!categoryName.trim() || loading"
        :inputColor="'#f5f5f5'"
        :borderColor="'#616161'"
      >
        {{ loading ? 'Saving...' : (editingCategory ? 'Update' : 'Create') }}
      </InputButton>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Modal from './Modal.vue'
import TextInput from './TextInput.vue'
import InputButton from './InputButton.vue'
import { categoryService, type Category } from '@/services/categoryService'

interface Props {
  modelValue: boolean
  editingCategory?: Category | null
}

interface Emits {
  'update:modelValue': [value: boolean]
  'categoryCreated': [category: Category]
  'categoryUpdated': [category: Category]
}

const props = withDefaults(defineProps<Props>(), {
  editingCategory: null
})

const emit = defineEmits<Emits>()

const isOpen = ref(props.modelValue)
const categoryName = ref('')
const loading = ref(false)
const error = ref('')

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  isOpen.value = newValue
  if (newValue) {
    // Reset form when opening
    categoryName.value = props.editingCategory?.attributes.name || ''
    error.value = ''
  }
})

watch(() => props.editingCategory, (newCategory) => {
  categoryName.value = newCategory?.attributes.name || ''
})

watch(isOpen, (newValue) => {
  emit('update:modelValue', newValue)
})

function closeModal() {
  isOpen.value = false
  categoryName.value = ''
  error.value = ''
}

async function saveCategory() {
  if (!categoryName.value.trim()) {
    error.value = 'Category name is required'
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    let savedCategory: Category
    
    if (props.editingCategory) {
      // Update existing category
      savedCategory = await categoryService.updateCategory(
        props.editingCategory.id, 
        categoryName.value.trim()
      )
      emit('categoryUpdated', savedCategory)
    } else {
      // Create new category
      savedCategory = await categoryService.createCategory(categoryName.value.trim())
      emit('categoryCreated', savedCategory)
    }
    
    closeModal()
  } catch (err: any) {
    error.value = err.response?.data?.error?.message || 'Failed to save category'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.category-modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.error-message {
  color: var(--color-error, #e74c3c);
  font-size: 0.9rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: #ffeaea;
  border-radius: 4px;
  border: 1px solid #ffcdd2;
}
</style>