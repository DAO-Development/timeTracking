<template>
  <div class="purchases flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Покупки</h1>
      <v-btn class="action-btn" color="primary" @click="formTitle='Добавление'; addForm = true">Добавить</v-btn>

      <v-menu ref="filterMenu" v-model="menus.filterMenu" :close-on-content-click="false" transition="scale-transition"
              offset-y min-width="auto">
        <template v-slot:activator="{ on, attrs }">
          <v-text-field v-model="filter.month" label="Месяц" prepend-icon="mdi-calendar" readonly
                        v-bind="attrs" v-on="on" outlined></v-text-field>
        </template>
        <v-date-picker v-model="filter.month" type="month"
                       :max="(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)"
                       min="1950-01-01" @change="$refs.filterMenu.save(filter.month); loadData()"></v-date-picker>
      </v-menu>

      <div class="purchases__content">
        <div>
          <h3>Статистика</h3>
          <div>Чеков {{ purchases.length }}</div>
          <div>Категорий {{ statistic.count_categories }}</div>
          <div>Сумма {{ statistic.sum }}</div>
          <strong>По каегориям: </strong>
          <template v-for="item in statistic.by_categories">
            <div :key="item.category__name">{{ item.category__name }} - {{ item.price__sum }}</div>
          </template>
        </div>
        <template v-for="cheque in purchases">
          <div class="purchases-single" :key="cheque.id">
            <v-img width="50" height="50" v-if="photos[cheque.id].length !== 0"
                   :src="$hostname+'media'+photos[cheque.id][0].path"></v-img>
            <div class="purchases-single__btns">
              <v-btn float color="primary" @click="$router.push({name: 'PurchaseOpen', params: {id: cheque.id}})">
                <v-icon>mdi-format-list-bulleted-square</v-icon>
              </v-btn>
              <v-btn float color="primary" @click="formTitle='Редактирование'; newPurchase=cheque; addForm=true"
                     v-if="$parent.$parent.edit.indexOf('Бухгалтерия') !== -1">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn float color="primary" @click="currentPurchase = cheque.id; confirmDeleteDialog = true"
                     v-if="$parent.$parent.edit.indexOf('Бухгалтерия') !== -1">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
            <ul>
              <li>Способ оплаты: {{ cheque.payment_method }}</li>
              <li>Налог: {{ cheque.tax.tax }}</li>
              <li>Дата покупки: {{ cheque.date }}</li>
              <li>Место покупки: {{ cheque.place }}</li>
              <li>Категория: {{ cheque.category.name }}</li>
            </ul>
          </div>
        </template>
      </div>
    </section>
    <v-dialog v-model="addForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="addForm = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="form" :model="newPurchase">
            <v-autocomplete v-if="$parent.$parent.admin" v-model="newPurchase.user_profile" outlined
                            label="Ответственный" :items="users" item-text="label" item-value="id"></v-autocomplete>
            <v-row>
              <v-autocomplete v-model="newPurchase.category" :items="categories" item-text="name" item-value="id"
                              label="Категория" :rules="reqRules" required outlined>
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title>
                      Категория не найдена
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
              <v-autocomplete v-model="newPurchase.tax" :items="taxes" item-text="tax" item-value="id"
                              label="Налог" :rules="reqRules" required outlined>
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title>
                      Налог не найден
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
            </v-row>
            <v-select v-model="newPurchase.payment_method" label="Способ оплаты"
                      :items="['Банковская карта', 'Банковский перевод', 'Наличные']" outlined></v-select>
            <v-text-field v-model="newPurchase.number" label="Номер счета" :rules="reqRules" required
                          outlined></v-text-field>
            <v-row>
              <v-menu v-model="menus.dateReceiptMenu" :close-on-content-click="false" :nudge-right="40"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newPurchase.date_receipt" label="Дата получения" readonly v-bind="attrs"
                                v-on="on" outlined></v-text-field>
                </template>
                <v-date-picker v-model="newPurchase.date_receipt"
                               @input="menus.dateReceiptMenu = false"></v-date-picker>
              </v-menu>
              <v-menu v-model="menus.dateMenu" :close-on-content-click="false" :nudge-right="40"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newPurchase.date" label="Дата покупки" readonly v-bind="attrs"
                                v-on="on" outlined></v-text-field>
                </template>
                <v-date-picker v-model="newPurchase.date" @input="menus.dateMenu = false"></v-date-picker>
              </v-menu>
            </v-row>
            <v-text-field v-model="newPurchase.place" label="Место покупки" :rules="reqRules" required
                          outlined></v-text-field>
            <v-text-field type="number" v-model="newPurchase.price" label="Сумма покупок" :rules="numRules"
                          required outlined></v-text-field>
            <v-select v-model="newPurchase.bundle" label="Набор чеков" :items="['Один чек', '2 и более']"
                      outlined></v-select>
            <v-file-input v-if="formTitle === 'Добавление'" v-model="newPhotos" multiple counter
                          label="Фото или документы" outlined prepend-icon=""></v-file-input>
            <v-textarea v-model="newPurchase.comment" label="Заметки" outlined></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addPurchase">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление чеков
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить выбранные чеки? Отменить это действие будет невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deletePurchase">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Header from "../components/Header";
import $ from "jquery";

export default {
  name: "Purchases",
  components: {Header},
  data() {
    return {
      purchases: [],
      taxes: [],
      categories: [],
      users: [],
      photos: [],
      statistic: {
        count_categories: 0,
        sum: 0,
        by_categories: [],
      },
      newPurchase: {
        id: 0,
        user_profile: '',
        date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        date_receipt: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        category: '',
        tax: '',
        payment_method: '',
        number: '',
        place: '',
        price: '',
        bundle: '',
        comment: ''
      },
      newPhotos: '',
      currentPurchase: 0,
      filter: {
        month: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 7)
      },
      menus: {
        filterMenu: false,
        dateMenu: false,
        dateReceiptMenu: false,
      },
      formTitle: 'Добавление',
      addForm: false,
      confirmDeleteDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      numRules: [
        v => v >= 0 || 'Необходимо заполнить поле'
      ],
    }
  },
  created() {
    console.log("init Purchases")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      this.$emit('load-functions')
      if (this.$parent.$parent.read.indexOf('Бухгалтерия') === -1)
        this.$router.push({name: "Index"})
      $.ajaxSetup({
        headers: {
          "Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')),
          "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').attr('value')
        }
      })
      this.loadData()
      this.loadCategories()
      this.loadTax()
      this.loadActiveUsers()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/purchases",
        type: "GET",
        data: {
          year: this.filter.month.substr(0, 4),
          month: this.filter.month.substr(5, 2)
        },
        success: (response) => {
          this.purchases = response.data.data
          this.photos = response.data.photos
          this.statistic = response.data.statistic
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
    loadCategories() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/categories",
        type: "GET",
        success: (response) => {
          this.categories = response.data.data
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
    loadTax() {
      $.ajax({
        url: this.$hostname + "time-tracking/accounting/taxes",
        type: "GET",
        success: (response) => {
          this.taxes = response.data.data
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
    loadActiveUsers() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles/active",
        type: "GET",
        success: (response) => {
          this.users = response.data.data
          this.users.forEach(user => {
            user.label = user.lastname + ' ' + user.name
          })
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
    addPurchase() {
      if (this.$refs.form.validate()) {
        if (this.newPurchase.id !== 0)
          this.putPurchase()
        else {
          $.ajax({
            url: this.$hostname + "time-tracking/cheque/purchases",
            type: "POST",
            data: this.newPurchase,
            success: (request) => {
              console.log("добавление покупки")
              this.addChequeDocuments(request.data.id)
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
        }
      } else {
        this.alertMsg = "Заполните все необходимые поля"
        this.alertError = true
      }
    },
    addChequeDocuments(id) {
      console.log("добавление фото")
      const axios = require('axios')
      // чтение файла в formData
      let fd = new FormData();
      let i = 0
      this.newPhotos.forEach(doc => {
        i++
        fd.append('document' + i, doc)
      })
      fd.append('sales', '')
      fd.append('purchases', id)
      axios({
        method: 'post',
        url: this.$hostname + "time-tracking/cheque/documents",
        headers: {
          "Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')),
          "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').attr('value')
        },
        data: fd
      })
          .then(() => {
            this.loadData()
            this.addForm = false
            this.newPurchase = {
              id: 0,
              user_profile: '',
              date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
              date_receipt: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
              category: '',
              tax: '',
              payment_method: '',
              number: '',
              place: '',
              price: '',
              bundle: '',
              comment: '',
              photo: '',
            }
          });
    },
    putPurchase() {
      if (this.$refs.form.validate())
        $.ajax({
          url: this.$hostname + "time-tracking/cheque/purchases",
          type: "PUT",
          data: this.newPurchase,
          success: () => {
            this.loadData()
            this.addForm = false
            this.newPurchase = {
              id: 0,
              user_profile: '',
              date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
              date_receipt: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
              category: '',
              tax: '',
              payment_method: '',
              number: '',
              place: '',
              price: '',
              bundle: '',
              comment: '',
              photo: '',
            }
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
      else {
        this.alertMsg = "Заполните все необходимые поля"
        this.alertError = true
      }
    },
    deletePurchase() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/purchases",
        type: "DELETE",
        data: {
          id: this.currentPurchase
        },
        success: () => {
          this.loadData()
          this.confirmDeleteDialog = false
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
  }
}
</script>

<style scoped>
.purchases__content {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-gap: 20px;
}
</style>