<template>
  <div class="settings flex-content">
    <Header/>
    <section class="summary-box">
      <h1>{{ $vuetify.lang.t('$vuetify.settings.h1Label') }}</h1>
      <v-row>
        <v-select v-model="settings.theme" :label="$vuetify.lang.t('$vuetify.settings.selectThemeLabel')"
                  :items="items" item-text="name" item-value="theme"
                  @change="putSettings"></v-select>
        <v-select v-model="settings.language" :label="$vuetify.lang.t('$vuetify.settings.selectLangLabel')"
                  :items="languages" @change="putSettings"></v-select>
      </v-row>
      <v-list v-if="$parent.$parent.admin">
        <v-list-item @click="$router.push({name: 'Groups'})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Управление группами</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="$parent.$parent.admin"
                     @click="$router.push({name: 'Positions',  params: {table: 'profile'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Специальности пользователей</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="$parent.$parent.admin"
                     @click="$router.push({name: 'Positions',  params: {table: 'client'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Должности контактов</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="$parent.$parent.admin"
                     @click="$router.push({name: 'Categories',  params: {table: 'cheque'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Категории чеков</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="$parent.$parent.admin"
                     @click="$router.push({name: 'Goals',  params: {table: 'waybill'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Цели поездок</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="$parent.$parent.admin"
                     @click="$router.push({name: 'IntegerField',  params: {table: 'term'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Сроки</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="$parent.$parent.admin"
                     @click="$router.push({name: 'IntegerField',  params: {table: 'tax'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Налог</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="$parent.$parent.admin"
                     @click="$router.push({name: 'IntegerField',  params: {table: 'card'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Карточки</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </section>
  </div>
</template>

<script>
import Header from "../components/Header";
import $ from "jquery";

export default {
  name: "Settings",
  components: {Header},
  data() {
    return {
      settings: {
        theme: 'light',
        language: 'ru',
      },
      items: [
        {theme: 'light', name: 'Светлая'},
        {theme: 'dark', name: 'Темная'},
        {theme: '#EA80FC', name: 'Фиолетовый'},
        {theme: '#8BC34A', name: 'Зеленый'},
      ],
      languages: ["ru", "en"]
    }
  },
  created() {
    console.log("init Settings")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      this.$emit('load-functions')
      $.ajaxSetup({
        headers: {
          "Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')),
          "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').attr('value')
        }
      })
      this.loadSettings()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadSettings() {
      console.log("loadSettings")
      $.ajax({
        url: this.$hostname + "time-tracking/user-settings",
        type: "GET",
        success: (response) => {
          this.settings = response.data.data
          this.$toggleTheme(response.data.data.theme, response.data.data.language)
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
              this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    },
    putSettings() {
      $.ajax({
        url: this.$hostname + "time-tracking/user-settings",
        type: "PUT",
        data: this.settings,
        success: () => {
          this.$toggleTheme(this.settings.theme, this.settings.language)
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
              this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    },
    toggleLanguage() {
      console.log(this.selectedLanguage)
    }
  }
}
</script>

<style scoped>

</style>