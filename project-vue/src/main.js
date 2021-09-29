import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import YimoVueEditor from 'yimo-vue-editor'


Vue.config.productionTip = false

new Vue({
    router,
    vuetify,
    render: h => h(App)
}).$mount('#app')


Vue.use(YimoVueEditor, {
    name: 'v-editor',//Custom name
    editorConfig: {
        uploadImgUrl: '/api/upload', // upload api
        printLog: false, // enable console.log
        useLang: 'en'  // lang config
    },//wagnEditor config
    uploadHandler: (type, resTxt) => {//Upload processing hook
        if (type === 'success') {
            var res = JSON.parse(resTxt)//Do not process the default look at the return value bit image path
            if (res.status !== 1) {
                return null
            }
            return res.data
        } else if (type === 'error') {
            //todo toast
        } else if (type === 'timeout') {
            //todo toast
        }
        return 'upload failed__'
    }
})
