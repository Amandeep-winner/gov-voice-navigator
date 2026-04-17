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

const isSidebarOpen = ref(false)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebar = () => {
  isSidebarOpen.value = false
}
</script>

<template>
  <div class="min-h-screen bg-gov-light-blue flex flex-col font-sans transition-colors duration-500 text-slate-900">
    
    <!-- Top Bar (Government Standard) -->
    <div class="bg-gov-blue text-white py-1">
      <div class="max-w-7xl mx-auto px-4 flex justify-between items-center text-xs sm:text-sm">
        <div class="flex items-center gap-4">
          <span class="font-semibold tracking-wider">GOVERNMENT OF INDIA</span>
          <span class="hidden sm:inline opacity-80">MINISTRY OF ELECTRONICS & IT</span>
        </div>
        <div class="flex items-center gap-4">
          <a href="#main-content" class="hover:underline focus:ring-2 focus:ring-white">Skip to Main Content</a>
          <!-- Accessibility Toggles -->
          <div class="hidden sm:flex items-center gap-1 mr-2 bg-white/10 px-2 py-0.5 rounded">
            <button class="hover:bg-white/20 px-1.5 py-0.5 rounded focus:ring-2 focus:ring-white transition-colors text-xs" title="Decrease Font Size">A-</button>
            <button class="hover:bg-white/20 px-1.5 py-0.5 rounded focus:ring-2 focus:ring-white transition-colors text-sm font-bold" title="Normal Font Size">A</button>
            <button class="hover:bg-white/20 px-1.5 py-0.5 rounded focus:ring-2 focus:ring-white transition-colors text-base" title="Increase Font Size">A+</button>
            <div class="w-px h-3 bg-white/30 mx-1"></div>
            <button class="hover:bg-white/20 px-1.5 py-0.5 rounded focus:ring-2 focus:ring-white transition-colors text-xs font-bold" title="High Contrast">HC</button>
          </div>
          <!-- Language Selector -->
          <div class="relative flex items-center gap-1 bg-white/10 px-2 py-0.5 rounded">
            <span class="font-bold text-xs">अ</span>
            <select 
              @change="changeLanguage" 
              :value="currentLanguage"
              class="appearance-none bg-transparent border-none text-xs sm:text-sm text-white focus:ring-0 cursor-pointer pr-4 font-bold"
            >
              <option v-for="lang in languages" :key="lang.code" :value="lang.code" class="text-slate-900">
                {{ lang.label }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Header -->
    <header class="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        
        <!-- Logo Area with Hamburger -->
        <div class="flex items-center gap-4">
          <button @click="toggleSidebar" class="text-gov-blue hover:text-gov-saffron focus:outline-none p-2 rounded-md hover:bg-slate-100 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          
          <router-link to="/" class="flex items-center gap-4 group">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" alt="State Emblem of India" class="h-12 w-auto" />
            <div class="flex flex-col">
              <span class="text-xl sm:text-2xl font-bold text-gov-blue tracking-tight leading-tight">
                Jan Sarthi AI
              </span>
              <span class="text-xs sm:text-sm font-semibold text-gov-saffron">
                Public Service Navigator
              </span>
            </div>
          </router-link>
        </div>

        <!-- Profile / Avatar Placeholder -->
        <div class="flex items-center">
          <router-link to="/account" class="h-10 w-10 rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center cursor-pointer shadow-sm hover:shadow transition-shadow">
             <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-500" viewBox="0 0 20 20" fill="currentColor">
               <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
             </svg>
          </router-link>
        </div>
      </div>
      
      <!-- Navigation Bar -->
      <div class="bg-gov-saffron">
        <div class="max-w-7xl mx-auto px-4">
          <nav class="flex items-center overflow-x-auto whitespace-nowrap hide-scrollbar">
            <router-link to="/" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Home</router-link>
            <router-link to="/ai-assistant" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Sarthi AI</router-link>
            <router-link to="/services" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Services</router-link>
            <router-link to="/documents" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">My Documents</router-link>
            <router-link to="/applications" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Track</router-link>
            <router-link to="/compare" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Compare</router-link>
            <router-link to="/legal" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Legal</router-link>
            <router-link to="/forum" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Forum</router-link>
            <router-link to="/admin" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Admin</router-link>
            <router-link to="/help" class="px-4 py-2 text-white hover:bg-gov-hover transition-colors font-medium text-sm border-r border-white/20" active-class="bg-gov-hover font-bold shadow-[inset_0_-2px_0_0_#fff]">Help</router-link>
          </nav>
        </div>
      </div>
    </header>

    <main id="main-content" class="flex-grow w-full relative">
      <div class="relative z-10 max-w-7xl mx-auto px-4 py-8">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- Sidebar Overlay -->
    <transition name="fade">
      <div 
        v-if="isSidebarOpen" 
        @click="closeSidebar" 
        class="fixed inset-0 bg-gov-blue/50 backdrop-blur-sm z-50 transition-opacity"
      ></div>
    </transition>

    <!-- Sidebar -->
    <transition name="slide-left">
      <aside 
        v-if="isSidebarOpen" 
        class="fixed top-0 left-0 bottom-0 w-80 bg-white z-50 shadow-2xl flex flex-col border-r-4 border-gov-saffron overflow-y-auto"
      >
        <div class="p-6 flex items-center justify-between border-b border-slate-200">
          <div class="flex items-center gap-3">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" alt="Emblem" class="h-10 w-auto" />
            <h2 class="text-xl font-bold text-gov-blue leading-tight">All Features</h2>
          </div>
          <button @click="closeSidebar" class="p-2 text-slate-500 hover:text-red-600 rounded-md hover:bg-red-50 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <nav class="flex-grow p-4 space-y-1">
          <router-link @click="closeSidebar" to="/" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
            Home
          </router-link>
          
          <router-link @click="closeSidebar" to="/ai-assistant" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg>
            Jan Sarthi AI
          </router-link>

          <router-link @click="closeSidebar" to="/services" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
            Services
          </router-link>

          <router-link @click="closeSidebar" to="/documents" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            My Documents
          </router-link>

          <router-link @click="closeSidebar" to="/applications" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
            Track Application
          </router-link>

          <router-link @click="closeSidebar" to="/profile" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
            My Profile
          </router-link>

          <router-link @click="closeSidebar" to="/legal" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" /></svg>
            Legal Rights
          </router-link>

          <router-link @click="closeSidebar" to="/compare" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            Compare Schemes
          </router-link>

          <router-link @click="closeSidebar" to="/forum" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" /></svg>
            Community Forum
          </router-link>

          <router-link @click="closeSidebar" to="/admin" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            Admin Dashboard
          </router-link>

          <router-link @click="closeSidebar" to="/help" class="flex items-center gap-3 px-4 py-2.5 rounded text-gov-blue font-bold hover:bg-gov-light-blue hover:text-gov-blue transition-colors border border-transparent hover:border-gov-blue/20" active-class="bg-gov-light-blue text-gov-blue shadow-sm border-gov-blue/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            Help & FAQs
          </router-link>
        </nav>
      </aside>
    </transition>

    <!-- Government Standard Footer -->
    <footer class="bg-gov-blue text-white py-6 border-t-4 border-gov-saffron mt-auto">
      <div class="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="text-sm max-w-xl">
          <p class="font-bold text-gov-saffron mb-1">Disclaimer</p>
          <p class="text-white/80 leading-relaxed text-xs">This is a citizen assistance platform. For official applications, please visit the respective government portals. We do not store sensitive personal information.</p>
          <p class="mt-3">© 2026 Government of India. All rights reserved.</p>
        </div>
        <div class="flex flex-wrap gap-4 text-sm font-medium">
          <a href="https://uidai.gov.in" target="_blank" class="hover:text-gov-saffron transition-colors hover:underline">UIDAI</a>
          <a href="https://www.nsdl.co.in" target="_blank" class="hover:text-gov-saffron transition-colors hover:underline">NSDL</a>
          <a href="https://portal2.passportindia.gov.in" target="_blank" class="hover:text-gov-saffron transition-colors hover:underline">Passport Seva</a>
          <div class="w-px h-4 bg-white/30 hidden sm:block"></div>
          <a href="#" class="hover:underline opacity-80">Privacy Policy</a>
          <a href="#" class="hover:underline opacity-80">Terms</a>
        </div>
      </div>
    </footer>

    <VoiceWidget />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-left-enter-active,
.slide-left-leave-active {
  transition: transform 0.3s ease;
}

.slide-left-enter-from,
.slide-left-leave-to {
  transform: translateX(-100%);
}
</style>