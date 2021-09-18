<template>
  <v-app>
    <!--    <Header></Header>-->
    <v-container>
      <!--      <Menu v-if="auth"></Menu>-->
      <router-view v-on:set-auth="setAuth"/>
    </v-container>
    <!--    <Footer></Footer>-->
  </v-app>
</template>

<script>
import $ from 'jquery';
import Vue from 'vue';

global.jQuery = global.$ = $;
global.appUrl = "http://localhost:8080/";
Vue.prototype.$hostname = "http://127.0.0.1:8000/";

export default {
  name: 'App',
  components: {},
  created() {
    if (localStorage.getItem('auth_token')) {
      this.auth = true
    } else if (sessionStorage.getItem(('auth_token'))) {
      this.auth = true
    }
  },
  data() {
    return {
      auth: false
    }
  },
  methods: {
    setAuth() {
      this.auth = true
    }
  }
};
</script>

<style>
@import "assets/css/main.css";
@import "assets/css/authorization.css";
</style>