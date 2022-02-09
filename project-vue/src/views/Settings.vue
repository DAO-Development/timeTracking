<template>
  <div class="settings flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Настройки</h1>
      <v-select v-model="selected" label="Тема" :items="items" item-text="name" item-value="theme"
                @change="toggleTheme"></v-select>
      <v-list>
        <v-list-item v-if="$parent.$parent.admin" @click="$router.push({name: 'Groups'})">
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
      selected: 'light',
      items: [
        {theme: 'light', name: 'Светлая'},
        {theme: 'dark', name: 'Темная'},
        {theme: '#EA80FC', name: 'Фиолетовый'},
        {theme: '#8BC34A', name: 'Зеленый'},
      ]
    }
  },
  created() {
    console.log("init Settings")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      this.$emit('load-functions')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    toggleTheme() {
      switch (this.selected) {
        case "dark":
          this.$vuetify.theme.light = false
          this.$vuetify.theme.dark = true
          break
        case "light":
          this.$vuetify.theme.dark = false
          this.$vuetify.theme.light = true
          break
        default:
          this.$vuetify.theme.dark = false
          this.$vuetify.theme.light = true
          this.$vuetify.theme.themes.light.primary = this.selected
          break
      }

    }
  }
}
</script>

<style scoped>

</style>