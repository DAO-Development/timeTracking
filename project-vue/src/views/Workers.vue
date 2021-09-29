<template>
  <div class="flex-main">
    <Menu class="flex-sidebar"/>
    <div class="workers flex-content">
      <div class="summary-box">
        <div class="summary-box__title">
          <h3>Работники</h3>
          <div class="addition-btn" @click="all = true" v-if="!all">
            К списку работников
            <back-icon/>
          </div>
        </div>
        <div class="workers-all" v-if="all">
          <div class="content-list__filters">
            <v-text-field placeholder="Фамилия Имя" v-model="filter.name" outlined @change="changeName"></v-text-field>
            <v-select v-model="filter.position" :items="selects" placeholder="Должность" @change="changeName"
                      outlined></v-select>
            <v-text-field placeholder="Почта" v-model="filter.email" outlined></v-text-field>
          </div>
          <v-list three-line class="workers__list content-list">
            <template v-for="profile in profiles">
              <v-list-item :key="profile.id" @click="openProfile(profile)"
                           v-if="profile.active !== archive && profile.auth_user_id.email.includes(filter.email) && (profile.name + ' ' + profile.lastname).includes(filter.name)  && (profile.position===filter.position || filter.position === 'Все')">
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
                  <v-icon color="grey lighten-1" @click="deleteUser(profile.auth_user_id.email)">$deleteIcon</v-icon>
                </v-list-item-action>
              </v-list-item>
            </template>
            <div class="content-list__btns">
              <v-list-item class="content-list__btns-add" @click="addForm=true">
                <v-list-item-icon>
                  <v-icon>mdi-plus</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Добавить работника</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item class="content-list__btns-add" @click="archive=!archive">
                <v-list-item-icon>
                  <v-icon>$archive</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Архив</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </div>
          </v-list>
        </div>
        <div class="workers-open" v-if="!all">
          <div class="profile__image">
            <v-img :lazy-src="require('../../../media'+currentProfile.photo_path)"
                   :src="require('../../../media'+currentProfile.photo_path)"></v-img>
            <div class="profile__change-photo">Сменить фото</div>
          </div>
          <div class="profile__info">
            <h3>Личная информация</h3>
            <ul>
              <li>
                <span class="profile__info-title">Имя</span>
                <span class="profile__info-content">{{ currentProfile.name }}</span>
              </li>
              <li>
                <span class="profile__info-title">Фамилия</span>
                <span class="profile__info-content">{{ currentProfile.lastname }}</span>
              </li>
              <li>
                <span class="profile__info-title">Должность</span>
                <span class="profile__info-content">{{ currentProfile.position }}</span></li>
            </ul>
            <h3>Контакты</h3>
            <ul>
              <li>
                <span class="profile__info-title">Телефон</span>
                <span class="profile__info-content">{{ currentProfile.phone }}</span>
              </li>
              <li>
                <span class="profile__info-title">E-mail</span>
                <span class="profile__info-content">{{ currentProfile.auth_user_id.email }}</span>
              </li>
            </ul>
          </div>
        </div>
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
import BackIcon from "../components/icons/backIcon";

export default {
  name: "Workers",
  components: {BackIcon, PdfIcon, Menu},
  data() {
    return {
      page: 'home',
      all: true,
      archive: false,
      profiles: {},
      positions: ["Администратор", "Маляр", "Строитель"],
      selects: ["Все", "Администратор", "Маляр", "Строитель"],
      newProfile: {
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: false,
      },
      currentProfile: {
        auth_user_id: "",
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: false,
        active: true
      },
      filter: {
        name: "",
        position: "Все",
        email: ""
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
    changeName() {
      console.log((this.filter.position === "Все" || this.filter.position === "Администратор") && true)
    },
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
          this.alertMsg = "Пользователь добавлен"
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
    deleteUser(email) {
      console.log(email)
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "DELETE",
        data: {
          email: email,
        },
        success: () => {
          this.alertMsg = "Пользователь удален"
          this.loadData()
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
    openProfile(profile) {
      this.currentProfile = profile
      this.all = false
    }
  }
}
</script>

<style scoped>

</style>