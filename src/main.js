import babelpolyfill from 'babel-polyfill'
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
//import './assets/theme/theme-green/index.css'
import VueRouter from 'vue-router'
import store from './vuex/store'
import Vuex from 'vuex'
import routes from './routes'
import 'font-awesome/css/font-awesome.min.css'

import Wechat from './plugins/wechat';
import {emoji} from './plugins/emoji/src/api/emoji.js';

Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(Wechat)

Vue.prototype.emoji = emoji;

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  let user = JSON.parse(sessionStorage.getItem('user'));
  if (!user && to.path != '/login') {
      next({ path: '/login' })
  }
  else if (user && to.path == '/login') {
      next({ path: '/main' })
  } else {
      next()
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

