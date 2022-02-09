<template>
  <div class="contacts flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Контакты</h3>
        <div class="addition-btn" @click="$router.go(-1)">
          <span>К списку контактов</span>
          <back-icon/>
        </div>
      </div>
      <div class="clients-open workers-open">
        <div class="profile__image clients-open__image">
          <v-img
              v-if="currentContact.photo_path" :lazy-src="$hostname+'media'+currentContact.photo_path"
              :src="$hostname+'media'+currentContact.photo_path"></v-img>
          <div v-if="$parent.$parent.edit.indexOf('Контакты') !== -1" class="profile__change-photo"
               @click="photoDialog = true">Сменить фото
          </div>
        </div>
        <div class="profile__info">
          <h3>Общая информация</h3>
          <ul>
            <li>
              <span class="profile__info-title">Имя</span>
              <span class="profile__info-content">{{ currentContact.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Фамилия</span>
              <span class="profile__info-content">{{ currentContact.lastname }}</span>
            </li>
            <li>
              <span class="profile__info-title">Должность</span>
              <span class="profile__info-content"
                    v-if="currentContact.position.name !== null">{{ currentContact.position.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Фирма</span>
              <span class="profile__info-content">{{ currentContact.client.name }}</span>
            </li>
          </ul>
          <h3>Контакты</h3>
          <ul>
            <li>
              <span class="profile__info-title">Телефон</span>
              <span class="profile__info-content">{{ currentContact.phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">Рабочий телефон</span>
              <span class="profile__info-content">{{ currentContact.work_phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">E-mail</span>
              <span class="profile__info-content">{{ currentContact.email }}</span>
            </li>
            <li>
              <span class="profile__info-title">Рабочий E-mail</span>
              <span class="profile__info-content">{{ currentContact.work_email }}</span>
            </li>
          </ul>
          <div class="news-open__actions open__actions" v-if="$parent.$parent.edit.indexOf('Контакты') !== -1">
            <div class="addition-btn" @click="openEditForm">
              <edit-icon/>
              Редактировать контакт
            </div>
            <div class="addition-btn" v-if="currentContact.active" @click="archiveContactOpen">
              <archive-icon/>
              Архивировать контакт
            </div>
            <div class="addition-btn" v-if="!currentContact.active" @click="archiveContactOpen">
              <archive-icon/>
              Удалить из архива
            </div>
            <div class="addition-btn" v-if="!currentContact.active" @click="confirmDeleteDialog = true">
              <waste-icon/>
              Удалить контакт
            </div>
          </div>
        </div>
      </div>
    </div>
    <v-dialog v-model="addForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="addForm=false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="addForm" :model="currentContact">
            <v-row>
              <v-text-field placeholder="Фамилия*" v-model="currentContact.lastname" :rules="reqRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Имя*" v-model="currentContact.name" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-combobox placeholder="Фирма*" v-model="currentContact.client" :items="selectsClient"
                          item-text="name" :rules="reqRules" required outlined></v-combobox>
              <v-combobox placeholder="Должность*" v-model="currentContact.position" :items="selectsPosition"
                          item-value="id" item-text="name" :rules="reqRules" required outlined></v-combobox>
            </v-row>
            <h4>Контакты</h4>
            <v-row>
              <v-text-field placeholder="Телефон" v-model="currentContact.phone" outlined></v-text-field>
              <v-text-field placeholder="Рабочий телефон*" v-model="currentContact.work_phone" :rules="phoneRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Почта" v-model="currentContact.email" required outlined></v-text-field>
              <v-text-field placeholder="Рабочая почта*" v-model="currentContact.work_email" :rules="emailRules"
                            required
                            outlined></v-text-field>
            </v-row>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="editContact">{{ formBtnText }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление контакта
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить контакт и все зависящие от него объекты? Отменить это действие
          будет невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteContact">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="photoDialog" max-width="500">
      <v-card>
        <v-card-title>
          Сменить фото
        </v-card-title>
        <v-card-text>
          <v-file-input v-model="photoField" placeholder="Фото" accept="image"
                        prepend-icon="" outlined></v-file-input>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="savePhoto">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import BackIcon from "../../components/icons/backIcon";
import $ from "jquery";
import WasteIcon from "../../components/icons/wasteIcon";
import EditIcon from "../../components/icons/editIcon";
import ArchiveIcon from "../../components/icons/archiveIcon";

export default {
  name: "ContactOpen",
  components: {ArchiveIcon, EditIcon, WasteIcon, BackIcon},
  props: {
    id: [String, Number]
  },
  data() {
    return {
      page: 'contacts',
      currentContact: {
        id: 0,
        name: '',
        lastname: '',
        position: '',
        phone: '',
        work_phone: '',
        email: '',
        work_email: '',
        client: {
          name: '',
        },
        photo_path: '',
        active: true
      },
      photoField: null,
      selectsClient: [],
      selectsPosition: [],
      formTitle: "Добавление клиента",
      formBtnText: "Добавить клиента",
      addForm: false,
      confirmDeleteDialog: false,
      photoDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      emailRules: [
        v => !!v || 'Необходимо заполнить поле',
        v => /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'Некорректный E-mail',
      ],
      phoneRules: [
        v => !!v || 'Необходимо заполнить поле',
        v => /^(\+)?((\d{2,3}) ?\d|\d)(([ -]?\d)|( ?(\d{2,3}) ?)){5,12}\d$/.test(v) || 'Некорректный номер телефона'
      ],
    }
  },
  created: function () {
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      if (this.$parent.$parent.read.indexOf('Контакты') === -1)
        this.$router.push({name: "Index"})
      this.$emit('set-auth')
      this.$emit('load-functions')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients-employees/" + this.id,
        type: "GET",
        success: (response) => {
          this.currentContact = response.data.data[0]
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    loadPositions() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients-employees/positions",
        type: "GET",
        success: (response) => {
          this.selectsPosition = response.data.positions
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    loadClients() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "GET",
        success: (response) => {
          this.selectsClient = response.data.data
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    archiveContactOpen() {
      this.currentContact.active = !this.currentContact.active
      $.ajax({
        url: this.$hostname + "time-tracking/clients-employees",
        type: "PUT",
        data: this.currentContact,
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    editContact() {
      if (this.$refs.addForm.validate()) {
        this.currentContact.client = this.currentContact.client.id
        this.currentContact.position = this.currentContact.position.id
        $.ajax({
          url: this.$hostname + "time-tracking/clients-employees",
          type: "PUT",
          data: this.currentContact,
          success: () => {
            this.addForm = false
            this.loadData()
          },
          error: (response) => {
            console.log(response)
            if (response.status === 500) {
              this.alertMsg = "Ошибка соединения с сервером"
            } else if (response.status === 401) {
              this.$refresh()
            } else {
              this.alertMsg = "Непредвиденная ошибка"
            }
            this.alertError = true
          }
        })
      } else {
        this.alertMsg = "Заполните все обязательные поля"
        this.alertError = true
      }
    },
    deleteContact() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients-employees",
        type: "DELETE",
        data: {
          id: this.currentContact.id
        },
        success: () => {
          this.confirmDeleteDialog = false
          this.$router.push({name: 'Contacts'})
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    savePhoto() {
      const axios = require('axios')
      // чтение файла в formData
      let fd = new FormData();
      let avatar = this.photoField;
      if (avatar !== null && avatar !== undefined) {
        fd.append('image', avatar)
      } else {
        console.log('ERROR')
        return
      }
      fd.append('id', this.currentContact.id)
      axios({
        method: 'put',
        url: this.$hostname + "time-tracking/clients-employees",
        headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
        data: fd
      })
          .then(response => {
            console.log(response.data.data)
            this.photoDialog = false
            this.photoField = null
            this.loadData()
          });
    },
    openAddForm() {
      this.formTitle = "Добавление контакта"
      this.formBtnText = "Добавить контакт"
      this.addForm = true
    },
    openEditForm() {
      this.loadClients()
      this.loadPositions()
      this.formTitle = "Редактирование контакта"
      this.formBtnText = "Сохранить"
      this.addForm = true
    },
    openConfirmDeleteDialog() {
      this.confirmDeleteDialog = true
    },
  }
}
</script>

<style scoped>

</style>