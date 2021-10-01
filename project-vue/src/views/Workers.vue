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
            <v-text-field placeholder="Фамилия Имя" v-model="filter.name" outlined></v-text-field>
            <v-select v-model="filter.position" :items="selects" placeholder="Должность" outlined></v-select>
            <v-text-field placeholder="Почта" v-model="filter.email" outlined></v-text-field>
          </div>
          <v-list three-line class="workers__list content-list">
            <template v-for="profile in profiles">
              <v-list-item :key="profile.id"
                           v-if="profile.active !== archive && profile.auth_user_id.email.includes(filter.email) && (profile.name + ' ' + profile.lastname).includes(filter.name)  && (profile.position===filter.position || filter.position === 'Все')">
                <v-list-item-avatar class="content-list__image">
                  <v-img v-if="profile.photo_path != null" :src="require('../../../media'+profile.photo_path)"></v-img>
                </v-list-item-avatar>
                <v-list-item-content @click="openProfile(profile)">
                  <v-list-item-title>{{ profile.name }} {{ profile.lastname }}</v-list-item-title>
                  <v-list-item-subtitle>
                    <span>{{ profile.position }}</span><br>
                    <span>{{ profile.auth_user_id.email }}</span>
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-icon color="grey lighten-1" @click="openConfirmDeleteDialog(profile.auth_user_id.email)">
                    $deleteIcon
                  </v-icon>
                </v-list-item-action>
              </v-list-item>
            </template>
            <div class="content-list__btns">
              <v-list-item v-if="!archive" class="content-list__btns-add" @click="addForm=true">
                <v-list-item-icon>
                  <v-icon>mdi-plus</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Добавить работника</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item v-if="!archive" class="content-list__btns-add" @click="archive=!archive">
                <v-list-item-icon>
                  <v-icon>$archive</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Архив</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item v-else class="content-list__btns-add" @click="archive=!archive">
                <v-list-item-icon>
                  <v-icon>$archive</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Выйти из архива</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </div>
          </v-list>
        </div>
        <div class="workers-open" v-if="!all">
          <div class="profile__image">
            <v-img v-if="currentProfile.photo_path != null"
                   :lazy-src="require('../../../media'+currentProfile.photo_path)"
                   :src="require('../../../media'+currentProfile.photo_path)"></v-img>
            <div class="profile__change-photo" @click="photoDialog = true">Сменить фото</div>
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
            <ul>
              <li>
                <span class="profile__info-title">Работает</span>
                <v-checkbox v-model="currentProfile.active" @change="openConfirmArchiveDialog"></v-checkbox>
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
      <v-dialog v-model="confirmDeleteDialog" max-width="500">
        <v-card>
          <v-card-title>
            Удаление работника
          </v-card-title>
          <v-card-text>Вы действительно хотите удалить профиль? Отменить это действие будет невозможно</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
            <v-btn color="primary" text @click="deleteUser(null)">Подтвердить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="confirmArchiveDialog" max-width="500">
        <v-card>
          <v-card-title>
            Увольнение работника
          </v-card-title>
          <v-card-text>
            Вы действительно хотите уволить работника? После подтверждения профиль будет перемещен в архив
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="cancelConfirmArchiveDialog">
              Отменить
            </v-btn>
            <v-btn color="primary" text @click="editProfile">Подтвердить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="photoDialog" max-width="500">
        <v-card>
          <v-card-title>
            Сменить фото
          </v-card-title>
          <v-card-text>
            <v-file-input v-model="photoField" placeholder="Фото профиля" accept="image/*"
                          prepend-icon="" outlined></v-file-input>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="savePhoto">Сохранить</v-btn>
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
        id: 0,
        auth_user_id: "",
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: false,
        active: true,
        photo_path: null,
      },
      filter: {
        name: "",
        position: "Все",
        email: ""
      },
      addForm: false,
      confirmArchiveDialog: false,
      confirmDeleteDialog: false,
      photoField: null,
      photoDialog: false,
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
    editProfile() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "PUT",
        data: {
          id: this.currentProfile.id,
          auth_user_id: this.currentProfile.auth_user_id,
          name: this.currentProfile.name,
          lastname: this.currentProfile.lastname,
          position: this.currentProfile.position,
          phone: this.currentProfile.phone,
          active: this.currentProfile.active,
          // photo_path: this.currentProfile.photo_path
        },
        success: () => {
          console.log("Профиль изменен")
          this.loadData()
          this.confirmArchiveDialog = false
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    savePhoto() {
      console.log(this.photoField.name)
      // let reader = new FileReader();
      this.currentProfile.photo_path = "/users/" + this.photoField.name
      // reader.readAsDataURL(this.photoField)
      // reader.onload = function () {
      //   console.log(reader.result);
      // };
      // reader.onerror = function (error) {
      //   console.log('Error: ', error);
      // };
      // console.log(this.currentProfile.photo_path.toDataURL(this.currentProfile.photo_path.type, 1.0))

      let fd = new FormData();
      let avatar = this.photoField;
      if (avatar !== undefined) {
        fd.append('image', avatar)
      } else {
        console.log("ERROR")
        return
      }

      $.ajax({
        url: this.$hostname + "time-tracking/profiles/" + this.currentProfile.id,
        type: "PUT",
        processData: false,
        data: fd,
        // data: {
        //   photo: this.photoField,
        //   photo_path: this.currentProfile.photo_path
        // },
        success: () => {
          console.log("Профиль изменен")
          this.loadData()
          this.photoDialog = false
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    deleteUser(email) {
      if (email == null) {
        email = this.currentProfile.email
      }
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
          this.confirmDeleteDialog = false
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    openProfile(profile) {
      this.currentProfile = profile
      this.all = false
    },
    closeForm() {
      this.addForm = false
      this.newProfile = {
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: false,
      }
    },
    openConfirmArchiveDialog() {
      if (!this.currentProfile.active) {
        this.confirmArchiveDialog = true
      } else {
        this.editProfile()
      }
    },
    cancelConfirmArchiveDialog() {
      this.currentProfile.active = true
      this.confirmArchiveDialog = false
    },
    openConfirmDeleteDialog(email) {
      this.currentProfile.email = email
      this.confirmDeleteDialog = true
    },
  }
}
</script>

<style scoped>

</style>