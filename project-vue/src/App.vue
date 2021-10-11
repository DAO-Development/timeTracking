<template>
  <v-app>
    <!--    <Header></Header>-->
    <v-container>
      <div class="flex-main">
        <Menu v-if="auth" class="flex-sidebar"/>
        <!--        <Menu v-if="auth" class="flex-sidebar"/>-->
        <!--      <Menu v-if="auth"></Menu>-->
        <router-view v-on:set-auth="setAuth"/>
      </div>
    </v-container>
    <!--    <Footer></Footer>-->
  </v-app>
</template>

<script>
import $ from 'jquery';
import Vue from 'vue';
import Menu from "./components/Menu";

global.jQuery = global.$ = $;
global.appUrl = "https://shielded-plateau-96200.herokuapp.com/";
Vue.prototype.$hostname = "https://shielded-plateau-96200.herokuapp.com/";

export default {
  name: 'App',
  components: {Menu},
  created() {
    var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
    console.log($crf_token)
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
@import "assets/css/style.css";
@import "assets/css/fotorama.css";
@import "assets/css/datepicker.min.css";
@import "assets/css/selectize.default.css";
@import "assets/css/main.css";
@import "assets/css/authorization.css";
@import "assets/css/profile.css";
@import "assets/css/news.css";
@import "assets/css/objects.css";
</style>