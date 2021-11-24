<template>
  <div class="groups flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Управление группами пользователей</h1>
      <v-list>
        <v-list-group v-for="group in groups" :key="group.id" v-model="group.active" no-action>
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="group.name"></v-list-item-title>
            </v-list-item-content>
          </template>
          <template v-for="func in functions[group.name]">
            <v-list-item :key="func.text">
              <v-list-item-content>
                <v-list-item-title>{{ func.name }}</v-list-item-title>
                Чтение: {{ func.read }}
                Редактирование: {{ func.edit }}
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list-group>
      </v-list>
    </section>
  </div>
</template>

<script>
import Header from "../components/Header";
import $ from "jquery";

export default {
  name: "Groups",
  components: {Header},
  created() {
    console.log("init Groups")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Login"})
    }
  },
  data() {
    return {
      groups: [],
      functions: [],
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/groups",
        type: "GET",
        success: (response) => {
          this.groups = response.data.groups
          this.functions = response.data.functions
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    }
  },
}
</script>

<style scoped>

</style>