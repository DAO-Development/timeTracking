<template>
  <div class="index flex-content">
    <v-btn class="action-btn" color="primary" @click="goLogin">Войти</v-btn>
  </div>
</template>

<script>
export default {
  name: "Index",
  methods: {
    goLogin() {
      this.$router.push({name: "Login"})
    }
  }
}
</script>

<style scoped>

</style>