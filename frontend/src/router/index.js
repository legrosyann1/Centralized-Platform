import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../plugins/vuex.js'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'Home',
    meta: {
      requiresAuth: true
    },
    icon: 'mdi-home',
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue')
  },
  {
    path: '/devices',
    name: 'Devices',
    meta: {
      requiresAuth: true
    },
    icon: 'mdi-cellphone-link',
    component: () => import(/* webpackChunkName: "about" */ '../views/Devices.vue')
  },
  {
    path: '/about',
    name: 'About',
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
  {
    path: '/email',
    name: 'Email',
    meta: {
      requiresAuth: true
    },
    icon: 'mdi-email',
    component: () => import(/* webpackChunkName: "about" */ '../views/Email.vue')
  }
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
