<script setup lang="ts">
import { ref } from 'vue'

const profile = ref({
  age: '',
  income: '',
  occupation: '',
  category: 'General'
})

const isMatching = ref(false)
const showResults = ref(false)

const matchedSchemes = ref([
  {
    id: 1,
    title: 'PM Kisan Samman Nidhi',
    type: 'Central Scheme',
    description: 'Income support of ₹6000/year for landholding farmer families.',
    benefits: ['₹6000 directly transferred to bank account annually', 'Financial stability for crop procurement'],
    documentsRequired: ['Aadhaar Card', 'Bank Account details', 'Land holding documents'],
    officeToVisit: 'Common Service Centre (CSC)'
  },
  {
    id: 2,
    title: 'Stand Up India Scheme',
    type: 'Central Scheme',
    description: 'Facilitates bank loans between 10 lakh and 1 Crore to at least one SC/ST borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.',
    benefits: ['Bank loans from 10 Lakhs to 1 Crore', 'Credit guarantee cover'],
    documentsRequired: ['Aadhaar Card', 'PAN Card', 'Caste Certificate (if applicable)', 'Project Report'],
    officeToVisit: 'Nearest Scheduled Commercial Bank'
  }
])

const findSchemes = () => {
  isMatching.value = true
  showResults.value = false
  
  // Simulate AI matching delay
  setTimeout(() => {
    isMatching.value = false
    showResults.value = true
  }, 1500)
}
</script>

<template>
  <div class="max-w-6xl mx-auto space-y-8 animate-fade-in-up">
    
    <div class="text-center max-w-2xl mx-auto mb-12">
      <h2 class="text-4xl font-extrabold text-slate-800 tracking-tight">Discover Your Schemes</h2>
      <p class="text-slate-500 mt-4 text-lg">Tell us a bit about yourself, and our AI will instantly match you with government schemes and scholarships you are eligible for.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Profile Form -->
      <div class="lg:col-span-1 bg-white p-6 rounded-md shadow-sm border border-slate-200 h-fit sticky top-24">
        <h3 class="text-xl font-bold text-gov-blue mb-6 flex items-center gap-2 border-b border-slate-200 pb-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gov-saffron" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Your Profile
        </h3>
        
        <form @submit.prevent="findSchemes" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">Age</label>
            <input v-model="profile.age" type="number" required placeholder="e.g. 25" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue focus:border-gov-blue outline-none transition-all">
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">Annual Income (₹)</label>
            <input v-model="profile.income" type="number" required placeholder="e.g. 300000" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue focus:border-gov-blue outline-none transition-all">
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">Occupation</label>
            <select v-model="profile.occupation" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue focus:border-gov-blue outline-none transition-all">
              <option value="">Select Occupation</option>
              <option value="student">Student</option>
              <option value="farmer">Farmer</option>
              <option value="business">Businessman / Entrepreneur</option>
              <option value="salaried">Salaried Employee</option>
              <option value="unemployed">Unemployed</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">Social Category</label>
            <select v-model="profile.category" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue focus:border-gov-blue outline-none transition-all">
              <option>General</option>
              <option>OBC</option>
              <option>SC/ST</option>
              <option>EWS</option>
            </select>
          </div>

          <button type="submit" :disabled="isMatching" class="w-full mt-4 bg-gov-blue hover:bg-blue-900 text-white font-bold py-3 px-6 rounded shadow transition-all flex justify-center items-center gap-2">
            <span v-if="!isMatching">Find Schemes</span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Matching...
            </span>
          </button>
        </form>
      </div>

      <!-- Results Area -->
      <div class="lg:col-span-2">
        
        <div v-if="!showResults && !isMatching" class="h-full flex flex-col items-center justify-center text-slate-500 bg-white rounded-md border border-slate-300 p-12">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <p class="text-xl font-medium">Fill your profile to see matched schemes</p>
        </div>

        <div v-if="isMatching" class="space-y-6">
          <div class="bg-white p-6 rounded-md border border-slate-300 shadow-sm animate-pulse">
            <div class="h-6 bg-slate-200 rounded w-1/3 mb-4"></div>
            <div class="h-4 bg-slate-200 rounded w-full mb-2"></div>
            <div class="h-4 bg-slate-200 rounded w-5/6"></div>
          </div>
          <div class="bg-white p-6 rounded-md border border-slate-300 shadow-sm animate-pulse">
            <div class="h-6 bg-slate-200 rounded w-1/4 mb-4"></div>
            <div class="h-4 bg-slate-200 rounded w-full mb-2"></div>
            <div class="h-4 bg-slate-200 rounded w-4/6"></div>
          </div>
        </div>

        <div v-if="showResults" class="space-y-6">
          <div class="flex items-center justify-between mb-2 border-b border-slate-200 pb-3">
            <h3 class="text-2xl font-bold text-gov-blue">Perfect Matches ({{ matchedSchemes.length }})</h3>
            <span class="text-sm text-white font-bold bg-gov-green px-3 py-1 rounded">System Verified</span>
          </div>

          <div v-for="scheme in matchedSchemes" :key="scheme.id" class="bg-white p-6 rounded-md shadow-sm border border-slate-300 hover:shadow-md transition-shadow relative overflow-hidden">
            <div class="absolute top-0 left-0 bottom-0 w-1 bg-gov-saffron"></div>
            <div class="absolute top-0 right-0 bg-gov-blue text-white text-xs font-bold px-3 py-1 rounded-bl-md">
              {{ scheme.type }}
            </div>
            
            <h4 class="text-xl font-bold text-gov-blue mb-2 pr-24 pl-3">{{ scheme.title }}</h4>
            <p class="text-slate-700 mb-6 pl-3">{{ scheme.description }}</p>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pl-3">
              <div>
                <strong class="text-gov-blue flex items-center gap-2 mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gov-green" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  Benefits
                </strong>
                <ul class="space-y-2">
                  <li v-for="(benefit, i) in scheme.benefits" :key="i" class="text-sm text-slate-700 flex items-start gap-2">
                    <span class="h-1.5 w-1.5 bg-gov-green rounded-full mt-1.5 shrink-0"></span>
                    {{ benefit }}
                  </li>
                </ul>
              </div>

              <div>
                <strong class="text-gov-blue flex items-center gap-2 mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gov-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                  Required Documents
                </strong>
                <ul class="space-y-2">
                  <li v-for="(doc, i) in scheme.documentsRequired" :key="i" class="text-sm text-slate-700 flex items-start gap-2">
                    <span class="h-1.5 w-1.5 bg-gov-blue rounded-full mt-1.5 shrink-0"></span>
                    {{ doc }}
                  </li>
                </ul>
              </div>
            </div>

            <div class="mt-6 pt-4 border-t border-slate-200 flex items-center justify-between pl-3">
              <div class="flex items-center gap-2 text-sm text-slate-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>
                Apply at: <strong class="text-slate-900">{{ scheme.officeToVisit }}</strong>
              </div>
              <button class="bg-gov-saffron hover:bg-gov-hover text-white px-5 py-2 rounded text-sm font-bold transition-colors shadow-sm">Apply Now</button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>
