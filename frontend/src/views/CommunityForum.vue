<script setup lang="ts">
import { ref } from 'vue'

const posts = ref([
  {
    id: 1,
    author: 'Rajiv Sharma',
    avatarInfo: 'RS',
    date: '2 hours ago',
    title: 'How long did the PM Kisan scheme take to deposit?',
    content: 'I submitted my Aadhaar integration last week. Does anyone know the average wait time for the first installment? The official tracker seems to be down today.',
    tags: ['PM Kisan', 'Wait Time'],
    upvotes: 45,
    replies: [
      { id: 101, author: 'Anita Desai', date: '1 hour ago', content: 'For me it took exactly 14 days after the Aadhaar authentication was marked successful. Check with your local CSC.' },
      { id: 102, author: 'Karan Patel', date: '30 mins ago', content: 'Yes, around 2 weeks is normal. Make sure your land seeding is showing as YES on the portal.' }
    ],
    showReplies: false
  },
  {
    id: 2,
    author: 'Suman Roy',
    avatarInfo: 'SR',
    date: '1 day ago',
    title: 'Rejected for Ayushman Bharat?',
    content: 'My application was rejected stating "Income criteria not met" even though my family income is below the threshold. How do I appeal this?',
    tags: ['Ayushman Bharat', 'Appeal'],
    upvotes: 112,
    replies: [],
    showReplies: false
  }
])

const toggleReplies = (post: any) => {
  post.showReplies = !post.showReplies
}
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-6 animate-fade-in-up">
    
    <!-- Community Header -->
    <div class="flex justify-between items-end mb-8">
      <div>
        <h2 class="text-4xl font-extrabold text-slate-800 tracking-tight">Community Forum</h2>
        <p class="text-slate-500 mt-2 text-lg">Real answers and experiences from people like you.</p>
      </div>
      <button class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-6 rounded-xl shadow-lg hover:shadow-indigo-500/30 transition-all flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
        New Question
      </button>
    </div>

    <!-- Filter/Search Bar -->
    <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 flex items-center gap-4">
      <div class="flex-grow relative">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        <input type="text" placeholder="Search questions or topics..." class="w-full bg-slate-50 border-none rounded-xl py-3 pl-12 pr-4 text-slate-700 focus:ring-2 focus:ring-indigo-500 transition-shadow">
      </div>
      <button class="p-3 text-slate-500 bg-slate-50 hover:bg-slate-100 rounded-xl transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" /></svg>
      </button>
    </div>

    <!-- Posts list -->
    <div class="space-y-6">
      <div v-for="post in posts" :key="post.id" class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
        
        <div class="flex items-start gap-4">
          <!-- Upvote column -->
          <div class="flex flex-col items-center bg-slate-50 rounded-xl p-2 min-w-[50px]">
            <button class="text-slate-400 hover:text-indigo-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" /></svg>
            </button>
            <span class="font-bold text-slate-700 my-1">{{ post.upvotes }}</span>
            <button class="text-slate-400 hover:text-red-500 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
            </button>
          </div>

          <!-- Content column -->
          <div class="flex-grow">
            <!-- Author Meta -->
            <div class="flex items-center gap-3 mb-2">
              <div class="bg-indigo-100 text-indigo-700 h-8 w-8 rounded-full flex items-center justify-center font-bold text-xs ring-2 ring-white">
                {{ post.avatarInfo }}
              </div>
              <span class="font-semibold text-sm text-slate-700">{{ post.author }}</span>
              <span class="text-xs text-slate-400 border-l border-slate-200 pl-3">{{ post.date }}</span>
            </div>

            <!-- Title & Body -->
            <h3 class="text-xl font-bold text-slate-900 mb-2">{{ post.title }}</h3>
            <p class="text-slate-600 leading-relaxed">{{ post.content }}</p>

            <!-- Tags -->
            <div class="flex gap-2 mt-4">
              <span v-for="tag in post.tags" :key="tag" class="bg-slate-100 text-slate-600 text-xs font-medium px-3 py-1 rounded-full cursor-pointer hover:bg-slate-200 transition-colors">
                {{ tag }}
              </span>
            </div>

            <!-- Action Bar -->
            <div class="flex items-center gap-6 mt-6 border-t border-slate-100 pt-4">
              <button 
                @click="toggleReplies(post)" 
                class="flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-indigo-600 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
                {{ post.replies.length }} Answers
              </button>
              <button class="flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-indigo-600 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" /></svg>
                Share
              </button>
            </div>

            <!-- Replies Section -->
            <div v-if="post.showReplies" class="mt-6 space-y-4 pl-6 border-l-2 border-indigo-100">
              <div v-for="reply in post.replies" :key="reply.id" class="bg-slate-50 rounded-2xl p-4">
                <div class="flex items-center gap-2 mb-2">
                   <span class="font-semibold text-sm text-slate-700">{{ reply.author }}</span>
                   <span class="text-xs text-slate-400">• {{ reply.date }}</span>
                </div>
                <p class="text-slate-600 text-sm">{{ reply.content }}</p>
              </div>

              <!-- Add Reply Box -->
              <div class="flex gap-3 items-start mt-4">
                <div class="bg-indigo-600 text-white h-8 w-8 rounded-full flex-shrink-0 flex items-center justify-center font-bold text-xs ring-2 ring-white">U</div>
                <input type="text" placeholder="Write an answer..." class="w-full bg-white border border-slate-200 rounded-xl py-2 px-4 text-sm text-slate-700 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-shadow">
                <button class="bg-slate-900 text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-slate-800 transition-colors">Post</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
