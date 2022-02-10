<template>
  <div class="offers flex-content">
    <Header/>
    <section class="summary-box">
      <div class="summary-box__title">
        <h1>Ценовое предложение</h1>
        <div class="addition-btn" @click="$router.push({name: 'Offers'})">
          <span>К списку предложений</span>
          <back-icon/>
        </div>
      </div>
      <div class="offers__content">
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
        <div class="document_date">Дата создания: {{ currentOffer.create_date }}</div>
        <div class="document_date">Предложение <span v-if="!currentOffer.active">не</span> <span>действует</span></div>
        <div class="document_date">Клиент: {{ currentOffer.client.name }}</div>
        <div>Срок: {{ currentOffer.term.days }} дней</div>

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
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="form" :model="currentOffer">
            <v-row>
              <v-text-field v-model="currentOffer.create_date" label="Дата создания" disabled></v-text-field>
              <v-checkbox v-model="currentOffer.active" label="Предложение действует"></v-checkbox>
            </v-row>
            <v-row>
              <v-autocomplete v-model="currentOffer.client" :items="clients" item-text="name" item-value="id"
                              label="Клиент" :rules="reqRules" required outlined>
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-title>
                      Клиенты не найдены
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
              <v-autocomplete v-model="currentOffer.term" :items="terms" item-text="days" item-value="id"
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
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="putOffer">Сохранить</v-btn>
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
import BackIcon from "../../components/icons/backIcon";
import WasteIcon from "../../components/icons/wasteIcon";
import EditIcon from "../../components/icons/editIcon";
import Header from "../../components/Header";
import $ from "jquery";

export default {
  name: "OffersOpen",
  components: {WasteIcon, EditIcon, Header, BackIcon},
  props: {
    id: [String, Number],
  },
  data() {
    return {
      items: [],
      terms: [],
      clients: [],
      currentOffer: {
        id: 0,
        create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        active: true,
        term: '',
        client: '',
      },
      itemsQuantity: 0,
      newItems: [],
      deletedItems: [],
      sum: {
        price: 0,
        tax: 0,
        discount: 0,
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
    console.log("init Offer open")
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
        url: this.$hostname + "time-tracking/offer/" + this.id,
        type: "GET",
        success: (response) => {
          this.currentOffer = response.data.data[0]
          this.items = response.data.items[this.id]
          this.newItems = response.data.items[this.id]
          this.itemsQuantity = response.data.items[this.id].length
          this.sum = {price: 0, tax: 0, discount: 0}
          this.items.forEach(item => {
            this.sum.price += item.price * item.quantity
            this.sum.tax += item.price * (1 + item.tax / 100) * item.quantity
            this.sum.discount += item.price * (1 + item.tax / 100) * (1 - item.discount / 100) * item.quantity
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
    putOffer() {
      if (this.$refs.form.validate()) {
        this.currentOffer.items = JSON.stringify(this.newItems)
        $.ajax({
          url: this.$hostname + "time-tracking/offer",
          type: "PUT",
          data: this.currentOffer,
          success: () => {
            this.putItems()
            this.addForm = false
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
        this.alertMsg = "Заполните все необходимые поля"
        this.alertError = true
      }
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