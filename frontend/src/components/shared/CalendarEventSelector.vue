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
// Dummy event data for demonstration
const events = ref([
  { id: 1, date: '2025-09-16', title: 'Board Meeting' },
  { id: 2, date: '2025-09-18', title: 'Workshop' },
  { id: 3, date: '2025-09-18', title: 'Team Lunch' },
])
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
  return events.value.some(e => e.date === date)
}
function getEvents(date: string) {
  return events.value.filter(e => e.date === date)
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



<style scoped>
.calendar-event-selector-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.5rem 0.5rem 0;
  gap: 1rem;
}
.calendar-header-center {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.calendar-month-select, .calendar-year-select {
  font-size: 1.1rem;
  font-weight: bold;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 2px 8px;
  background: #fff;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.calendar-month-select:hover, .calendar-year-select:hover, .calendar-month-select:focus, .calendar-year-select:focus {
  background: #ede3d2;
  border-color: #bfa77a;
}
.calendar-arrow {
  font-size: 1.5rem;
  font-weight: bold;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  width: 2.2rem;
  height: 2.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 4px #bfa77a33;
}
.calendar-arrow:hover {
  background: #ede3d2;
  border-color: #bfa77a;
  box-shadow: 0 2px 8px #bfa77a55;
}
.calendar-grid {
  flex: 1 1 0;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 6px;
  width: 100%;
  height: 100%;
  background: none;
  border-radius: 8px;
  padding: 0.5rem 0;
}
.calendar-day-name {
  font-weight: 600;
  text-align: center;
  padding-bottom: 4px;
}
.calendar-day {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  cursor: pointer;
  transition: box-shadow 0.2s;
  height: 100%;
}
.calendar-day.blank {
  background: transparent;
  border: none;
  cursor: default;
}
.calendar-day.has-event {
  background: #ede3d2;
  border-color: #bfa77a;
  font-weight: 600;
}
.calendar-day:hover {
  box-shadow: 0 2px 8px #d6bfa7;
}
.calendar-tooltip {
  position: absolute;
  z-index: 10;
  background: #fffbe6;
  border: 1px solid #bfa77a;
  border-radius: 6px;
  padding: 8px 12px;
  top: 100%;
  left: 0;
  min-width: 120px;
  box-shadow: 0 2px 8px #d6bfa7;
  margin-top: 6px;
  font-size: 0.95rem;
}
.event-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fffbe6;
  border: 1px solid #bfa77a;
  border-radius: 10px;
  box-shadow: 0 4px 24px #bfa77a44;
  padding: 24px 32px;
  z-index: 1000;
}
</style>
