import Vue from 'vue'

import App from './App.vue'
import './registerServiceWorker'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faSync } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// import VueCookie from 'vue-cookie'
// Vue.use(VueCookie)

library.add(faSync)
Vue.component('font-awesome-icon', FontAwesomeIcon)

import VueCookies from 'vue-cookies'
Vue.use(VueCookies)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
