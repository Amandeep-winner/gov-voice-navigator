<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  message: string
  type: string
}>()

const bannerStyles = computed(() => {
  if (props.type === 'urgent') return 'bg-red-50 border-l-4 border-l-red-600 border-y-0 border-r-0 text-red-900'
  return 'bg-amber-50 border-l-4 border-l-gov-saffron border-y-0 border-r-0 text-amber-900'
})
</script>

<template>
  <div :class="['px-4 py-3 rounded-r-md border shadow-sm flex items-center gap-3', bannerStyles]">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <p class="font-medium text-sm">{{ message }}</p>
  </div>
</template>