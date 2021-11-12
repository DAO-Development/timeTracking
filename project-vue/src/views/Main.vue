<template>
  <div class="index news flex-content">
    <div class="header">
      <div class="header__left">
        <img class="header__logo" src="src/assets/logo.png" loading="lazy" alt="logo.png">
      </div>
      <div class="header__right">
        <div class="header__datetime">
          <span>{{ date }}</span> <span>|</span> <span>{{ time }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Main.vue"
}
</script>

<style scoped>

</style>