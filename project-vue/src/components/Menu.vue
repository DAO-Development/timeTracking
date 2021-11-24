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
    <v-navigation-drawer permanent color="primary" class="menu-list">
      <v-list>
        <v-list-item-group v-model="selectedItem">
          <v-list-item @click="goPage(0)">
            <v-list-item-icon>
              <v-icon>mdi-home</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Главная</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="goPage(1)">
            <v-list-item-icon>
              <v-icon>mdi-bullhorn</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Новости</v-list-item-title>
            </v-list-item-content>
            <v-list-item-icon>
              <v-icon>$tile</v-icon>
            </v-list-item-icon>
          </v-list-item>
          <v-list-item @click="goPage(2)">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Профиль</v-list-item-title>
            </v-list-item-content>
            <v-list-item-icon>
              <v-icon>mdi-pencil</v-icon>
            </v-list-item-icon>
          </v-list-item>
          <!--          <v-list-item v-for="(item, i) in items" :key="i" @click="goPage(i+3)">-->
          <!--            <v-list-item-icon>-->
          <!--              <v-icon></v-icon>-->
          <!--            </v-list-item-icon>-->
          <!--            <v-list-item-content>-->
          <!--              <v-list-item-title v-text="item.text"></v-list-item-title>-->
          <!--            </v-list-item-content>-->
          <!--            <v-list-item-icon>-->
          <!--              <v-icon>$tile</v-icon>-->
          <!--            </v-list-item-icon>-->
          <!--          </v-list-item>-->

          <v-list-item @click="goPage(3)">
            <v-list-item-icon>
              <v-icon>mdi-account-group</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Работники</v-list-item-title>
            </v-list-item-content>
            <v-list-item-icon>
              <v-icon>$tile</v-icon>
            </v-list-item-icon>
          </v-list-item>
          <v-list-item @click="goPage(4)">
            <v-list-item-icon>
              <v-icon>mdi-handshake</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Клиенты</v-list-item-title>
            </v-list-item-content>
            <v-list-item-icon>
              <v-icon>$tile</v-icon>
            </v-list-item-icon>
          </v-list-item>
          <v-list-item @click="goPage(5)">
            <v-list-item-icon>
              <v-icon>mdi-account-box</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Контакты</v-list-item-title>
            </v-list-item-content>
            <v-list-item-icon>
              <v-icon>$tile</v-icon>
            </v-list-item-icon>
          </v-list-item>
          <v-list-item @click="goPage(6)">
            <v-list-item-icon>
              <v-icon>mdi-crane</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Объекты</v-list-item-title>
            </v-list-item-content>
            <v-list-item-icon>
              <v-icon>$tile</v-icon>
            </v-list-item-icon>
          </v-list-item>
          <v-list-item @click="goPage(7)">
            <v-list-item-icon>
              <v-icon>mdi-cash</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Бухгалтерия</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item @click="goPage(8)">
            <!--          <v-list-item @click="goPage(3+items.length)">-->
            <v-list-item-icon>
              <v-icon>mdi-cog-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Настройки</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="goPage(9)">
            <!--          <v-list-item @click="goPage(3+items.length+1)">-->
            <v-list-item-icon>
              <v-icon>$support</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Поддержка</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="goPage(10)">
            <!--          <v-list-item @click="goPage(3+items.length+2)">-->
            <v-list-item-icon>
              <v-icon>mdi-calendar-range</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Календарь</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="goPage(11)">
            <!--          <v-list-item @click="goPage(3+items.length+3)">-->
            <v-list-item-icon>
              <v-icon>mdi-exit-to-app</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Выход</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "Menu",
  created() {
    console.log("init Menu")
    if ($(window).width() <= '568') {
      console.log("<= 568")
      this.loadUser()
    }
    console.log(this.$router.getMatchedComponents()[0].name)
    switch (this.$router.getMatchedComponents()[0].name) {
      case "Index":
        this.selectedItem = 0
        this.page = "Главная"
        break
      case "News":
        this.selectedItem = 1
        this.page = "Новости"
        break
      case "Profile":
        this.selectedItem = 2
        this.page = "Профиль"
        break
      case "Workers":
        this.selectedItem = 3
        this.page = "Работники"
        break
      case "Clients":
        this.selectedItem = 4
        this.page = "Клиенты"
        break
      case "Contacts":
        this.selectedItem = 5
        this.page = "Контакты"
        break
      case "Objects":
        this.selectedItem = 6
        this.page = "Объекты"
        break
      case "Settings":
        // this.selectedItem = this.items.length + 2
        this.selectedItem = 8
        this.page = "Настройки"
        break
      case "Support":
        // this.selectedItem = this.items.length + 3
        this.selectedItem = 9
        this.page = "Поддержка"
        break
      case "Calendar":
        // this.selectedItem = this.items.length + 4
        this.selectedItem = 10
        this.page = "Календарь"
        break
        // default:
        //   var i = -1;
        //   this.items.forEach(item => {
        //     i++
        //     if (item.name === this.$router.getMatchedComponents()[0].name) {
        //       this.page = item.text
        //       this.selectedItem = i + 3
        //     }
        //   })
    }
    console.log(this.selectedItem)
    console.log(this.page)
  },
  data: () => ({
    user: {},
    selectedItem: 0,
    items: [
      {text: 'Объекты', name: 'Objects'},
      {text: 'Работники', name: 'Workers'},
      {text: 'Клиенты', name: 'Clients'},
      {text: 'Контакты', name: 'Contacts'},
      // {text: 'Калькулятор'},
    ],
    page: '',
  }),
  methods: {
    goPage(selected) {
      console.log("go page")
      if (selected === this.selectedItem) {
        return
      }
      if ($(".menu").hasClass("open"))
        $(".menu").removeClass("open")
      switch (selected) {
        case 0:
          this.$router.push({name: "Index"})
          this.selectedItem = 0
          break
        case 1:
          this.$router.push({name: "News"})
          this.selectedItem = 1
          break
        case 2:
          this.$router.push({name: "Profile"})
          this.selectedItem = 2
          break
        case 3:
          this.$router.push({name: "Workers"})
          this.selectedItem = 3
          break
        case 4:
          this.$router.push({name: "Clients"})
          this.selectedItem = 4
          break
        case 5:
          this.$router.push({name: "Contacts"})
          this.selectedItem = 5
          break
        case 6:
          this.$router.push({name: "Objects"})
          this.selectedItem = 6
          break
        case 7:
          break
        case 8:
          this.$router.push({name: "Settings"})
          this.selectedItem = 8
          break
        case 9:
          break
        case 10:
          // this.$router.push({name: "Profile"})
          // this.selectedItem = 10
          break
          // case this.items.length + 3:
          //   break
          // case this.items.length + 4:
          //   break
          // case this.items.length + 5:
          //   break
          // case this.items.length + 6:
        case 11:
          this.logout()
          break
          // default:
          //   this.$router.push({name: this.items[selected - 3].name})
          //   break
      }
    },
    logout() {
      $.ajax({
        url: this.$hostname + "auth/token/logout/",
        type: "POST",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
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
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "GET",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        success: (response) => {
          this.user = response.data.data
          console.log(this.user.photo_path)
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
  }
}
</script>

<style scoped>

</style>