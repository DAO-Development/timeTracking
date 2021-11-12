import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from "../views/Index"
import Profile from "../views/Profile"
import Login from "../views/Login"
import RecoverPassword from "../views/RecoverPassword";
import News from "../views/News";
import Objects from "../views/Objects";
import Workers from "../views/Workers";
import Documents from "../views/Documents";
import NewOpen from "../views/NewOpen";
import Clients from "../views/Clients";
import ClientOpen from "../views/ClientOpen";
import Contacts from "../views/Contacts";
import ContactOpen from "../views/ContactOpen";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Index',
        component: Index
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile
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
    {
        path: '/clients',
        name: 'Clients',
        component: Clients
    },
    {
        path: '/clients/:id',
        name: 'ClientOpen',
        component: ClientOpen,
        props: true
    },
    {
        path: '/contacts',
        name: 'Contacts',
        component: Contacts
    },
    {
        path: '/clients/contacts/:idClient',
        name: 'ClientsEmployees',
        component: Contacts,
        props: true
    },
    {
        path: '/contacts/:id',
        name: 'ContactOpen',
        component: ContactOpen,
        props: true
    },
]

const router = new VueRouter({
    routes
})

export default router
