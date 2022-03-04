<template>
  <div class="purchases flex-content">
    <Header/>
    <section class="summary-box">
      <div class="summary-box__title">
        <h1>Продажи</h1>
        <div class="addition-btn" @click="$router.push({name: 'Sales'})">
          <span>К списку чеков</span>
          <back-icon/>
        </div>
      </div>
      <div class="purchases__content">
        <div v-if="$parent.$parent.edit.indexOf('Бухгалтерия') !== -1" class="open__actions">
          <div class="addition-btn" @click="addForm=true">
            <edit-icon/>
            Редактировать
          </div>
          <div class="addition-btn" @click="confirmDeletePhotoDialog = true">
            <waste-icon/>
            Удалить
          </div>
        </div>
        <v-btn class="action-btn" color="primary" @click="printSale">Скачать</v-btn>
        <div>Номер счета: {{ currentSale.id + 9999 }}</div>
        <div class="document_date">Дата создания: {{ currentSale.create_date }}</div>
        <div class="document_date">Клиент: {{ currentSale.client.name }}</div>
        <div>Объект: {{ currentSale.object.city }} {{ currentSale.object.street }} {{ currentSale.object.house }}</div>
        <div>Номер объекта: {{ currentSale.object_number }}</div>
        <div>Срок оплаты: {{ currentSale.payment_terms.days }} дней</div>
        <div>Номер ссылки: {{ currentSale.number_link }}</div>
        <div>Пояснение: {{ currentSale.description }}</div>
        <div>Заметки: {{ currentSale.comment }}</div>

        <div class="unit-title">
          <h3>Документы:</h3>
          <v-btn color="primary" fab x-small @click="addPhotoDialog = true">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </div>
        <v-list class="documents">
          <template v-for="item in photos">
            <v-list-item :key="item.id">
              <a @click="downloadFile(item.path)">{{ item.path.substr(item.path.lastIndexOf("/") + 1) }}</a>
              <v-list-item-action>
                <v-icon color="grey lighten-1" @click="photoId = item.id; confirmDeletePhotoDialog = true">
                  mdi-close
                </v-icon>
              </v-list-item-action>
            </v-list-item>
            <v-img :key="item.path"
                   v-if="item.path.substr(item.path.lastIndexOf('.') + 1).toLowerCase() === 'jpg' || item.path.substr(item.path.lastIndexOf('.') + 1).toLowerCase() === 'png'"
                   width="200" height="200" :src="$hostname+'media'+item.path"></v-img>

          </template>
        </v-list>
        <h3>Товары:</h3>
        <v-simple-table>
          <template v-slot:default>
            <thead>
            <tr>
              <th class="text-left">№</th>
              <th class="text-left">Название</th>
              <th class="text-left">Стоимость без налога</th>
              <th class="text-left">Налог</th>
              <th class="text-left">Стоимость</th>
              <th class="text-left">Скидка</th>
              <th class="text-left">Количество</th>
              <th class="text-left">Единицы измерения</th>
              <th class="text-left">Итого</th>
            </tr>
            </thead>
            <tfoot>
            <tr>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left">Итого</th>
              <th class="text-left">{{ sum.price.toFixed(2) }}</th>
            </tr>
            <tr>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left">Итого с налогом</th>
              <th class="text-left">{{ sum.tax.toFixed(2) }}</th>
            </tr>
            <tr>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left"></th>
              <th class="text-left">Итого со скидкой</th>
              <th class="text-left">{{ sum.discount.toFixed(2) }}</th>
            </tr>
            </tfoot>
            <tbody>
            <tr v-for="(item, i) in items" :key="item.name">
              <td>{{ i + 1 }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.price }}</td>
              <td>{{ item.tax }}</td>
              <td>{{ (item.price * (1 + item.tax / 100)).toFixed(2) }}</td>
              <td>{{ item.discount }}</td>
              <td>{{ item.quantity }}</td>
              <td>{{ item.measurement }}</td>
              <td>{{ (item.price * (1 + item.tax / 100) * (1 - item.discount / 100) * item.quantity).toFixed(2) }}</td>
            </tr>
            </tbody>
          </template>
        </v-simple-table>
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
        <h3>Редактирование</h3>
        <v-card-text>
          <v-form ref="form" :model="currentSale">
            <v-text-field v-model="currentSale.id" label="Номер квитанции" disabled></v-text-field>
            <v-menu v-model="menus.dateMenu" :close-on-content-click="false" :nudge-right="40"
                    transition="scale-transition" offset-y min-width="auto">
              <template v-slot:activator="{ on, attrs }">
                <v-text-field v-model="currentSale.create_date" label="Дата" readonly v-bind="attrs"
                              v-on="on" outlined></v-text-field>
              </template>
              <v-date-picker v-model="currentSale.create_date" @input="menus.dateMenu = false"></v-date-picker>
            </v-menu>
            <v-row>
              <v-autocomplete v-model="currentSale.client" :items="clients" item-text="name" item-value="id"
                              label="Клиент" :rules="reqRules" required outlined @change="loadObjectsByCLient">
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title>
                      Клиенты не найдены
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
              <v-autocomplete v-model="currentSale.object" :items="objects" item-text="label" item-value="id"
                              label="Объект" :rules="reqRules" required outlined>
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title v-if="currentSale.client.name === ''">
                      Выберите клиента
                    </v-list-item-title>
                    <v-list-item-title v-else>
                      Объекты не найдены
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
            </v-row>
            <v-text-field v-model=" currentSale.object_number
                    " label="Номер объекта" required outlined></v-text-field>
            <v-select v-model="currentSale.payment_terms" label="Срок оплаты" :items="terms" item-value="id"
                      item-text="days" outlined></v-select>
            <v-text-field v-model="currentSale.number_link" label="Номер ссылки" required outlined></v-text-field>

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


            <v-textarea v-model="currentSale.description" label="Пояснение к счету" outlined></v-textarea>
            <v-textarea v-model="currentSale.comment" label="Заметки" outlined></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="putSale">Сохранить</v-btn>
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
    <v-dialog v-model="addPhotoDialog" max-width="500">
      <v-card>
        <v-card-title>
          Добавить документ
        </v-card-title>
        <v-card-text>
          <v-file-input v-model="newPhotos" placeholder="Документы" accept="*" multiple counter
                        prepend-icon="" outlined></v-file-input>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="addPhotoDialog = false; newPhotos = ''">Отменить</v-btn>
          <v-btn color="primary" text @click="addChequeDocuments">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeletePhotoDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление докуметов
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить выбранный документ? Отменить это действие будет невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeletePhotoDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteChequeDocument">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import BackIcon from "../../components/icons/backIcon";
import Header from "../../components/Header";
import $ from "jquery";
import EditIcon from "../../components/icons/editIcon";
import WasteIcon from "../../components/icons/wasteIcon";

export default {
  name: "SalesOpen",
  components: {WasteIcon, EditIcon, Header, BackIcon},
  props: {
    id: [String, Number],
  },
  data() {
    return {
      clients: [],
      objects: [],
      terms: [],
      items: [],
      photos: [],
      currentSale: {
        id: 0,
        client: {
          id: '',
          name: '',
        },
        create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        object_number: '',
        object: {
          city: '',
          street: '',
          house: '',
        },
        payment_terms: '',
        number_link: '',
        description: '',
        comment: '',
        items: [1],
      },
      sum: {
        price: 0,
        tax: 0,
        discount: 0,
      },
      photoId: 0,
      menus: {
        dateMenu: false,
      },
      newPhotos: null,
      newItems: [],
      deletedItems: [],
      itemsQuantity: 0,
      addForm: false,
      addPhotoDialog: false,
      confirmDeleteDialog: false,
      confirmDeletePhotoDialog: false,
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
    console.log("init Sales open")
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
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/sales/" + this.id,
        type: "GET",
        success: (response) => {
          this.currentSale = response.data.data[0]
          this.photos = response.data.photos[this.id]
          this.items = response.data.items[this.id]
          this.newItems = response.data.items[this.id]
          this.itemsQuantity = response.data.items[this.id].length
          this.currentSale.object.label = this.currentSale.object.city + ' ' + this.currentSale.object.street + ' ' + this.currentSale.object.house
          this.sum = {price: 0, tax: 0, discount: 0}
          this.items.forEach(item => {
            this.sum.price += item.price * item.quantity
            this.sum.tax += item.price * (1 + item.tax / 100) * item.quantity
            this.sum.discount += item.price * (1 + item.tax / 100) * (1 - item.discount / 100) * item.quantity
          })
          this.loadObjectsByCLient()
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
    loadObjectsByCLient() {
      let url = ''
      if (this.currentSale.client.id)
        url = this.$hostname + "time-tracking/objects/" + this.currentSale.client.id
      else
        url = this.$hostname + "time-tracking/objects/" + this.currentSale.client
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
    addChequeDocuments() {
      const axios = require('axios')
      // чтение файла в formData
      let fd = new FormData();
      let i = 0
      this.newPhotos.forEach(doc => {
        i++
        fd.append('document' + i, doc)
      })
      fd.append('sales', this.currentSale.id)
      fd.append('purchases', '')
      axios({
        method: 'post',
        url: this.$hostname + "time-tracking/cheque/documents",
        headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
        data: fd
      })
          .then(() => {
            this.loadData()
            this.addPhotoDialog = false
            this.newPhotos = ''
          });
    },
    putSale() {
      this.currentSale.items = JSON.stringify(this.newItems)
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/sales",
        type: "PUT",
        data: this.currentSale,
        success: () => {
          this.putItems()
          if (this.newPhotos !== null) {
            this.addChequeDocuments(this.currentSale.id)
          } else {
            this.loadData()
            this.addForm = false
          }
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
    deleteSale() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/sales",
        type: "DELETE",
        data: {
          id: this.id
        },
        success: () => {
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
    deleteChequeDocument() {
      $.ajax({
        url: this.$hostname + "time-tracking/cheque/documents",
        type: "DELETE",
        data: {
          id: this.photoId
        },
        success: () => {
          this.loadData()
          this.confirmDeletePhotoDialog = false
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
    printSale() {
      let path = ''
      $.ajax({
        url: this.$hostname + "time-tracking/print-sale/" + this.id,
        type: "GET",
        success: (response) => {
          path = response.data.path
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
        async: false
      })
      if (path !== '') {
        const axios = require('axios')
        axios({
          url: this.$hostname + path,
          method: 'GET',
          responseType: 'blob',
        }).then((response) => {
          var fileURL = window.URL.createObjectURL(new Blob([response.data]));
          var fileLink = document.createElement('a');

          fileLink.href = fileURL;
          fileLink.setAttribute('download', path.substr(path.lastIndexOf('/') + 1));
          document.body.appendChild(fileLink);

          fileLink.click();
        })
      }
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
  }
}
</script>

<style scoped>

</style>