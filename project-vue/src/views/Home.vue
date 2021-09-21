<template>
  <v-container>
    <div>Привет, {{ groups }}</div>
    <!--  <v-list v-for="group in groups" :key="group.id">-->
    <!--    <v-list-item>{{ group.name }}</v-list-item>-->
    <!--  </v-list>-->
    <v-btn color="primary" @click="goPage('News')">News</v-btn>
    <v-btn color="primary" @click="goPage('Objects')">Objects</v-btn>
    <v-btn color="primary" @click="logout">Выход</v-btn>
    <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
      {{ alertMsg }}
    </v-alert>
  </v-container>
</template>

<script>
import $ from 'jquery'

export default {
  name: 'Home',
  data() {
    return {
      page: 'home',
      groups: [],
      alertError: false,
      alertMsg: "",
    }
  },
  created() {
    if (localStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + localStorage.getItem("auth_token")}
      })
      this.loadData()
    } else if (sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + sessionStorage.getItem("auth_token")}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Login"})
    }
  },
  methods: {
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
    goPage(str) {
      this.$router.push({name: str});
    },
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/group",
        type: "GET",
        success: (response) => {
          this.groups = response.data.data[0].name
        },
        error: (response) => {
          console.log(response)
        }
      })
    },
  }
}
</script>
