<template>
  <div class="purchases flex-content">
    <Header/>
    <section class="summary-box">
      <div class="summary-box__title">
        <h1>Продажи</h1>
        <div class="addition-btn" @click="$router.push({name: 'Sales'})">
          <span>К списку чеков</span>
          <back-icon/>
        </div>
      </div>
      <div class="purchases__content">
      </div>
    </section>
  </div>
</template>

<script>
import BackIcon from "../../components/icons/backIcon";
import Header from "../../components/Header";

export default {
  name: "SalesOpen",
  components: {Header, BackIcon}
}
</script>

<style scoped>

</style>