<template>
  <div class="objects flex-main">
    <div class="flex-sidebar">
      {{ objects }}
    </div>
    <div class="flex-content">
      <v-text-field label="Индекс" v-model="newObject.index" :rules="reqRules" required outlined></v-text-field>
      <v-text-field label="Город" v-model="newObject.city" :rules="reqRules" required outlined></v-text-field>
      <v-btn @click="openAdd">Сохранить объект</v-btn>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'

export default {
  name: "Objects",
  data() {
    return {
      page: 'objects',
      objects: '',
      newObject: {
        id: 0,
        index: '',
        city: '',
        street: '',
        house: '',
        entrance: '',
        flat: '',
        date_start: '',
        date_end: '',
        active: false,
        client_id: ''
      },
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      alertError: false,
      alertSuccess: false,
      alertMsg: '',
    }
  },
  created() {
    if (localStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + localStorage.getItem("auth_token")}
      })
      this.loadData()
    } else if (sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + sessionStorage.getItem("auth_token")}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Login"})
    }
  }
  ,
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "GET",
        success: (response) => {
          this.objects = response.data
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    }
    ,
    openAdd() {

    },
    addObject() {
      if (this.newObject.id === 0) {
        $.ajax({
          url: this.$hostname + "time-tracking/objects",
          type: "POST",
          data: {
            index: this.newObject.index,
            city: this.newObject.city,
            street: this.newObject.street,
            house: this.newObject.house,
            entrance: this.newObject.entrance,
            flat: this.newObject.flat,
            date_start: this.newObject.date_start,
            date_end: this.newObject.date_end,
            active: this.newObject.active,
            client_id: this.newObject.client_id
          },
          success: (response) => {
            console.log("Объект добавлен " + response.data)
          },
          error: (response) => {
            this.alertError = true
            this.alertMsg = "Непредвиденная ошибка"
            console.log(response.data)
          },
        })
      }
    }
  }
}
</script>

<style scoped>

</style>