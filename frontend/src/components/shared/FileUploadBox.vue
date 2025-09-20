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
    <v-dialog v-model="showCreateFolder" max-width="400">
      <v-card>
        <v-card-title>Create Folder</v-card-title>
        <v-card-text>
          <v-text-field v-model="newFolderName" label="Folder Name" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showCreateFolder = false">Cancel</v-btn>
          <v-btn color="primary" text @click="onCreateFolder">Create</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits, computed } from 'vue';
import Dropdown from './Dropdown.vue';
import InputButton from './InputButton.vue';

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
.file-upload-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.upload-drop-area-wrapper {
  flex: 1 1 auto;
  display: flex;
}
.upload-drop-area.full-box {
  border: 2px dashed #aaa;
  border-radius: 8px;
  padding: 32px 0;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
  background: #fafafa;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.upload-drop-area.full-box.drag-active {
  border-color: #1976d2;
  background: #e3f2fd;
}
.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.folder-selector {
  margin-bottom: 8px;
}
</style>
