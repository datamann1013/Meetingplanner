<template>
  <div class="rsvp-admin-view">
    <DashboardBox variant="long">
      <RsvpEventsTable />
    </DashboardBox>
  </div>
</template>

<script setup lang="ts">
import RsvpEventsTable from '@/components/admin/rsvp/RsvpEventsTable.vue'
import DashboardBox from '@/components/admin/DashboardBox.vue'
</script>

<style scoped>
.rsvp-admin-view {
  padding: 16px;
}
</style>
