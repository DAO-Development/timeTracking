<template>
  <div class="index news flex-content">
    <Header/>
    <div class="summary-box">
      <h1>Главная</h1>
      <div v-if="auth" class="index__hello">
        Добро пожаловать, {{ user.name }} {{ user.lastname }}
      </div>
      <div v-if="auth" class="index__today">
        <h2>На сегодня</h2>
        <ul class="today-list">
          <li>
            <span class="today__unit bold-text">Новости:</span>
            <span class="today__quantity">12 новостей</span>
          </li>
          <li>
            <span class="today__unit bold-text">Работники:</span>
            <span class="today__quantity">12 работников</span>
            <span class="today__now">Новых на сегодня: </span>
            <span class="today__now">Работает:</span>
          </li>
          <li>
            <span class="today__unit bold-text">Клиенты:</span>
            <span class="today__quantity">12 клиентов</span>
            <span class="today__now">Новых на сегодня: </span>
          </li>
          <li>
            <span class="today__unit bold-text">Объекты:</span>
            <span class="today__quantity">12 объекта</span>
            <span class="today__now">В работе:</span>
          </li>
          <li>
            <span class="today__unit bold-text">Календарь:</span>
            <span class="today__quantity">12 события</span>
            <span class="today__now">На этой неделе: </span>
            <span class="today__now">Сегодня:</span>
          </li>
        </ul>
      </div>
      <div v-if="!auth" class="news-all all">
        <div class="news-all__grid">
          <template v-for="item in news">
            <v-card class="news-single" :key="item.id" color="primary" v-if="item.photo_path"
                    @click="$router.push({name: 'NewOpen', params: {id: item.id}})"
                    v-bind:style="{'background-image': 'url('+$hostname+'media'+item.photo_path+ ')', 'background-size': 'cover', 'background-position': 'center'}">
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
import Header from "../components/Header";

export default {
  name: "Index",
  components: {Header},
  created() {
    console.log("init Index")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.auth = true
    }
    this.loadData()
  },
  data() {
    return {
      auth: false,
      news: {},
      user: {},
    }
  },
  methods: {
    goLogin() {
      this.$router.push({name: "Login"})
    },
    loadData() {
      if (this.auth)
        $.ajax({
          url: this.$hostname + "time-tracking/user",
          type: "GET",
          headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
          success: (response) => {
            this.user = response.data.data
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
      else
        $.ajax({
          url: this.$hostname + "time-tracking/news",
          type: "GET",
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