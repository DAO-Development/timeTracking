<template>
  <div class="menu">
    <div class="menu-burger" @click="showMobileMenu">
      <div class="menu-burger__item"></div>
      <div class="menu-burger__item"></div>
      <div class="menu-burger__item"></div>
    </div>
    <div class="menu__profile" @click="goPage(0)">
      <v-img v-if="user.photo_path != null"
             :lazy-src="require('../../../media'+user.photo_path)"
             :src="require('../../../media'+user.photo_path)"></v-img>
    </div>
    <v-list dense nav class="menu-list" color="primary">
      <h2 @click="goPage(-1)">Главная</h2>
      <v-list-item-group v-model="selectedItem">
        <v-list-item @click="goPage(0)">
          <v-list-item-content>
            <v-list-item-title>Профиль</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="goPage(1)">
          <v-list-item-content>
            <v-list-item-title>Новости</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-spacer></v-spacer>
        <v-list-item v-for="(item, i) in items" :key="i" @click="goPage(i+2)">
          <v-list-item-content>
            <v-list-item-title v-text="item.text"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-spacer></v-spacer>
        <v-list-item @click="goPage(2+items.length)">
          <v-list-item-content>
            <v-list-item-title>Настройки</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="goPage(2+items.length+1)">
          <v-list-item-content>
            <v-list-item-title>Выход</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "Menu",
  created() {
    if ($(window).width() <= '568') {
      this.loadUser()
    }
    switch (this.$router.getMatchedComponents()[0].name) {
      case "Index":
        this.selectedItem = -1
        this.page = "Главная"
        break
      case "Home":
        this.selectedItem = 0
        this.page = "Профиль"
        break
      case "News":
        this.selectedItem = 1
        this.page = "Новости"
        break
      case "Settings":
        this.selectedItem = this.items.length + 1
        this.page = "Настройки"
        break
      case "Documents":
        //@todo fix that later
        this.selectedItem = -1
        this.page = "Документы"
        break
      default:
        var i = -1;
        this.items.forEach(item => {
          i++
          if (item.name === this.$router.getMatchedComponents()[0].name) {
            this.page = item.text
            this.selectedItem = i + 2
          }
        })
        console.log(this.selectedItem)
        console.log(this.page)

        // this.page = this.items[this.selectedItem - 2].name
    }
  },
  data: () => ({
    user: {},
    selectedItem: 0,
    items: [
      {text: 'Объекты', name: 'Objects'},
      {text: 'Работники', name: 'Workers'},
      {text: 'Клиенты', name: 'Clients'},
      // {text: 'Калькулятор'},
    ],
    page: '',
  }),
  methods: {
    goPage(selected) {
      if ($(".menu").hasClass("open"))
        $(".menu").removeClass("open")
      switch (selected) {
        case -1:
          this.$router.push({name: "Index"})
          this.selectedItem = -1
          break
        case 0:
          this.$router.push({name: "Home"})
          this.selectedItem = 0
          break
        case 1:
          this.$router.push({name: "News"})
          break
        case this.items.length + 2:
          break
        case this.items.length + 3:
          this.logout()
          break
        default:
          this.$router.push({name: this.items[selected - 2].name})
          break
      }
    },
    logout() {
      $.ajax({
        url: this.$hostname + "auth/token/logout/",
        type: "POST",
        success: () => {
          localStorage.clear()
          sessionStorage.clear()
          window.location = '/'
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    showMobileMenu() {
      console.log("open menu")
      if ($(".menu").hasClass("open"))
        $(".menu").removeClass("open")
      else
        $(".menu").addClass("open")
    },
    loadUser() {
      if (localStorage.getItem('auth_token')) {
        $.ajaxSetup({
          headers: {"Authorization": "Token " + localStorage.getItem("auth_token")}
        })
      } else if (sessionStorage.getItem('auth_token')) {
        $.ajaxSetup({
          headers: {"Authorization": "Token " + sessionStorage.getItem("auth_token")}
        })
      }
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "GET",
        success: (response) => {
          this.user = response.data.data
          console.log(this.user.photo_path)
        },
        error: (response) => {
          if (response.status === 500) {
            console.log("Ошибка соединения с сервером")
          } else {
            console.log("Непредвиденная ошибка")
          }
        }
      })
    },
  }
}
</script>

<style scoped>

</style>