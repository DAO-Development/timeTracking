<template>
  <div class="news">
    <div></div>
    <div>
      <v-text-field label="Заголовок" v-model="newNew.title" :rules="titleRules" required outlined></v-text-field>
      <v-textarea label="Текст новости" v-model="newNew.text" outlined></v-textarea>
      <v-btn @click="openAdd">Добавить новость</v-btn>
    </div>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "News",
  data() {
    return {
      page: 'home',
      newNew: {
        title: '',
        text: ''
      },
      titleRules: [
        v => !!v || 'Необходимо ввести заголовок'
      ],
      alertError: false,
      alertSuccess: false,
      alertMsg: '',
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
  }
  ,
  methods: {
    loadData() {

    }
    ,
    openAdd() {

    }
  }
}
</script>

<style scoped>

</style>