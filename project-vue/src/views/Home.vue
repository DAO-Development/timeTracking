<template>
  <div>Привет</div>
</template>

<script>
import $ from 'jquery'

export default {
  name: 'Home',
  data() {
    return {
      page: 'home',
    }
  },
  created() {
    if (localStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": localStorage.getItem("auth_token")}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Login"})
    }
  },
  methods: {
    loadData() {

    },
  }
}
</script>
