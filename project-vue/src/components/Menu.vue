<template>
  <v-list dense nav class="menu" color="primary">
    <h2>{{ page }}</h2>
    <v-list-item-group v-model="selectedItem">
      <v-list-item v-for="(item, i) in items" :key="i" @click="goPage(i)">
        <v-list-item-content>
          <v-list-item-title v-text="item.text"></v-list-item-title>
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
    switch (this.$router.getMatchedComponents()[0].name) {
      case "News":
        this.selectedItem = 1
        this.page = "Новости"
        break
      case "Objects":
        this.selectedItem = 2
        this.page = "Объекты"
        break
      default:
        this.selectedItem = 0
        this.page = "Главная"
    }
  },
  data: () => ({
    alertSuccess: false,
    alertError: false,
    alertMsg: '',
    selectedItem: 0,
    items: [
      {text: 'Профиль'},
      {text: 'Новости'},
      {text: 'Объекты'},
      {text: 'Выход'},
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
        case 2:
          this.$router.push({name: "Objects"})
          break
        case 3:
          this.logout()
          break
        default:
          console.log(selected)
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