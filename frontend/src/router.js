import Vue from 'vue'
import Router from 'vue-router'
import Samples from './views/Samples.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'samples',
      component: Samples
    },
    {
      path: '/createSamples',
      name: 'createSamples',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "createSamples" */ './views/createSamples.vue')
    },
    {
      path: '/result/:id',
      name: 'result',
      component: () => import(/* webpackChunkName: "result" */ './views/Result.vue')
    }
  ]
})
