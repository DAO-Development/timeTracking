<template>
  <div class="flex-main">
    <Menu class="flex-sidebar"/>
    <div class="objects flex-content">
      <div class="summary-box">
        <h3>Объекты</h3>
        <v-list three-line class="workers__list content-list" v-if="all">
          <template v-for="object in objects">
            <v-list-item :key="object.id" v-if="!object.active">
              <v-list-item-content>
                <v-list-item-title>{{ object.city }} {{ object.street }} {{ object.house }}</v-list-item-title>
                <v-list-item-subtitle>
                  <span>{{ object.date_start }} - {{ object.date_end }}</span><br>
                  <span>{{ object.client_id.name }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon color="grey lighten-1" @click="deleteObject(object.id)">$deleteIcon</v-icon>
              </v-list-item-action>
            </v-list-item>
          </template>
          <v-list-item class="content-list__add" @click="addForm=true">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Добавить объект</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </div>
      <v-dialog v-model="addForm" persistent>
        <v-card>
          <v-toolbar flat>
            <v-spacer></v-spacer>
            <v-btn icon @click="closeForm">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-toolbar>
          <h3>Добавление объекта</h3>
          <v-card-text>
            <v-text-field placeholder="Индекс*" v-model="newObject.index" :rules="reqRules" required
                          outlined></v-text-field>
            <v-text-field placeholder="Город*" v-model="newObject.city" :rules="reqRules"
                          required outlined></v-text-field>
            <v-text-field placeholder="Улица*" v-model="newObject.street" :rules="reqRules" required
                          outlined></v-text-field>
            <v-text-field placeholder="Дом*" v-model="newObject.house" :rules="reqRules"
                          required outlined></v-text-field>
            <v-text-field placeholder="Подъезд" v-model="newObject.house" outlined></v-text-field>
            <v-text-field placeholder="Квартира" v-model="newObject.house" outlined></v-text-field>
            <v-combobox ref="positionCombobox" v-model="newObject.client_id" :items="clients" placeholder="Клиент*"
                        outlined dense></v-combobox>
          </v-card-text>
          <v-card-actions>
            <div class="addition-btn">
              <add-photo-icon/>
              Загрузить изображение
            </div>
            <v-spacer></v-spacer>
            <v-btn class="action-btn" color="primary" @click="addObject">Добавить объект</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
import Menu from "../components/Menu";
import AddPhotoIcon from "../components/icons/addPhotoIcon";

export default {
  name: "Objects",
  components: {AddPhotoIcon, Menu},
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
        active: true,
        client_id: ''
      },
      clients: "",
      all: true,
      formTitle: "Добавление объекта",
      addForm: false,
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
          this.objects = response.data.data
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    openEditForm(item) {
      this.newObject = item
      this.addForm = true
    },
    addObject() {
      if (this.newObject.id === 0)
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
          success: () => {
            console.log("Объект добавлен ")
            this.loadData()
            this.closeForm()
          },
          error: (response) => {
            this.alertError = true
            this.alertMsg = "Непредвиденная ошибка"
            console.log(response.data)
          },
        })
      else
        this.editObject()
    },
    editObject() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "PUT",
        data: this.newObject,
        //     {
        //   index: this.newObject.index,
        //   city: this.newObject.city,
        //   street: this.newObject.street,
        //   house: this.newObject.house,
        //   entrance: this.newObject.entrance,
        //   flat: this.newObject.flat,
        //   date_start: this.newObject.date_start,
        //   date_end: this.newObject.date_end,
        //   active: this.newObject.active,
        //   client_id: this.newObject.client_id
        // },
        success: () => {
          console.log("Объект добавлен ")
          this.loadData()
          this.closeForm()
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    deleteObject() {

    },
    closeForm() {
      this.addForm = false
      this.newObject = {
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
      }
    },
  }
}
</script>

<style scoped>

</style>