import { createRouter, createWebHistory } from 'vue-router'

import MainPage from '../pages/MainPage.vue';
import Usage from '../pages/Usage.vue';
import Advice from '../pages/Advice.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Home', component: MainPage },
        { path: '/usage/', name: 'Usage', component: Usage },
        { path: '/advice/', name: 'Advice', component: Advice },
    ]
})

export default router
