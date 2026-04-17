<script setup lang="ts">
import { ref } from 'vue'

const user = ref({
  fullName: 'Priya Sharma',
  dob: '1995-08-15',
  email: 'priya.sharma@example.com',
  phone: '+91 98765 43210',
  aadhaar: 'XXXX-XXXX-1234',
  address: 'Block A, Vasant Kunj, New Delhi, 110070',
  gender: 'Female'
})

const isEditing = ref(false)
const showSuccessMsg = ref(false)

const saveProfile = () => {
  // Simulate saving
  isEditing.value = false
  showSuccessMsg.value = true
  setTimeout(() => {
    showSuccessMsg.value = false
  }, 3000)
}
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-6 animate-fade-in-up">
    
    <!-- Header -->
    <div class="bg-white p-6 rounded-md shadow-sm border border-slate-200 flex justify-between items-center border-t-4 border-t-gov-blue">
      <div>
        <h2 class="text-3xl font-extrabold text-gov-blue tracking-tight">User Profile</h2>
        <p class="text-slate-500 mt-1 font-medium">Manage your personal information and preferences.</p>
      </div>
      <div class="h-20 w-20 rounded-full bg-slate-200 border-2 border-gov-saffron flex items-center justify-center overflow-hidden shadow-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-slate-500 mt-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="showSuccessMsg" class="bg-green-50 border-l-4 border-gov-green p-4 rounded-md shadow-sm flex items-center gap-3">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gov-green" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
      <p class="text-green-800 font-bold">Profile updated successfully!</p>
    </div>

    <!-- Profile Form -->
    <div class="bg-white p-6 rounded-md shadow-sm border border-slate-200">
      <div class="flex justify-between items-center mb-6 border-b border-slate-200 pb-3">
        <h3 class="text-xl font-bold text-slate-800 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gov-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
          </svg>
          Personal Details
        </h3>
        <button v-if="!isEditing" @click="isEditing = true" class="bg-gov-light-blue text-gov-blue hover:bg-slate-200 px-4 py-2 rounded text-sm font-bold transition-colors border border-gov-blue/20">
          Edit Profile
        </button>
      </div>

      <form @submit.prevent="saveProfile" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1">Full Name</label>
          <input v-model="user.fullName" :disabled="!isEditing" type="text" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue outline-none transition-colors disabled:opacity-70 disabled:bg-slate-100">
        </div>

        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1">Date of Birth</label>
          <input v-model="user.dob" :disabled="!isEditing" type="date" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue outline-none transition-colors disabled:opacity-70 disabled:bg-slate-100">
        </div>

        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1">Gender</label>
          <select v-model="user.gender" :disabled="!isEditing" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue outline-none transition-colors disabled:opacity-70 disabled:bg-slate-100">
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1">Email Address</label>
          <input v-model="user.email" :disabled="!isEditing" type="email" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue outline-none transition-colors disabled:opacity-70 disabled:bg-slate-100">
        </div>

        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1">Mobile Number</label>
          <input v-model="user.phone" :disabled="!isEditing" type="tel" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue outline-none transition-colors disabled:opacity-70 disabled:bg-slate-100">
        </div>

        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1">Aadhaar Number (Masked)</label>
          <input v-model="user.aadhaar" disabled type="text" class="w-full bg-slate-100 border border-slate-300 rounded px-4 py-2 outline-none opacity-70 cursor-not-allowed">
          <p class="text-xs text-slate-500 mt-1">Aadhaar cannot be changed online.</p>
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm font-bold text-slate-700 mb-1">Residential Address</label>
          <textarea v-model="user.address" :disabled="!isEditing" rows="3" class="w-full bg-slate-50 border border-slate-300 rounded px-4 py-2 focus:ring-1 focus:ring-gov-blue outline-none transition-colors disabled:opacity-70 disabled:bg-slate-100"></textarea>
        </div>

        <div v-if="isEditing" class="md:col-span-2 flex justify-end gap-3 mt-4 border-t border-slate-200 pt-6">
          <button type="button" @click="isEditing = false" class="px-5 py-2 rounded font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 transition-colors border border-slate-300">
            Cancel
          </button>
          <button type="submit" class="bg-gov-blue hover:bg-blue-900 text-white px-6 py-2 rounded font-bold shadow-sm transition-colors border border-transparent">
            Save Changes
          </button>
        </div>

      </form>
    </div>

  </div>
</template>
