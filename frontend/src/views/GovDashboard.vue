<script setup lang="ts">
import { ref } from 'vue'

const schemeForm = ref({
  title: '',
  description: '',
  category: 'agriculture',
  benefitAmount: '',
  eligibility: '',
})

const isSubmitting = ref(false)
const successMessage = ref('')

const handleUpload = () => {
  isSubmitting.value = true
  // Mock API call to Qdrant/SQLite backend
  setTimeout(() => {
    isSubmitting.value = false
    successMessage.value = 'Scheme successfully vectorized and uploaded to knowledge base!'
    
    setTimeout(() => {
      successMessage.value = ''
      schemeForm.value = {
        title: '',
        description: '',
        category: 'agriculture',
        benefitAmount: '',
        eligibility: '',
      }
    }, 3000)
  }, 1500)
}
</script>

<template>
  <div class="max-w-3xl mx-auto animate-fade-in-up">
    
    <div class="mb-8">
      <div class="flex items-center gap-3 mb-2">
        <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">Admin Portal</span>
      </div>
      <h2 class="text-4xl font-extrabold text-slate-800 tracking-tight">Upload Scheme</h2>
      <p class="text-slate-500 mt-2 text-lg">Digitize and add new government schemes to the global vector store. Voice AI will immediately learn about this document.</p>
    </div>

    <!-- Success Feedback -->
    <transition name="fade">
      <div v-if="successMessage" class="bg-emerald-50 border border-emerald-200 text-emerald-800 px-4 py-3 rounded-xl mb-6 flex items-center gap-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span class="font-medium">{{ successMessage }}</span>
      </div>
    </transition>

    <div class="bg-white rounded-3xl shadow-xl border border-slate-100 p-8 relative overflow-hidden">
      <!-- Background pattern -->
      <div class="absolute top-0 right-0 p-12 -mt-10 -mr-10 bg-indigo-50 rounded-full opacity-50 pointer-events-none"></div>

      <form @submit.prevent="handleUpload" class="space-y-6 relative z-10">
        
        <div class="space-y-2">
          <label class="block text-sm font-bold text-slate-700">Scheme Title</label>
          <input 
            v-model="schemeForm.title" 
            type="text" 
            required
            class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none transition-shadow"
            placeholder="e.g., National Startup Grant"
          >
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="block text-sm font-bold text-slate-700">Category</label>
            <select 
              v-model="schemeForm.category"
              class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none transition-shadow appearance-none cursor-pointer"
            >
              <option value="agriculture">Agriculture & Farmers</option>
              <option value="health">Healthcare & Insurance</option>
              <option value="education">Education & Students</option>
              <option value="business">Business & Startups</option>
            </select>
          </div>
          
          <div class="space-y-2">
            <label class="block text-sm font-bold text-slate-700">Benefit Description (Amount/Type)</label>
            <input 
              v-model="schemeForm.benefitAmount" 
              type="text" 
              required
              class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none transition-shadow"
              placeholder="e.g., ₹50,000 Subsidy"
            >
          </div>
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-bold text-slate-700">Detailed Description (For AI Vector Store)</label>
          <textarea 
            v-model="schemeForm.description" 
            required
            rows="4"
            class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none transition-shadow resize-none"
            placeholder="Provide full details. The AI agent will use this text to answer citizen inquiries..."
          ></textarea>
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-bold text-slate-700">Eligibility Criteria</label>
          <input 
            v-model="schemeForm.eligibility" 
            type="text" 
            required
            class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none transition-shadow"
            placeholder="e.g., Age 18-35, Income < 5 Lakhs"
          >
        </div>

        <!-- File Upload Area Placeholder -->
        <div class="border-2 border-dashed border-slate-300 rounded-2xl p-8 text-center hover:bg-slate-50 transition-colors cursor-pointer cursor-not-allowed opacity-70">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mx-auto text-slate-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
          <p class="text-sm font-medium text-slate-600">Drag & Drop official gazette PDF here</p>
          <p class="text-xs text-slate-400 mt-1">(Optical Character Recognition Auto-fills form)</p>
        </div>

        <button 
          type="submit" 
          :disabled="isSubmitting"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-6 rounded-xl shadow-lg hover:shadow-indigo-500/30 transition-all flex items-center justify-center gap-2 mt-8 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isSubmitting ? 'Vectorizing Document...' : 'Publish to Knowledge Base' }}
        </button>

      </form>
    </div>
  </div>
</template>
