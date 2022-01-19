<template>
  <div class="purchases flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Продажи</h1>
      <v-btn class="action-btn" color="primary" @click="openAddForm">
        Добавить
      </v-btn>

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

      <div class="sales__content">
        <div>
          <h3>Статистика</h3>
          <div>Счетов за месяц: {{ sales.length }}</div>
          <div>Клиентов: {{ statistic.count_clients }}</div>
          <div>Сумма без налога {{ statistic.sum }}</div>
          <div>Сумма с налогом {{ statistic.sum_tax }}</div>
        </div>
        <template v-for="cheque in sales">
          <div class="purchases-single" :key="cheque.id">
            <v-img width="50" height="50" v-if="photos[cheque.id].length !== 0"
                   :src="$hostname+'media'+photos[cheque.id][0].path"></v-img>
            <div class="purchases-single__btns">
              <v-btn float color="primary" @click="$router.push({name: 'SalesOpen', params: {id: cheque.id}})">
                <v-icon>mdi-format-list-bulleted-square</v-icon>
              </v-btn>
              <v-btn float color="primary" @click="openEditForm(cheque)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn float color="primary" @click="currentSale = cheque.id; confirmDeleteDialog = true">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
            <ul>
              <li>Клиент: {{ cheque.client.name }}</li>
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
            <v-text-field v-model="newSale.object_number" label="Номер объекта" outlined></v-text-field>
            <v-select v-model="newSale.payment_terms" label="Срок оплаты" :items="terms" item-value="id"
                      item-text="days" outlined></v-select>
            <v-text-field v-model="newSale.number_link" label="Номер ссылки" outlined></v-text-field>
            <v-file-input v-if="formTitle === 'Добавление'" v-model="newPhotos" multiple counter
                          label="Фото или документы" outlined prepend-icon=""></v-file-input>
            <v-row>
              <v-col cols="11"><h3>Товары/услуги</h3></v-col>
              <v-col cols="1">
                <v-btn color="primary" fab x-small @click="addNewItem">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-col>
            </v-row>

            <template v-for="i in itemsQuantity">
              <div :key="i">
                <v-row>
                  <v-col cols="1">
                    <strong style="font-size: 20px">{{ i }}</strong>
                  </v-col>
                  <v-col cols="10">
                    <v-text-field v-model="newItems[i-1].name" label="Название"
                                  :rules="reqRules" outlined></v-text-field>
                  </v-col>
                  <v-col cols="1">
                    <v-btn icon @click="deleteNewItem(i)">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-text-field type="number" v-model="newItems[i-1].price" label="Стоимость без налога"
                                  :rules="reqRules" outlined></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="10">
                    <v-text-field type="number" v-model="newItems[i-1].tax" label="Налог"
                                  :rules="reqRules" outlined></v-text-field>
                  </v-col>
                  <v-col cols="2">
                    <v-text-field type="number" v-text="(newItems[i-1].price * (1+newItems[i-1].tax/100)).toFixed(2)"
                                  label="Стоимость с налогом" outlined disabled></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="10">
                    <v-text-field v-model="newItems[i-1].discount" label="Скидка" outlined></v-text-field>
                  </v-col>
                  <v-col cols="2">
                    <v-text-field type="number"
                                  v-text="(newItems[i-1].price * (1+newItems[i-1].tax/100) * (1-newItems[i-1].discount/100)).toFixed(2)"
                                  label="Стоимость со скидкой" outlined disabled></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6">
                    <v-text-field type="number" v-model="newItems[i-1].quantity"
                                  label="Количество" outlined :rules="reqRules"></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field v-model="newItems[i-1].measurement"
                                  label="Единицы измерения" outlined :rules="reqRules"></v-text-field>
                  </v-col>
                </v-row>
              </div>
            </template>

            <v-textarea v-model="newSale.description" label="Пояснение к счету" outlined></v-textarea>
            <v-textarea v-model="newSale.comment" label="Заметки" outlined></v-textarea>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
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
      statistic: {
        count_clients: 0,
        sum: 0,
        sum_tax: 0,
      },
      newSale: {
        id: 0,
        client: {
          name: ''
        },
        create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        object_number: '',
        object: {},
        payment_terms: '',
        number_link: '',
        description: '',
        comment: '',
      },
      newPhotos: null,
      itemsQuantity: 0,
      newItems: [],
      deletedItems: [],
      currentSale: 0,
      filter: {
        month: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 7)
      },
      menus: {
        filterMenu: false,
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
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/sales",
        type: "GET",
        data: {
          year: this.filter.month.substr(0, 4),
          month: this.filter.month.substr(5, 2)
        },
        success: (response) => {
          this.sales = response.data.data
          this.photos = response.data.photos
          this.items = response.data.items
          this.statistic = response.data.statistic
          this.sales.forEach(sale => {
            sale.object.label = sale.object.city + ' ' + sale.object.street + ' ' + sale.object.house
          })
          if (this.sales.length !== 0)
            this.newSale.id = this.sales[0].id + 1
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
      let client;
      if ((typeof this.newSale.client) === 'object')
        client = this.newSale.client.id
      else
        client = this.newSale.client
      $.ajax({
        url: this.$hostname + "time-tracking/objects/" + client,
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
          this.newSale.items = JSON.stringify(this.newItems)
          $.ajax({
            url: this.$hostname + "time-tracking/cheque/sales",
            type: "POST",
            data: this.newSale,
            success: (request) => {
              if (this.newPhotos.length > 0) {
                this.addChequeDocuments(request.data.id)
              } else {
                this.loadData()
                this.addForm = false
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
          });
    },
    putSale() {
      this.newSale.items = JSON.stringify(this.newItems)
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/sales",
        type: "PUT",
        data: this.newSale,
        success: () => {
          this.putItems()
          if (this.newPhotos !== null) {
            this.addChequeDocuments(this.newSale.id)
          } else {
            this.loadData()
            this.addForm = false
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
    },
    putItems() {
      this.newItems.forEach(item => {
        if (item.id !== undefined) {
          $.ajax({
            url: this.$hostname + "time-tracking/item",
            type: "PUT",
            data: item,
            success: () => {
              console.log('товар отредактирован')
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
      })
      this.deletedItems.forEach(item => {
        this.deleteItem(item)
      })
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
    },
    deleteItem(item) {
      $.ajax({
        url: this.$hostname + "time-tracking/item",
        type: "DELETE",
        data: {
          sale_id: this.newSale.id,
          id: item.id
        },
        success: () => {
          console.log('товар удален')
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
    addNewItem() {
      this.itemsQuantity += 1
      this.newItems.push({name: '', price: '', tax: '', discount: '', quantity: '', measurement: ''})
    },
    deleteNewItem(i) {
      if (this.newItems[i - 1].id !== undefined) {
        this.deletedItems.push(this.newItems[i - 1])
      }
      this.itemsQuantity = this.itemsQuantity - 1
      this.newItems.splice(i - 1, 1)
    },
    openAddForm() {
      this.formTitle = 'Добавление'
      this.edit = false
      this.addForm = true
      this.itemsQuantity = 0
      this.newItems = []
      this.newPhotos = null
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
        comment: '',
      }
      if (this.sales.length !== 0)
        this.newSale.id = this.sales[0].id + 1
      else
        this.newSale.id = 10000
    },
    openEditForm(item) {
      this.newSale = item
      this.loadObjectsByCLient()
      this.itemsQuantity = this.items[item.id].length
      this.newItems = this.items[item.id]
      this.formTitle = 'Редактирование'
      this.edit = true
      this.addForm = true
    }
  }
}
</script>

<style scoped>

</style>