<template>
  <div class="flex-main">
    <Menu class="flex-sidebar"/>
    <div class="workers flex-content">
      <div class="summary-box">
        <h3>Работники</h3>
        <v-list three-line class="workers__list content-list">
          <template v-for="profile in profiles">
            <v-list-item :key="profile.id" v-if="profile.active">
              <v-list-item-avatar class="content-list__image">
                <v-img v-if="profile.photo_path != null" :src="require('../../../media'+profile.photo_path)"></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>{{ profile.name }} {{ profile.lastname }}</v-list-item-title>
                <v-list-item-subtitle>
                  <span>{{ profile.position }}</span><br>
                  <span>{{ profile.auth_user_id.email }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon color="grey lighten-1">$deleteIcon</v-icon>
              </v-list-item-action>
            </v-list-item>
          </template>
          <v-list-item class="content-list__add" @click="addForm=true">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Добавить работника</v-list-item-title>
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
          <h3>Добавление работника</h3>
          <v-card-text>
            <v-text-field placeholder="Фамилия*" v-model="newProfile.lastname" :rules="reqRules" required
                          outlined></v-text-field>
            <v-text-field placeholder="Имя*" v-model="newProfile.name" :rules="reqRules"
                          required outlined></v-text-field>
            <v-combobox ref="positionCombobox" v-model="newProfile.position" :items="positions" placeholder="Должность*"
                        outlined dense></v-combobox>
            <v-text-field placeholder="Почта*" v-model="newProfile.email" :rules="emailRules" required
                          outlined></v-text-field>
            <v-text-field placeholder="Телефон*" v-model="newProfile.phone" :rules="phoneRules"
                          required outlined></v-text-field>
          </v-card-text>
          <v-card-actions>
            <div class="addition-btn">
              <pdf-icon/>
              Конвертировать в .pdf
            </div>
            <v-spacer></v-spacer>
            <v-btn class="action-btn" color="primary" @click="addUser">Добавить работника</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import Menu from "../components/Menu";
import $ from "jquery";
import PdfIcon from "../components/icons/pdfIcon";

export default {
  name: "Workers",
  components: {PdfIcon, Menu},
  data() {
    return {
      page: 'home',
      profiles: {},
      positions: ["Администратор", "Маляр", "Строитель"],
      newProfile: {
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: false,
      },
      addForm: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      emailRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      phoneRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
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
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "GET",
        success: (response) => {
          this.profiles = response.data.data
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    addUser() {
      console.log(this.newProfile.position === "Администратор")
      if (this.newProfile.position === "Администратор") {
        this.newProfile.is_staff = true
      }
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "POST",
        data: {
          username: this.newProfile.email,
          email: this.newProfile.email,
          is_staff: this.newProfile.is_staff,
          password: "12345678"
        },
        success: (response) => {
          this.addProfile(response.data.data.id)
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    addProfile(id) {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "POST",
        data: {
          auth_user_id: id,
          name: this.newProfile.name,
          lastname: this.newProfile.lastname,
          position: this.newProfile.position,
          phone: this.newProfile.phone,
          active: true
        },
        success: () => {
          console.log("Profile is added")
          this.alertMsg = "Пользователь добавлен"
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    closeForm() {
      this.addForm = false
      this.newProfile = {
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: "",
      }
    },
  }
}
</script>

<style scoped>

</style>