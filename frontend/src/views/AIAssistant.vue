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
  <!-- Background with subtle watermark -->
  <div class="max-w-5xl mx-auto flex flex-col h-[calc(100vh-8rem)] bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden relative">
    
    <!-- Watermark Background -->
    <div class="absolute inset-0 pointer-events-none opacity-[0.03] flex items-center justify-center z-0">
      <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" alt="Watermark" class="h-96 w-auto grayscale" />
    </div>

    <!-- Main Content Area (relative z-10 for content above watermark) -->
    <div class="flex-grow overflow-y-auto flex flex-col relative z-10">
      
      <!-- Chat Area -->
      <div class="flex-grow p-4 md:p-8 space-y-6">
        
        <!-- Hero Section (Visible only when chat is empty) -->
        <div v-if="chatHistory.length === 0" class="h-full flex flex-col items-center justify-center text-center max-w-3xl mx-auto space-y-10 mt-6">
          <div class="space-y-4">
            <div class="inline-block bg-gov-light-blue text-gov-blue px-3 py-1 rounded-full text-xs font-bold mb-2 tracking-wide uppercase">Beta Citizen Assistant</div>
            <h1 class="text-3xl md:text-5xl font-bold text-gov-blue tracking-tight leading-tight">How can I help you today?</h1>
            <p class="text-slate-600 text-lg">Ask about government documents, requirements, and application processes</p>
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
            <button @click="sendQuery('What are the Aadhaar Card Documents required?')" class="bg-white border border-slate-200 hover:border-gov-blue/50 hover:shadow-md p-5 rounded-2xl text-left transition-all group flex items-start gap-4 z-10">
              <div class="bg-gov-light-blue p-3 rounded-xl text-gov-blue group-hover:bg-gov-blue group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
              </div>
              <div>
                <h3 class="font-bold text-gov-blue text-lg">Aadhaar Card Documents</h3>
                <p class="text-sm text-slate-500 mt-1">Know the list of required proofs</p>
              </div>
            </button>
            <button @click="sendQuery('What is the PAN Card Application process?')" class="bg-white border border-slate-200 hover:border-gov-blue/50 hover:shadow-md p-5 rounded-2xl text-left transition-all group flex items-start gap-4 z-10">
              <div class="bg-gov-light-blue p-3 rounded-xl text-gov-blue group-hover:bg-gov-blue group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
              </div>
              <div>
                <h3 class="font-bold text-gov-blue text-lg">PAN Card Application</h3>
                <p class="text-sm text-slate-500 mt-1">Step-by-step application guide</p>
              </div>
            </button>
            <button @click="sendQuery('How to do Driving License Renewal?')" class="bg-white border border-slate-200 hover:border-gov-blue/50 hover:shadow-md p-5 rounded-2xl text-left transition-all group flex items-start gap-4 z-10">
              <div class="bg-gov-light-blue p-3 rounded-xl text-gov-blue group-hover:bg-gov-blue group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
              <div>
                <h3 class="font-bold text-gov-blue text-lg">Driving License Renewal</h3>
                <p class="text-sm text-slate-500 mt-1">Process and online forms</p>
              </div>
            </button>
            <button @click="sendQuery('What is the Passport Process?')" class="bg-white border border-slate-200 hover:border-gov-blue/50 hover:shadow-md p-5 rounded-2xl text-left transition-all group flex items-start gap-4 z-10">
              <div class="bg-gov-light-blue p-3 rounded-xl text-gov-blue group-hover:bg-gov-blue group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
              <div>
                <h3 class="font-bold text-gov-blue text-lg">Passport Process</h3>
                <p class="text-sm text-slate-500 mt-1">Appointments and police verification</p>
              </div>
            </button>
          </div>
        </div>

        <!-- Chat History -->
        <div v-for="msg in chatHistory" :key="msg.id" class="flex z-10 relative" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <!-- User Message -->
          <div v-if="msg.role === 'user'" class="!bg-gov-saffron !text-black rounded-2xl rounded-tr-sm px-6 py-4 max-w-[80%] shadow-sm border border-orange-300">
            <p class="text-[16px] font-medium">{{ msg.content }}</p>
          </div>

          <!-- Assistant Message -->
          <div v-else class="bg-white border border-slate-200 rounded-2xl rounded-tl-sm p-6 max-w-[95%] shadow-sm flex flex-col gap-4 relative">
            <div class="absolute top-0 left-0 bottom-0 w-1.5 bg-gov-blue rounded-l-2xl"></div>
            
            <div v-if="msg.data" class="w-full pl-2">
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-bold text-gov-blue flex items-center gap-3">
                  <span class="bg-gov-light-blue p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gov-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </span>
                  {{ msg.data.document_name }}
                </h3>
                <button @click="speakResponse(formatResponseText(msg.data))" class="p-2.5 text-gov-blue hover:bg-gov-light-blue rounded-full transition-colors flex-shrink-0 border border-slate-200 shadow-sm" title="Read Aloud">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
              
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 text-[15px]">
                
                <!-- Requirements -->
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200">
                  <strong class="text-gov-blue flex items-center gap-2 mb-4 text-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gov-saffron" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
                    Required Documents
                  </strong>
                  <ul class="space-y-3">
                    <li v-for="(item, idx) in msg.data.required_documents" :key="idx" class="flex gap-3 text-slate-700">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gov-green flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                      <span>{{ item }}</span>
                    </li>
                  </ul>
                </div>
                
                <!-- Process -->
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200">
                  <strong class="text-gov-blue flex items-center gap-2 mb-4 text-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gov-saffron" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" /></svg>
                    Application Steps
                  </strong>
                  <div class="space-y-4">
                    <div v-for="(step, idx) in msg.data.application_process" :key="idx" class="flex gap-3 text-slate-700">
                      <div class="flex-shrink-0 w-6 h-6 rounded-full bg-gov-blue text-white flex items-center justify-center text-xs font-bold">{{ idx + 1 }}</div>
                      <span>{{ step }}</span>
                    </div>
                  </div>
                </div>

                <!-- Info Cards -->
                <div class="lg:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div class="bg-white border border-slate-200 rounded-xl p-4 flex items-start gap-4 shadow-sm hover:shadow-md transition-shadow">
                     <div class="bg-blue-50 text-blue-600 p-2.5 rounded-lg"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></div>
                     <div><p class="text-xs text-slate-500 font-bold uppercase tracking-wide">Processing Time</p><p class="text-[15px] font-bold text-gov-blue mt-0.5">{{ msg.data.processing_time || '10-15 Working Days' }}</p></div>
                  </div>
                  <div class="bg-white border border-slate-200 rounded-xl p-4 flex items-start gap-4 shadow-sm hover:shadow-md transition-shadow">
                     <div class="bg-green-50 text-green-600 p-2.5 rounded-lg"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></div>
                     <div><p class="text-xs text-slate-500 font-bold uppercase tracking-wide">Fees</p><p class="text-[15px] font-bold text-gov-blue mt-0.5">{{ msg.data.fees || 'Standard Gov Fees Apply' }}</p></div>
                  </div>
                  <div class="bg-white border border-slate-200 rounded-xl p-4 flex items-start gap-4 shadow-sm hover:shadow-md transition-shadow">
                     <div class="bg-orange-50 text-orange-600 p-2.5 rounded-lg"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg></div>
                     <div>
                       <p class="text-xs text-slate-500 font-bold uppercase tracking-wide">Nearby Office</p>
                       <p class="text-[15px] font-bold text-gov-blue mt-0.5">{{ msg.data.office_to_visit }}</p>
                       <a :href="`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(msg.data.office_to_visit + ' near me')}`" target="_blank" class="text-blue-600 hover:text-blue-800 hover:underline text-sm font-bold mt-1 inline-flex items-center gap-1">
                         View on Map
                         <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                       </a>
                     </div>
                  </div>
                </div>
              </div>
              
              <div v-if="msg.data.additional_notes" class="mt-5 bg-amber-50 text-amber-800 p-4 rounded-xl border border-amber-200 text-sm flex gap-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 flex-shrink-0 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <p class="text-[15px] leading-relaxed"><strong>Important Note:</strong> {{ msg.data.additional_notes }}</p>
              </div>

              <!-- Document Upload Section integrated in response -->
              <div class="mt-8 pt-6 border-t border-slate-200">
                <h4 class="font-bold text-gov-blue mb-4 text-xl flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gov-green" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                  Verify Your Documents Online
                </h4>
                <div class="grid grid-cols-1 lg:grid-cols-5 gap-5">
                  <!-- Drag & Drop -->
                  <div class="lg:col-span-2 border-2 border-dashed border-gov-blue/30 rounded-xl bg-gov-light-blue/30 hover:bg-gov-light-blue transition-colors flex flex-col items-center justify-center p-6 text-center cursor-pointer">
                    <div class="bg-white p-4 rounded-full shadow-sm mb-4">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gov-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
                    </div>
                    <p class="font-bold text-gov-blue text-[15px]">Upload your documents to verify completeness</p>
                    <p class="text-sm text-slate-500 mt-2">Drag & drop or click to browse (PDF, JPG, PNG)</p>
                  </div>
                  <!-- AI Feedback Example -->
                  <div class="lg:col-span-3 bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
                    <p class="text-[15px] font-bold text-slate-800 mb-3 border-b pb-2 flex justify-between items-center">
                      AI Verification Status
                      <span class="text-xs font-normal bg-slate-100 text-slate-600 px-2 py-1 rounded-full">Example</span>
                    </p>
                    <ul class="space-y-3">
                      <li class="flex items-center gap-3 text-slate-700 font-medium">
                        <div class="bg-green-100 p-1 rounded-full"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gov-green" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg></div>
                        Identity Proof (Aadhaar)
                      </li>
                      <li class="flex items-center gap-3 text-slate-700 font-medium">
                        <div class="bg-green-100 p-1 rounded-full"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gov-green" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg></div>
                        Age Proof
                      </li>
                      <li class="flex items-center gap-3 text-red-600 font-bold">
                        <div class="bg-red-100 p-1 rounded-full"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg></div>
                        Missing: Address Proof
                      </li>
                    </ul>
                    <div class="mt-4 bg-red-50 text-red-800 p-3 rounded-lg border border-red-200 text-sm font-medium flex gap-3">
                       <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                       <span>You are missing Address Proof. Please upload an Electricity Bill, Rent Agreement, or Voter ID to complete your file.</span>
                    </div>
                  </div>
                </div>
              </div>

            </div>
            
            <div v-else class="text-[16px] text-slate-700 pl-2">
              {{ msg.content }}
            </div>
          </div>
        </div>

        <div v-if="isLoading" class="flex justify-start relative z-10">
          <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm flex items-center gap-2">
            <div class="w-3 h-3 bg-gov-blue rounded-full animate-bounce"></div>
            <div class="w-3 h-3 bg-gov-blue rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-3 h-3 bg-gov-blue rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </div>
        
        <!-- Bottom padding for scroll -->
        <div class="h-4 relative z-10"></div>
      </div>

    </div>

    <!-- AI Interaction Panel (Bottom) -->
    <div class="p-4 md:p-6 bg-white border-t border-slate-200 shrink-0 relative z-20 shadow-[0_-10px_15px_-3px_rgba(0,0,0,0.05)]">
      
      <!-- Live Transcription display -->
      <transition name="fade">
        <div v-if="isRecording && transcript" class="absolute -top-14 left-0 right-0 flex justify-center pointer-events-none z-30">
          <div class="bg-slate-800 text-white text-sm px-6 py-3 rounded-full shadow-lg max-w-xl truncate border border-slate-700 font-medium">
            "{{ transcript }}..."
          </div>
        </div>
      </transition>

      <div class="flex flex-col gap-3 max-w-4xl mx-auto w-full relative">
        <div class="flex items-center gap-3 w-full bg-white border-2 border-slate-200 rounded-full p-1.5 focus-within:border-gov-blue focus-within:ring-4 focus-within:ring-gov-light-blue transition-all shadow-sm">
          
          <!-- Voice / Mic Button (Left/Center aligned depending on text presence) -->
          <button 
            @click="toggleRecording" 
            :class="[
              'w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300 flex-shrink-0 ml-1',
              isRecording 
                ? 'bg-red-600 hover:bg-red-700 shadow-[0_0_15px_rgba(220,38,38,0.5)] text-white scale-110' 
                : 'bg-gov-light-blue hover:bg-gov-blue hover:text-white text-gov-blue'
            ]"
            :title="isRecording ? 'Stop Recording' : 'Start Voice Input'"
          >
            <svg v-if="!isRecording" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
            <div v-else class="flex items-center gap-1">
               <div class="w-1.5 h-3 bg-white rounded-full animate-bounce"></div>
               <div class="w-1.5 h-4 bg-white rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
               <div class="w-1.5 h-3 bg-white rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </button>

          <!-- Text Input -->
          <input 
            v-model="textInput" 
            @keyup.enter="handleTextSubmit"
            type="text" 
            :placeholder="isRecording ? 'Listening to your voice...' : 'Ask in voice or type your query...'" 
            class="flex-grow px-2 py-3 bg-transparent border-none focus:outline-none focus:ring-0 text-slate-800 text-[16px] placeholder-slate-400 font-medium"
            :disabled="isLoading"
          />

          <!-- Submit Button -->
          <button 
            @click="handleTextSubmit"
            :disabled="!textInput.trim() || isLoading"
            class="w-12 h-12 rounded-full flex items-center justify-center text-white disabled:bg-slate-200 disabled:text-slate-400 bg-gov-blue hover:bg-blue-800 transition-colors flex-shrink-0 mr-1 shadow-sm"
            title="Send Query"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
        
        <div class="flex justify-between items-center px-4">
          <div v-if="isSpeaking" class="flex items-center gap-2 text-sm text-gov-blue font-bold bg-gov-light-blue px-4 py-1.5 rounded-full w-max border border-gov-blue/20">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
            </svg>
            <span>Assistant is speaking...</span>
            <button @click="stopSpeaking" class="ml-2 text-red-600 hover:text-red-800 underline text-xs font-bold">Stop Audio</button>
          </div>
          <div v-else class="text-xs text-slate-500 font-medium flex items-center gap-1.5 ml-auto">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gov-saffron" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
            <span class="opacity-80">Powered by AI for Public Service</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
