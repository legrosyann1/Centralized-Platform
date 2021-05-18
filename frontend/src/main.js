import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import store from './plugins/vuex';
import VueTour from 'vue-tour'

Vue.config.productionTip = false

require('vue-tour/dist/vue-tour.css')

Vue.use(VueTour)

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
