import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import SchemeComparison from '../views/SchemeComparison.vue'
import CommunityForum from '../views/CommunityForum.vue'
import GovDashboard from '../views/GovDashboard.vue'
import AIAssistant from '../views/AIAssistant.vue'
import UserProfile from '../views/UserProfile.vue'
import LegalRights from '../views/LegalRights.vue'
import ApplicationTracker from '../views/ApplicationTracker.vue'
import AccountProfile from '../views/AccountProfile.vue'
import Services from '../views/Services.vue'
import MyDocuments from '../views/MyDocuments.vue'
import HelpFAQ from '../views/HelpFAQ.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/compare',
      name: 'Compare',
      component: SchemeComparison
    },
    {
      path: '/forum',
      name: 'Forum',
      component: CommunityForum
    },
    {
      path: '/admin',
      name: 'Admin',
      component: GovDashboard
    },
    {
      path: '/ai-assistant',
      name: 'AIAssistant',
      component: AIAssistant
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: UserProfile
    },
    {
      path: '/legal',
      name: 'LegalRights',
      component: LegalRights
    },
    {
      path: '/applications',
      name: 'Applications',
      component: ApplicationTracker
    },
    {
      path: '/account',
      name: 'Account',
      component: AccountProfile
    },
    {
      path: '/services',
      name: 'Services',
      component: Services
    },
    {
      path: '/documents',
      name: 'MyDocuments',
      component: MyDocuments
    },
    {
      path: '/help',
      name: 'HelpFAQ',
      component: HelpFAQ
    }
  ]
})

export default router