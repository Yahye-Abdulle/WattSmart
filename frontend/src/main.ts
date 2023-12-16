import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

library.add(fas);

const app = createApp(App)

app.use(router)

app.mount('#app')

app.component('font-awesome-icon', FontAwesomeIcon);