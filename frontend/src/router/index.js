import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../plugins/vuex.js'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'Home',
    id: 'v-step-1',
    meta: {
      requiresAuth: true
    },
    icon: 'mdi-home',
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue')
  },
  {
    path: '/change-management',
    name: 'Change Management',
    id: 'v-step-3',
    meta: {
      requiresAuth: true
    },
    icon: 'mdi-calendar-month',
    component: () => import(/* webpackChunkName: "about" */ '../views/ChangeManagement.vue')
  },
  {
    path: '/devices',
    name: 'Devices',
    id: 'v-step-5',
    meta: {
      requiresAuth: true
    },
    icon: 'mdi-cellphone-link',
    component: () => import(/* webpackChunkName: "about" */ '../views/Devices.vue')
  },
  {
    path: '/operations-center',
    name: 'Operations Center',
    id: 'v-step-8',
    meta:{
      requiresAuth: true
    },
    icon: 'mdi-tools',
    component: () => import(/* webpackChunkName: "action" */ '../views/OperationsCenter.vue'),
  },
  {
    path: '/tower-manager',
    name: 'Tower Manager',
    id: 'v-step-9',
    meta:{
      requiresAuth: true
    },
    icon: 'mdi-ansible',
    component: () => import(/* webpackChunkName: "tower" */ '../views/TowerManager.vue'),
  },
  {
    path: '/networks',
    name: 'Network Addressing',
    id: 'v-step-10',
    meta:{
      requiresAuth: true
    },
    icon: 'mdi-fire',
    component: () => import(/* webpackChunkName: "tower" */ '../views/Networks.vue'),
  },
  {
    path: '/email',
    name: 'Email',
    id: 'v-step-11',
    meta: {
      requiresAuth: true
    },
    icon: 'mdi-email',
    component: () => import(/* webpackChunkName: "about" */ '../views/Email.vue')
  },
  {
    path: '/about',
    name: 'About',
    id: 'v-step-12',
    meta: {
      requiresAuth: true
    },
    icon: 'mdi-information-outline',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/',
    name: 'Login',
    meta: {
      sidebar: false,
      requiresAuth: false
    },
    icon: 'mdi-login',
    component: () => import(/* webpackChunkName: "about" */ '../views/Login.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!store.state.isAuthenticated) {
      next({ name: 'Login' })
    } else {
      next() // go to wherever I'm going
    }
  } else {
    next() // does not require auth, make sure to always call next()!
  }
})

export default router
