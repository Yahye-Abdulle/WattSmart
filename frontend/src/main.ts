import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

library.add(fas);

const app = createApp(App)

app.config.globalProperties.$getCsrfToken = function () {
    const value = `; ${document.cookie}`;
    const parts = value.split('; csrftoken=');
    return parts.length === 2 ? parts.pop()?.split(';').shift() ?? '' : '';
};

app.use(router)

app.use(VueSweetalert2);

app.mount('#app')

app.component('font-awesome-icon', FontAwesomeIcon);