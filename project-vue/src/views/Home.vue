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
            <span class="profile__info-title">Дата рождения</span>
            <span class="profile__info-content">{{ user.birthdate }}</span>
          </li>
          <li>
            <span class="profile__info-title">Гражданство</span>
            <span class="profile__info-content">{{ user.citizenship }}</span>
          </li>
          <li>
            <span class="profile__info-title">Должность</span>
            <span class="profile__info-content">{{ user.position }}</span>
          </li>
          <li>
            <span class="profile__info-title">Номер соц. страхования</span>
            <span class="profile__info-content">{{ user.social_code_own }}</span>
          </li>
          <li>
            <span class="profile__info-title">Финский номер соц. страхования</span>
            <span class="profile__info-content">{{ user.social_code_fin }}</span>
          </li>
        </ul>
        <h3>Контакты</h3>
        <ul>
          <li>
            <span class="profile__info-title">Телефон</span>
            <span class="profile__info-content">{{ user.phone }}</span>
          </li>
          <li>
            <span class="profile__info-title">Телефон в Финляндии</span>
            <span class="profile__info-content">{{ user.phone_fin }}</span>
          </li>
          <li>
            <span class="profile__info-title">E-mail</span>
            <span class="profile__info-content">{{ user.auth_user_id.email }}</span>
          </li>
        </ul>
        <h3>Банковская информация</h3>
        <ul>
          <li>
            <span class="profile__info-title">Налоговый номер</span>
            <span class="profile__info-content">{{ user.tax_number }}</span>
          </li>
          <li>
            <span class="profile__info-title">Счет в банке</span>
            <span class="profile__info-content">{{ user.bank_account }}</span>
          </li>
        </ul>

        <div class="open__actions">
          <div class="addition-btn" @click="full = !full">
            <span v-if="full">Скрыть полную информацию</span>
            <span v-if="!full">Показать полную информацию</span>
          </div>
        </div>
        <div class="profile__info profile__info-full" v-if="full">
          <h3>Адреса</h3>
          <ul>
            <li>
              <span class="profile__info-title">Адрес в своей стране</span>
              <span class="profile__info-content">{{ user.address_own }}</span>
            </li>
            <li>
              <span class="profile__info-title">Адрес в Финляндии</span>
              <span class="profile__info-content">{{ user.address_fin }}</span>
            </li>
          </ul>
          <h3>Одежда (размеры)</h3>
          <ul>
            <li>
              <span class="profile__info-title">Ботинки</span>
              <span class="profile__info-content">{{ user.boots }}</span>
            </li>
            <li>
              <span class="profile__info-title">Куртка</span>
              <span class="profile__info-content">{{ user.jacket }}</span>
            </li>
            <li>
              <span class="profile__info-title">Штаны</span>
              <span class="profile__info-content">{{ user.pants }}</span>
            </li>
            <li>
              <span class="profile__info-title">Футболка</span>
              <span class="profile__info-content">{{ user.shirt }}</span>
            </li>
          </ul>
          <h3>Языки</h3>
          <ul>
            <li>
              <span class="profile__info-title">Русский</span>
              <v-checkbox class="profile__info-content" v-model="user.russian" disabled></v-checkbox>
            </li>
            <li>
              <span class="profile__info-title">Английский</span>
              <v-checkbox class="profile__info-content" v-model="user.english" disabled></v-checkbox>
            </li>
            <li>
              <span class="profile__info-title">Эстонский</span>
              <v-checkbox class="profile__info-content" v-model="user.estonian" disabled></v-checkbox>
            </li>
            <li>
              <span class="profile__info-title">Финский</span>
              <v-checkbox class="profile__info-content" v-model="user.finnish" disabled></v-checkbox>
            </li>
            <li>
              <span class="profile__info-title">Другие</span>
              <span class="profile__info-content">{{ user.other_language }}</span>
            </li>
          </ul>
          <h3>Другое</h3>
          <ul>
            <li>
              <span class="profile__info-title">Свой автомобиль</span>
              <v-checkbox class="profile__info-content" v-model="user.auto" disabled></v-checkbox>
            </li>
            <li>
              <span class="profile__info-title">Свой инструмент</span>
              <v-checkbox class="profile__info-content" v-model="user.tool" disabled></v-checkbox>
            </li>
            <li>
              <span class="profile__info-title">Навыки</span>
              <span class="profile__info-content">{{ user.skills }}</span>
            </li>
          </ul>
        </div>
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
      user: {
        auth_user_id: {
          email: ""
        }
      },
      groups: [],
      full: false,
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
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "GET",
        success: (response) => {
          this.user = response.data.data
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
