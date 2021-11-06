<template>
  <div class="index flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Новости</h3>
        <div class="addition-btn" @click="$router.go(-1)">
          <span>К списку новостей</span>
          <back-icon/>
        </div>
      </div>
      <div class="news-open">
        <h4>{{ currentNew.title }}</h4>
        <div class="news-open__image">
          <v-img v-if="currentNew.photo_path" :src="$hostname+'media'+currentNew.photo_path"></v-img>
        </div>
        <div class="news-open__text" v-html="currentNew.text"></div>
      </div>
    </div>
  </div>
</template>

<script>
import BackIcon from "../components/icons/backIcon";
import $ from "jquery";

export default {
  name: "NewOpen",
  components: {BackIcon},
  props: {
    id: [String, Number],
  },
  created() {
    console.log(this.currentNew)
    $.ajax({
      url: this.$hostname + "time-tracking/news/" + this.id,
      type: "GET",
      success: (response) => {
        this.currentNew = response.data.data[0]
        console.log(this.currentNew)
      },
      error: (response) => {
        this.alertError = true
        this.alertMsg = "Непредвиденная ошибка"
        console.log(response.data)
      },
    })
  },
  data() {
    return {
      currentNew: null
    }
  }
}
</script>

<style scoped>

</style>