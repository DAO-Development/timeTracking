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
        <div>Номер счета: {{ currentSale.id }}</div>
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
        <!--        <v-btn class="action-btn" color="primary" @click="downloadAll">Скачать все файлы</v-btn>-->
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
      photoId: 0,
      menus: {
        dateMenu: false,
      },
      newPhotos: '',
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
        url: this.$hostname + "time-tracking/cheque/sales/" + this.id,
        type: "GET",
        success: (response) => {
          this.currentSale = response.data.data[0]
          this.photos = response.data.photos[this.id]
          this.currentSale.object.label = this.currentSale.object.city + ' ' + this.currentSale.object.street + ' ' + this.currentSale.object.house

          this.loadObjectsByCLient()
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
        url: this.$hostname + "time-tracking/objects/" + this.currentSale.client.id,
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
    putSale() {
      if (this.$refs.form.validate())
        $.ajax({
          url: this.$hostname + "time-tracking/cheque/sales",
          type: "PUT",
          data: this.currentSale,
          success: () => {
            this.loadData()
            this.addForm = false
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