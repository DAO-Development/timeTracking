<template>
  <v-app>
    <v-container class="flex-main">
      <Menu v-if="auth" class="flex-sidebar"/>
      <router-view v-on:set-auth="setAuth"
                   v-on:set-admin="setAdmin"
                   v-on:load-functions="loadFunctions"
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
Vue.prototype.$hostname = "http://127.0.0.1:8000/";
// Vue.prototype.$admin = false
Vue.prototype.$refresh = function () {
  localStorage.clear()
  sessionStorage.clear()
  this.$router.push({name: "Index"})
  $.ajaxSetup({
    headers: {"Authorization": ""}
  })
}

export default {
  name: 'App',
  components: {Menu},
  created() {
    console.log("init App")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.auth = true
      this.loadFunctions()
      this.loadUser()
    }
  },
  data() {
    return {
      auth: false,
      admin: false,
      read: [],
      edit: [],
    }
  },
  methods: {
    setAuth() {
      console.log("auth")
      this.auth = true
    },
    setAdmin() {
      Vue.prototype.$admin = true
    },
    loadFunctions() {
      $.ajax({
        url: this.$hostname + "time-tracking/group",
        type: "GET",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        success: (response) => {
          this.read = response.data.read
          this.edit = response.data.edit
        },
        error: (response) => {
          if (response.status === 500) {
            console.log("Ошибка соединения с сервером")
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            console.log("Непредвиденная ошибка")
          }
        }
      })
    },
    loadUser() {
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "GET",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        success: (response) => {
          this.admin = response.data.data.auth_user_id.is_staff
          console.log(response.data.data.auth_user_id.is_staff)
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