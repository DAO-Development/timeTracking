<template>
  <div class="profile flex-content">
    <div class="summary-box">
      <div class="profile__image">
        <v-img v-if="user.photo_path != null" :lazy-src="require('../../../media'+user.photo_path)"
               :src="require('../../../media'+user.photo_path)"></v-img>
<!--        <div class="profile__change-photo">Сменить фото</div>-->
      </div>
      <div class="profile__info">
        <h3>Личная информация</h3>
        <ul>
          <li>
            <span class="profile__info-title">Имя</span>
            <span class="profile__info-content">{{ user.name }}</span>
          </li>
          <li>
            <span class="profile__info-title">Фамилия</span>
            <span class="profile__info-content">{{ user.lastname }}</span>
          </li>
          <li>
            <span class="profile__info-title">Должность</span>
            <span class="profile__info-content">{{ user.position }}</span></li>
        </ul>
        <h3>Контакты</h3>
        <ul>
          <li>
            <span class="profile__info-title">Телефон</span>
            <span class="profile__info-content">{{ user.phone }}</span>
          </li>
          <li>
            <span class="profile__info-title">E-mail</span>
            <span class="profile__info-content">{{ user.auth_user_id.email }}</span>
          </li>
        </ul>
      </div>
    </div>
    <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
      {{ alertMsg }}
    </v-alert>
  </div>
</template>

<script>
import $ from 'jquery'

export default {
  name: 'Home',
  data() {
    return {
      page: 'home',
      user: {},
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
        url: this.$hostname + "time-tracking/user",
        type: "GET",
        success: (response) => {
          this.user = response.data.data
          console.log(response.data.data)
          // this.user.photo_path = "../../../media" + this.user.photo_path
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
