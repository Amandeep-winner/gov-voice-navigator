<script setup lang="ts">
import { ref } from 'vue'

const situations = ref([
  {
    id: 1,
    title: 'Police Officer Demanding a Bribe',
    icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
    color: 'red',
    rights: [
      'You have the right to refuse paying any bribe. It is illegal under the Prevention of Corruption Act, 1988.',
      'You have the right to ask for the officer\'s name, ID number, and designation.',
      'You can record the conversation or video if done safely and legally in a public space (though exercise extreme caution).'
    ],
    action: 'Lodge a complaint with the Anti-Corruption Bureau (ACB) or dial the anti-corruption helpline.',
    helpline: '1064 (Anti-Corruption Helpline)'
  },
  {
    id: 2,
    title: 'Unlawful Detainment or Arrest',
    icon: 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1',
    color: 'orange',
    rights: [
      'Right to be informed of the grounds of arrest (Section 50 of CrPC).',
      'Right to have a relative or friend informed about your arrest (Section 50A of CrPC).',
      'Right to be produced before a magistrate within 24 hours (Article 22 of the Constitution).',
      'Right to consult a lawyer of your choice.'
    ],
    action: 'Demand to make your phone call. Do not sign any confession documents without your lawyer present.',
    helpline: '112 (National Emergency Number)'
  },
  {
    id: 3,
    title: 'Medical Emergency at a Private Hospital',
    icon: 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z',
    color: 'rose',
    rights: [
      'Supreme Court ruling states that ALL hospitals (public or private) must provide immediate emergency medical care to preserve life, regardless of the patient\'s ability to pay immediately.',
      'Hospitals cannot demand police clearance before starting emergency treatment in medico-legal cases (accidents).'
    ],
    action: 'Cite the Supreme Court ruling (Pt. Parmanand Katara vs Union Of India). If they refuse, you can file a police complaint for medical negligence.',
    helpline: '104 (Health Helpline) / 112'
  }
])

const selectedSituation = ref(situations.value[0])

const selectSituation = (situation: any) => {
  selectedSituation.value = situation
}
</script>

<template>
  <div class="max-w-6xl mx-auto space-y-8 animate-fade-in-up pb-20">
    
    <div class="bg-red-50 border border-red-200 border-t-4 border-t-red-600 rounded-md p-8 md:p-12 text-center shadow-sm relative overflow-hidden">
      <div class="bg-red-100 w-16 h-16 mx-auto rounded flex items-center justify-center text-red-600 mb-6 shadow-sm border border-red-200">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
        </svg>
      </div>
      <h2 class="text-3xl font-bold text-red-800 tracking-tight">Emergency Legal Rights</h2>
      <p class="text-red-700 mt-4 text-lg max-w-2xl mx-auto font-medium">Know your fundamental rights in critical situations. Nobody is above the law. Use this portal to defend yourself against extortion, unlawful detainment, or denial of basic rights.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <!-- Situation Selector -->
      <div class="lg:col-span-4 space-y-3">
        <h3 class="text-xl font-bold text-slate-800 mb-4 px-2">Select Situation</h3>
        
        <button 
          v-for="sit in situations" 
          :key="sit.id"
          @click="selectSituation(sit)"
          :class="[
            'w-full text-left p-4 rounded transition-all duration-200 border flex items-center gap-4 shadow-sm',
            selectedSituation.id === sit.id 
              ? `bg-gov-light-blue border-l-4 border-l-gov-blue border-y-gov-blue/20 border-r-gov-blue/20 text-gov-blue` 
              : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-700'
          ]"
        >
          <div :class="[
            'p-2 rounded shrink-0',
            selectedSituation.id === sit.id ? `bg-white text-gov-blue shadow-sm border border-gov-blue/20` : 'bg-slate-50 text-slate-500 border border-slate-200'
          ]">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="sit.icon" />
            </svg>
          </div>
          <span :class="['font-bold', selectedSituation.id === sit.id ? `text-gov-blue` : 'text-slate-700']">
            {{ sit.title }}
          </span>
        </button>
      </div>

      <!-- Rights Display -->
      <div class="lg:col-span-8">
        <transition name="fade" mode="out-in">
          <div :key="selectedSituation.id" class="bg-white rounded-md shadow border border-slate-300 p-8 md:p-10 relative overflow-hidden">
            <div class="absolute top-0 left-0 right-0 h-1 bg-gov-blue"></div>
            
            <div class="relative z-10 mt-2">
              <h3 class="text-2xl font-bold text-gov-blue mb-8 pb-4 border-b border-slate-200">{{ selectedSituation.title }}</h3>
              
              <div class="space-y-8">
                <div>
                  <h4 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gov-green" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                    Your Rights
                  </h4>
                  <ul class="space-y-4">
                    <li v-for="(right, idx) in selectedSituation.rights" :key="idx" class="flex items-start gap-3 bg-slate-50 p-4 rounded border border-slate-200 text-slate-800 leading-relaxed font-medium shadow-sm">
                      <span class="bg-gov-green text-white font-bold h-6 w-6 rounded flex items-center justify-center shrink-0 mt-0.5 text-sm">{{ idx + 1 }}</span>
                      {{ right }}
                    </li>
                  </ul>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div class="bg-gov-light-blue border border-gov-blue/20 rounded p-6 shadow-sm">
                    <h4 class="text-gov-blue font-bold mb-2 flex items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                      Immediate Action
                    </h4>
                    <p class="text-slate-800 text-sm leading-relaxed font-medium">{{ selectedSituation.action }}</p>
                  </div>

                  <div class="bg-red-50 border border-red-200 rounded p-6 flex flex-col justify-center items-center text-center shadow-sm">
                    <h4 class="text-red-800 font-bold mb-2">Emergency Helpline</h4>
                    <div class="text-2xl font-bold text-red-700 tracking-wider font-mono">{{ selectedSituation.helpline }}</div>
                    <button class="mt-4 bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded shadow transition-colors w-full font-bold">
                      Dial Now
                    </button>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </transition>
      </div>

    </div>
  </div>
</template>

<style scoped>
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
