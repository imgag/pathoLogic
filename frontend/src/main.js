import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import store from './store'
import 'material-icons/css/material-icons.min.css'
import router from './router'

Vue.config.productionTip = false
Vue.prototype.$basePath = (process.env.VUE_APP_ENDPOINT !== undefined && process.env.VUE_APP_ENDPOINT.length) ? process.env.VUE_APP_ENDPOINT : 'http://localhost:8080/v1'

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
