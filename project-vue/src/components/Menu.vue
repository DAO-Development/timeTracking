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

          <v-list-item @click="goPage(3)" v-if="$parent.$parent.read.indexOf('Работники') !== -1">
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
          <v-list-item @click="goPage(4)" v-if="$parent.$parent.read.indexOf('Клиенты') !== -1">
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
          <v-list-item @click="goPage(5)" v-if="$parent.$parent.read.indexOf('Контакты') !== -1">
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
          <v-list-item @click="goPage(6)" v-if="$parent.$parent.read.indexOf('Объекты') !== -1">
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
          <!--          <v-list-item @click="goPage(7)" v-if="$parent.$parent.read.indexOf('Бухгалтерия') !== -1">-->
          <v-list-group v-if="$parent.$parent.read.indexOf('Бухгалтерия') !== -1">
            <template v-slot:activator>
              <v-list-item-icon>
                <v-icon>mdi-cash</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Бухгалтерия</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item @click="$router.push({name: 'Purchases'})">
              <v-list-item-content>
                <v-list-item-title>Покупки</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item @click="$router.push({name: 'Sales'})">
              <v-list-item-content>
                <v-list-item-title>Продажи</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item @click="$router.push({name: 'Accounting', params: {type: 'reports'}})">
              <v-list-item-content>
                <v-list-item-title>Отчеты</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item @click="$router.push({name: 'Accounting', params: {type: 'extracts'}})">
              <v-list-item-content>
                <v-list-item-title>Выписки</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item @click="$router.push({name: 'Accounting', params: {type: 'documents'}})">
              <v-list-item-content>
                <v-list-item-title>Документы</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item @click="$router.push({name: 'Accounting', params: {type: 'contracts'}})">
              <v-list-item-content>
                <v-list-item-title>Договора с клиентами</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item @click="$router.push({name: 'Accounting', params: {type: 'property'}})">
              <v-list-item-content>
                <v-list-item-title>Документы на собственность</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item @click="$router.push({name: 'Offers'})">
              <v-list-item-content>
                <v-list-item-title>Ценовые предложения</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item @click="$router.push({name: 'Waybill'})">
              <v-list-item-content>
                <v-list-item-title>Путевые листы</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
          <v-list-item @click="$router.push({name: 'Calendar'})">
            <v-list-item-icon>
              <v-icon>mdi-calendar</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Календарь</v-list-item-title>
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
        this.selectedItem = this.$parent.$parent.read.indexOf('Работники') + 1 + 2
        this.page = "Работники"
        break
      case "Clients":
        // this.selectedItem = 4
        this.selectedItem = this.$parent.$parent.read.indexOf('Клиенты') + 1 + 2
        this.page = "Клиенты"
        break
      case "Contacts":
        // this.selectedItem = 5
        this.selectedItem = this.$parent.$parent.read.indexOf('Контакты') + 1 + 2
        this.page = "Контакты"
        break
      case "Objects":
        // this.selectedItem = 6
        this.selectedItem = this.$parent.$parent.read.indexOf('Объекты') + 1 + 2
        this.page = "Объекты"
        break
      case "Accounting":
        // this.selectedItem = 7
        this.selectedItem = this.$parent.$parent.read.indexOf('Бухгалтерия') + 1 + 2
        this.page = "Бухгалтерия"
        break
      case "Settings":
        this.selectedItem = this.$parent.$parent.read.length + 3
        // this.selectedItem = 8
        this.page = "Настройки"
        break
      case "Support":
        this.selectedItem = this.$parent.$parent.read.length + 4
        this.page = "Поддержка"
        break
      case "Calendar":
        // this.selectedItem = 10
        this.selectedItem = this.$parent.$parent.read.length + 5
        this.page = "Календарь"
        break
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
          break
        case 1:
          this.$router.push({name: "News"})
          break
        case 2:
          this.$router.push({name: "Profile"})
          break
        case 3:
          this.$router.push({name: "Workers"})
          break
        case 4:
          this.$router.push({name: "Clients"})
          break
        case 5:
          this.$router.push({name: "Contacts"})
          break
        case 6:
          this.$router.push({name: "Objects"})
          break
        case 7:
          break
        case 8:
          this.$router.push({name: "Settings"})
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
        headers: {
          "Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')),
          "X-CSRF-TOKEN": $('[name="csrfmiddlewaretoken"]').attr('value')
        },
        success: () => {
          localStorage.clear()
          sessionStorage.clear()
          window.location = '/'
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response)
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
        headers: {
          "Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')),
          "X-CSRF-TOKEN": $('[name="csrfmiddlewaretoken"]').attr('value')
        },
        success: (response) => {
          this.user = response.data
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