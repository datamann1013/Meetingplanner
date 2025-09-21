<template>
  <div class="event-table-wrapper">
    <h3 class="event-section-title">Event List</h3>
    <div class="event-list-top-bar">
      <TextInput
        class="event-search-input"
        id="event-search"
        label="Search events..."
        v-model="searchQuery"
      />
      <InputButton disabled>Advanced Search</InputButton>
      <InputButton disabled>Filter</InputButton>
      <InputButton disabled>Bulk Edit</InputButton>
      <InputButton disabled>Bulk Delete</InputButton>
    </div>
    <div v-if="loading" class="event-list-loading">Loading events...</div>
    <div v-else-if="error" class="event-list-error">Error loading events: {{ error.message }}
    </div>
    <div class="event-table-inner-bg">
      <TableEntry :columns="columns" :rows="events">
        <template #select="{ row }">
          <input type="checkbox" :value="row.id" v-model="selectedEvents" />
        </template>
        <template #name="{ row }">
          <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'name'" @mouseleave="hoveredEvent = null; hoveredField = null">
            {{ row.name }}
            <div v-if="hoveredEvent === row.id && hoveredField === 'name'" class="popup-info">
              <strong>Name:</strong> {{ row.name }}
            </div>
          </span>
        </template>
        <template #date="{ row }">
          <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'date'" @mouseleave="hoveredEvent = null; hoveredField = null">
            {{ formatDateTime(row.date || '') }}
            <div v-if="hoveredEvent === row.id && hoveredField === 'date'" class="popup-info">
              <strong>Date:</strong> {{ formatDateTime(row.date || '') }}
            </div>
          </span>
        </template>
        <template #status="{ row }">
          <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'status'" @mouseleave="hoveredEvent = null; hoveredField = null">
            {{ row.status }}
            <div v-if="hoveredEvent === row.id && hoveredField === 'status'" class="popup-info">
              <strong>Status:</strong> {{ row.status }}
            </div>
          </span>
        </template>
        <template #rsvp="{ row }">
          <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'rsvp'" @mouseleave="hoveredEvent = null; hoveredField = null">
            {{ row.rsvp }}
            <div v-if="hoveredEvent === row.id && hoveredField === 'rsvp'" class="popup-info">
              <strong>RSVP:</strong> {{ row.rsvp }}
            </div>
          </span>
        </template>
        <template #signup_deadline="{ row }">
          <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'signup_deadline'" @mouseleave="hoveredEvent = null; hoveredField = null">
            {{ formatDateTime(row.signup_deadline || '') }}
            <div v-if="hoveredEvent === row.id && hoveredField === 'signup_deadline'" class="popup-info">
              <strong>Signup Deadline:</strong> {{ formatDateTime(row.signup_deadline || '') }}
            </div>
          </span>
        </template>
        <template #description="{ row }">
          <span class="hoverable-cell" @mouseenter="hoveredEvent = row.id; hoveredField = 'description'" @mouseleave="hoveredEvent = null; hoveredField = null">
            {{ row.description }}
            <div v-if="hoveredEvent === row.id && hoveredField === 'description'" class="popup-info">
              <strong>Description:</strong> {{ row.description }}
            </div>
          </span>
        </template>
      </TableEntry>
      <div v-if="hoveredEvent" class="event-row-details">
        <strong>Details for:</strong> {{ events.find(e => e.id === hoveredEvent)?.name }}<br>
        RSVP: {{ events.find(e => e.id === hoveredEvent)?.rsvp }}<br>
        Status: {{ events.find(e => e.id === hoveredEvent)?.status }}
        <br />Signup Deadline: {{ events.find(e => e.id === hoveredEvent)?.signup_deadline }}
        <br />Description: {{ events.find(e => e.id === hoveredEvent)?.description }}
        <br />Date: {{ formatDateTime(events.find(e => e.id === hoveredEvent)?.date || '') }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import TableEntry from "../../shared/TableEntry.vue";
import TextInput from "../../shared/TextInput.vue";
import InputButton from "../../shared/InputButton.vue";
import { ref } from "vue";
import { EventTable } from "@/composables/EventTable";


const searchQuery = ref("");
const {
  events,
  loading,
  error,
  selectedEvents,
  hoveredEvent,
  hoveredField,
  columns,
  formatDateTime,
} = EventTable();


</script>

<style scoped>
.event-table-inner-bg {
  background: var(--color-table-header-bg, #f5f5f5);
  padding: 0.5rem 0.5rem 0.5rem 0.5rem;
}
</style>
