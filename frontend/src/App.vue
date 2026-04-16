<script setup lang="ts">
import { ref } from 'vue'
import VoiceWidget from './components/VoiceWidget.vue'

const currentLanguage = ref('en')
const languages = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिंदी (Hindi)' },
  { code: 'ta', label: 'தமிழ் (Tamil)' },
  { code: 'te', label: 'తెలుగు (Telugu)' }
]

const changeLanguage = (e: Event) => {
  const target = e.target as HTMLSelectElement
  currentLanguage.value = target.value
  const event = new CustomEvent('language-change', { detail: currentLanguage.value })
  window.dispatchEvent(event)
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex flex-col font-sans transition-colors duration-500 text-slate-900">
    
    <!-- Premium Header with Glassmorphism -->
    <header class="sticky top-0 z-40 bg-white/70 backdrop-blur-md border-b border-white/20 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        
        <!-- Logo Area -->
        <router-link to="/" class="flex items-center gap-3 group">
          <div class="bg-indigo-600 text-white p-2 rounded-xl shadow-lg group-hover:scale-105 transition-transform duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" />
            </svg>
          </div>
          <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-700 to-purple-600 tracking-tight">
            Jan Sarthi AI
          </span>
        </router-link>

        <!-- Navigation & Actions -->
        <div class="flex items-center gap-6">
          <nav class="space-x-1 hidden md:flex items-center">
            <router-link to="/" class="px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-indigo-600 transition-colors font-medium" active-class="bg-indigo-50 text-indigo-700">Dashboard</router-link>
            <router-link to="/compare" class="px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-indigo-600 transition-colors font-medium" active-class="bg-indigo-50 text-indigo-700">Compare Settings</router-link>
            <router-link to="/forum" class="px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-indigo-600 transition-colors font-medium" active-class="bg-indigo-50 text-indigo-700">Community Forum</router-link>
            <router-link to="/admin" class="px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-indigo-600 transition-colors font-medium" active-class="bg-indigo-50 text-indigo-700">Gov Admin</router-link>
          </nav>

          <!-- Divider -->
          <div class="h-6 w-px bg-slate-200 hidden md:block"></div>

          <!-- Language Selector -->
          <div class="relative flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
            </svg>
            <select 
              @change="changeLanguage" 
              :value="currentLanguage"
              class="appearance-none bg-transparent border-none text-sm font-medium text-slate-700 focus:ring-0 cursor-pointer pr-4"
            >
              <option v-for="lang in languages" :key="lang.code" :value="lang.code">
                {{ lang.label }}
              </option>
            </select>
          </div>

          <!-- Profile / Avatar Placeholder -->
          <div class="h-9 w-9 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 p-0.5 cursor-pointer shadow-md hover:shadow-lg transition-shadow">
            <div class="h-full w-full rounded-full border-2 border-white overflow-hidden bg-white">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-full w-full text-slate-300 translate-y-1" viewBox="0 0 20 20" fill="currentColor">
                 <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
               </svg>
            </div>
          </div>
        </div>

      </div>
    </header>

    <main class="flex-grow w-full">
      <!-- Using a subtle pattern overlay on the main content area -->
      <div class="absolute inset-0 z-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjEiIGZpbGw9InJnYmEoMCwgMCwgMCwgMC4wNCkiLz48L3N2Zz4=')] opacity-50 pointer-events-none"></div>
      
      <div class="relative z-10 max-w-7xl mx-auto px-4 py-8">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <VoiceWidget />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>