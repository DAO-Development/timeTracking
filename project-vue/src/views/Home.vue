<template>
  <div>Привет, {{ groups }}</div>
  <!--  <v-list v-for="group in groups" :key="group.id">-->
  <!--    <v-list-item>{{ group.name }}</v-list-item>-->
  <!--  </v-list>-->
</template>

<script>
import $ from 'jquery'

export default {
  name: 'Home',
  data() {
    return {
      page: 'home',
      groups: [],
    }
  },
  created() {
    if (localStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + localStorage.getItem("auth_token")}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Login"})
    }
  },
  methods: {
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
