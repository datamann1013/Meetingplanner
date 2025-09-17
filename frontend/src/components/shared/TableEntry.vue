<template>
  <table class="table-entry">
    <thead>
      <tr>
        <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in rows" :key="row.id || row.key">
        <td v-for="col in columns" :key="col.key">
          <slot :name="col.key" :row="row">
            {{ row[col.key] }}
          </slot>
        </td>
      </tr>
    </tbody>
  </table>
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
</script>
