import Vue from 'vue'

import App from './App.vue'
import './registerServiceWorker'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faSync } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import VueCookie from 'vue-cookie'

library.add(faSync)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(VueCookie)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
