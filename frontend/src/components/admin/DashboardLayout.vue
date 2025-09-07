    <template>
      <div class="dashboard-layout">
        <header class="dashboard-header">
          <h2>{{ title }}</h2>
        </header>
        <div class="dashboard-content">
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

    <script setup lang="ts">
    import DashboardBox from './DashboardBox.vue'
    import EventActionsBox from './EventActionsBox.vue'
    import EventCalendarBox from './EventCalendarBox.vue'
    type BoxConfig = { size: string, label?: string, flex?: number, content?: any }
    const props = defineProps<{ title?: string, layoutConfig: Array<Array<BoxConfig>> }>()
    </script>

    <style scoped>
    .dashboard-layout {
      padding: 0;
      background: transparent;
      border-radius: 0;
      box-shadow: none;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .dashboard-header {
      border-bottom: none;
      padding-bottom: 0.75rem;
      margin-bottom: 1rem;
    }
    .dashboard-header h2 {
      margin: 0;
      font-size: 2rem;
      font-weight: 600;
      color: var(--v-theme-primary);
    }
    .dashboard-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .dashboard-row {
      display: flex;
      gap: 1rem;
    }
</style>

