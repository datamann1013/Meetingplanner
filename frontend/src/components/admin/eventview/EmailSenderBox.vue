<template>
  <div class="email-sender-box">
    <h3 class="box-title">Send Mass Email</h3>
    <div class="form-row">
      <v-select
        v-model="recipientType"
        :items="recipientOptions"
        label="Recipients"
        outlined
        dense
        class="form-item"
      />
      <v-select
        v-model="eventId"
        :items="eventOptions"
        label="Regarding Event"
        outlined
        dense
        class="form-item"
      />
      <v-btn
        color="primary"
        @click="triggerFileInput"
        class="form-item"
        outlined
      >
        Add Attachments
      </v-btn>
      <input
        ref="fileInput"
        type="file"
        multiple
        style="display: none"
        @change="handleFiles"
      />
    </div>
    <div class="form-row">
      <v-textarea
        v-model="emailBody"
        label="Email Body"
        rows="6"
        outlined
        class="form-item"
      />
    </div>
    <div class="form-row actions">
      <v-btn color="success" @click="sendEmail" :loading="sending" :disabled="!canSend">
        Send Email
      </v-btn>
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
.email-sender-box {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
.box-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 16px;
}
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