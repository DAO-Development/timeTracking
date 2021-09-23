import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from "../views/Home"
import Login from "../views/Login.vue"
import RecoverPassword from "../views/RecoverPassword";
import News from "../views/News";
import Objects from "../views/Objects";
import Workers from "../views/Workers";

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
    {
        path: '/news',
        name: 'News',
        component: News
    },
    {
        path: '/objects',
        name: 'Objects',
        component: Objects
    },
    {
        path: '/workers',
        name: 'Workers',
        component: Workers
    },
]

const router = new VueRouter({
    routes
})

export default router
