<template>
  <div class="calendar-event-selector-box">
    <div class="calendar-header">
      <button class="calendar-arrow" @click="prevMonth" title="Previous Month">&#8592;</button>
      <div class="calendar-header-center">
        <select v-model="month" class="calendar-month-select">
          <option v-for="(m, idx) in monthNames" :key="m" :value="idx">{{ m }}</option>
        </select>
        <select v-model="selectedYear" class="calendar-year-select">
          <option v-for="y in yearRange" :key="y" :value="y">{{ y }}</option>
        </select>
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
        :class="{ 'has-event': hasEvent(day.date) }"
        @mouseenter="showTooltip(day.date, $event)"
        @mouseleave="hideTooltip"
        @click="openEventModal(day.date)"
      >
        {{ day.day }}
        <div v-if="tooltipDate === day.date && hasEvent(day.date)" class="calendar-tooltip" :style="tooltipStyle">
          <div v-for="event in getEvents(day.date)" :key="event.id">
            {{ event.title }}
          </div>
        </div>
      </div>
    </div>
  <EditEventModal v-if="modalDate" :date="modalDate" :events="getEvents(modalDate)" @close="modalDate = null" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import EditEventModal from "../admin/eventview/EditEventModal.vue"
import { EventTable } from '@/composables/EventTable'

// Use the same event fetching logic as the admin event table
const { events } = EventTable()
const today = new Date()
const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]
const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const selectedYear = ref(today.getFullYear())
const year = computed(() => selectedYear.value)
const month = ref(today.getMonth())
const daysInMonth = computed(() => {
  const days = []
  const numDays = new Date(year.value, month.value + 1, 0).getDate()
  for (let i = 1; i <= numDays; i++) {
    const date = `${year.value}-${String(month.value + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    days.push({ day: i, date })
  }
  return days
})
const firstDayOfWeek = computed(() => {
  return new Date(year.value, month.value, 1).getDay()
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
function prevMonth() {
  if (month.value === 0) {
    month.value = 11
    selectedYear.value--
  } else {
    month.value--
  }
}
function nextMonth() {
  if (month.value === 11) {
    month.value = 0
    selectedYear.value++
  } else {
    month.value++
  }
}
function changeYear() {
  // No-op, v-model already updates selectedYear
}
const tooltipDate = ref<string | null>(null)
const tooltipStyle = ref<Record<string, string>>({})
const modalDate = ref<string | null>(null)
function hasEvent(date: string) {
  // Match only the date part (YYYY-MM-DD) of event.date
  return events.value.some(e => e.date && e.date.slice(0, 10) === date)
}
function getEvents(date: string) {
  return events.value.filter(e => e.date && e.date.slice(0, 10) === date)
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
    modalDate.value = date
  }
}
</script>



