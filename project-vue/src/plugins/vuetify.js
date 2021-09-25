import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import loginIcon from "../components/icons/loginIcon";
import passwordIcon from "../components/icons/passwordIcon";
import deleteIcon from "../components/icons/deleteIcon";
import pdfIcon from "../components/icons/pdfIcon";
import addPhotoIcon from "../components/icons/addPhotoIcon";
import addNewIcon from "../components/icons/addNewIcon";

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            options: {
                customProperties: true,
            },
            light: {
                primary: '#3D6FB6',
                secondary: '#6386B9',
                accent: '#673ab7',
                alert: '#f44336',
                error: '#f44336',
                warning: '#ff9800',
                info: '#3D6FB6',
                success: '#3D6FB6',
                text: {
                    primary: '#333333',
                    secondary: '#616161'
                }
            },
        },
    },
    icons: {
        values: {
            login: {
                component: loginIcon
            },
            password: {
                component: passwordIcon
            },
            deleteIcon: {
                component: deleteIcon
            },
            pdf: {
                component: pdfIcon
            },
            addPhoto: {
                component: addPhotoIcon
            },
            addNew: {
                component: addNewIcon
            },
        }
    }
});
