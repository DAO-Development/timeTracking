<template>
  <div class="settings flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Настройки</h1>
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
                     @click="$router.push({name: 'Positions',  params: {table: 'cheque'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Категории чеков</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="$parent.$parent.admin"
                     @click="$router.push({name: 'Positions',  params: {table: 'waybill'}})">
          <v-list-item-icon>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Цели поездок</v-list-item-title>
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
  created() {
    console.log("init Settings")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      // this.loadData()
    } else {
      this.$router.push({name: "Login"})
    }
  },
}
</script>

<style scoped>

</style>