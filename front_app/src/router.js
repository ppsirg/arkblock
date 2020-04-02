import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/keys',
      name: 'blockkeys',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "blockkeys" */ './views/Keys.vue')
    },
    {
      path: '/messages',
      name: 'blockmessages',
      component: () => import(/* webpackChunkName: "blockmessages" */ './views/Messages.vue')
    },
    {
      path: '/user',
      name: 'usermanagement',
      component: () => import(/* webpackChunkName: "usermanagement" */ './views/UserPanel.vue')
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { x: 0, y: 0 }
    }
  }
})
