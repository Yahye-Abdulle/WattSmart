// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import Usage from '../pages/Usage.vue';
import Advice from '../pages/Advice.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Home', component: MainPage },
        { path: '/other/', name: 'Usage', component: Usage },
        { path: '/assistance/', name: 'Advice', component: Advice },
    ]
})

export default router
