<template>
  <div class="accounting flex-content">
    <Header/>
    <section class="summary-box">
      <h1>{{ title }}</h1>
      <v-btn class="action-btn" color="primary" @click="addForm=true">Добавить документ</v-btn>
      <div class="documents-all">
        <!--        <v-data-table :headers="headers" :items="documents" item-key="id" @click:row="downloadFile">-->
        <v-data-table :headers="headers" :items="documents" item-key="id">
          <template v-slot:item.actions="{ item }">
            <!--            <v-icon small class="mr-2" @click="openEditForm(item)">mdi-pencil</v-icon>-->
            <v-icon small @click="currentDocument=item.id; confirmDeleteDialog=true"
                    v-if="$parent.$parent.edit.indexOf('Бухгалтерия') !== -1">
              mdi-delete
            </v-icon>
          </template>
          <template v-slot:item.name="{ item }">
            <span @click="$router.push({name: 'AccountingOpen', params: {type: type, id: item.id}})">
              {{ item.name }}
            </span>
          </template>
          <template v-slot:no-data>
            Документы не загружены
          </template>
        </v-data-table>
      </div>
      <v-dialog v-model="addForm" max-width="500">
        <v-card>
          <v-card-title>
            Новый документ
          </v-card-title>
          <v-card-text>
            <v-form ref="form" :model="newDocument">
              <v-text-field label="Название*" v-model="newDocument.name" outlined :rules="reqRules"
                            required></v-text-field>
              <v-menu v-model="menu" :close-on-content-click="false" :nudge-right="40" transition="scale-transition"
                      offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newDocument.create_date" label="Дата создания" readonly v-bind="attrs"
                                v-on="on" outlined></v-text-field>
                </template>
                <v-date-picker v-model="newDocument.create_date" @input="menu = false"></v-date-picker>
              </v-menu>
              <v-combobox v-if="type === 'contracts' || type === 'property'" placeholder="Фирма*"
                          v-model="newDocument.client" :items="clients" item-text="name"
                          item-value="id" :rules="reqRules" required outlined></v-combobox>

              <v-file-input v-model="newDocument.path" placeholder="Выберите документ*" accept="*"
                            prepend-icon="" outlined multiple counter :rules="reqRules"></v-file-input>

            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="addForm=false">Отменить</v-btn>
            <v-btn color="primary" text @click="addDocument">Сохранить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="confirmDeleteDialog" max-width="500">
        <v-card>
          <v-card-title>
            Удаление документа
          </v-card-title>
          <v-card-text>Вы действительно хотите удалить выбранный документ? Отменить это действие будет
            невозможно
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
            <v-btn color="primary" text @click="deleteDocument">Подтвердить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </section>
  </div>
</template>

<script>
import Header from "../components/Header";
import $ from "jquery";

export default {
  name: "Accounting",
  components: {Header},
  props: {
    type: String
  },
  data() {
    return {
      title: '',
      url: '',
      mode: 0,
      documents: [],
      clients: [],
      newDocument: {
        id: 0,
        name: '',
        create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        path: '',
        client: '',
      },
      currentDocument: 0,
      headers: [
        {text: 'Название', align: 'start', sortable: true, value: 'name',},
        {text: 'Дата создания', value: 'create_date'},
        {text: '', value: 'actions', sortable: false},
      ],
      menu: false,
      addForm: false,
      confirmDeleteDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле',
      ],
    }
  },
  created() {
    console.log("init Accounting " + this.type)
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      this.$emit('load-functions')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      switch (this.type) {
        case 'reports':
          this.title = "Бухгалтерские отчеты"
          this.url = "time-tracking/accounting/documents"
          this.mode = 1
          break
        case 'extracts':
          this.title = "Бухгалтерские выписки"
          this.url = "time-tracking/accounting/documents"
          this.mode = 2
          break
        case 'documents':
          this.title = "Бухгалтерские документы"
          this.url = "time-tracking/accounting/documents"
          this.mode = 3
          break
        case 'contracts':
          this.headers = [
            {text: 'Название', align: 'start', sortable: true, value: 'name',},
            {text: 'Дата создания', value: 'create_date'},
            {text: 'Клиент', value: 'client.name'},
            {text: '', value: 'actions', sortable: false},
          ]
          this.title = "Договора с клиентами"
          this.url = "time-tracking/accounting/documents-client"
          this.mode = 4
          this.loadClients()
          break
        case 'property':
          this.headers = [
            {text: 'Название', align: 'start', sortable: true, value: 'name',},
            {text: 'Дата создания', value: 'create_date'},
            {text: 'Клиент', value: 'client.name'},
            {text: '', value: 'actions', sortable: false},
          ]
          this.title = "Документы на собственность"
          this.url = "time-tracking/accounting/documents-client"
          this.mode = 5
          this.loadClients()
          break
      }
      this.loadData()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + this.url + "/" + this.mode,
        type: "GET",
        success: (response) => {
          this.documents = response.data.data
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
    loadClients() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "GET",
        success: (response) => {
          this.clients = response.data.data
        },
        error: (response) => {
          console.log(response)
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
    addDocument() {
      console.log(this.newDocument.path)
      if (this.$refs.form.validate()) {
        const axios = require('axios')
        // чтение файла в formData
        let fd = new FormData();
        let i = 0
        this.newDocument.path.forEach(doc => {
          console.log(doc)
          i++
          fd.append('document' + i, doc)
        })
        fd.append('id', this.newDocument.id)
        fd.append('create_date', this.newDocument.create_date)
        fd.append('name', this.newDocument.name)
        if (this.type === 'contracts' || this.type === 'property')
          fd.append('client', this.newDocument.client.id)
        axios({
          method: 'put',
          url: this.$hostname + this.url + "/" + this.mode,
          headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
          data: fd
        })
            .then(response => {
              console.log(response)
              this.addForm = false
              this.newDocument = {
                id: 0,
                name: '',
                create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
                path: '',
                client: '',
              }
              this.loadData()
            });
      }
    },
    deleteDocument() {
      $.ajax({
        url: this.$hostname + this.url,
        type: "DELETE",
        data: {
          "id": this.currentDocument
        },
        success: () => {
          console.log("Документ удален")
          this.confirmDeleteDialog = false
          this.loadData()
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
  }

}
</script>

<style scoped>

</style>