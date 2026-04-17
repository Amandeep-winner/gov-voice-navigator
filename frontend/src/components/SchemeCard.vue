<script setup lang="ts">
defineProps<{
  title: string
  description: string
  matchPercentage: number
}>()
</script>

<template>
  <div class="bg-white rounded-md shadow-sm border border-slate-200 p-5 hover:shadow-md transition-shadow duration-300 flex flex-col h-full relative overflow-hidden">
    <!-- Top accent border -->
    <div class="absolute top-0 left-0 right-0 h-1 bg-gov-blue"></div>
    
    <div class="flex justify-between items-start mb-3 mt-1">
      <h4 class="text-lg font-bold text-gov-blue line-clamp-2 leading-tight">{{ title }}</h4>
      <span class="bg-gov-green text-white text-xs font-bold px-2 py-1 rounded shrink-0 ml-2">
        {{ matchPercentage }}% Match
      </span>
    </div>
    
    <p class="text-slate-700 text-sm mb-6 flex-grow line-clamp-3">
      {{ description }}
    </p>
    
    <div class="mt-auto pt-4 border-t border-slate-200 flex justify-between items-center">
      <button class="text-gov-blue font-semibold text-sm hover:underline">Read Details</button>
      <button class="bg-gov-blue text-white px-4 py-1.5 rounded text-sm font-medium hover:bg-blue-900 transition-colors">Compare</button>
    </div>
  </div>
</template>