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
import { defineProps } from 'vue'

defineProps<{
  columns: Array<{ key: string, label: string }>
  rows: Array<Record<string, any>>
}>()
</script>

<style scoped>
.table-entry {
  width: 100%;
  border-collapse: collapse;
}
.table-entry th, .table-entry td {
  border: 1px solid #e0e0e0;
  padding: 0.5rem 1rem;
  text-align: left;
}
.table-entry th {
  background: #f5f5f5;
}
</style>
