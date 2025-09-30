
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
        :class="{ 'row-hovered': hoveredRow && (hoveredRow.id === row.id || hoveredRow.key === row.key), 'table-row-clickable': true }"
        @click="onRowClick(row, $event)"
      >
    <td v-for="(col, colIdx) in columns" :key="col.key"
      :class="[col.key === 'select' ? 'checkbox-cell not-clickable' : '', { 'not-clickable': col.key === 'select' } ]"
      @click.stop="col.key === 'select' ? undefined : onCellClick(row, col, $event)"
    >
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
import { ref, defineEmits } from 'vue'
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

const emit = defineEmits(['row-click'])

function onRowClick(row: any, event: MouseEvent) {
  emit('row-click', row, event)
}

function onCellClick(row: any, col: any, event: MouseEvent) {
  if (col.key !== 'select') {
    emit('row-click', row, event)
  }
}
</script>
<style scoped>
.row-hovered {
  background: #f5f5f5;
}
.table-row-clickable {
  cursor: pointer;
}
.not-clickable {
  cursor: default !important;
}
.checkbox-cell {
  width: 38px;
  min-width: 38px;
  max-width: 44px;
  padding-left: 8px !important;
  padding-right: 8px !important;
  text-align: center;
}
</style>
