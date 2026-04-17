<script setup lang="ts">
import { ref } from 'vue'

const schemesToCompare = ref([
  {
    id: 1,
    title: 'PM Kisan Samman Nidhi',
    benefitAmount: '₹6000/year',
    eligibility: 'Landholding Farmers',
    documents: ['Aadhaar', 'Bank Account', 'Land Records'],
    processingTime: '15-30 Days',
    color: 'emerald'
  },
  {
    id: 2,
    title: 'State Crop Relief Scheme',
    benefitAmount: '₹4000/year',
    eligibility: 'Small/Marginal Farmers',
    documents: ['Aadhaar', 'Income Certificate', 'Land Records'],
    processingTime: '30-45 Days',
    color: 'blue'
  }
])
</script>

<template>
  <div class="space-y-8 animate-fade-in-up">
    <div class="border-b border-slate-200 pb-4">
      <h2 class="text-3xl font-bold text-gov-blue tracking-tight">Compare Schemes</h2>
      <p class="text-slate-700 mt-2 text-lg font-medium">Side-by-side analysis of benefits, eligibility, and requirements to help you choose the best option.</p>
    </div>

    <!-- Comparison Table/Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 relative">
      
      <!-- VS Badge -->
      <div class="hidden md:flex absolute inset-y-0 left-1/2 -ml-5 items-center justify-center z-10 pointer-events-none">
        <div class="bg-gov-saffron text-white rounded-full h-10 w-10 flex items-center justify-center font-bold shadow-md border-4 border-white">
          VS
        </div>
      </div>

      <div v-for="scheme in schemesToCompare" :key="scheme.id" class="bg-white border border-slate-300 p-8 rounded-md shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
        <!-- Top accent line -->
        <div class="absolute top-0 left-0 right-0 h-1 bg-gov-blue"></div>
        
        <div class="flex items-center gap-4 mb-6">
          <div class="bg-gov-light-blue text-gov-blue p-3 rounded shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gov-blue">{{ scheme.title }}</h3>
        </div>

        <div class="space-y-6">
          <div>
            <span class="text-sm text-slate-500 uppercase tracking-wider font-bold">Benefit</span>
            <p class="text-3xl font-extrabold text-gov-green mt-1">{{ scheme.benefitAmount }}</p>
          </div>

          <div class="divider h-px w-full bg-slate-100"></div>

          <div>
            <span class="text-sm text-slate-500 uppercase tracking-wider font-bold flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              Eligibility
            </span>
            <p class="text-lg text-slate-800 font-medium mt-1">{{ scheme.eligibility }}</p>
          </div>

          <div class="divider h-px w-full bg-slate-200"></div>

          <div>
            <span class="text-sm text-slate-500 uppercase tracking-wider font-bold flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              Required Documents
            </span>
            <ul class="mt-3 space-y-2">
              <li v-for="doc in scheme.documents" :key="doc" class="flex items-center gap-3 text-slate-800 bg-slate-50 p-2 border border-slate-200 rounded">
                <svg class="h-5 w-5 text-gov-green flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                <span class="font-medium">{{ doc }}</span>
              </li>
            </ul>
          </div>

          <div class="divider h-px w-full bg-slate-200"></div>

          <div>
            <span class="text-sm text-slate-500 uppercase tracking-wider font-bold flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              Processing Time
            </span>
            <p class="text-lg text-slate-800 font-medium mt-1">{{ scheme.processingTime }}</p>
          </div>
        </div>

        <button class="mt-8 w-full bg-gov-blue hover:bg-blue-900 text-white font-bold py-3 px-6 rounded shadow hover:shadow-md transition-colors flex items-center justify-center gap-2">
          Apply for this Scheme
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
        </button>
      </div>
    </div>
  </div>
</template>
