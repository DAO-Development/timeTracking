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

global.jQuery = global.$ = $;
global.url = "http://localhost:8080/";

export default {
  name: 'App',
  components: {},
  created() {
    if (localStorage.getItem('auth_token')) {
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
/*@import "assets/css/style.css";*/
</style>