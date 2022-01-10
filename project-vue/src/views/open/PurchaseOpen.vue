<template>
  <div class="purchases flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Покупки</h1>
      <div class="purchases__content">
        <div>Ответственный: {{ currentPurchase.user_profile.last_name }} {{ currentPurchase.user_profile.name }}</div>
        <div class="document_date">Дата получения: {{ currentPurchase.date_receipt }}</div>
        <div class="document_date">Дата покупки: {{ currentPurchase.date }}</div>
        <div>Категория: {{ currentPurchase.category.name }}</div>
        <div>Налог: {{ currentPurchase.tax.tax }}</div>
        <div>Способ оплаты: {{ currentPurchase.payment_method }}</div>
        <div>Номер счета: {{ currentPurchase.number }}</div>
        <div>Место покупки: {{ currentPurchase.place }}</div>
        <div>Сумма покупки: {{ currentPurchase.price }}</div>
        <div>Количество чеков: {{ currentPurchase.bundle }}</div>
        <div>Заметки: {{ currentPurchase.comment }}</div>

        <strong>Документы:</strong>
        <ul class="documents">
          <template v-for="item in photos">
            <li @click="downloadFile(item.path)" :key="item.id">
              <a>{{ item.path.substr(item.path.lastIndexOf("/") + 1) }}</a>
            </li>
            <v-img :key="item.id"
                   v-if="item.path.substr(item.path.lastIndexOf('.') + 1).toLowerCase() === 'jpg' || item.path.substr(item.path.lastIndexOf('.') + 1).toLowerCase() === 'png'"
                   width="200" height="200" :src="$hostname+'media'+item.path"></v-img>

          </template>
        </ul>
        <!--        <v-btn class="action-btn" color="primary" @click="downloadAll">Скачать все файлы</v-btn>-->
      </div>
    </section>
    <!--    <v-dialog v-model="addForm">-->
    <!--      <v-card>-->
    <!--        <v-toolbar flat>-->
    <!--          <v-spacer></v-spacer>-->
    <!--          <v-btn icon @click="addForm = false">-->
    <!--            <v-icon>mdi-close</v-icon>-->
    <!--          </v-btn>-->
    <!--        </v-toolbar>-->
    <!--        <h3>Добавление</h3>-->
    <!--        <v-card-text>-->
    <!--          <v-form ref="form" :model="newPurchase">-->
    <!--            <v-autocomplete v-if="$parent.$parent.admin" v-model="newPurchase.user_profile"-->
    <!--                            label="Ответственный" :items="users" item-text="label" item-value="id"></v-autocomplete>-->
    <!--            <v-menu v-model="menus.dateReceiptMenu" :close-on-content-click="false" :nudge-right="40"-->
    <!--                    transition="scale-transition" offset-y min-width="auto">-->
    <!--              <template v-slot:activator="{ on, attrs }">-->
    <!--                <v-text-field v-model="newPurchase.date_receipt" label="Дата покупки" readonly v-bind="attrs"-->
    <!--                              v-on="on" outlined></v-text-field>-->
    <!--              </template>-->
    <!--              <v-date-picker v-model="newPurchase.date_receipt" @input="menus.dateReceiptMenu = false"></v-date-picker>-->
    <!--            </v-menu>-->
    <!--            <v-menu v-model="menus.dateMenu" :close-on-content-click="false" :nudge-right="40"-->
    <!--                    transition="scale-transition" offset-y min-width="auto">-->
    <!--              <template v-slot:activator="{ on, attrs }">-->
    <!--                <v-text-field v-model="newPurchase.date" label="Дата покупки" readonly v-bind="attrs"-->
    <!--                              v-on="on" outlined></v-text-field>-->
    <!--              </template>-->
    <!--              <v-date-picker v-model="newPurchase.date" @input="menus.dateMenu = false"></v-date-picker>-->
    <!--            </v-menu>-->
    <!--            <v-autocomplete v-model="newPurchase.category" :items="categories" item-text="name" item-value="id"-->
    <!--                            label="Категория" :rules="reqRules" required outlined>-->
    <!--              <template v-slot:no-data>-->
    <!--                <v-list-item>-->
    <!--                  <v-list-item-title>-->
    <!--                    Категория не найдена-->
    <!--                  </v-list-item-title>-->
    <!--                </v-list-item>-->
    <!--              </template>-->
    <!--            </v-autocomplete>-->
    <!--            <v-autocomplete v-model="newPurchase.tax" :items="taxes" item-text="tax" item-value="id"-->
    <!--                            label="Налог" :rules="reqRules" required outlined>-->
    <!--              <template v-slot:no-data>-->
    <!--                <v-list-item>-->
    <!--                  <v-list-item-title>-->
    <!--                    Налог не найден-->
    <!--                  </v-list-item-title>-->
    <!--                </v-list-item>-->
    <!--              </template>-->
    <!--            </v-autocomplete>-->
    <!--          </v-form>-->
    <!--        </v-card-text>-->
    <!--        <v-card-actions>-->
    <!--          <v-spacer></v-spacer>-->
    <!--          <v-btn class="action-btn" color="primary" @click="addWaybill">Сохранить</v-btn>-->
    <!--        </v-card-actions>-->
    <!--      </v-card>-->
    <!--    </v-dialog>-->
    <!--    <v-dialog v-model="confirmDeleteDialog" max-width="500">-->
    <!--      <v-card>-->
    <!--        <v-card-title>-->
    <!--          Удаление чеков-->
    <!--        </v-card-title>-->
    <!--        <v-card-text>Вы действительно хотите удалить выбранные чеки? Отменить это действие будет невозможно-->
    <!--        </v-card-text>-->
    <!--        <v-card-actions>-->
    <!--          <v-spacer></v-spacer>-->
    <!--          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>-->
    <!--          <v-btn color="primary" text @click="deletePurchase">Подтвердить</v-btn>-->
    <!--        </v-card-actions>-->
    <!--      </v-card>-->
    <!--    </v-dialog>-->
  </div>
</template>

<script>
import Header from "../../components/Header";
import $ from "jquery";

export default {
  name: "PurchaseOpen",
  components: {Header},
  props: {
    id: [String, Number],
  },
  data() {
    return {
      taxes: [],
      categories: [],
      users: [],
      photos: [],
      currentPurchase: {
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
      },
      menus: {
        dateMenu: false,
        dateReceiptMenu: false,
      },
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
    console.log("init Purchases open")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      if (this.$parent.$parent.read.indexOf('Бухгалтерия') === -1)
        this.$router.push({name: "Index"})
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
        url: this.$hostname + "time-tracking/cheque/purchases/" + this.id,
        type: "GET",
        success: (response) => {
          this.currentPurchase = response.data.data[0]
          this.photos = response.data.photos[this.id]
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
    downloadFile(item) {
      console.log(this.$hostname + 'media' + item)
      const axios = require('axios')
      axios({
        url: this.$hostname + 'media' + item,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        var fileURL = window.URL.createObjectURL(new Blob([response.data]));
        var fileLink = document.createElement('a');

        fileLink.href = fileURL;
        fileLink.setAttribute('download', item);
        document.body.appendChild(fileLink);

        fileLink.click();
      });
    },
  }
}
</script>

<style scoped>

</style>