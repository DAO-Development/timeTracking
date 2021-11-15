<template>
  <v-app>
    <v-container class="flex-main">
      <Menu v-if="auth" class="flex-sidebar"/>
      <router-view v-on:set-auth="setAuth" v-on:set-admin="setAdmin" :key="$route.path"/>
    </v-container>
  </v-app>
</template>

<script>
import $ from 'jquery';
import Vue from 'vue';
import Menu from "./components/Menu";

global.jQuery = global.$ = $;
Vue.prototype.$hostname = "https://shielded-plateau-96200.herokuapp.com/";
// Vue.prototype.$hostname = "http://127.0.0.1:8000/";
Vue.prototype.$admin = false
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
    this.auth = !!(localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'));
  },
  data() {
    return {
      auth: false
    }
  },
  methods: {
    setAuth() {
      this.auth = true
    },
    setAdmin() {
      Vue.prototype.$admin = true
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
</style>