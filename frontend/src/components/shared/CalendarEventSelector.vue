<template>
  <div class="calendar-event-selector-box">
    <div class="calendar-header">
      <button class="calendar-arrow" @click="prevMonth" title="Previous Month">&#8592;</button>
  <div class="calendar-header-center">
        <Dropdown
          id="month"
          label="Month"
          v-model="month"
          :options="monthDropdownOptions"
          inputColor="#f5f5f5"
          borderColor="#616161"
          class="calendar-month-select"
        />
        <Dropdown
          id="year"
          label="Year"
          v-model="selectedYear"
          :options="yearDropdownOptions"
          inputColor="#f5f5f5"
          borderColor="#616161"
          class="calendar-year-select"
        />
      </div>
      <button class="calendar-arrow" @click="nextMonth" title="Next Month">&#8594;</button>
    </div>
    <div class="calendar-grid">
      <div class="calendar-day-name" v-for="d in dayNames" :key="d">{{ d }}</div>
      <div v-for="blank in firstDayOfWeek" :key="'b'+blank" class="calendar-day blank"></div>
      <div
        v-for="day in daysInMonth"
        :key="day.date"
        class="calendar-day"
        :class="{ 'has-event': hasEvent(day.date), 'has-multiple-events': getEvents(day.date).length > 1 }"
        @mouseenter="showTooltip(day.date, $event)"
        @mouseleave="hideTooltip"
        @click="openEventModal(day.date)"
      >
        {{ day.day }}
        <div v-if="hasEvent(day.date)" class="event-count">{{ getEvents(day.date).length }}</div>
        <div v-if="tooltipDate === day.date && hasEvent(day.date)" class="calendar-tooltip" :style="tooltipStyle">
          <div v-for="event in getEvents(day.date)" :key="event.id">
            {{ event.title }}
          </div>
        </div>
      </div>
    </div>
  <EditEventModal v-if="modalDate" :date="modalDate" :events="getEvents(modalDate)" @close="modalDate = null" @editEvent="openEditModal" />
  
  <!-- Edit Modal (same as EventTable) -->
  <Modal v-model="editModal" :hide-default-close="true">
    <div class="modal-header-row">
      <h3 class="modal-title">Edit Event</h3>
      <button class="modal-close-btn" @click="editModal = false" aria-label="Close">×</button>
    </div>
    <div class="modal-body">
      <EventCreateDuplicate :mode="'edit'" />
    </div>
  </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import EditEventModal from "../admin/eventview/EditEventModal.vue"
import Modal from "../shared/Modal.vue"
import EventCreateDuplicate from "../admin/eventview/EventCreateDuplicate.vue"
import { EventTable } from '@/composables/EventTable'
import { getDateOnly } from '@/composables/DateUtils'
import Dropdown from '../shared/Dropdown.vue'

// Use the same event fetching logic as the admin event table
const { events } = EventTable()
const today = new Date()
const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]
const monthDropdownOptions = monthNames.map((m, idx) => ({ text: m, value: idx.toString() }))
const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const selectedYear = ref(today.getFullYear().toString())
const year = computed(() => parseInt(selectedYear.value, 10))
const month = ref(today.getMonth().toString())
const daysInMonth = computed(() => {
  const days = []
  const monthNum = parseInt(month.value, 10)
  const numDays = new Date(year.value, monthNum + 1, 0).getDate()
  for (let i = 1; i <= numDays; i++) {
    const date = `${year.value}-${String(monthNum + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    days.push({ day: i, date })
  }
  return days
})
const firstDayOfWeek = computed(() => {
  const monthNum = parseInt(month.value, 10)
  return new Date(year.value, monthNum, 1).getDay()
})
const yearRange = computed(() => {
  const range = []
  const startYear = 2020
  const endYear = today.getFullYear() + 10
  for (let y = startYear; y <= endYear; y++) {
    range.push(y)
  }
  return range
})
const yearDropdownOptions = computed(() => yearRange.value.map(y => ({ text: y.toString(), value: y.toString() })))
function prevMonth() {
  let monthNum = parseInt(month.value, 10)
  let yearNum = parseInt(selectedYear.value, 10)
  if (monthNum === 0) {
    month.value = '11'
    selectedYear.value = (yearNum - 1).toString()
  } else {
    month.value = (monthNum - 1).toString()
  }
}
function nextMonth() {
  let monthNum = parseInt(month.value, 10)
  let yearNum = parseInt(selectedYear.value, 10)
  if (monthNum === 11) {
    month.value = '0'
    selectedYear.value = (yearNum + 1).toString()
  } else {
    month.value = (monthNum + 1).toString()
  }
}
// changeYear function removed as v-model updates selectedYear directly
const tooltipDate = ref<string | null>(null)
const tooltipStyle = ref<Record<string, string>>({})
const modalDate = ref<string | null>(null)
const editModal = ref(false)

function openEditModal(event: any) {
  modalDate.value = null // Close the event selection modal
  editModal.value = true // Open the edit modal
}
function hasEvent(date: string) {
  // Use DateUtils for consistent date formatting
  return events.value.some(e => e.date && getDateOnly(e.date) === date)
}
function getEvents(date: string) {
  return events.value.filter(e => e.date && getDateOnly(e.date) === date)
}
function showTooltip(date: string, evt: MouseEvent) {
  tooltipDate.value = date
  tooltipStyle.value = {
    left: evt.offsetX + 20 + 'px',
    top: evt.offsetY + 20 + 'px',
  }
}
function hideTooltip() {
  tooltipDate.value = null
}
function openEventModal(date: string) {
  if (hasEvent(date)) {
    const eventsOnDate = getEvents(date)
    if (eventsOnDate.length === 1) {
      // If only one event, open edit modal directly
      editModal.value = true
    } else {
      // If multiple events, show selection modal
      modalDate.value = date
    }
  }
}
</script>



