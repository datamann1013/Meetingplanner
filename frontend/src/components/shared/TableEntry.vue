
<template>
  <table class="table-entry">
    <thead>
      <tr>
        <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="row in rows"
        :key="row.id || row.key"
        @mouseenter="setHoveredRow(row)"
        @mouseleave="clearHoveredRow"
        :class="{ 'row-hovered': hoveredRow && (hoveredRow.id === row.id || hoveredRow.key === row.key) }"
      >
        <td v-for="col in columns" :key="col.key">
          <slot :name="col.key" :row="row" :hoveredRow="hoveredRow">
            {{ row[col.key] }}
          </slot>
        </td>
      </tr>
    </tbody>
  </table>
  <slot name="after-rows" :hoveredRow="hoveredRow"></slot>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { TableEntry as useTableEntry } from '@/composables/TableEntry'

interface TableEntryColumn {
  key: string
  label: string
}

interface TableEntryProps {
  columns: TableEntryColumn[]
  rows: Array<Record<string, any>>
}

const props = defineProps<TableEntryProps>()
const refValue = ref(props.rows)
useTableEntry(props.rows, refValue)

const hoveredRow = ref<any | null>(null)
function setHoveredRow(row: any) {
  hoveredRow.value = row
}
function clearHoveredRow() {
  hoveredRow.value = null
}
</script>
<style scoped>
.row-hovered {
  background: #f5f5f5;
}
</style>
