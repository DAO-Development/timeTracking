<template>
  <div class="purchases flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Продажи</h1>
      <v-btn class="action-btn" color="primary" @click="formTitle='Добавление'; edit = false; addForm = true">
        Добавить
      </v-btn>
      <div class="purchases__content">
        <template v-for="cheque in sales">
          <div class="purchases-single" :key="cheque.id">
            <v-img width="50" height="50" v-if="photos[cheque.id].length !== 0"
                   :src="$hostname+'media'+photos[cheque.id][0].path"></v-img>
            <div class="purchases-single__btns">
              <v-btn float color="primary" @click="$router.push({name: 'SalesOpen', params: {id: cheque.id}})">
                <v-icon>mdi-format-list-bulleted-square</v-icon>
              </v-btn>
              <v-btn float color="primary"
                     @click="formTitle='Редактирование'; edit = true; newSale=cheque; addForm=true">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn float color="primary" @click="currentSale = cheque.id; confirmDeleteDialog = true">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
            <ul>
              <li>Клиент: {{ cheque.object.client_id.name }}</li>
              <li>Объект: {{ cheque.object_number }}</li>
              <li>Дата создания: {{ cheque.create_date }}</li>
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
          <v-form ref="form" :model="newSale">
            <v-text-field v-model="newSale.id" label="Номер квитанции" disabled></v-text-field>
            <v-menu v-model="menus.dateMenu" :close-on-content-click="false" :nudge-right="40"
                    transition="scale-transition" offset-y min-width="auto">
              <template v-slot:activator="{ on, attrs }">
                <v-text-field v-model="newSale.create_date" label="Дата" readonly v-bind="attrs"
                              v-on="on" outlined></v-text-field>
              </template>
              <v-date-picker v-model="newSale.create_date" @input="menus.dateMenu = false"></v-date-picker>
            </v-menu>
            <v-row>
              <v-autocomplete v-model="newSale.client" :items="clients" item-text="name" item-value="id"
                              label="Клиент" :rules="reqRules" required outlined @change="loadObjectsByCLient">
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title>
                      Клиенты не найдены
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
              <v-autocomplete v-model="newSale.object" :items="objects" item-text="label" item-value="id"
                              label="Объект" :rules="reqRules" required outlined>
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title v-if="newSale.client.name === ''">
                      Выберите клиента
                    </v-list-item-title>
                    <v-list-item-title v-else>
                      Объекты не найдены
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
            </v-row>
            <v-text-field v-model=" newSale.object_number
                    " label="Номер объекта" :rules="reqRules" required
                          outlined></v-text-field>
            <v-select v-model="newSale.payment_terms" label="Срок оплаты" :items="terms" item-value="id"
                      item-text="days" outlined></v-select>
            <v-text-field v-model="newSale.number_link" label="Номер ссылки" :rules="reqRules" required
                          outlined></v-text-field>
            <v-file-input v-if="formTitle === 'Добавление'" v-model="newPhotos" multiple counter
                          label="Фото или документы" outlined prepend-icon=""></v-file-input>
            <v-textarea v-model="newSale.description" label="Пояснение к счету" outlined></v-textarea>
            <v-textarea v-model="newSale.comment" label="Заметки" outlined></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addSale">Сохранить</v-btn>
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
          <v-btn color="primary" text @click="deleteSale">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Header from "../components/Header";
import $ from "jquery";

export default {
  name: "Sales",
  components: {Header},
  data() {
    return {
      sales: [],
      clients: [],
      objects: [],
      terms: [],
      items: [],
      photos: [],
      newSale: {
        id: 0,
        client: '',
        create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        object_number: '',
        object: {
          client_id: {
            name: ''
          }
        },
        payment_terms: '',
        number_link: '',
        description: '',
        comment: '',
        items: [1],
      },
      newPhotos: '',
      currentSale: 0,
      menus: {
        dateMenu: false
      },
      edit: false,
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
    console.log("init Sales")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      if (this.$parent.$parent.read.indexOf('Бухгалтерия') === -1)
        this.$router.push({name: "Index"})
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
      this.loadClients()
      this.loadTerms()
    } else {
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/sales",
        type: "GET",
        success: (response) => {
          this.sales = response.data.data
          this.photos = response.data.photos
          if (this.sales.length !== 0)
            this.newSale.id = this.sales[this.sales.length - 1].id + 1
          else
            this.newSale.id = 10000
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
    loadClients() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "GET",
        success: (response) => {
          this.clients = response.data.data
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
    loadTerms() {
      $.ajax({
        url: this.$hostname + "time-tracking/accounting/terms",
        type: "GET",
        success: (response) => {
          this.terms = response.data.data
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
    loadObjectsByCLient() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/" + this.newSale.client,
        type: "GET",
        success: (response) => {
          this.objects = response.data.data
          this.objects.forEach(object => {
            object.label = object.city + ' ' + object.street + ' ' + object.house
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
        },
      })
    },
    addSale() {
      if (this.$refs.form.validate()) {
        if (this.edit)
          this.putSale()
        else {
          $.ajax({
            url: this.$hostname + "time-tracking/cheque/sales",
            type: "POST",
            data: this.newSale,
            success: (request) => {
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
      console.log('Добавление фото')
      const axios = require('axios')
      // чтение файла в formData
      let fd = new FormData();
      let i = 0
      this.newPhotos.forEach(doc => {
        i++
        fd.append('document' + i, doc)
      })
      fd.append('sales', id)
      fd.append('purchases', '')
      axios({
        method: 'post',
        url: this.$hostname + "time-tracking/cheque/documents",
        headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
        data: fd
      })
          .then(() => {
            this.loadData()
            this.addForm = false
            this.newSale = {
              id: 0,
              client: {
                name: ''
              },
              create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
              object_number: '',
              object: '',
              payment_terms: '',
              number_link: '',
              description: '',
              comment: ''
            }
          });
    },
    putSale() {

    },
    deleteSale() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/sales",
        type: "DELETE",
        data: {
          id: this.currentSale
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
    }
  }
}
</script>

<style scoped>

</style>