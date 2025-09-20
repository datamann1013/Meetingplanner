<template>
  <div class="email-sender-box">
  <!-- Removed redundant section title -->
    <div class="form-row">
      <Dropdown
        v-model="recipientType"
        :options="recipientOptions"
        label="Recipients"
        inputColor="#f5f5f5"
        borderColor="#616161"
        class="form-item"
      />
      <Dropdown
        v-model="eventId"
        :options="eventOptions"
        label="Regarding Event"
        inputColor="#f5f5f5"
        borderColor="#616161"
        class="form-item"
      />
      <InputButton
        type="button"
        class="form-item"
        inputColor="#f5f5f5"
        borderColor="#616161"
        @click="triggerFileInput"
      >
        Add Attachments
      </InputButton>
      <input
        ref="fileInput"
        type="file"
        multiple
        style="display: none"
        @change="handleFiles"
      />
    </div>
    <div class="form-row">
      <TextArea
        v-model="emailBody"
        label="Email Body"
        :rows="11"
        class="form-item email-body-area"
      />
    </div>
    <div class="form-row actions">
      <InputButton
        type="button"
        class="full-width-button send-email-button"
        inputColor="#f5f5f5"
        borderColor="#616161"
        :disabled="!canSend || sending"
        @click="sendEmail"
      >
        <span v-if="!sending">Send Email</span>
        <span v-else>Sending...</span>
      </InputButton>
    </div>
    <div v-if="attachments.length" class="attachments-list">
      <div v-for="(file, idx) in attachments" :key="idx" class="attachment-item">
        <v-icon small color="grey">mdi-paperclip</v-icon>
        <span>{{ file.name }}</span>
        <v-btn icon small @click="removeAttachment(idx)"><v-icon small color="red">mdi-close</v-icon></v-btn>
      </div>
    </div>
    <v-alert v-if="successMsg" type="success" dense>{{ successMsg }}</v-alert>
    <v-alert v-if="errorMsg" type="error" dense>{{ errorMsg }}</v-alert>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import Dropdown from '../../shared/Dropdown.vue';
import InputButton from '../../shared/InputButton.vue';
import TextArea from '../../shared/TextArea.vue';
import { EventTable } from '@/composables/event/EventTable';

const recipientOptions = [
  { text: 'Attending', value: 'attending' },
  { text: 'All', value: 'all' },
  { text: 'Specific', value: 'specific' },
];

const recipientType = ref('attending');
const eventId = ref(null);
const emailBody = ref('');
const attachments = ref<File[]>([]);
const sending = ref(false);
const successMsg = ref('');
const errorMsg = ref('');


const eventOptions = ref<{ text: string; value: any }[]>([]);
onMounted(async () => {
  try {
    const eventTable = EventTable();
    // Wait for events to load if needed
    if (eventTable.loading?.value) {
      // Wait for loading to finish (simulate)
      await new Promise((res) => setTimeout(res, 500));
    }
    eventOptions.value = eventTable.events.value.map((ev: any) => ({ text: ev.name || ev.title, value: ev.id }));
  } catch (e) {
    eventOptions.value = [];
  }
});

const canSend = computed(() => !!emailBody.value && !!recipientType.value && !!eventId.value);

function triggerFileInput() {
  (fileInput.value as HTMLInputElement)?.click();
}

const fileInput = ref<HTMLInputElement | null>(null);
function handleFiles(e: Event) {
  const files = (e.target as HTMLInputElement).files;
  if (files) {
    attachments.value = [...attachments.value, ...Array.from(files)];
  }
}
function removeAttachment(idx: number) {
  attachments.value.splice(idx, 1);
}

async function sendEmail() {
  sending.value = true;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    // Simulate API call
    await new Promise((res) => setTimeout(res, 1200));
    successMsg.value = 'Email sent successfully!';
    emailBody.value = '';
    attachments.value = [];
  } catch (e) {
    errorMsg.value = 'Failed to send email.';
  } finally {
    sending.value = false;
  }
}
</script>

<style scoped>
.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
}
.form-item {
  min-width: 180px;
  flex: 1;
}
.email-body-area {
  min-height: 160px;
  flex: 1 1 100%;
  resize: vertical;
}
.send-email-button {
  flex: 1 1 100%;
  width: 100%;
}
.actions {
  justify-content: flex-end;
}
.attachments-list {
  margin-top: 8px;
}
.attachment-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95em;
  margin-bottom: 4px;
}
</style>