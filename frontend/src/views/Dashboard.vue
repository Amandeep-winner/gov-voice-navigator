<script setup lang="ts">
import { ref } from 'vue'
import SchemeCard from '../components/SchemeCard.vue'
import NotificationBanner from '../components/NotificationBanner.vue'

// Mock Data for Hackathon UI
const notifications = ref([
  { id: 1, message: 'Your Driving License expires in 15 days. Tap the mic to learn how to renew it.', type: 'urgent' }
])

const recommendedSchemes = ref([
  { id: 1, title: 'PM Kisan Samman Nidhi', description: 'Income support of ₹6000/year for landholding farmer families. Requires Aadhaar and bank details.', match: 95 },
  { id: 2, title: 'Startup India Seed Fund', description: 'Financial assistance to startups for proof of concept, prototype development, and product trials.', match: 88 },
  { id: 3, title: 'Ayushman Bharat Yojana', description: 'Health insurance coverage up to ₹5 Lakhs per family per year for secondary and tertiary care hospitalization.', match: 76 }
])
</script>

<template>
  <div class="space-y-8 pb-20">
    
    <section>
      <h2 class="text-3xl font-bold text-gray-800 mb-2">Welcome back, User</h2>
      <p class="text-gray-600 mb-6">Here is your personalized government services overview.</p>
      
      <div class="space-y-3">
        <NotificationBanner 
          v-for="note in notifications" 
          :key="note.id" 
          :message="note.message" 
          :type="note.type" 
        />
      </div>
    </section>

    <section>
      <div class="flex justify-between items-end mb-4">
        <h3 class="text-2xl font-semibold text-gray-800">Recommended Schemes</h3>
        <button class="text-blue-600 hover:text-blue-800 font-medium text-sm">View All</button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SchemeCard 
          v-for="scheme in recommendedSchemes" 
          :key="scheme.id"
          :title="scheme.title"
          :description="scheme.description"
          :matchPercentage="scheme.match"
        />
      </div>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
      <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start gap-4 cursor-pointer hover:shadow-md transition">
        <div class="bg-green-100 p-3 rounded-lg text-green-600">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" /></svg>
        </div>
        <div>
          <h4 class="text-lg font-bold text-gray-800">Community Forum</h4>
          <p class="text-gray-500 text-sm mt-1">Read reviews and ask questions about scheme applications.</p>
        </div>
      </div>

      <div class="bg-red-50 p-6 rounded-xl border border-red-100 shadow-sm flex items-start gap-4 cursor-pointer hover:shadow-md transition">
        <div class="bg-red-100 p-3 rounded-lg text-red-600">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
        </div>
        <div>
          <h4 class="text-lg font-bold text-red-800">Legal Emergency</h4>
          <p class="text-red-600 text-sm mt-1">Tap the mic and say "I need legal help" to instantly know your rights.</p>
        </div>
      </div>
    </section>
  </div>
</template>