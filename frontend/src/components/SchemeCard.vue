<script setup lang="ts">
defineProps<{
  title: string
  description: string
  matchPercentage: number
}>()
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-lg transition-shadow duration-300 flex flex-col h-full">
    <div class="flex justify-between items-start mb-3">
      <h4 class="text-lg font-bold text-gray-800 line-clamp-2 leading-tight">{{ title }}</h4>
      <span class="bg-green-100 text-green-800 text-xs font-bold px-2.5 py-1 rounded-full shrink-0 ml-2">
        {{ matchPercentage }}% Match
      </span>
    </div>
    
    <p class="text-gray-600 text-sm mb-6 flex-grow line-clamp-3">
      {{ description }}
    </p>
    
    <div class="mt-auto pt-4 border-t border-gray-100 flex justify-between items-center">
      <button class="text-blue-600 font-semibold text-sm hover:underline">Read Details</button>
      <button class="bg-blue-50 text-blue-700 px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-blue-100 transition">Compare</button>
    </div>
  </div>
</template>