import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import loginIcon from "../components/icons/loginIcon";
import passwordIcon from "../components/icons/passwordIcon";
import deleteIcon from "../components/icons/deleteIcon";
import pdfIcon from "../components/icons/pdfIcon";
import addPhotoIcon from "../components/icons/addPhotoIcon";
import addNewIcon from "../components/icons/addNewIcon";
import wasteIcon from "../components/icons/wasteIcon";
import editIcon from "../components/icons/editIcon";
import archiveIcon from "../components/icons/archiveIcon";
import supportIcon from "../components/icons/supportIcon";
import tileIcon from "../components/icons/tileIcon";

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            options: {
                customProperties: true,
            },
            light: {
                primary: '#3D6FB6',
                secondary: '#616161',
                text: {
                    primary: '#333333',
                    secondary: '#616161'
                }
            },
            dark: {
                primary: '#2A3C52',
                secondary: '#344D69',
                text: {
                    primary: '#FFFFFF'
                }
            },
        },
    },
    icons: {
        values: {
            addNew: {
                component: addNewIcon
            },
            addPhoto: {
                component: addPhotoIcon
            },
            archive: {
                component: archiveIcon
            },
            deleteIcon: {
                component: deleteIcon
            },
            edit: {
                component: editIcon
            },
            login: {
                component: loginIcon
            },
            password: {
                component: passwordIcon
            },
            pdf: {
                component: pdfIcon
            },
            support: {
                component: supportIcon
            },
            tile: {
                component: tileIcon
            },
            waste: {
                component: wasteIcon
            },
        }
    }
});
