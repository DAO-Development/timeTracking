<template>
  <v-app>
    <v-container class="flex-main">
      <Menu v-if="auth" class="flex-sidebar"/>
      <router-view v-on:set-auth="setAuth"
                   v-on:set-not-auth="setNotAuth"
                   v-on:set-admin="setAdmin"
                   v-on:load-functions="loadFunctions"
                   v-on:load-settings="loadSettings"
                   :key="$route.path"/>
    </v-container>
  </v-app>
</template>

<script>
import $ from 'jquery';
import Vue from 'vue';
import Menu from "./components/Menu";

// global.jQuery = global.$ = $;
// Vue.prototype.$hostname = "https://shielded-plateau-96200.herokuapp.com/";
Vue.prototype.$hostname = "http://65.21.185.61/";
// Vue.prototype.$hostname = "http://127.0.0.1:8000/";
// Vue.prototype.$admin = false
Vue.prototype.$refresh = function () {
  localStorage.clear()
  sessionStorage.clear()
  this.$emit('set-not-auth')
  $.ajaxSetup({
    headers: {"Authorization": ""}
  })
  this.$router.push({name: "Index"})
}

Vue.prototype.$toggleTheme = function (color, language) {
  console.log("toggleTheme global")
  this.$vuetify.lang.current = language
  switch (color) {
    case "dark":
      this.$vuetify.theme.light = false
      this.$vuetify.theme.dark = true
      break
    case "light":
      this.$vuetify.theme.dark = false
      this.$vuetify.theme.light = true
      this.$vuetify.theme.themes.light.primary = "#3D6FB6"
      break
    default:
      this.$vuetify.theme.dark = false
      this.$vuetify.theme.light = true
      this.$vuetify.theme.themes.light.primary = color
      break
  }
}

export default {
  name: 'App',
  components: {Menu},
  created() {
    console.log("init App")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      $.ajaxSetup({
        headers: {
          "Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')),
          "X-CSRF-TOKEN": $('[name="csrfmiddlewaretoken"]').attr('value')
        }
      })
      this.auth = true
      this.loadFunctions()
      this.loadUser()
      this.loadSettings()
    }
  },
  data() {
    return {
      auth: false,
      admin: false,
      read: ['Работники', 'Клиенты', 'Контакты', 'Объекты', 'Бухгалтерия'],
      edit: ['Работники', 'Клиенты', 'Контакты', 'Объекты', 'Бухгалтерия'],
    }
  },
  methods: {
    setAuth() {
      console.log("auth")
      this.auth = true
    },
    setNotAuth() {
      this.auth = false
    },
    setAdmin() {
      this.admin = true
    },
    loadFunctions() {
      console.log('loadFunctions')
      $.ajax({
        url: this.$hostname + "time-tracking/group",
        type: "GET",
        headers: {
          "Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token")),
          "X-CSRF-TOKEN": $('[name="csrfmiddlewaretoken"]').attr('value')
        },
        success: (response) => {
          this.read = response.data.read
          this.edit = response.data.edit
          this.admin = response.data.admin
        },
        error: (response) => {
          if (response.status === 500) {
            console.log("Ошибка соединения с сервером")
            // } else if (response.status === 401) {
            //   this.$refresh()
          } else {
            console.log("Непредвиденная ошибка")
          }
        },
        async: false,
      })
    },
    loadUser() {
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "GET",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        success: (response) => {
          //todo исправить определение админа по группе
          // this.admin = response.data.auth_user_id.is_staff
          console.log(response)
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
        async: false,
      })
    },
    loadSettings() {
      console.log("loadSettings")
      $.ajax({
        url: this.$hostname + "time-tracking/user-settings",
        type: "GET",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        success: (response) => {
          this.$toggleTheme(response.data.data.theme, response.data.data.language)
        },
        error: (response) => {
          if (response.status === 500) {
            console.log("Ошибка соединения с сервером")
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            console.log("Непредвиденная ошибка")
          }
        },
        async: false,
      })
    }
  }
};
</script>

<style>
@import "assets/css/general.css";
@import "assets/css/menu.css";
@import "assets/css/index.css";
/*@import "assets/css/style.css";*/
/*@import "assets/css/fotorama.css";*/
/*@import "assets/css/datepicker.min.css";*/
/*@import "assets/css/selectize.default.css";*/
@import "assets/css/main.css";
@import "assets/css/authorization.css";
@import "assets/css/profile.css";
@import "assets/css/news.css";
@import "assets/css/objects.css";
@import "assets/css/groups.css";
</style>