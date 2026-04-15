<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  message: string
  type: string
}>()

const bannerStyles = computed(() => {
  if (props.type === 'urgent') return 'bg-red-100 border-red-400 text-red-800'
  return 'bg-yellow-100 border-yellow-400 text-yellow-800'
})
</script>

<template>
  <div :class="['px-4 py-3 rounded-lg border flex items-center gap-3 shadow-sm', bannerStyles]">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <p class="font-medium text-sm">{{ message }}</p>
  </div>
</template>