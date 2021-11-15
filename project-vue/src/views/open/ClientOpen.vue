<template>
  <div class="clients flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Клиенты</h3>
        <div class="addition-btn" @click="$router.go(-1)">
          <span>К списку клиентов</span>
          <back-icon/>
        </div>
      </div>
      <div class="clients-open workers-open">
        <div class="profile__image clients-open__image">
          <v-img
              v-if="currentClient.logo_path" :lazy-src="$hostname+'media'+currentClient.logo_path"
              :src="$hostname+'media'+currentClient.logo_path"></v-img>
          <div class="profile__change-photo" @click="photoDialog = true">Сменить фото</div>
        </div>
        <div class="profile__info">
          <h3>Общая информация</h3>
          <ul>
            <li>
              <span class="profile__info-title">Название</span>
              <span class="profile__info-content">{{ currentClient.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Краткое название</span>
              <span class="profile__info-content">{{ currentClient.short_name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Отрасль</span>
              <span class="profile__info-content">{{ currentClient.branch }}</span>
            </li>
            <li>
              <span class="profile__info-title">ОГРН</span>
              <span class="profile__info-content">{{ currentClient.ogrn }}</span>
            </li>
          </ul>
          <h3>Контакты</h3>
          <ul>
            <li>
              <span class="profile__info-title">Телефон</span>
              <span class="profile__info-content">{{ currentClient.phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">E-mail</span>
              <span class="profile__info-content">{{ currentClient.email }}</span>
            </li>
            <li>
              <span class="profile__info-title">Сайт</span>
              <span class="profile__info-content">{{ currentClient.site }}</span>
            </li>
          </ul>

          <div class="profile__info profile__info-full" v-if="full">
            <h3>Адреса</h3>
            <ul>
              <li>
                <span class="profile__info-title">Юридический адрес</span>
                <span class="profile__info-content"
                      v-if="currentClient.business_address !== null || currentClient.business_address.city !== ''">{{
                    currentClient.business_address.index
                  }} {{ currentClient.business_address.country }}, г.{{
                    currentClient.business_address.city
                  }}, {{ currentClient.business_address.street }}, д.{{
                    currentClient.business_address.house
                  }}, {{ currentClient.business_address.entrance }}, кв.{{ currentClient.business_address.flat }}</span>
              </li>
              <li>
                <span class="profile__info-title">Адрес доставки</span>
                <span class="profile__info-content"
                      v-if="currentClient.warehouse_address.city !== ''">{{
                    currentClient.warehouse_address.index
                  }} {{ currentClient.warehouse_address.country }}, г.{{
                    currentClient.warehouse_address.city
                  }}, {{ currentClient.warehouse_address.street }}, д.{{
                    currentClient.warehouse_address.house
                  }}, {{ currentClient.warehouse_address.entrance }}, кв.{{
                    currentClient.warehouse_address.flat
                  }}</span>
              </li>
            </ul>
            <h3>Банковская информация</h3>
            <ul>
              <li>
                <span class="profile__info-title">Банковский счет</span>
                <span class="profile__info-content">{{ currentClient.bank_account }}</span>
              </li>
              <li>
                <span class="profile__info-title">Банк</span>
                <span class="profile__info-content">{{ currentClient.bank }}</span>
              </li>
              <li>
                <span class="profile__info-title">BIC/SWIFT</span>
                <span class="profile__info-content">{{ currentClient.bic }}</span>
              </li>
              <li>
                <span class="profile__info-title">НДС</span>
                <span class="profile__info-content">{{ currentClient.vat }}%</span>
              </li>
            </ul>
            <h3>Электронные счета</h3>
            <ul>
              <li>
                <span class="profile__info-title">Оператор электронных счетов</span>
                <span class="profile__info-content">{{ currentClient.account_operator }}</span>
              </li>
              <li>
                <span class="profile__info-title">Индекс посредника</span>
                <span class="profile__info-content">{{ currentClient.index_operator }}</span>
              </li>
              <li>
                <span class="profile__info-title">Номер электронных счетов</span>
                <span class="profile__info-content">{{ currentClient.electronic_number }}</span>
              </li>
              <li>
                <span class="profile__info-title">Email для счетов</span>
                <span class="profile__info-content">{{ currentClient.account_email }}</span>
              </li>
            </ul>
          </div>
          <div class="open__actions">
            <div class="addition-btn" @click="full = !full">
              <span v-if="full">Скрыть полную информацию</span>
              <span v-if="!full">Показать полную информацию</span>
            </div>
            <div class="addition-btn" @click="$router.push({name: 'ClientsEmployees', params: {idClient: id}})">
              Контакты
            </div>
          </div>
          <div class="news-open__actions open__actions">
            <div class="addition-btn" @click="openEditForm">
              <edit-icon/>
              Редактировать клиента
            </div>
            <div class="addition-btn" v-if="currentClient.active" @click="archiveClientOpen">
              <archive-icon/>
              Архивировать клиента
            </div>
            <div class="addition-btn" v-if="!currentClient.active" @click="archiveClientOpen">
              <archive-icon/>
              Удалить из архива клиента
            </div>
            <div class="addition-btn" v-if="!currentClient.active" @click="confirmDeleteDialog = true">
              <waste-icon/>
              Удалить клиента
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
          <v-form ref="addForm" :model="currentClient">
            <v-row>
              <v-text-field placeholder="Название юрлица*" v-model="currentClient.name" :rules="reqRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Краткое название*" v-model="currentClient.short_name" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-combobox placeholder="Отрасль*" v-model="currentClient.branch" :items="selectsBranch" :rules="reqRules"
                          required outlined></v-combobox>
              <v-text-field placeholder="ОГРН*" v-model="currentClient.ogrn" :rules="reqRules" required
                            outlined></v-text-field>
            </v-row>
            <h4>Юридический адрес</h4>
            <v-row>
              <v-text-field placeholder="Страна*" v-model="currentClient.business_address.country" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Город*" v-model="currentClient.business_address.city" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Улица*" v-model="currentClient.business_address.street" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Индекс*" v-model="currentClient.business_address.index" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Дом*" v-model="currentClient.business_address.house" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Подъезд" v-model="currentClient.business_address.entrance"
                            outlined></v-text-field>
              <v-text-field placeholder="Квартира" v-model="currentClient.business_address.flat"
                            outlined></v-text-field>
            </v-row>
            <h4>Адрес доставки</h4>
            <v-row>
              <v-text-field placeholder="Страна" v-model="currentClient.warehouse_address.country"
                            outlined></v-text-field>
              <v-text-field placeholder="Город" v-model="currentClient.warehouse_address.city" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Улица" v-model="currentClient.warehouse_address.street"
                            outlined></v-text-field>
              <v-text-field placeholder="Индекс" v-model="currentClient.warehouse_address.index"
                            outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Дом" v-model="currentClient.warehouse_address.house" outlined></v-text-field>
              <v-text-field placeholder="Подъезд" v-model="currentClient.warehouse_address.entrance"
                            outlined></v-text-field>
              <v-text-field placeholder="Квартира" v-model="currentClient.warehouse_address.flat"
                            outlined></v-text-field>
            </v-row>
            <h4>Контакты</h4>
            <v-row>
              <v-text-field placeholder="Телефон*" v-model="currentClient.phone" :rules="phoneRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Почта*" v-model="currentClient.email" :rules="emailRules" required
                            outlined></v-text-field>
            </v-row>
            <v-text-field placeholder="Сайт" v-model="currentClient.site" outlined></v-text-field>
            <h4>Банковская информация</h4>
            <v-text-field placeholder="Номер счета в банке*" v-model="currentClient.bank_account"
                          outlined></v-text-field>
            <v-row>
              <v-text-field placeholder="Банк" v-model="currentClient.bank" outlined></v-text-field>
              <v-text-field placeholder="BIC/SWIFT" v-model="currentClient.bic" outlined></v-text-field>
            </v-row>
            <v-select v-model="currentClient.vat" :items="selectsVat" placeholder="НДС" item-text="text"
                      item-value="value"
                      outlined></v-select>
            <v-row>
              <v-text-field placeholder="Оператор эл. счетов" v-model="currentClient.account_operator"
                            outlined></v-text-field>
              <v-text-field placeholder="Индекс посредника" v-model="currentClient.index_operator"
                            outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Номер эл. счетов" v-model="currentClient.electronic_number"
                            outlined></v-text-field>
              <v-text-field placeholder="Email для счетов" v-model="currentClient.account_email"
                            outlined></v-text-field>
            </v-row>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="editClient">{{ formBtnText }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление клиента
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить клиента? Отменить это действие будет невозможно</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteClient">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="photoDialog" max-width="500">
      <v-card>
        <v-card-title>
          Сменить фото
        </v-card-title>
        <v-card-text>
          <v-file-input v-model="photoField" placeholder="Логотип организации" accept="image"
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
import $ from "jquery";
import BackIcon from "../../components/icons/backIcon";
import WasteIcon from "../../components/icons/wasteIcon";
import EditIcon from "../../components/icons/editIcon";
import ArchiveIcon from "../../components/icons/archiveIcon";

export default {
  name: "ClientOpen",
  components: {ArchiveIcon, EditIcon, WasteIcon, BackIcon},
  props: {
    id: [String, Number],
  },
  data() {
    return {
      page: 'clients',
      employees: [],
      currentClient: {
        id: 0,
        name: '',
        short_name: '',
        ogrn: '',
        business_address: {
          index: '',
          country: '',
          city: '',
          street: '',
          house: '',
          entrance: '',
          flat: '',
        },
        warehouse_address: {
          index: '',
          country: '',
          city: '',
          street: '',
          house: '',
          entrance: '',
          flat: '',
        },
        phone: '',
        email: '',
        site: '',
        vat: 0,
        branch: '',
        bank_account: '',
        bank: '',
        bic: '',
        account_operator: '',
        index_operator: '',
        electronic_number: '',
        account_email: '',
        logo_path: '',
        active: true
      },
      selectsVat: [
        {text: '0%', value: 0},
        {text: '10%', value: 10},
        {text: '20%', value: 20},
      ],
      selectsBranch: [],
      photoField: null,
      full: false,
      formTitle: "Редактирование клиента",
      formBtnText: "Сохранить",
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
  created() {
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients/" + this.id,
        type: "GET",
        success: (response) => {
          this.currentClient = response.data.data[0]
          if (this.currentClient.warehouse_address == null) {
            this.currentClient.warehouse_address = {
              index: '',
              country: '',
              city: '',
              street: '',
              house: '',
              entrance: '',
              flat: '',
            }
          }
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
    loadEmployees() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients/employees/" + this.id,
        type: "GET",
        success: (response) => {
          this.employees = response.data.data
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
    loadBranches() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients/branches",
        type: "GET",
        success: (response) => {
          this.selectsBranch = response.data.branches
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
        }
      })
    },
    archiveClientOpen() {
      this.currentClient.active = !this.currentClient.active
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "PUT",
        data: this.currentClient,
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
    editClient() {
      console.log("edit")
      if (this.$refs.addForm.validate()) {
        this.currentClient.business_address = JSON.stringify(this.currentClient.business_address)
        this.currentClient.warehouse_address = JSON.stringify(this.currentClient.warehouse_address)
        $.ajax({
          url: this.$hostname + "time-tracking/clients",
          type: "PUT",
          data: this.currentClient,
          success: () => {
            this.addForm = false
            this.loadData()
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
          }
        })
      } else {
        console.log("Заполните обязательные поля")
        this.alertMsg = "Заполните обязательные поля"
        this.alertError = true
      }
    },
    deleteClient() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "DELETE",
        data: {
          id: this.currentClient.id
        },
        success: () => {
          this.confirmDeleteDialog = false
          this.$router.push({name: 'Clients'})
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "На этого клиента зарегистрированы объекты или контакты"
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
      fd.append('id', this.currentClient.id)
      axios({
        method: 'put',
        url: this.$hostname + "time-tracking/clients",
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
    openEditForm() {
      this.formTitle = "Редактирование клиента"
      this.formBtnText = "Сохранить"
      this.addForm = true
      this.loadBranches()
    },
  },
}
</script>

<style scoped>

</style>