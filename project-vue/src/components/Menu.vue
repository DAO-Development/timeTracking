<template>
  <v-list dense nav class="menu" color="primary">
    <h2>{{ page }}</h2>
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
    <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
      {{ alertMsg }}
    </v-alert>
    <v-alert v-model="alertSuccess" close-text="Закрыть" color="success" dismissible>
      {{ alertMsg }}
    </v-alert>
  </v-list>
</template>

<script>
import $ from "jquery";

export default {
  name: "Menu",
  created() {
    console.log(this.$router.getMatchedComponents()[0].name)
    switch (this.$router.getMatchedComponents()[0].name) {
      case "Home":
        this.selectedItem = 0
        this.page = "Главная"
        break
      case "News":
        this.selectedItem = 1
        this.page = "Новости"
        break
      case "Settings":
        this.selectedItem = this.items.length + 1
        this.page = "Настройки"
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
    alertSuccess: false,
    alertError: false,
    alertMsg: '',
    selectedItem: 0,
    items: [
      {text: 'Объекты', name: 'Objects'},
      {text: 'Работники', name: 'Workers'},
      // {text: 'Калькулятор'},
    ],
    page: '',
  }),
  methods: {
    goPage(selected) {
      switch (selected) {
        case 0:
          this.$router.push({name: "Home"})
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
  }
}
</script>

<style scoped>

</style>