
<template>
  <div class="dashboard-layout">
    <header class="dashboard-header">
      <h2>{{ title }}</h2>
    </header>
    <div class="dashboard-content-scrollable">
      <div v-for="(row, rowIdx) in layoutConfig" :key="rowIdx" class="dashboard-row">
        <DashboardBox
          v-for="(box, boxIdx) in row"
          :key="boxIdx"
          :variant="box.size"
          :flex="box.flex"
        >
          <template v-if="box.content">
            <component :is="box.content" />
          </template>
          <template v-else>
            <h3>{{ box.label || `Row ${rowIdx + 1} Box ${boxIdx + 1}` }}</h3>
          </template>
        </DashboardBox>
      </div>
    </div>
  </div>
</template>



<style scoped>
.dashboard-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.dashboard-header {
  flex-shrink: 0;
  background: #fff;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0,0,0,0.03);
  padding: 1rem 2rem 0.5rem 2rem;
}
.dashboard-content-scrollable {
  flex: 1;
  min-height: 0;
  padding: 24px;
  background: #fafbfc;
  box-sizing: border-box;
}
.dashboard-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
</style>


<script setup lang="ts">
import DashboardBox from './DashboardBox.vue'
type BoxConfig = { size: string, label?: string, flex?: number, content?: any }
const props = defineProps<{ title?: string, layoutConfig: Array<Array<BoxConfig>> }>()
</script>

