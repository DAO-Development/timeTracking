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
import NewOpen from "../views/open/NewOpen";
import Clients from "../views/Clients";
import ClientOpen from "../views/open/ClientOpen";
import Contacts from "../views/Contacts";
import ContactOpen from "../views/open/ContactOpen";
import Groups from "../views/Groups";
import Settings from "../views/Settings";
import WorkerOpen from "../views/open/WorkerOpen";
import Positions from "../views/Positions";
import Accounting from "../views/Accounting";
import AccountingOpen from "../views/open/AccountingOpen";

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
        path: '/workers/:id',
        name: 'WorkerOpen',
        component: WorkerOpen,
        props: true
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
    {
        path: '/settings',
        name: 'Settings',
        component: Settings
    },
    {
        path: '/groups',
        name: 'Groups',
        component: Groups
    },
    {
        path: '/positions-:table',
        name: 'Positions',
        component: Positions,
        props: true
    },
    {
        path: '/categories-:table',
        name: 'Categories',
        component: Positions,
        props: true
    },
    {
        path: '/goals-:table',
        name: 'Goals',
        component: Positions,
        props: true
    },
    {
        path: '/:table',
        name: 'IntegerField',
        component: Positions,
        props: true
    },
    {
        path: '/accounting/:type',
        name: 'Accounting',
        component: Accounting,
        props: true
    },
    {
        path: '/accounting/:type/:id',
        name: 'AccountingOpen',
        component: AccountingOpen,
        props: true
    },
]

const router = new VueRouter({
    routes
})

export default router
