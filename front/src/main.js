import Vue from 'vue';
import axios from 'axios';

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import VueClipboard from 'vue-clipboard2'


axios.defaults.baseAPIURL = process.env.VUE_APP_BASE_API_URL

Vue.use(ElementUI);
Vue.prototype.$http = axios //全局注册，使用方法为:this.$axios
Vue.use(VueClipboard)


new Vue({
    el: '#app',
    render: h => h(App)
});