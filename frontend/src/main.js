import Vue from 'vue';
import Meta from 'vue-meta';
import Cookies from 'js-cookie';
import axios from 'axios';
import App from './App.vue';
import store from './store';
import router from './router';


Vue.use(Meta);

axios.defaults.headers.common['X-CSRFTOKEN'] = Cookies.get('csrftoken');
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});
