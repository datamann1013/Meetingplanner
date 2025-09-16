<template>
  <div class="calendar-event-selector-box">
    <div class="calendar-selector">
      <div class="calendar-grid">
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
      <EventModal v-if="modalDate" :date="modalDate" :events="getEvents(modalDate)" @close="modalDate = null" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
// Dummy event data for demonstration
const events = ref([
  { id: 1, date: '2025-09-16', title: 'Board Meeting' },
  { id: 2, date: '2025-09-18', title: 'Workshop' },
  { id: 3, date: '2025-09-18', title: 'Team Lunch' },
])
const today = new Date()
const year = today.getFullYear()
const month = today.getMonth()
const daysInMonth = computed(() => {
  const days = []
  const numDays = new Date(year, month + 1, 0).getDate()
  for (let i = 1; i <= numDays; i++) {
    const date = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    days.push({ day: i, date })
  }
  return days
})
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

<!-- Dummy EventModal for demonstration -->
<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'EventModal',
  props: ['date', 'events'],
  emits: ['close'],
  template: `<div class='event-modal'><button @click="$emit('close')">Close</button><div v-for='event in events' :key='event.id'>{{ event.title }}</div></div>`
})
</script>

<style scoped>
.calendar-event-selector-box {
  min-height: 400px;
}
.calendar-selector {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 6px;
  background: #f5eee6;
  border-radius: 8px;
  padding: 12px;
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
