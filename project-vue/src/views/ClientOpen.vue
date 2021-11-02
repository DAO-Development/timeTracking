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
              v-if="currentClient.logo_path" :lazy-src="require('../../../media'+currentClient.logo_path)"
              :src="require('../../../media'+currentClient.logo_path)"></v-img>
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
                <span class="profile__info-content">{{
                    currentClient.business_address.index
                  }} {{ currentClient.business_address.country }}, г.{{
                    currentClient.business_address.city
                  }}, {{ currentClient.business_address.street }}, д.{{
                    currentClient.business_address.house
                  }}, {{ currentClient.business_address.entrance }}, кв.{{ currentClient.business_address.flat }}</span>
              </li>
              <li>
                <span class="profile__info-title">Адрес доставки</span>
                <span class="profile__info-content" v-if="currentClient.address_fin !== null">{{
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
          </div>
          <div class="news-open__actions open__actions">
            <div class="addition-btn" @click="openEditForm">
              <edit-icon/>
              Редактировать работника
            </div>
            <div class="addition-btn" @click="this.confirmDeleteDialog = true">
              <waste-icon/>
              Удалить работника
            </div>
          </div>
        </div>
      </div>
    </div>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление работника
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить профиль? Отменить это действие будет невозможно</v-card-text>
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
import BackIcon from "../components/icons/backIcon";
import WasteIcon from "../components/icons/wasteIcon";
import EditIcon from "../components/icons/editIcon";

export default {
  name: "ClientOpen",
  components: {EditIcon, WasteIcon, BackIcon},
  props: {
    id: [String, Number],
  },
  data() {
    return {
      page: 'clients',
      clients: [],
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
      },
      selectsVat: [
        {text: '0%', value: 0},
        {text: '10%', value: 10},
        {text: '20%', value: 20},
      ],
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
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth-token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth-token'))}
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
    editClient() {
      if (this.$refs.addForm.validate()) {
        $.ajax({
          url: this.$hostname + "time-tracking/clients",
          type: "POST",
          data: this.currentClient,
          success: () => {
            this.addForm = false
            this.loadData()
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
      } else {
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
          this.loadData()
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
            // this.currentClient.photo_path = response.data.data.name
            this.loadData()
          });
    },
    openEditForm() {
      this.formTitle = "Редактирование клиента"
      this.formBtnText = "Сохранить"
      this.addForm = true
    },
  },
}
</script>

<style scoped>

</style>