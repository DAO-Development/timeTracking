<template>
  <div class="index news flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Главная</h3>
      </div>
      <div class="news-all all">
        <div class="news-all__grid">
          <template v-for="item in news">
            <v-card class="news-single" :key="item.id" color="primary" v-if="item.photo_path"
                    @click="$router.push({name: 'NewOpen', params: {id: item.id}})"
                    v-bind:style="{'background-image': 'url('+require('../../../media'+item.photo_path)+ ')',
              'background-size': 'cover', 'background-position': 'center'}">
              <div class="news-single__title">{{ item.title }}</div>
              <div class="news-single__text" v-html="item.text"></div>
            </v-card>
            <v-card class="news-single" :key="item.id" color="primary" v-else
                    @click="$router.push({name: 'NewOpen', params: {currentNew: item, id: item.id}})">
              <div class="news-single__title">{{ item.title }}</div>
              <div class="news-single__text" v-html="item.text"></div>
            </v-card>
          </template>
        </div>
      </div>
    </div>

    <v-btn v-if="!auth" class="action-btn" color="primary" @click="goLogin">Войти</v-btn>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "Index",
  created() {
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.auth = true
    }
    this.loadData()
  },
  data() {
    return {
      auth: false,
      news: {},
    }
  },
  methods: {
    goLogin() {
      this.$router.push({name: "Login"})
    },
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/news",
        type: "GET",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        success: (response) => {
          this.news = response.data.data
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
  }
}
</script>

<style scoped>

</style>