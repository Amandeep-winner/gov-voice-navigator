import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import SchemeComparison from '../views/SchemeComparison.vue'
import CommunityForum from '../views/CommunityForum.vue'
import GovDashboard from '../views/GovDashboard.vue'

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
    }
  ]
})

export default router