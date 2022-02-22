<template>
  <div class="contacts flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Контакты</h3>
        <div class=" addition-btn content-list__filters-mobile" @click="openFilters">
          Фильтры
        </div>
      </div>
      <div class="contacts-all all">
        <div class="content-list__filters">
          <v-icon color="grey lighten-1" @click="closeFilters">
            $deleteIcon
          </v-icon>
          <v-text-field placeholder="ФИО" v-model="filter.name" outlined></v-text-field>
          <v-select v-model="filter.client" :items="['Все'].concat(selectsClient)" item-text="name" placeholder="Клиент"
                    outlined></v-select>
          <v-select v-model="filter.position" :items="[{id: 0, name: 'Все'}].concat(selectsPosition)"
                    item-text="name" item-value="name" placeholder="Должность" outlined></v-select>
        </div>
        <v-list three-line class="clients__list content-list">
          <template v-for="contact in contacts">
            <v-list-item :key="contact.id"
                         v-if="contact.active === !archive && (contact.lastname + ' ' + contact.name).includes(filter.name) && (contact.client.name === filter.client || filter.client === 'Все') && (contact.position.name === filter.position || filter.position === 'Все')">
              <v-list-item-avatar class="content-list__image">
                <v-img v-if="contact.photo_path" :src="$hostname+'media'+contact.photo_path"></v-img>
              </v-list-item-avatar>
              <v-list-item-content @click="$router.push({name: 'ContactOpen', params: {id: contact.id}})">
                <v-list-item-title>{{ contact.lastname }} {{ contact.name }}</v-list-item-title>
                <v-list-item-subtitle>
                  <span>{{ contact.client.name }}, <span v-if="contact.position.name !== null">{{
                      contact.position.name
                    }}</span></span><br>
                  <span>{{ contact.work_email }} {{ contact.work_phone }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action v-if="$parent.$parent.edit.indexOf('Контакты') !== -1">
                <v-icon color="grey lighten-1" @click="openConfirmDeleteDialog(contact)">
                  $deleteIcon
                </v-icon>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
        <v-list class="content-list__btns">
          <v-list-item v-if="!archive && $parent.$parent.edit.indexOf('Контакты') !== -1"
                       class="content-list__btns-add" @click="openAddForm">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Добавить контакт</v-list-item-title>
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
        </v-list>
      </div>
    </div>
    <v-dialog v-model="addForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeForm">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="addForm" :model="newContact">
            <v-row>
              <v-text-field placeholder="Фамилия*" v-model="newContact.lastname" :rules="reqRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Имя*" v-model="newContact.name" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-combobox placeholder="Фирма*" v-model="newContact.client" :items="selectsClient" item-text="name"
                          item-value="id" :rules="reqRules" required outlined></v-combobox>
              <v-combobox placeholder="Должность*" v-model="newContact.position" :items="selectsPosition"
                          item-value="id" item-text="name" :rules="reqRules" required outlined></v-combobox>
            </v-row>
            <h4>Контакты</h4>
            <v-row>
              <v-text-field placeholder="Телефон" v-model="newContact.phone" :rules="phoneRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Рабочий телефон*" v-model="newContact.work_phone" :rules="phoneRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Почта" v-model="newContact.email" :rules="emailRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Рабочая почта*" v-model="newContact.work_email" :rules="emailRules" required
                            outlined></v-text-field>
            </v-row>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addContact">{{ formBtnText }}</v-btn>
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
    <v-dialog v-model="confirmArchiveDialog" max-width="500">
      <v-card>
        <v-card-title>
          Архивирование контакта
        </v-card-title>
        <v-card-text>
          Вы действительно хотите архивировать контакт? После подтверждения контакт будет перемещен в архив
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmArchiveDialog = false">
            Отменить
          </v-btn>
          <v-btn color="primary" text @click="archiveContact">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "Contacts",
  props: {
    idClient: [String, Number, null]
  },
  data() {
    return {
      page: 'contacts',
      archive: false,
      contacts: [],
      newContact: {
        name: '',
        lastname: '',
        position: '',
        phone: '',
        work_phone: '',
        email: '',
        work_email: '',
        client: '',
        photo_path: ''
      },
      currentContact: {
        id: 0,
        active: true
      },
      filter: {
        name: "",
        client: "Все",
        position: "Все"
      },
      selectsClient: [],
      selectsPosition: [],
      formTitle: "Добавление клиента",
      formBtnText: "Добавить клиента",
      addForm: false,
      confirmDeleteDialog: false,
      confirmArchiveDialog: false,
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
  created() {
    console.log("init Contacts")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      if (this.$parent.$parent.read.indexOf('Контакты') === -1)
        this.$router.push({name: "Index"})
      this.$emit('set-auth')
      this.$emit('load-functions')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
      this.loadPositions()
      this.loadClients()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      let url = ""
      if (this.idClient !== null && this.idClient !== undefined) {
        url = "time-tracking/clients/employees/" + this.idClient
        this.filter.client = this.idClient
      } else
        url = "time-tracking/clients-employees"
      $.ajax({
        url: this.$hostname + url,
        type: "GET",
        success: (response) => {
          this.contacts = response.data.data
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
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
          this.selectsPosition = response.data.data
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
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
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
              this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    addContact() {
      if (this.$refs.addForm.validate()) {
        this.newContact.client = this.newContact.client.id
        this.newContact.position = this.newContact.position.id
        $.ajax({
          url: this.$hostname + "time-tracking/clients-employees",
          type: "POST",
          data: this.newContact,
          success: () => {
            this.closeForm()
            this.loadData()
            this.loadPositions()
          },
          error: (response) => {
            switch (response.status) {
              case 500:
                this.alertMsg = "Ошибка соединения с сервером"
                break
              case 400:
                this.alertMsg = "Ошибка в данных"
                break
              case 401:
                this.$refresh()
                break
              case 403:
                this.alertMsg = "Нет доступа"
                break
              default:
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
    archiveContact() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients-employees",
        type: "PUT",
        data: {
          id: this.currentContact.id,
          active: !this.currentContact.active
        },
        success: () => {
          this.loadData()
          this.confirmArchiveDialog = false
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
              this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    deleteContact() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients-employees",
        type: "DELETE",
        data: {
          id: this.currentContact.id
        },
        success: () => {
          this.loadData()
          this.confirmDeleteDialog = false
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
              this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    openAddForm() {
      this.formTitle = "Добавление контакта"
      this.formBtnText = "Добавить контакт"
      this.addForm = true
    },
    openEditForm(item) {
      this.formTitle = "Редактирование контакта"
      this.formBtnText = "Сохранить"
      this.newContact = item
      this.addForm = true
    },
    closeForm() {
      this.addForm = false
      this.alertError = false
      this.newContact = {
        name: '',
        lastname: '',
        position: '',
        phone: '',
        work_phone: '',
        email: '',
        work_email: '',
        client: '',
        photo_path: ''
      }
    },
    openConfirmDeleteDialog(item) {
      this.currentContact.id = item.id
      this.currentContact.active = item.active
      if (this.archive)
        this.confirmDeleteDialog = true
      else
        this.confirmArchiveDialog = true
    },
    openFilters() {
      console.log("open filters")
      $('.content-list__filters').addClass('open')
      $('.content-list__btns').addClass('hidden')
    },
    closeFilters() {
      console.log("open filters")
      $('.content-list__filters').removeClass('open')
      $('.content-list__btns').removeClass('hidden')
    },
  }
}
</script>

<style scoped>

</style>