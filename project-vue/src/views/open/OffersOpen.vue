<template>
  <div class="offers flex-content">
    <Header/>
    <section class="summary-box">
      <div class="summary-box__title">
        <h1>Ценовое предложение</h1>
        <div class="addition-btn" @click="$router.push({name: 'Offers'})">
          <span>К списку предложений</span>
          <back-icon/>
        </div>
      </div>
      <div class="offers__content">
      </div>
    </section>
  </div>
</template>

<script>
import BackIcon from "../../components/icons/backIcon";

export default {
  name: "OffersOpen",
  components: {BackIcon}
}
</script>

<style scoped>

</style>