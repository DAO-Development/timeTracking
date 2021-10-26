import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from "../views/Index"
import Home from "../views/Home"
import Login from "../views/Login"
import RecoverPassword from "../views/RecoverPassword";
import News from "../views/News";
import Objects from "../views/Objects";
import Workers from "../views/Workers";
import Documents from "../views/Documents";
import NewOpen from "../views/NewOpen";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Index',
        component: Index
    },
    {
        path: '/profile',
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
    {
        path: '/documents/:type&:id',
        name: 'Documents',
        component: Documents,
        props: true
    },
    {
        path: '/news/:id',
        name: 'NewOpen',
        component: NewOpen,
        props: true
    },
]

const router = new VueRouter({
    routes
})

export default router
