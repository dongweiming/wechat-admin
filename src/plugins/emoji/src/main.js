import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import './assets/css/iconfont.css'
import { emoji } from './api/emoji.js'

Vue.prototype.emoji = emoji

Vue.use(ElementUI)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  ...App
})
