<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import Vapi from '@vapi-ai/web'

const isActive = ref(false)
const isConnecting = ref(false)
const language = ref('en')

// Vite envs (public-only keys used in browser).
const publicKey = import.meta.env.VITE_VAPI_PUBLIC_KEY || ''
const assistantId = import.meta.env.VITE_VAPI_ASSISTANT_ID || ''

// Backend base URL (used to create a fresh Vapi call per click).
// Example: http://localhost:5000
const backendBaseUrl =
  import.meta.env.VITE_BACKEND_URL ||
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:5000'

// Singleton to prevent duplicate Vapi/Daily/Krisp initialization (HMR/remounts).
type VapiInstance = {
  start?: (assistantId: string) => Promise<void> | void
  stop: () => Promise<void> | void
  reconnect: (webCall: { id?: string; webCallUrl: string }) => Promise<void>
  on: (event: string, handler: (...args: any[]) => void) => void
}

declare global {
  interface Window {
    __vapiWidgetVapi?: VapiInstance | null
    __vapiWidgetListenersAttached?: boolean
  }
}

let vapi: VapiInstance | null = null
let isStopping = false
let isStarting = false

const resetUiState = () => {
  isActive.value = false
  isConnecting.value = false
  isStopping = false
  isStarting = false
}

const initVapiOnce = () => {
  if (typeof window === 'undefined') return

  if (window.__vapiWidgetVapi) {
    vapi = window.__vapiWidgetVapi
  }
  if (!vapi) {
    if (!publicKey) {
      console.error('Vapi public key missing: set `VITE_VAPI_PUBLIC_KEY`')
      return
    }
    // Handle Vite/Rollup import differences for CommonJS default exports
    const VapiConstructor = (Vapi as any).default || Vapi
    vapi = new VapiConstructor(publicKey) as VapiInstance
    window.__vapiWidgetVapi = vapi
  }

  if (!window.__vapiWidgetListenersAttached) {
    // Attach listeners once to avoid duplicate Krisp initialization warnings.
    vapi!.on('call-start', () => {
      isActive.value = true
      isConnecting.value = false
      isStarting = false
    })

    vapi!.on('call-end', (call: any) => {
      const endedReason =
        call?.endedReason ?? call?.ended_reason ?? call?.endReason ?? 'unknown'

      // If the meeting ended due to ejection, we just reset so the user can start again.
      console.log('[Vapi] call-end:', endedReason)
      resetUiState()
    })

    vapi!.on('call-start-failed', (e: any) => {
      console.error('[Vapi] call-start-failed:', e)
      resetUiState()
      try {
        vapi?.stop()
      } catch {}
    })

    vapi!.on('error', (e: any) => {
      console.error('[Vapi] error:', e)
      resetUiState()
      try {
        vapi?.stop()
      } catch {}
    })

    window.__vapiWidgetListenersAttached = true
  }
}

const onLanguageChange = (e: any) => {
  language.value = e.detail
}

onMounted(() => {
  initVapiOnce()
  window.addEventListener('language-change', onLanguageChange)
})

onUnmounted(() => {
  window.removeEventListener('language-change', onLanguageChange)
  try {
    vapi?.stop()
  } catch {}
})

const toggleVoice = async () => {
  if (!vapi) initVapiOnce()
  if (!vapi) return

  // Stop current session.
  if (isActive.value || isConnecting.value || isStopping) {
    if (isStopping) return
    isStopping = true
    try {
      await Promise.resolve(vapi.stop())
    } catch (e) {
      console.warn('[Vapi] stop() failed:', e)
    } finally {
      resetUiState()
    }
    return
  }

  // Start a NEW session (fresh callId from backend).
  if (isStarting) return
  if (!assistantId) {
    console.error('Vapi assistantId missing: set `VITE_VAPI_ASSISTANT_ID`')
    return
  }

  isStarting = true
  isConnecting.value = true

  try {
    const startResp = await fetch(`${backendBaseUrl}/api/start-call`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ assistantId, publicKey }),
    })

    if (!startResp.ok) {
      const text = await startResp.text()
      throw new Error(`Backend /api/start-call failed: ${startResp.status} ${text}`)
    }

    const data = await startResp.json()
    const callId = data.call_id || data.callId || data.id
    const webCallUrl = data.webCallUrl

    if (!callId || !webCallUrl) {
      throw new Error(
        `Missing call identifiers from backend (callId=${String(
          callId
        )}, webCallUrl=${String(webCallUrl)})`
      )
    }

    // Ensure we don't reuse a stale transport/session.
    try {
      await Promise.resolve(vapi.stop())
    } catch {}

    await vapi.reconnect({ id: callId, webCallUrl })
  } catch (err) {
    console.error('[Vapi] Failed to start fresh session:', err)
    resetUiState()
  } finally {
    isStarting = false
  }
}
</script>

<template>
  <div class="fixed bottom-8 right-8 z-50 flex flex-col items-end gap-4">
    
    <!-- Multi-lingual setup placeholder/indicator - we keep it subtle near the mic -->
    <div v-if="isActive || isConnecting" class="bg-gov-blue text-white rounded px-3 py-1 text-xs font-bold shadow-md animate-fade-in-up border border-gov-blue/20">
      {{ isConnecting ? 'Connecting...' : 'Listening (' + language.toUpperCase() + ')' }}
    </div>

    <div class="relative">
      <div v-if="isActive" class="absolute inset-0 bg-gov-saffron rounded-full animate-ping opacity-75"></div>
      <div v-if="isActive" class="absolute -inset-2 bg-gov-saffron/50 rounded-full animate-pulse opacity-50"></div>
      
      <button 
        @click="toggleVoice"
        :class="[
          'relative flex items-center justify-center h-16 w-16 rounded-full shadow-lg transition-all duration-300 transform hover:scale-105 border-2 border-white',
          isActive ? 'bg-red-600 hover:bg-red-700' : isConnecting ? 'bg-gov-saffron' : 'bg-gov-blue hover:bg-blue-900'
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