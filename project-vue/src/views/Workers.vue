<template>
  <div class="flex-main">
    <Menu class="flex-sidebar"/>
    <div class="workers flex-content">
      <div class="summary-box">
        <h3>Работники</h3>
        <v-list three-line class="workers__list content-list">
          <template v-for="profile in profiles">
            <v-list-item :key="profile.id" v-if="profile.active">
              <v-list-item-avatar class="list__image">
                <v-img :src="require('../../../media'+profile.photo_path)"></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>{{ profile.name }} {{ profile.lastname }}</v-list-item-title>
                <v-list-item-subtitle>
                  <span>{{ profile.position }}</span><br>
                  <span>{{ profile.auth_user_id.email }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon color="grey lighten-1">$deleteIcon</v-icon>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
      </div>
    </div>
  </div>
</template>

<script>
import Menu from "../components/Menu";
import $ from "jquery";

export default {
  name: "Workers",
  components: {Menu},
  data() {
    return {
      page: 'home',
      profiles: {},
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
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "GET",
        success: (response) => {
          this.profiles = response.data.data
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
  }
}
</script>

<style scoped>

</style>