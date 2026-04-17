<script setup lang="ts">
import { ref } from 'vue'

const applications = ref([
  {
    id: 'APP-8842-AX',
    title: 'Ayushman Bharat Yojana',
    date: '10 Apr 2026',
    status: 'Rejected',
    rejectionReason: 'Income proof document uploaded is blurry and missing the sub-divisional magistrate signature.',
    resolutionSteps: [
      'Obtain a fresh, digitally signed Income Certificate from your state portal or e-Mitra.',
      'Ensure the document clearly displays the SDM seal and your family members\' names.',
      'Re-upload the document using the "Update Application" button below.'
    ],
    helpline: '14555 (National Health Authority)'
  },
  {
    id: 'APP-9921-BZ',
    title: 'PM Kisan Samman Nidhi',
    date: '02 Apr 2026',
    status: 'Approved',
    rejectionReason: '',
    resolutionSteps: [],
    helpline: ''
  }
])

const documentServices = ref([
  {
    title: 'Remake Lost Aadhaar Card',
    description: 'Order a PVC replacement card directly to your registered address.',
    icon: 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z',
    color: 'blue'
  },
  {
    title: 'Update Mobile Number in Aadhaar',
    description: 'Book an appointment at the nearest ASK to update your biometrics or phone number.',
    icon: 'M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z',
    color: 'emerald'
  },
  {
    title: 'Renew Driving License',
    description: 'Apply for renewal online if your license expired within the last year.',
    icon: 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4',
    color: 'amber'
  }
])
</script>

<template>
  <div class="max-w-6xl mx-auto space-y-12 animate-fade-in-up pb-20">
    
    <!-- Header -->
    <div class="border-b border-slate-200 pb-4">
      <h2 class="text-3xl font-bold text-gov-blue tracking-tight">My Applications & Services</h2>
      <p class="text-slate-700 mt-2 text-lg font-medium">Track your scheme applications, resolve rejections, and request document updates.</p>
    </div>

    <!-- Application Tracker Section -->
    <section>
      <h3 class="text-2xl font-bold text-gov-blue mb-6 flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gov-saffron" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        Application Status
      </h3>

      <div class="space-y-6">
        <div v-for="app in applications" :key="app.id" class="bg-white rounded-md p-6 shadow-sm border border-slate-300 hover:shadow-md transition-shadow relative overflow-hidden">
          <div class="absolute top-0 left-0 bottom-0 w-1 bg-gov-blue"></div>
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4 mb-4 pl-3">
            <div>
              <div class="flex items-center gap-3 mb-1">
                <span class="text-xs font-mono font-bold text-slate-500 bg-slate-100 px-2 py-1 rounded border border-slate-200">{{ app.id }}</span>
                <span class="text-sm text-slate-600 font-bold">Applied: {{ app.date }}</span>
              </div>
              <h4 class="text-xl font-bold text-gov-blue">{{ app.title }}</h4>
            </div>
            
            <div>
              <span v-if="app.status === 'Approved'" class="bg-green-50 text-gov-green border border-green-200 px-4 py-2 rounded font-bold text-sm flex items-center gap-2 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                Approved
              </span>
              <span v-if="app.status === 'Rejected'" class="bg-red-50 text-red-700 border border-red-200 px-4 py-2 rounded font-bold text-sm flex items-center gap-2 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                Action Required (Rejected)
              </span>
            </div>
          </div>

          <!-- Rejection Helper -->
          <div v-if="app.status === 'Rejected'" class="bg-red-50 rounded p-6 border border-red-200 relative overflow-hidden ml-3 shadow-sm">
            <div class="absolute top-0 right-0 p-4 opacity-5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-32 w-32 text-red-700" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            </div>
            
            <div class="relative z-10">
              <h5 class="text-red-900 font-bold mb-2 text-lg">Reason for Rejection</h5>
              <p class="text-red-800 mb-6 bg-white p-3 rounded border border-red-200 font-medium shadow-sm">{{ app.rejectionReason }}</p>

              <h5 class="text-gov-green font-bold mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                How to Resolve This
              </h5>
              
              <ul class="space-y-3 mb-6">
                <li v-for="(step, i) in app.resolutionSteps" :key="i" class="flex items-start gap-3 text-slate-800 bg-white p-3 rounded shadow-sm border border-slate-200 font-medium">
                  <span class="bg-gov-blue text-white h-6 w-6 rounded flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">{{ i + 1 }}</span>
                  {{ step }}
                </li>
              </ul>

              <div class="flex flex-wrap items-center gap-4">
                <button class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded shadow transition-colors flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                  Update Application
                </button>
                <div class="bg-white border border-slate-300 px-4 py-2 rounded text-sm font-bold text-slate-700 flex items-center gap-2 shadow-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gov-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
                  Helpline: <span class="font-mono text-gov-blue">{{ app.helpline }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Document Services Section -->
    <section>
      <div class="flex items-end justify-between mb-6">
        <h3 class="text-2xl font-bold text-gov-blue flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gov-green" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 21h7a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v11m0 5l4-8 4 8m-4-8v8" />
          </svg>
          Document Updates & Renewals
        </h3>
        <button class="text-gov-blue hover:underline text-sm font-bold">View Directory</button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="srv in documentServices" :key="srv.title" class="bg-white border border-slate-300 p-6 rounded shadow-sm hover:shadow-md transition-shadow cursor-pointer group relative overflow-hidden">
          <div class="absolute top-0 left-0 bottom-0 w-1 bg-gov-saffron"></div>
          <div class="bg-gov-light-blue text-gov-blue w-12 h-12 rounded flex items-center justify-center mb-5 border border-gov-blue/20">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="srv.icon" />
            </svg>
          </div>
          <h4 class="text-lg font-bold text-gov-blue mb-2 pl-2">{{ srv.title }}</h4>
          <p class="text-slate-700 text-sm mb-6 pl-2 font-medium">{{ srv.description }}</p>
          <div class="flex items-center gap-2 text-gov-saffron font-bold text-sm pl-2">
            Apply Now
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>
