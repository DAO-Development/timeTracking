<template>
  <div class="header">
    <div class="header__left">
      <img class="header__logo" src="../assets/logo.png" alt="logo.png">
    </div>
    <div class="header__right">
      <div class="header__datetime">
        <span>{{ date }}</span> <span class="line"></span> <span>{{ time }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",
  created() {
    this.refreshTime()
    setInterval(() => {
      this.refreshTime()
    }, 1000)
  },
  computed: {
    date: function () {
      let now = new Date()
      return now.getDate() + "." + (now.getMonth() + 1) + "." + now.getFullYear()
    },
  },
  data() {
    return {
      time: ''
    }
  },
  methods: {
    refreshTime() {
      let now = new Date()
      let minutes = now.getMinutes()
      if (minutes < 10)
        minutes = "0" + minutes
      this.time = now.getHours() + ":" + minutes
    },
  }
}
</script>

<style scoped>

</style>