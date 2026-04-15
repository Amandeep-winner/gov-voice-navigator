<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import Vapi from '@vapi-ai/web'

const isActive = ref(false)
const isConnecting = ref(false)
const language = ref('en')

// This should come from env in production
const publicKey = import.meta.env.VITE_VAPI_PUBLIC_KEY || 'dummy-vapi-public-key'
const assistantId = import.meta.env.VITE_VAPI_ASSISTANT_ID || 'dummy-assistant-id'

let vapi: any = null;

onMounted(() => {
  // Handle Vite/Rollup import differences for CommonJS default exports
  const VapiConstructor = (Vapi as any).default || Vapi
  vapi = new VapiConstructor(publicKey)
  
  vapi.on('call-start', () => {
    isActive.value = true
    isConnecting.value = false
  })
  
  vapi.on('call-end', () => {
    isActive.value = false
    isConnecting.value = false
  })
  
  vapi.on('call-start-failed', (e: any) => {
    console.error('Vapi start failed:', e)
    isActive.value = false
    isConnecting.value = false
  })
  
  vapi.on('error', (e: any) => {
    console.error('Vapi errored:', e)
    isActive.value = false
    isConnecting.value = false
  })
})

onUnmounted(() => {
  if (vapi) {
    vapi.stop()
  }
})

// Listen for a global event for language change if needed
window.addEventListener('language-change', (e: any) => {
  language.value = e.detail
})

const toggleVoice = () => {
  if (isActive.value || isConnecting.value) {
    vapi.stop()
    isActive.value = false
    isConnecting.value = false
  } else {
    isConnecting.value = true
    
    // Attempting to inject unconfigured variables (like 'language') via assistantOverrides 
    // without defining them in the Vapi Dashboard can cause the connection to be rejected (Bad Request).
    // Starting with just the Assistant ID natively avoids these validation drops.
    try {
       vapi.start(assistantId)
    } catch(err) {
       console.error("Local Error starting Vapi:", err)
       isConnecting.value = false
    }
  }
}
</script>

<template>
  <div class="fixed bottom-8 right-8 z-50 flex flex-col items-end gap-4">
    
    <!-- Multi-lingual setup placeholder/indicator - we keep it subtle near the mic -->
    <div v-if="isActive || isConnecting" class="bg-white rounded-full px-3 py-1 text-xs font-semibold shadow-md text-gray-700 animate-fade-in-up">
      {{ isConnecting ? 'Connecting...' : 'Listening (' + language.toUpperCase() + ')' }}
    </div>

    <div class="relative">
      <div v-if="isActive" class="absolute inset-0 bg-blue-400 rounded-full animate-ping opacity-75"></div>
      <div v-if="isActive" class="absolute -inset-2 bg-blue-300 rounded-full animate-pulse opacity-50"></div>
      
      <button 
        @click="toggleVoice"
        :class="[
          'relative flex items-center justify-center h-16 w-16 rounded-full shadow-2xl transition-all duration-300 transform hover:scale-105',
          isActive ? 'bg-red-500 hover:bg-red-600' : isConnecting ? 'bg-yellow-500' : 'bg-blue-600 hover:bg-blue-700'
        ]"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke-width="2" 
          stroke="currentColor" 
          class="w-8 h-8 text-white"
        >
          <!-- Mic icon when idle -->
          <path v-if="!isActive && !isConnecting" stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
          <!-- Stop icon when active -->
          <path v-else-if="isActive" stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          <!-- Dots when connecting -->
          <path v-else stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
@keyframes fade-in-up {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-up {
  animation: fade-in-up 0.3s ease-out forwards;
}
</style>