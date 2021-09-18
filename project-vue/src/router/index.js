import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from "../views/Home"
import Login from "../views/Login.vue"
import RecoverPassword from "../views/RecoverPassword";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/recover',
        name: 'RecoverPassword',
        component: RecoverPassword
    },
]

const router = new VueRouter({
    routes
})

export default router
