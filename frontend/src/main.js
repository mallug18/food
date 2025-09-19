// /frontend/src/main.js

import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // <-- Step 1: Import the router

const app = createApp(App)

app.use(router) // <-- Step 2: Tell the app to use the router

app.mount('#app')