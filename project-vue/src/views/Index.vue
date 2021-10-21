<template>
  <div class="index flex-content">
    <v-btn v-if="!auth" class="action-btn" color="primary" @click="goLogin">Войти</v-btn>
  </div>
</template>

<script>
export default {
  name: "Index",
  created() {
    if (localStorage.getItem('auth_token')) {
      this.auth = true
    } else if (sessionStorage.getItem(('auth_token'))) {
      this.auth = true
    }
  },
  data() {
    return {
      auth: false
    }
  },
  methods: {
    goLogin() {
      this.$router.push({name: "Login"})
    }
  }
}
</script>

<style scoped>

</style>