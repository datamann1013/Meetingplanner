<template>
  <div :class="['dashboard-box', variantClass]" :style="{ flex: flexValue }">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ variant?: string, flex?: number }>()
const variantClass = computed(() => {
  return props.variant ? `dashboard-box--${props.variant.replace(/\s+/g, '-')}` : ''
})
const flexValue = computed(() => props.flex ?? 1)
</script>

<style scoped>
.dashboard-box {
  background: #f5eee6;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: box-shadow 0.2s;
}
.dashboard-box--primary {
  background: #ede3d2;
  color: #4b3f2a;
}
.dashboard-box--secondary {
  background: #f3e9db;
  color: #4b3f2a;
}
.dashboard-box--accent {
  background: #e9e3d6;
  color: #4b3f2a;
}
.dashboard-box--long {
  min-height: 120px;
  background: #e3dac9;
  color: #4b3f2a;
}
</style>
