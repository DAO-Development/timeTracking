<template>
  <div class="clients flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Клиенты</h3>
        <div class=" addition-btn content-list__filters-mobile" @click="openFilters">
          Фильтры
        </div>
      </div>
      <div class="clients-all all">
        <div class="content-list__filters">
          <v-icon color="grey lighten-1" @click="closeFilters">
            $deleteIcon
          </v-icon>
          <v-text-field placeholder="Название" v-model="filter.name" outlined></v-text-field>
          <v-select v-model="filter.branch" :items="['Все'].concat(selectsBranch)" placeholder="Отрасль"
                    outlined></v-select>
        </div>
        <v-list three-line class="clients__list content-list">
          <template v-for="client in clients">
            <v-list-item :key="client.id"
                         v-if="client.active === !archive && client.name.includes(filter.name) && (client.branch === filter.branch || filter.branch === 'Все')">
              <v-list-item-avatar class="content-list__image">
                <v-img v-if="client.logo_path" :src="$hostname+'media'+client.logo_path"></v-img>
              </v-list-item-avatar>
              <v-list-item-content @click="$router.push({name: 'ClientOpen', params: {id: client.id}})">
                <v-list-item-title>{{ client.name }}</v-list-item-title>
                <v-list-item-subtitle>
                  <span>{{ client.phone }}</span><br>
                  <span>{{ client.email }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action v-if="$parent.$parent.edit.indexOf('Клиенты') !== -1">
                <v-icon color="grey lighten-1" @click="openConfirmDeleteDialog(client)">
                  $deleteIcon
                </v-icon>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
        <v-list class="content-list__btns">
          <v-list-item v-if="!archive && $parent.$parent.edit.indexOf('Клиенты') !== -1" class="content-list__btns-add"
                       @click="openAddForm">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Добавить клиента</v-list-item-title>
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
          <v-form ref="addForm" :model="newClient">
            <v-row>
              <v-text-field placeholder="Название юрлица*" v-model="newClient.name" :rules="reqRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Краткое название*" v-model="newClient.short_name" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-combobox placeholder="Отрасль*" v-model="newClient.branch" :items="selectsBranch" :rules="reqRules"
                          required outlined></v-combobox>
              <v-text-field placeholder="ОГРН*" v-model="newClient.ogrn" :rules="reqRules" required
                            outlined></v-text-field>
            </v-row>
            <h4>Юридический адрес</h4>
            <v-row>
              <v-text-field placeholder="Страна*" v-model="newClient.business_address.country" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Город*" v-model="newClient.business_address.city" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Улица*" v-model="newClient.business_address.street" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Индекс*" v-model="newClient.business_address.index" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Дом*" v-model="newClient.business_address.house" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Подъезд" v-model="newClient.business_address.entrance" outlined></v-text-field>
              <v-text-field placeholder="Квартира" v-model="newClient.business_address.flat" outlined></v-text-field>
            </v-row>
            <h4>Адрес доставки</h4>
            <v-row>
              <v-text-field placeholder="Страна" v-model="newClient.warehouse_address.country" outlined></v-text-field>
              <v-text-field placeholder="Город" v-model="newClient.warehouse_address.city" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Улица" v-model="newClient.warehouse_address.street" outlined></v-text-field>
              <v-text-field placeholder="Индекс" v-model="newClient.warehouse_address.index" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Дом" v-model="newClient.warehouse_address.house" outlined></v-text-field>
              <v-text-field placeholder="Подъезд" v-model="newClient.warehouse_address.entrance"
                            outlined></v-text-field>
              <v-text-field placeholder="Квартира" v-model="newClient.warehouse_address.flat" outlined></v-text-field>
            </v-row>
            <h4>Контакты</h4>
            <v-row>
              <v-text-field placeholder="Телефон*" v-model="newClient.phone" :rules="phoneRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Почта*" v-model="newClient.email" :rules="emailReqRules" required
                            outlined></v-text-field>
            </v-row>
            <v-text-field placeholder="Сайт" v-model="newClient.site" outlined></v-text-field>
            <h4>Банковская информация</h4>
            <v-text-field placeholder="Номер счета в банке*" v-model="newClient.bank_account" outlined></v-text-field>
            <v-row>
              <v-text-field placeholder="Банк" v-model="newClient.bank" outlined></v-text-field>
              <v-text-field placeholder="BIC/SWIFT" v-model="newClient.bic" outlined></v-text-field>
            </v-row>
            <v-select v-model="newClient.vat" :items="selectsVat" placeholder="НДС" item-text="text" item-value="value"
                      outlined></v-select>
            <v-row>
              <v-text-field placeholder="Оператор эл. счетов" v-model="newClient.account_operator"
                            outlined></v-text-field>
              <v-text-field placeholder="Индекс посредника" v-model="newClient.index_operator" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Номер эл. счетов" v-model="newClient.electronic_number"
                            outlined></v-text-field>
              <v-text-field placeholder="Email для счетов" v-model="newClient.account_email" outlined></v-text-field>
            </v-row>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addClient">{{ formBtnText }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление клиента
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить фирму? Отменить это действие будет невозможно</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteClient(null)">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmArchiveDialog" max-width="500">
      <v-card>
        <v-card-title>
          Архивирование клиента
        </v-card-title>
        <v-card-text>
          Вы действительно хотите архивировать клиента? После подтверждения клиент будет перемещен в архив
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmArchiveDialog = false">
            Отменить
          </v-btn>
          <v-btn color="primary" text @click="archiveClient">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "Clients",
  data() {
    return {
      page: 'clients',
      archive: false,
      clients: [],
      newClient: {
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
      currentClient: {
        id: 0,
        active: true,
      },
      selectsVat: [
        {text: '0%', value: 0},
        {text: '10%', value: 10},
        {text: '20%', value: 20},
      ],
      selectsBranch: [],
      filter: {
        name: "",
        branch: "Все"
      },
      photoField: null,
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
      emailReqRules: [
        v => !!v || 'Необходимо заполнить поле',
        v => /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'Некорректный E-mail',
      ],
      emailRules: [
        v => /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'Некорректный E-mail',
      ],
      phoneRules: [
        v => !!v || 'Необходимо заполнить поле',
        v => /^(\+)?((\d{2,3}) ?\d|\d)(([ -]?\d)|( ?(\d{2,3}) ?)){5,12}\d$/.test(v) || 'Некорректный номер телефона'
      ],
    }
  },
  created() {
    console.log("init Clients")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      if (this.$parent.$parent.read.indexOf('Клиенты') === -1)
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
        url: this.$hostname + "time-tracking/clients",
        type: "GET",
        success: (response) => {
          this.clients = response.data.data
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
      $.ajax({
        url: this.$hostname + "time-tracking/clients/branches",
        type: "GET",
        success: (response) => {
          this.selectsBranch = response.data.branches
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
    addClient() {
      if (this.$refs.addForm.validate()) {
        $.ajax({
          url: this.$hostname + "time-tracking/clients",
          type: "POST",
          data: {
            name: this.newClient.name,
            short_name: this.newClient.short_name,
            ogrn: this.newClient.ogrn,
            business_address: JSON.stringify(this.newClient.business_address),
            warehouse_address: JSON.stringify(this.newClient.warehouse_address),
            phone: this.newClient.phone,
            email: this.newClient.email,
            site: this.newClient.site,
            vat: this.newClient.vat,
            branch: this.newClient.branch,
            bank_account: this.newClient.bank_account,
            bank: this.newClient.bank,
            bic: this.newClient.bic,
            account_operator: this.newClient.account_operator,
            index_operator: this.newClient.index_operator,
            electronic_number: this.newClient.electronic_number,
            account_email: this.newClient.account_email,
            logo_path: this.newClient.logo_path,
          },
          success: () => {
            this.closeForm()
            this.loadData()
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
        this.alertMsg = "Заполните обязательные поля"
        this.alertError = true
      }
    },
    archiveClient() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "PUT",
        data: {
          id: this.currentClient.id,
          active: !this.currentClient.active
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
    deleteClient() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "DELETE",
        data: {
          id: this.currentClient.id
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
      this.formTitle = "Добавление клиента"
      this.formBtnText = "Добавить клиента"
      this.addForm = true
    },
    openEditForm(item) {
      this.formTitle = "Редактирование клиента"
      this.formBtnText = "Сохранить"
      this.newClient = item
      this.addForm = true
    },
    closeForm() {
      this.addForm = false
      this.alertError = false
      this.newClient = {
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
      }
    },
    openConfirmDeleteDialog(item) {
      this.currentClient.id = item.id
      this.currentClient.active = item.active
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