<template>
  <div class="file-upload-box">
    <div v-if="mode === 'attachment'" class="folder-selector">
      <v-row align="center" class="mb-2">
        <v-col cols="9">
          <Dropdown
            v-model="selectedFolder"
            :options="folderOptions"
            label="Select folder"
            inputColor="#f5f5f5"
            borderColor="#616161"
            style="min-width: 180px"
          />
        </v-col>
        <v-col cols="3">
          <InputButton
            type="button"
            inputColor="#f5f5f5"
            borderColor="#616161"
            style="min-width: 120px; min-height: 36px; width: 100%;"
            @click="showCreateFolder = true"
          >
            Create Folder
          </InputButton>
        </v-col>
      </v-row>
      <v-divider class="mb-2" />
    </div>
    <div class="upload-drop-area-wrapper">
      <div
        class="upload-drop-area full-box"
        @dragover.prevent="dragActive = true"
        @dragleave.prevent="dragActive = false"
        @drop.prevent="onDrop"
        @click="onClickBox"
        :class="{ 'drag-active': dragActive }"
      >
        <input
          ref="fileInput"
          type="file"
          :multiple="mode === 'attachment'"
          class="d-none"
          @change="onFileChange"
        />
        <div class="upload-content">
          <v-icon size="36">mdi-upload</v-icon>
          <div class="mt-2">
            <span v-if="mode === 'import'">Drag & drop to import events, or click to select file</span>
            <span v-else>Drag & drop to upload files, or click to select</span>
          </div>
        </div>
      </div>
    </div>
    <Modal v-model="showCreateFolder" title="Create New Folder">
      <div class="folder-input-group">
          <label for="folderName" class="folder-label">Folder Name</label>
          <input 
            id="folderName"
            v-model="newFolderName" 
            type="text"
            class="folder-input"
            placeholder="Enter folder name..."
            @keyup.enter="onCreateFolder"
          />
        </div>
        <div class="folder-actions">
          <button class="folder-btn folder-btn-cancel" @click="showCreateFolder = false">Cancel</button>
          <button class="folder-btn folder-btn-create" @click="onCreateFolder">Create</button>
        </div>
    </Modal>
  </div>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits, computed } from 'vue';
import Dropdown from './Dropdown.vue';
import InputButton from './InputButton.vue';
import Modal from './Modal.vue';

const props = defineProps({
  mode: {
    type: String,
    default: 'import', // 'import' or 'attachment'
  },
  folders: {
    type: Array as () => string[],
    default: () => [],
  },
});

const emit = defineEmits(['file-selected', 'create-folder']);

const dragActive = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const selectedFolder = ref(props.folders[0] || '');
const folderOptions = computed(() => props.folders.map(f => ({ text: f, value: f })));
const showCreateFolder = ref(false);
const newFolderName = ref('');

function onClickBox() {
  fileInput.value?.click();
}

function onFileChange(e: Event) {
  const files = (e.target as HTMLInputElement).files;
  if (files && files.length > 0) {
    emit('file-selected', { files, folder: selectedFolder.value });
  }
  dragActive.value = false;
}

function onDrop(e: DragEvent) {
  dragActive.value = false;
  if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
    emit('file-selected', { files: e.dataTransfer.files, folder: selectedFolder.value });
  }
}

function onCreateFolder() {
  emit('create-folder', newFolderName.value);
  showCreateFolder.value = false;
  newFolderName.value = '';
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
  color: var(--v-theme-on-surface, #000);
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--v-theme-on-surface, #000);
  padding: 0.25rem;
  line-height: 1;
}

.modal-close-btn:hover {
  color: var(--v-theme-on-surface-variant, #666);
}

.modal-body {
  margin-top: 0;
  min-width: 400px;
  padding: 1rem;
}

.folder-input-group {
  margin-bottom: 2rem;
}

.folder-label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  font-size: 1rem;
  color: var(--v-theme-on-surface, #000);
}

.folder-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.2s;
  box-sizing: border-box;
}

.folder-input:focus {
  outline: none;
  border-color: var(--v-theme-primary);
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.1);
}

.folder-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.folder-btn {
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 120px;
  white-space: nowrap;
  text-align: center;
}

.folder-btn-cancel {
  background-color: #f8f9fa;
  color: #495057;
  border: 2px solid #dee2e6;
}

.folder-btn-cancel:hover {
  background-color: #e9ecef;
  border-color: #adb5bd;
  transform: translateY(-1px);
}

.folder-btn-create {
  background-color: #76944C;
  color: white;
  border: 2px solid #76944C;
  box-shadow: 0 2px 4px rgba(118, 148, 76, 0.2);
}

.folder-btn-create:hover {
  background-color: #5a7139;
  border-color: #5a7139;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(118, 148, 76, 0.3);
}
</style>

