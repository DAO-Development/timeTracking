<template>
  <div class="offers flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Ценовые предложения</h1>
      <v-row>
        <v-btn class="action-btn" color="primary" @click="formTitle='Добавление'; addForm = true">Добавить</v-btn>
        <v-autocomplete v-model="filter.active" label="Статус" :items="status" item-text="name" item-value="value"
                        outlined @change="loadData"></v-autocomplete>
        <v-autocomplete v-model="filter.client" label="Клиент" :items="[{name: 'Все', id: 'Все'}].concat(clients)"
                        item-value="id" item-text="name" outlined @change="loadData"></v-autocomplete>
      </v-row>
      <div class="offers__content">
        <template v-for="offer in offers">
          <div class="offers-single" :key="offer.id">
            <div class="purchases-single__btns">
              <v-btn float color="primary" @click="$router.push({name: 'OffersOpen', params: {id: offer.id}})">
                <v-icon>mdi-format-list-bulleted-square</v-icon>
              </v-btn>
              <v-btn float color="primary" @click="openEditForm(offer)"
                     v-if="$parent.$parent.edit.indexOf('Бухгалтерия') !== -1">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn float color="primary" @click="currentOffer = offer.id; confirmDeleteDialog = true"
                     v-if="$parent.$parent.edit.indexOf('Бухгалтерия') !== -1">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
            <ul>
              <li>Дата создания: {{ offer.create_date }}</li>
              <li v-if="offer.client != null">Клиент: {{ offer.client.name }}</li>
              <li>Срок: {{ offer.term.days }} дней</li>
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
          <v-form ref="form" :model="newOffer">
            <v-row>
              <v-autocomplete v-model="newOffer.client" :items="clients" item-text="name" item-value="id"
                              label="Клиент" :rules="reqRules" required outlined @change="loadObjects">
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title>
                      Клиенты не найдены
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
              <v-autocomplete v-model="newOffer.object" :items="objects" item-text="label" item-value="id"
                              label="Объект" :rules="reqRules" required outlined @change="loadWorkers">
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title>
                      Объекты не найдены
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
              <v-autocomplete v-model="newOffer.contact" :items="contacts" item-text="label" item-value="id"
                              label="Рабочий" outlined>
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title v-if="newOffer.object">
                      Рабочие не найдены
                    </v-list-item-title>
                    <v-list-item-title v-else>
                      Выберите объект
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
            </v-row>
            <v-row>
              <v-autocomplete v-model="newOffer.term" :items="terms" item-text="days" item-value="id"
                              label="Срок предложения" :rules="reqRules" required outlined>
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title>
                      Сроки не найдены
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
            </v-row>


            <v-row>
              <v-col cols="6"><strong>От клиента</strong></v-col>
            </v-row>
            <v-checkbox v-model="newOffer.from_client.material"
                        label="материалы, все крепежи и расходники"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.delivery"
                        label="доставка материала со склада или магазина на объект"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.tool" label="инструмент"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.lifts" label="подъемники"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.scaffolding" label="леса"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.montage_scaffolding" label="монтаж и демонтаж лесов"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.garbage" label="вывоз и утилизация мусора"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.garbage_containers" label="мусорные контейнера"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.security" label="охрана объекта"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.social_room"
                        label="социальные помещения с водой, возможностью переодеваться и поесть, туалет"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.unloading" label="разгрузка материала"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.spreading" label="разнос материала по объекту"></v-checkbox>
            <v-checkbox v-model="newOffer.from_client.cleaning" label="уборка на объекте"></v-checkbox>

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
                    <v-select v-model="newItems[i-1].type" label="Тип"
                              :items="[{name: 'Материал', value: 'material'},{name:  'Услуга', value: 'service'}]"
                              item-text="name" item-value="value" outlined :rules="reqRules"></v-select>
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
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addOffer">Сохранить</v-btn>
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
          <v-btn color="primary" text @click="deleteOffer">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Header from "../components/Header";
import $ from "jquery";
export default {
  name: "Offers",
  components: {Header},
  data() {
    return {
      offers: [],
      items: [],
      terms: [],
      clients: [],
      contacts: [],
      objects: [],
      status: [
        {name: 'Все', value: 'Все'},
        {name: 'Активно', value: true},
        {name: 'Не активно', value: false},
      ],
      newOffer: {
        id: 0,
        create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        active: true,
        term: '',
        client: '',
        object: '',
        contact: '',
        from_client: {
          materials: false,
          delivery: false,
          tool: false,
          lifts: false,
          scaffolding: false,
          montage_scaffolding: false,
          garbage: false,
          garbage_containers: false,
          security: false,
          social_room: false,
          unloading: false,
          spreading: false,
          cleaning: false,
        },
      },
      itemsQuantity: 0,
      newItems: [],
      deletedItems: [],
      currentOffer: 0,
      filter: {
        active: 'Все',
        client: 'Все',
      },
      formTitle: 'Добавление',
      addForm: false,
      confirmDeleteDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
    }
  },
  created() {
    console.log("init Offers")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      this.$emit('load-functions')
      if (this.$parent.$parent.read.indexOf('Бухгалтерия') === -1)
        this.$router.push({name: "Index"})
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
      this.loadClients()
      this.loadTerms()
      this.loadObjects()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/offer",
        type: "GET",
        data: this.filter,
        success: (response) => {
          this.offers = response.data.data
          this.items = response.data.items
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
    },
    loadTerms() {
      $.ajax({
        url: this.$hostname + "time-tracking/accounting/terms",
        type: "GET",
        success: (response) => {
          this.terms = response.data.data
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
    loadObjects() {
      let url = ''
      if (this.newOffer.client)
        url = this.$hostname + "time-tracking/objects/" + this.newOffer.client
      else
        url = this.$hostname + "time-tracking/objects"
      $.ajax({
        url: url,
        type: "GET",
        success: (response) => {
          this.objects = response.data.data
          this.objects.forEach(object => {
            object.label = object.city + ' ' + object.street + ' ' + object.house
          })
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
        },
      })
    },
    loadWorkers() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/employees/" + this.newOffer.object,
        type: "GET",
        success: (response) => {
          this.contacts = response.data.data
          let workers = []
          this.contacts.forEach(contact => {
            workers.push(contact.user_profile_id)
          })
          this.contacts = workers
          this.contacts.forEach(contact => {
            contact.label = contact.name + ' ' + contact.lastname + ', ' + contact.position.name
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
      $.ajax({
        url: this.$hostname + "time-tracking/objects/employees",
        type: "GET",
        success: (response) => {
          this.workers = response.data.data
          this.workers.forEach(worker => {
            worker.label = worker.lastname + ' ' + worker.name + ', ' + worker.position
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
    addOffer() {
      if (this.$refs.form.validate()) {
        this.newOffer.items = JSON.stringify(this.newItems)
        this.newOffer.from_client = JSON.stringify(this.newOffer.from_client)
        if (this.newOffer.id !== 0)
          this.putOffer()
        else {
          $.ajax({
            url: this.$hostname + "time-tracking/offer",
            type: "POST",
            data: this.newOffer,
            success: () => {
              this.loadData()
              this.addForm = false
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
        }
      } else {
        this.alertMsg = "Заполните все необходимые поля"
        this.alertError = true
      }
    },
    putOffer() {
      $.ajax({
        url: this.$hostname + "time-tracking/offer",
        type: "PUT",
        data: this.newOffer,
        success: () => {
          this.putItems()
          this.loadData()
          this.addForm = false
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
    deleteOffer() {
      $.ajax({
        url: this.$hostname + "time-tracking/offer",
        type: "DELETE",
        data: {
          id: this.currentOffer
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
        }
      })
      this.deletedItems.forEach(item => {
        this.deleteItem(item)
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
    addNewItem() {
      this.itemsQuantity += 1
      this.newItems.push({name: '', price: '', tax: '', discount: '', quantity: '', measurement: '', type: ''})
    },
    deleteNewItem(i) {
      if (this.newItems[i - 1].id !== undefined) {
        this.deletedItems.push(this.newItems[i - 1])
      }
      this.itemsQuantity = this.itemsQuantity - 1
      this.newItems.splice(i - 1, 1)
    },
    openAddForm() {
      this.newOffer = {
        id: 0,
        active: true,
        term: '',
        client: '',
      }
      this.itemsQuantity = 0
      this.newItems = []
      this.formTitle = 'Добавление'
      this.addForm = true
    },
    openEditForm(item) {
      this.newOffer = item
      this.itemsQuantity = this.items[item.id].length
      this.newItems = this.items[item.id]
      this.formTitle = 'Редактирование'
      this.addForm = true
    }
  }
}
</script>

<style scoped>
</style>