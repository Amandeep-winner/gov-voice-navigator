<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  data?: any;
}

const isRecording = ref(false)
const transcript = ref('')
const textInput = ref('')
const chatHistory = ref<ChatMessage[]>([])
const isLoading = ref(false)

const recognition = ref<any>(null)
const isSpeaking = ref(false)

// Backend Base URL
const backendBaseUrl = import.meta.env.VITE_BACKEND_URL || import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

onMounted(() => {
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
  if (SpeechRecognition) {
    recognition.value = new SpeechRecognition()
    recognition.value.continuous = false
    recognition.value.interimResults = true
    recognition.value.lang = 'en-IN'

    recognition.value.onstart = () => {
      isRecording.value = true
    }

    recognition.value.onresult = (event: any) => {
      let interimTranscript = ''
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          transcript.value += event.results[i][0].transcript
        } else {
          interimTranscript += event.results[i][0].transcript
        }
      }
      textInput.value = transcript.value + interimTranscript
    }

    recognition.value.onerror = (event: any) => {
      console.error('Speech recognition error', event.error)
      isRecording.value = false
    }

    recognition.value.onend = () => {
      isRecording.value = false
      if (textInput.value.trim()) {
        sendQuery(textInput.value)
      }
    }
  } else {
    console.warn("Speech Recognition API not supported in this browser.")
  }
})

onUnmounted(() => {
  stopSpeaking()
})

const toggleRecording = () => {
  if (isRecording.value) {
    recognition.value?.stop()
  } else {
    transcript.value = ''
    textInput.value = ''
    recognition.value?.start()
  }
}

const handleTextSubmit = () => {
  if (textInput.value.trim()) {
    sendQuery(textInput.value)
  }
}

const formatResponseText = (data: any) => {
  return `For a ${data.document_name}, you will need the following documents: ${data.required_documents.join(', ')}. The application process is as follows: ${data.application_process.join(', ')}. You should visit the ${data.office_to_visit}. Additional notes: ${data.additional_notes || 'None'}.`
}

const speakResponse = (text: string) => {
  if ('speechSynthesis' in window) {
    stopSpeaking()
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'en-IN'
    
    utterance.onstart = () => isSpeaking.value = true
    utterance.onend = () => isSpeaking.value = false
    utterance.onerror = () => isSpeaking.value = false
    
    window.speechSynthesis.speak(utterance)
  }
}

const stopSpeaking = () => {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel()
    isSpeaking.value = false
  }
}

const sendQuery = async (query: string) => {
  textInput.value = ''
  chatHistory.value.push({
    id: Date.now().toString(),
    role: 'user',
    content: query
  })
  
  isLoading.value = true
  
  try {
    const response = await fetch(`${backendBaseUrl}/api/ai-assistant/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    })
    
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`)
    }
    
    const data = await response.json()
    
    if (data.error) {
      chatHistory.value.push({
        id: Date.now().toString(),
        role: 'assistant',
        content: "I'm sorry, I couldn't process your request. " + data.error
      })
      speakResponse("I'm sorry, I couldn't process your request.")
    } else {
      const responseText = formatResponseText(data)
      chatHistory.value.push({
        id: Date.now().toString(),
        role: 'assistant',
        content: responseText,
        data: data
      })
      speakResponse(responseText)
    }
    
  } catch (err) {
    console.error("Error communicating with AI Assistant API", err)
    chatHistory.value.push({
      id: Date.now().toString(),
      role: 'assistant',
      content: "I'm having trouble connecting right now. Please try again later."
    })
    speakResponse("I'm having trouble connecting right now. Please try again later.")
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto flex flex-col h-[calc(100vh-8rem)] bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
    <!-- Header -->
    <div class="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white shrink-0">
      <h1 class="text-2xl font-bold flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
        </svg>
        AI Document Assistant
      </h1>
      <p class="text-indigo-100 mt-1">Ask via voice or text about any Indian government document.</p>
    </div>

    <!-- Chat Area -->
    <div class="flex-grow overflow-y-auto p-6 space-y-6 bg-slate-50">
      <div v-if="chatHistory.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400">
        <div class="w-24 h-24 mb-4 rounded-full bg-indigo-50 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-indigo-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        </div>
        <p class="text-lg">Try asking: "What documents are required for Aadhaar card?"</p>
      </div>

      <div v-for="msg in chatHistory" :key="msg.id" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
        <!-- User Message -->
        <div v-if="msg.role === 'user'" class="bg-indigo-600 text-white rounded-2xl rounded-tr-sm px-5 py-3 max-w-[80%] shadow-md">
          <p class="text-[15px]">{{ msg.content }}</p>
        </div>

        <!-- Assistant Message -->
        <div v-else class="bg-white border border-slate-200 rounded-2xl rounded-tl-sm p-5 max-w-[85%] shadow-sm flex flex-col gap-3">
          
          <!-- Structured JSON Data rendering -->
          <div v-if="msg.data" class="w-full">
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-xl font-bold text-indigo-700 border-b-2 border-indigo-100 pb-1 w-full">{{ msg.data.document_name }}</h3>
              <button @click="speakResponse(formatResponseText(msg.data))" class="ml-4 p-2 text-indigo-600 hover:bg-indigo-50 rounded-full transition-colors flex-shrink-0" title="Play Audio">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
            
            <div class="space-y-4 text-slate-700 text-[15px]">
              <div>
                <strong class="text-slate-900 block mb-1">Required Documents:</strong>
                <ul class="list-disc pl-5 space-y-1">
                  <li v-for="(item, idx) in msg.data.required_documents" :key="idx">{{ item }}</li>
                </ul>
              </div>
              
              <div>
                <strong class="text-slate-900 block mb-1">Application Process:</strong>
                <ol class="list-decimal pl-5 space-y-1">
                  <li v-for="(step, idx) in msg.data.application_process" :key="idx">{{ step }}</li>
                </ol>
              </div>
              
              <div class="flex items-start gap-2 bg-slate-50 p-3 rounded-lg border border-slate-100">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <div>
                  <strong class="text-slate-900">Office to Visit:</strong>
                  <p>
                    {{ msg.data.office_to_visit }}
                    <a :href="`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(msg.data.office_to_visit + ' India')}`" target="_blank" class="text-indigo-600 hover:text-indigo-800 ml-2 inline-flex items-center text-sm font-medium">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      View on Map
                    </a>
                  </p>
                </div>
              </div>
              
              <div v-if="msg.data.additional_notes" class="bg-yellow-50 text-yellow-800 p-3 rounded-lg border border-yellow-100 text-sm">
                <strong>Note:</strong> {{ msg.data.additional_notes }}
              </div>

              <!-- Related Documents -->
              <div v-if="msg.data.related_documents && msg.data.related_documents.length > 0" class="mt-4 pt-4 border-t border-slate-100">
                <strong class="text-slate-900 block mb-2 text-sm">Related Documents:</strong>
                <div class="flex flex-wrap gap-2">
                  <button 
                    v-for="(doc, idx) in msg.data.related_documents" 
                    :key="idx"
                    @click="sendQuery(`What is the process for ${doc}?`)"
                    class="bg-indigo-50 text-indigo-700 px-3 py-1.5 rounded-full text-sm hover:bg-indigo-100 hover:shadow-sm transition-all border border-indigo-100 flex items-center gap-1"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                    </svg>
                    {{ doc }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Fallback text rendering if no data -->
          <div v-else class="text-[15px] text-slate-700">
            {{ msg.content }}
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-white border border-slate-200 rounded-2xl rounded-tl-sm p-4 shadow-sm flex items-center gap-2">
          <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></div>
          <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="p-4 bg-white border-t border-slate-200 shrink-0">
      <div class="flex items-center gap-3">
        <!-- Voice Input Button -->
        <button 
          @click="toggleRecording" 
          :class="[
            'p-4 rounded-full transition-all duration-300 shadow-md flex-shrink-0',
            isRecording 
              ? 'bg-red-500 hover:bg-red-600 animate-pulse text-white' 
              : 'bg-indigo-100 hover:bg-indigo-200 text-indigo-600'
          ]"
          :title="isRecording ? 'Stop Recording' : 'Start Recording'"
        >
          <svg v-if="!isRecording" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
          </svg>
        </button>

        <!-- Text Input -->
        <div class="relative flex-grow">
          <input 
            v-model="textInput" 
            @keyup.enter="handleTextSubmit"
            type="text" 
            :placeholder="isRecording ? 'Listening...' : 'Type your query here or use the microphone...'" 
            class="w-full pl-4 pr-12 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-shadow bg-slate-50 focus:bg-white"
            :disabled="isLoading"
          />
          <button 
            @click="handleTextSubmit"
            :disabled="!textInput.trim() || isLoading"
            class="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-indigo-600 disabled:text-slate-400 hover:bg-indigo-50 rounded-lg transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
      
      <div v-if="isSpeaking" class="mt-3 flex items-center justify-center gap-2 text-sm text-indigo-600">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
        </svg>
        <span>Assistant is speaking...</span>
        <button @click="stopSpeaking" class="ml-2 text-slate-500 hover:text-red-500 underline">Stop</button>
      </div>
    </div>
  </div>
</template>
